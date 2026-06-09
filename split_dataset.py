import os, shutil, random
from pathlib import Path

SOURCE = "./dataset/merged"
OUTPUT = "./dataset/final_split"

random.seed(42)
images = sorted(Path(SOURCE + "/images").glob("*.jpg"))
random.shuffle(images)

n_train = int(len(images) * 0.80)
splits = {
    "train": images[:n_train],
    "val":   images[n_train:],
}

for split, imgs in splits.items():
    (Path(OUTPUT) / "images" / split).mkdir(parents=True, exist_ok=True)
    (Path(OUTPUT) / "labels" / split).mkdir(parents=True, exist_ok=True)
    for img in imgs:
        lbl = Path(SOURCE) / "labels" / (img.stem + ".txt")
        shutil.copy(img, Path(OUTPUT) / "images" / split / img.name)
        if lbl.exists():
            shutil.copy(lbl, Path(OUTPUT) / "labels" / split / lbl.name)
    print(split + ": " + str(len(imgs)) + " goruntu")