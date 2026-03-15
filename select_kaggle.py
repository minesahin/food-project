from pathlib import Path
import shutil
import random

KAGGLE_DIR = r"C:\Users\sahim\OneDrive\Masaüstü\Klasörler\bil-müh\bahar\proje\data-set\Turkish Food"
OUTPUT_DIR = "./dataset/kaggle_selected"
IMAGES_PER_CLASS = 150

OPEN_IMAGES_LABELS = {
    "elma", "portakal", "muz", "cilek", "uzum", "karpuz",
    "armut", "domates", "havuc", "salatalik", "patates",
    "brokoli", "mantar", "kabak", "beyaz_ekmek", "dondurma",
    "turk_kahvesi", "cay", "hindi", "beyaz_peynir",
}

MANUAL_MAP = {
    "adana-kebap":              "adana_kebap",
    "anne-koftesi":             "kofte",
    "armut":                    "armut",
    "avokado":                  "avokado",
    "ayran":                    "ayran",
    "baklava":                  "baklava",
    "beyaz-lahana-sarmasi":     "sarma",
    "biber-dolma":              "dolma",
    "brokoli":                  "brokoli",
    "bulgur-pilavi":            "bulgur_pilavi",
    "cacik":                    "cacik",
    "cay":                      "cay",
    "cig-kofte":                "cig_kofte",
    "cilek":                    "cilek",
    "cipura":                   "levrek_cipura",
    "coban-salatasi":           "coban_salatasi",
    "domates":                  "domates",
    "domates-corbasi":          "domates_corbasi",
    "dondurma":                 "dondurma",
    "doner":                    "doner",
    "ekmek":                    "beyaz_ekmek",
    "elma":                     "elma",
    "erik":                     "erik",
    "et-sote":                  "et_sote",
    "hamsi-tava":               "hamsi",
    "haslanmis-yumurta":        "yumurta",
    "havuc":                    "havuc",
    "hunkar-begendi":           "hunkar_begendi",
    "icli-kofte":               "kofte",
    "incir":                    "incir",
    "iskender":                 "iskender",
    "ispanak-yemegi":           "ispanak",
    "kabak-mucver":             "kabak",
    "karnabahar":               "karnabahar",
    "karniyarik":               "karniyarik",
    "karpuz":                   "karpuz",
    "kavun":                    "kavun",
    "kayisi":                   "kayisi",
    "kazandibi":                "kazandibi",
    "kiraz":                    "visne_kiraz",
    "kisir":                    "kisir",
    "kivi":                     "kivi",
    "kiymali-borek":            "borek_genel",
    "kiymali-pide":             "pide_dolgulu",
    "lahmacun":                 "lahmacun",
    "levrek":                   "levrek_cipura",
    "lokma":                    "lokma",
    "manti":                    "manti",
    "menemen":                  "menemen",
    "mercimek-corbasi":         "mercimek_corbasi",
    "mercimek-koftesi":         "kofte",
    "midye-dolma":              "dolma",
    "midye-tava":               "midye_tava",
    "muz":                      "muz",
    "nar":                      "nar",
    "omlet":                    "omlet",
    "patates-kizartmasi":       "patates_kizartma",
    "patates-puresi":           "patates",
    "patates-salatasi":         "patates",
    "patlican-kebabi":          "patlican",
    "peynirli-borek":           "borek_genel",
    "pilav":                    "beyaz_pilav",
    "pirasa":                   "pirasa",
    "portakal":                 "portakal",
    "sahlep":                   "salep",
    "salatalik":                "salatalik",
    "salcali-makarna":          "makarna",
    "sandvic":                  "sandvic",
    "sehriye-corbasi":          "sehriye_corbasi",
    "siyah-zeytin":             "zeytin",
    "su-boregi":                "su_boregi",
    "sucuklu-yumurta":          "yumurta",
    "sulu-bamya-yemegi":        "bamya",
    "sulu-barbunya-yemegi":     "barbunya",
    "sulu-bezelye-yemegi":      "bezelye",
    "sulu-kuru-fasulye-yemegi": "kuru_fasulye",
    "sulu-mercimek-yemegi":     "mercimek",
    "sulu-nohut-yemegi":        "nohut",
    "sulu-patates-yemegi":      "patates",
    "sutlac":                   "sutlac",
    "tantuni":                  "tantuni",
    "tarhana-corbasi":          "tarhana_corbasi",
    "tas-kebabi":               "tas_kebabi",
    "tavuk-sote":               "tavuk_sote",
    "tulumba-tatlisi":          "tulumba_tatlisi",
    "turk-kahvesi":             "turk_kahvesi",
    "uzum":                     "uzum",
    "yaprak-sarma":             "sarma",
    "yayla-corbasi":            "yayla_corbasi",
    "yesil-zeytin":             "zeytin",
    "yogurt":                   "yogurt",
    "yogurtlu-makarna":         "makarna",
    "zeytinyagli-fasulye":      "zeytinyagli_fasulye",
}


def select():
    kaggle_path = Path(KAGGLE_DIR)
    output_path = Path(OUTPUT_DIR)


    if output_path.exists():
        shutil.rmtree(output_path)
    output_path.mkdir(parents=True)

    random.seed(42)

    label_counts = {}
    total_copied = 0
    skipped_oi = 0
    skipped_none = 0

    print("Her kategoriden " + str(IMAGES_PER_CLASS) + " goruntu seciliyor...")
    print("(Open Images kategorileri atlaniyor)")
    print("=" * 60)

    for folder in sorted(kaggle_path.iterdir()):
        if not folder.is_dir():
            continue

        my_label = MANUAL_MAP.get(folder.name)

        if my_label is None:
            skipped_none += 1
            continue

        if my_label in OPEN_IMAGES_LABELS:
            print("ATLA (Open Images): " + folder.name + " -> " + my_label)
            skipped_oi += 1
            continue

        images = (
            list(folder.glob("*.jpg")) +
            list(folder.glob("*.jpeg")) +
            list(folder.glob("*.png")) +
            list(folder.glob("*.JPG")) +
            list(folder.glob("*.PNG"))
        )

        if not images:
            continue

        selected = random.sample(images, min(len(images), IMAGES_PER_CLASS))

        dest_dir = output_path / my_label
        dest_dir.mkdir(exist_ok=True)

        copied = 0
        for img in selected:
            ext = img.suffix.lower()
            idx = len(list(dest_dir.glob("*"))) + 1
            new_name = my_label + "_" + str(idx).zfill(4) + ext
            shutil.copy(img, dest_dir / new_name)
            copied += 1

        label_counts[my_label] = label_counts.get(my_label, 0) + copied
        total_copied += copied
        print(folder.name[:30].ljust(30) + " -> " + my_label[:22].ljust(22) + " : " + str(copied))

    print("=" * 60)
    print("TOPLAM KOPYALANAN       : " + str(total_copied))
    print("ATLAN (Open Images)     : " + str(skipped_oi))
    print("ATLAN (listede yok)     : " + str(skipped_none))
    print("BENZERSIZ KATEGORI      : " + str(len(label_counts)))

    cok = [(k, v) for k, v in label_counts.items() if v > 150]
    if cok:
        print("\nBIRDEN FAZLA KAYNAKTAN GELEN (toplam > 150):")
        for k, v in sorted(cok, key=lambda x: x[1], reverse=True):
            print("  " + k.ljust(25) + " : " + str(v))

    print("\nKonum: " + str(output_path.absolute()))


if __name__ == "__main__":
    select()