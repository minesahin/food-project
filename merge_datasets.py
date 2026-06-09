import os
import shutil
from pathlib import Path


OI_CLASSES = [
    'ananas', 'armut', 'brokoli', 'cay', 'cilek',
    'domates', 'dondurma', 'ekmek', 'elma', 'hamburger',
    'havuc', 'hindi', 'hot_dog', 'istakoz', 'kabak',
    'turk_kahvesi', 'karides', 'karpuz', 'kurabiye', 'lahana',
    'limon', 'mango', 'mantar', 'muz', 'pasta_kek',
    'patates', 'beyaz_peynir', 'pizza', 'portakal', 'salatalik',
    'seftali', 'tavuk', 'uzum', 'waffle'
]

LS_CLASSES = [
    'adana_kebap', 'avokado', 'ayran', 'baklava', 'bamya',
    'barbunya', 'beyaz_pilav', 'bezelye', 'biber', 'borek_genel',
    'bulgur_pilavi', 'cacik', 'cay', 'cig_kofte', 'cilek',
    'coban_salatasi', 'dolma', 'domates', 'domates_corbasi', 'doner',
    'ekmek', 'elma', 'erik', 'et_sote', 'gozleme',
    'hamsi', 'humus', 'hunkar_begendi', 'incir', 'iskender',
    'ispanak', 'karnabahar', 'karniyarik', 'kavun', 'kayisi',
    'kazandibi', 'kisir', 'kivi', 'kofte', 'kuru_fasulye',
    'lahmacun', 'levrek_cipura', 'limon', 'lokma', 'makarna',
    'manti', 'marul', 'menemen', 'mercimek', 'mercimek_corbasi',
    'midye_tava', 'muz', 'nar', 'nohut', 'omlet',
    'patates', 'patates_kizartma', 'patlican', 'pide_dolgulu', 'pirasa',
    'pogaca', 'salatalik', 'salep', 'sandvic', 'sarma',
    'sehriye_corbasi', 'simit', 'su_boregi', 'sutlac', 'tantuni',
    'tarhana_corbasi', 'tas_kebabi', 'tavuk_sote', 'tulumba_tatlisi', 'turk_kahvesi',
    'tursu', 'visne_kiraz', 'yaban_mersini', 'yayla_corbasi', 'yogurt',
    'yumurta', 'zeytin', 'zeytinyagli_fasulye'
]

FINAL_CLASSES = [
    'adana_kebap', 'ananas', 'armut', 'avokado', 'ayran',
    'baklava', 'barbunya', 'beyaz_peynir', 'beyaz_pilav', 'biber',
    'brokoli', 'bulgur_pilavi', 'cacik', 'cay', 'cig_kofte',
    'cilek', 'coban_salatasi', 'dolma', 'domates', 'dondurma',
    'doner', 'ekmek', 'elma', 'et_sote', 'hamburger',
    'hamsi', 'havuc', 'hindi', 'hot_dog', 'ispanak',
    'istakoz', 'kabak', 'karides', 'karniyarik', 'karpuz',
    'kisir', 'kofte', 'kurabiye', 'kuru_fasulye', 'lahana',
    'lahmacun', 'limon', 'makarna', 'mango', 'mantar',
    'menemen', 'mercimek', 'mercimek_corbasi', 'muz', 'nohut',
    'pasta_kek', 'patlican', 'patates', 'pizza', 'pogaca',
    'portakal', 'salatalik', 'sandvic', 'sarma', 'seftali',
    'simit', 'su_boregi', 'sutlac', 'tavuk', 'tulumba_tatlisi',
    'turk_kahvesi', 'uzum', 'waffle', 'yogurt', 'yumurta',
    'zeytin'
]


OI_TO_FINAL = {
    i: FINAL_CLASSES.index(cls)
    for i, cls in enumerate(OI_CLASSES)
    if cls in FINAL_CLASSES
}

LS_TO_FINAL = {
    i: FINAL_CLASSES.index(cls)
    for i, cls in enumerate(LS_CLASSES)
    if cls in FINAL_CLASSES
}

def remap_label_file(src_path, dst_path, remap):
    try:
        with open(src_path, encoding='utf-8') as f:
            lines = f.readlines()
    except:
        return
    new_lines = []
    for line in lines:
        parts = line.strip().split()
        if not parts:
            continue
        old_id = int(parts[0])
        if old_id in remap:
            parts[0] = str(remap[old_id])
            new_lines.append(' '.join(parts) + '\n')
    if new_lines:
        with open(dst_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)

SOURCES = [
    {
        "images": "C:/dataset/labeled_v1/images",
        "labels": "C:/dataset/labeled_v1/labels",
        "name": "tur1",
        "remap": LS_TO_FINAL
    },
    {
        "images": "C:/dataset/labeled_v2/images",
        "labels": "C:/dataset/labeled_v2/labels",
        "name": "tur2",
        "remap": LS_TO_FINAL
    },
]

OUTPUT = "./dataset/merged"

def merge():
    out_img = Path(OUTPUT) / "images"
    out_lbl = Path(OUTPUT) / "labels"
    out_img.mkdir(parents=True, exist_ok=True)
    out_lbl.mkdir(parents=True, exist_ok=True)

    total = 0
    for src in SOURCES:
        img_dir = Path(src["images"])
        lbl_dir = Path(src["labels"])
        name    = src["name"]
        remap   = src["remap"]

        if not img_dir.exists():
            print(f"ATLA (yok): {img_dir}")
            continue

        images = list(img_dir.glob("*.jpg")) + list(img_dir.glob("*.png"))
        count  = 0

        for img in images:
            lbl = lbl_dir / (img.stem + ".txt")
            if not lbl.exists():
                continue
            yeni_isim = f"{name}_{img.name}"
            shutil.copy(img, out_img / yeni_isim)
            dst_lbl = out_lbl / f"{name}_{img.stem}.txt"
            remap_label_file(lbl, dst_lbl, remap)
            count += 1
            total += 1

        print(f"{name}: {count} goruntu eklendi")

    print(f"\nTOPLAM: {total} goruntu → {OUTPUT}")
    print(f"Kategori sayisi: {len(FINAL_CLASSES)}")

if __name__ == "__main__":
    merge()