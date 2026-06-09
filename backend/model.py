from ultralytics import YOLO
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "best.pt")
model = YOLO(MODEL_PATH)


def detect_foods(image_path: str, conf: float = 0.45):
    print("Goruntu yolu: " + image_path)
    print("Dosya var mi: " + str(os.path.exists(image_path)))
    results = model(image_path, conf=conf)
    result = results[0]

    detected = []
    for box in result.boxes:
        cls_id = int(box.cls[0])
        cls_name = model.names[cls_id]
        confidence = float(box.conf[0])
        x1, y1, x2, y2 = box.xyxy[0].tolist()
        img_w = result.orig_shape[1]
        img_h = result.orig_shape[0]

        detected.append({
            "label": cls_name,
            "confidence": round(confidence, 3),
            "bbox": {
                "x": round(x1 / img_w * 100, 2),
                "y": round(y1 / img_h * 100, 2),
                "width": round((x2 - x1) / img_w * 100, 2),
                "height": round((y2 - y1) / img_h * 100, 2),
            }
        })

    return detected
