import albumentations as A
import cv2, os, shutil
from pathlib import Path

INPUT_IMG  = "C:/dataset/labeled_v1/images"
INPUT_LBL  = "C:/dataset/labeled_v1/labels"
OUTPUT_IMG = "./dataset/mini_final/images/train"
OUTPUT_LBL = "./dataset/mini_final/labels/train"

Path(OUTPUT_IMG).mkdir(parents=True, exist_ok=True)
Path(OUTPUT_LBL).mkdir(parents=True, exist_ok=True)

transform = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.RandomBrightnessContrast(p=0.3),
    A.GaussNoise(p=0.2),
    A.Blur(blur_limit=3, p=0.2),
], bbox_params=A.BboxParams(
    format="yolo",
    label_fields=["class_labels"],
    min_visibility=0.3
))

AUGMENT_COUNT = 2

images = list(Path(INPUT_IMG).glob("*.jpg"))
total = 0

for img_path in images:
    lbl_path = Path(INPUT_LBL) / (img_path.stem + ".txt")
    if not lbl_path.exists():
        continue

    img = cv2.imread(str(img_path))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    bboxes, class_labels = [], []
    with open(lbl_path) as f:
        for line in f:
            parts = line.strip().split()
            class_labels.append(int(parts[0]))
            bboxes.append([float(x) for x in parts[1:]])


    shutil.copy(img_path, Path(OUTPUT_IMG) / img_path.name)
    shutil.copy(lbl_path, Path(OUTPUT_LBL) / (img_path.stem + ".txt"))
    total += 1


    for i in range(AUGMENT_COUNT):
        try:
            result = transform(image=img, bboxes=bboxes, class_labels=class_labels)
            if not result["bboxes"]:
                continue

            out_name = img_path.stem + "_aug" + str(i)
            out_img = cv2.cvtColor(result["image"], cv2.COLOR_RGB2BGR)
            cv2.imwrite(str(Path(OUTPUT_IMG) / (out_name + ".jpg")), out_img)

            with open(Path(OUTPUT_LBL) / (out_name + ".txt"), "w") as f:
                for cls, bbox in zip(result["class_labels"], result["bboxes"]):
                    f.write(str(cls) + " " + " ".join([str(round(x, 6)) for x in bbox]) + "\n")
            total += 1
        except:
            continue

print("Toplam: " + str(total) + " goruntu")


shutil.copytree(
    "C:/Users/sahim/PycharmProjects/pythonProject/food_project/dataset/mini_split/images/val",
    "./dataset/mini_final/images/val",
    dirs_exist_ok=True
)
shutil.copytree(
    "C:/Users/sahim/PycharmProjects/pythonProject/food_project/dataset/mini_split/labels/val",
    "./dataset/mini_final/labels/val",
    dirs_exist_ok=True
)
print("Val kopyalandi")