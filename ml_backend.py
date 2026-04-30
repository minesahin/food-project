from label_studio_ml.model import LabelStudioMLBase
from ultralytics import YOLO
import numpy as np
import os


class YOLOBackend(LabelStudioMLBase):

    def __init__(self, **kwargs):
        super(YOLOBackend, self).__init__(**kwargs)
        model_path = os.path.join(os.path.dirname(__file__), "best.pt")
        print("Model yukleniyor: " + model_path)
        self.model = YOLO(model_path)
        print("Model yuklendi!")

    def predict(self, tasks, **kwargs):
        predictions = []

        for task in tasks:
            image_path = task["data"]["image"]

            if "/data/upload/" in image_path:
                filename = image_path.split("/data/upload/")[-1]
                base = os.path.join(
                    os.path.expanduser("~"),
                    "AppData", "Local", "label-studio",
                    "label-studio", "media", "upload"
                )
                image_path = os.path.join(base, filename)
            print("Aranan yol: " + image_path)
            if not os.path.exists(image_path):
                print("DOSYA BULUNAMADI: " + image_path)
                predictions.append({"result": [], "score": 0})
                continue

            try:
                results = self.model(image_path, conf=0.25)
                result = results[0]

                annotations = []
                img_w = result.orig_shape[1]
                img_h = result.orig_shape[0]

                for box in result.boxes:
                    x1, y1, x2, y2 = box.xyxy[0].tolist()
                    conf = float(box.conf[0])
                    cls_id = int(box.cls[0])
                    cls_name = self.model.names[cls_id]

                    x = (x1 / img_w) * 100
                    y = (y1 / img_h) * 100
                    w = ((x2 - x1) / img_w) * 100
                    h = ((y2 - y1) / img_h) * 100

                    annotations.append({
                        "from_name": "label",
                        "to_name": "image",
                        "type": "rectanglelabels",
                        "score": conf,
                        "value": {
                            "rectanglelabels": [cls_name],
                            "x": x,
                            "y": y,
                            "width": w,
                            "height": h,
                        },
                    })

                predictions.append({
                    "result": annotations,
                    "score": float(np.mean([a["score"] for a in annotations])) if annotations else 0,
                })

            except Exception as e:
                print("HATA: " + str(e))
                predictions.append({"result": [], "score": 0})

        return predictions


if __name__ == "__main__":
    from label_studio_ml.api import init_app
    app = init_app(model_class=YOLOBackend)
    app.run(host="0.0.0.0", port=9090, debug=False)