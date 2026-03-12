from pathlib import Path
from collections import defaultdict

LABELS_DIR = "./dataset/yolo/labels/train"

MY_LABELS = sorted([
    "elma", "portakal", "muz", "limon", "cilek", "uzum",
    "karpuz", "ananas", "mango", "seftali", "armut", "domates",
    "havuc", "salatalik", "patates", "brokoli", "mantar", "lahana",
    "kabak", "karides", "istakoz", "peynir", "tavuk", "hindi",
    "pizza", "hamburger", "hot_dog", "ekmek", "pasta", "kurabiye",
    "waffle", "dondurma", "kahve", "cay",
])

def check_distribution():
    counts = defaultdict(int)

    for txt_file in Path(LABELS_DIR).glob("*.txt"):
        with open(txt_file) as f:
            for line in f:
                parts = line.strip().split()
                if parts:
                    cls_idx = int(parts[0])
                    label = MY_LABELS[cls_idx]
                    counts[label] += 1

    print(f"\nKategori Dagilimi ({len(counts)} kategori):")
    print(f"{'Etiket':<20} {'Goruntu Sayisi':>15}")
    print("-" * 37)

    for label, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
        bar = "█" * (count // 20)
        print(f"{label:<20} {count:>6}  {bar}")

    print("-" * 37)
    print(f"TOPLAM BBOX    : {sum(counts.values())}")
    print(f"TOPLAM GORUNTU : {len(list(Path(LABELS_DIR).glob('*.txt')))}")
    print(f"Eksik kategoriler: {[l for l in MY_LABELS if l not in counts]}")

if __name__ == "__main__":
    check_distribution()