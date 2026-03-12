import albumentations as A
import cv2
from pathlib import Path
import shutil
from collections import defaultdict
import random
import yaml

CAP = 120
AUGMENT = 3

CURRENT_COUNTS = {
    "cilek": 1481, "domates": 1287, "portakal": 1046, "mantar": 925,
    "kurabiye": 849, "ekmek": 825, "tavuk": 781, "pasta": 776,
    "elma": 741, "uzum": 669, "dondurma": 534, "kahve": 468,
    "pizza": 404, "hamburger": 384, "peynir": 382, "muz": 330,
    "limon": 318, "karides": 303, "havuc": 268, "cay": 233,
    "brokoli": 225, "salatalik": 198, "kabak": 198, "karpuz": 185,
    "seftali": 146, "patates": 140, "armut": 139, "ananas": 114,
    "mango": 109, "istakoz": 106, "hot_dog": 101, "lahana": 99,
    "waffle": 82, "hindi": 79,
}

MY_LABELS = sorted(CURRENT_COUNTS.keys())
IDX_TO_LABEL = {idx: lbl for idx, lbl in enumerate(MY_LABELS)}

INPUT_DIR = "./dataset/yolo"
OUTPUT_DIR = "./dataset/yolo_final"

transform = A.Compose(
    [
        A.HorizontalFlip(p=0.5),
        A.RandomBrightnessContrast(brightness_limit=0.25, contrast_limit=0.25, p=0.5),
        A.HueSaturationValue(hue_shift_limit=10, sat_shift_limit=20, val_shift_limit=10, p=0.4),
        A.Rotate(limit=10, p=0.4),
        A.GaussNoise(var_limit=(5, 30), p=0.3),
        A.Blur(blur_limit=3, p=0.2),
    ],
    bbox_params=A.BboxParams(
        format="yolo",
        label_fields=["class_labels"],
        min_visibility=0.3
    )
)


def get_dominant_label(txt_path):
    with open(txt_path) as f:
        line = f.readline().strip().split()
        if line:
            return IDX_TO_LABEL.get(int(line[0]))
    return None


def read_labels(txt_path):
    bboxes = []
    classes = []
    with open(txt_path) as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) >= 5:
                classes.append(int(parts[0]))
                bboxes.append([float(x) for x in parts[1:5]])
    return bboxes, classes


def run():
    input_img = Path(INPUT_DIR) / "images" / "train"
    input_lbl = Path(INPUT_DIR) / "labels" / "train"
    out_img = Path(OUTPUT_DIR) / "images" / "train"
    out_lbl = Path(OUTPUT_DIR) / "labels" / "train"
    out_img.mkdir(parents=True, exist_ok=True)
    out_lbl.mkdir(parents=True, exist_ok=True)

    print("Goruntuler gruplandiriliyor...")
    label_to_imgs = defaultdict(list)
    for txt in input_lbl.glob("*.txt"):
        lbl = get_dominant_label(txt)
        if lbl:
            label_to_imgs[lbl].append(txt.stem)

    print("CAP=" + str(CAP) + " uygulanıyor...")
    selected = {}
    for lbl, imgs in label_to_imgs.items():
        random.seed(42)
        chosen = random.sample(imgs, min(len(imgs), CAP))
        for stem in chosen:
            selected[stem] = True
        status = "KIRPILDI" if len(imgs) > CAP else "TAMAM"
        print("  " + lbl + " : " + str(len(imgs)) + " -> " + str(len(chosen)) + "  " + status)

    print("Orijinaller kopyalanıyor: " + str(len(selected)) + " goruntu")
    for stem in selected:
        img_src = input_img / (stem + ".jpg")
        lbl_src = input_lbl / (stem + ".txt")
        if img_src.exists():
            shutil.copy(img_src, out_img / (stem + ".jpg"))
        if lbl_src.exists():
            shutil.copy(lbl_src, out_lbl / (stem + ".txt"))

    print("Augmentation baslıyor: her goruntu " + str(AUGMENT) + "x cogaltılıyor...")
    aug_count = 0
    errors = 0

    for stem in selected:
        img_path = input_img / (stem + ".jpg")
        lbl_path = input_lbl / (stem + ".txt")

        if not img_path.exists() or not lbl_path.exists():
            continue

        image = cv2.imread(str(img_path))
        if image is None:
            continue

        bboxes, classes = read_labels(lbl_path)
        if not bboxes:
            continue

        for i in range(AUGMENT):
            try:
                aug = transform(
                    image=image,
                    bboxes=bboxes,
                    class_labels=classes
                )
                if not aug["bboxes"]:
                    continue

                out_name = stem + "_aug" + str(i)
                cv2.imwrite(str(out_img / (out_name + ".jpg")), aug["image"])

                lines = []
                for cls, bbox in zip(aug["class_labels"], aug["bboxes"]):
                    lines.append(str(cls) + " " + " ".join(f"{v:.6f}" for v in bbox))
                (out_lbl / (out_name + ".txt")).write_text("\n".join(lines))
                aug_count += 1

            except Exception:
                errors += 1

    total = len(list(out_img.glob("*.jpg")))
    print("=========================================")
    print("TAMAMLANDI!")
    print("=========================================")
    print("Secilen orijinal : " + str(len(selected)))
    print("Augmented eklenen: " + str(aug_count))
    print("Hatali atlanan   : " + str(errors))
    print("TOPLAM           : " + str(total))
    print("Konum: " + str(Path(OUTPUT_DIR).absolute()))

    with open(Path(INPUT_DIR) / "data.yaml") as f:
        data = yaml.safe_load(f)
    data["path"] = str(Path(OUTPUT_DIR).absolute())
    with open(Path(OUTPUT_DIR) / "data.yaml", "w") as f:
        yaml.dump(data, f, allow_unicode=True)
    print("data.yaml olusturuldu")


if __name__ == "__main__":
    run()