import os
import cv2
import shutil
import random
import numpy as np
from pathlib import Path
from collections import defaultdict
import albumentations as A

INPUT_IMG  = "./dataset/final_split/images/train"
INPUT_LBL  = "./dataset/final_split/labels/train"
OUTPUT_IMG = "./dataset/final_augmented/images/train"
OUTPUT_LBL = "./dataset/final_augmented/labels/train"

HEDEF = 150
RANDOM_SEED = 42

transform = A.Compose([
    A.HorizontalFlip(p=0.5),
    A.RandomBrightnessContrast(p=0.3),
    A.GaussNoise(p=0.2),
    A.Blur(blur_limit=3, p=0.2),
    A.RandomRotate90(p=0.3),
], bbox_params=A.BboxParams(
    format="yolo",
    label_fields=["class_labels"],
    min_visibility=0.3
))

random.seed(RANDOM_SEED)
Path(OUTPUT_IMG).mkdir(parents=True, exist_ok=True)
Path(OUTPUT_LBL).mkdir(parents=True, exist_ok=True)


def get_labels(lbl_path):
    if not lbl_path.exists():
        return []
    with open(lbl_path) as f:
        lines = [l.strip() for l in f.readlines() if l.strip()]
    return [int(l.split()[0]) for l in lines]

def read_bboxes(lbl_path):
    bboxes, class_labels = [], []
    if not lbl_path.exists():
        return bboxes, class_labels
    with open(lbl_path) as f:
        for line in f:
            parts = line.strip().split()
            if not parts:
                continue
            class_labels.append(int(parts[0]))
            bboxes.append([float(x) for x in parts[1:]])
    return bboxes, class_labels

def write_bboxes(lbl_path, bboxes, class_labels):
    with open(lbl_path, 'w') as f:
        for cls, bbox in zip(class_labels, bboxes):
            f.write(str(cls) + " " + " ".join([str(round(x, 6)) for x in bbox]) + "\n")


cat_images = defaultdict(list)
img_dir = Path(INPUT_IMG)
lbl_dir = Path(INPUT_LBL)

images = list(img_dir.glob("*.jpg")) + list(img_dir.glob("*.png"))
print(f"Toplam train görüntüsü: {len(images)}")

for img_path in images:
    lbl_path = lbl_dir / (img_path.stem + ".txt")
    labels = get_labels(lbl_path)
    for cls_id in set(labels):
        cat_images[cls_id].append(img_path)

print(f"Etiketli kategori sayısı: {len(cat_images)}")
print(f"Kategori başına hedef: {HEDEF}")


copied = 0
for img_path in images:
    lbl_path = lbl_dir / (img_path.stem + ".txt")
    if not lbl_path.exists():
        continue
    shutil.copy(img_path, Path(OUTPUT_IMG) / img_path.name)
    shutil.copy(lbl_path, Path(OUTPUT_LBL) / (img_path.stem + ".txt"))
    copied += 1

print(f"\nOrijinal kopyalandı: {copied}")


aug_total = 0

for cls_id, img_list in sorted(cat_images.items()):
    mevcut = len(img_list)

    if mevcut >= HEDEF:
        # Zaten yeterli, augmentation yapma
        continue

    eksik = HEDEF - mevcut
    aug_per_img = max(1, round(eksik / mevcut))

    augmented = 0
    random.shuffle(img_list)

    for img_path in img_list * (aug_per_img + 1):
        if augmented >= eksik:
            break

        lbl_path = lbl_dir / (img_path.stem + ".txt")
        bboxes, class_labels = read_bboxes(lbl_path)

        if not bboxes:
            continue

        img = cv2.imread(str(img_path))
        if img is None:
            continue
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        try:
            result = transform(
                image=img,
                bboxes=bboxes,
                class_labels=class_labels
            )
            if not result["bboxes"]:
                continue

            out_name = f"aug{cls_id}_{augmented}_{img_path.stem}"
            out_img_path = Path(OUTPUT_IMG) / (out_name + img_path.suffix)
            out_lbl_path = Path(OUTPUT_LBL) / (out_name + ".txt")

            out_img = cv2.cvtColor(result["image"], cv2.COLOR_RGB2BGR)
            cv2.imwrite(str(out_img_path), out_img)
            write_bboxes(out_lbl_path, result["bboxes"], result["class_labels"])

            augmented += 1
            aug_total += 1

        except Exception as e:
            continue

print(f"Augmented eklenen: {aug_total}")

shutil.copytree(
    "./dataset/final_split/images/val",
    "./dataset/final_augmented/images/val",
    dirs_exist_ok=True
)
shutil.copytree(
    "./dataset/final_split/labels/val",
    "./dataset/final_augmented/labels/val",
    dirs_exist_ok=True
)
print("Val kopyalandı (augmentation uygulanmadı)")


train_count = len(list(Path(OUTPUT_IMG).glob("*.jpg"))) + \
              len(list(Path(OUTPUT_IMG).glob("*.png")))
val_count   = len(list(Path("./dataset/final_augmented/images/val").glob("*.jpg"))) + \
              len(list(Path("./dataset/final_augmented/images/val").glob("*.png")))

print(f"\n{'='*40}")
print(f"SONUÇ:")
print(f"  Train: {train_count} görüntü")
print(f"  Val:   {val_count} görüntü")
print(f"  Toplam: {train_count + val_count}")
print(f"{'='*40}")