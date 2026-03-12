import cv2
import random
from pathlib import Path

LABELS_DIR = "./dataset/yolo/labels/train"
IMAGES_DIR = "./dataset/yolo/images/train"

MY_LABELS = sorted([
    "elma", "portakal", "muz", "limon", "cilek", "uzum",
    "karpuz", "ananas", "mango", "seftali", "armut", "domates",
    "havuc", "salatalik", "patates", "brokoli", "mantar", "lahana",
    "kabak", "karides", "istakoz", "peynir", "tavuk", "hindi",
    "pizza", "hamburger", "hot_dog", "ekmek", "pasta", "kurabiye",
    "waffle", "dondurma", "kahve", "cay",
])

def show_samples(n=5):
    label_files = list(Path(LABELS_DIR).glob("*.txt"))
    samples = random.sample(label_files, min(n, len(label_files)))

    for lbl_path in samples:
        img_path = Path(IMAGES_DIR) / (lbl_path.stem + ".jpg")
        if not img_path.exists():
            continue

        img = cv2.imread(str(img_path))
        if img is None:
            continue

        h, w = img.shape[:2]

        with open(lbl_path) as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) < 5:
                    continue
                cls_idx = int(parts[0])
                cx, cy, bw, bh = map(float, parts[1:])

                x1 = int((cx - bw/2) * w)
                y1 = int((cy - bh/2) * h)
                x2 = int((cx + bw/2) * w)
                y2 = int((cy + bh/2) * h)

                label_name = MY_LABELS[cls_idx]
                cv2.rectangle(img, (x1,y1), (x2,y2), (0,255,0), 2)
                cv2.putText(img, label_name, (x1, y1-8),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        cv2.imshow(f"{lbl_path.stem}", img)
        print(f"Gosteriliyor: {lbl_path.stem} — devam icin herhangi bir tusa bas")
        cv2.waitKey(0)

    cv2.destroyAllWindows()
    print("Kontrol tamamlandi!")

show_samples(5)