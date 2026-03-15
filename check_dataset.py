from pathlib import Path

DATASET_DIR = r"C:\Users\sahim\OneDrive\Masaüstü\Klasörler\bil-müh\bahar\proje\data-set\Turkish Food"

MY_FINAL_LABELS = [
    "beyaz_ekmek", "tam_bugday_ekmek", "cavdar_ekmek", "simit", "pide",
    "beyaz_pilav", "bulgur_pilavi", "makarna", "sehriye",
    "patates", "patates_kizartma", "misir",
    "kofte", "adana_kebap", "urfa_kebap", "sis_kebap", "doner",
    "iskender", "lahmacun", "pide_dolgulu", "cig_kofte",
    "tas_kebabi", "tantuni", "manti", "hunkar_begendi",
    "tavuk_izgara", "tavuk_kanat", "tavuk_kizartma", "tavuk_sote", "tavuk_corbasi",
    "et_sote", "kuzu_pirzola", "sac_kavurma", "terbiyeli_kofte", "kuru_fasulye_et",
    "mercimek_corbasi", "yayla_corbasi", "ezogelin_corbasi", "domates_corbasi",
    "sehriye_corbasi", "iskembe_corbasi", "tarhana_corbasi", "corba_genel",
    "imam_bayildi", "karniyarik", "dolma", "sarma", "turlu",
    "zeytinyagli_fasulye", "patlican_kizartma", "bamya",
    "cacik", "humus", "patlican_salatasi", "coban_salatasi", "kisir", "tarator",
    "su_boregi", "sigara_boregi", "gozleme", "pogaca", "acma", "borek_genel",
    "menemen", "omlet", "yumurta",
    "somon", "ton_baligi", "hamsi", "levrek_cipura", "balik_genel", "midye_tava",
    "sosis", "sucuk", "pastirma", "hindi",
    "beyaz_peynir", "kasar_peynir", "lor_peynir", "yogurt", "ayran",
    "sut", "tereyagi", "kaymak",
    "kuru_fasulye", "nohut", "mercimek", "bezelye", "barbunya", "soya",
    "domates", "salatalik", "biber", "patlican", "kabak", "brokoli",
    "karnabahar", "ispanak", "havuc", "sogan", "mantar",
    "misir_sebze", "taze_fasulye", "pirasa", "kereviz", "semizotu",
    "elma", "armut", "muz", "portakal", "mandalina", "uzum", "karpuz",
    "kavun", "cilek", "visne_kiraz", "nar", "incir", "kayisi", "kivi",
    "erik", "kuru_meyve",
    "zeytinyagi", "aycicek_yagi", "zeytin", "bal", "recel_marmelat",
    "ketcap_sos", "mayonez", "seker", "tahin",
    "avokado", "ceviz", "badem", "findik", "antep_fistigi", "susam", "cekirdek",
    "baklava", "sutlac", "kazandibi", "asure", "helva", "lokum", "lokma",
    "tulumba_tatlisi", "pasta_kek", "biskuvi_kraker", "cikolata", "dondurma",
    "cay", "turk_kahvesi", "neskafe_kahve", "meyve_suyu", "kola_gazoz",
    "su", "boza", "salep",
    "pizza", "burger", "sandvic", "wrap_durum", "hot_dog", "nugget",
]


MANUAL_MAP = {
    # Kaggle klasör adı  →  benim etiket adım
    "adana-kebap":              "adana_kebap",
    "anne-koftesi":             "kofte",
    "armut":                    "armut",
    "avokado":                  "avokado",
    "ayran":                    "ayran",
    "baklava":                  "baklava",
    "beyaz-lahana-sarmasi":     "sarma",
    "biber-dolma":              "dolma",
    "brokoli":                  "brokoli",
    "bruksel-lahanasi":         None,        # listede yok
    "bulgur-pilavi":            "bulgur_pilavi",
    "cacik":                    "cacik",
    "canak-enginar":            None,        # enginar listede yok
    "cay":                      "cay",
    "cig-kofte":                "cig_kofte",
    "cilek":                    "cilek",
    "cipura":                   "levrek_cipura",
    "coban-salatasi":           "coban_salatasi",
    "domates":                  "domates",       # ← düzeltildi
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
    "kalburabasti":             None,        # listede yok
    "karnabahar":               "karnabahar",
    "karniyarik":               "karniyarik",
    "karpuz":                   "karpuz",
    "kavun":                    "kavun",
    "kayisi":                   "kayisi",
    "kazandibi":                "kazandibi",
    "kemal-pasa-tatlisi":       None,        # listede yok
    "kiraz":                    "visne_kiraz",
    "kisir":                    "kisir",
    "kivi":                     "kivi",
    "kiymali-borek":            "borek_genel",
    "kiymali-pide":             "pide_dolgulu",
    "kokorec":                  None,        # listede yok
    "lahmacun":                 "lahmacun",
    "levrek":                   "levrek_cipura",
    "lokma":                    "lokma",
    "mango":                    None,        # listede yok
    "manti":                    "manti",
    "menemen":                  "menemen",
    "mercimek-corbasi":         "mercimek_corbasi",
    "mercimek-koftesi":         "kofte",
    "midye-dolma":              "dolma",
    "midye-tava":               "midye_tava",
    "mumbar-dolmasi":           None,        # listede yok
    "muz":                      "muz",
    "nar":                      "nar",
    "omlet":                    "omlet",
    "patates-kizartmasi":       "patates_kizartma",  # ← düzeltildi
    "patates-puresi":           "patates",
    "patates-salatasi":         "patates",
    "patlican-kebabi":          "patlican",
    "peynirli-borek":           "borek_genel",
    "pilav":                    "beyaz_pilav",
    "pirasa":                   "pirasa",
    "portakal":                 "portakal",
    "sahlep":                   "salep",             # ← sahlep = salep
    "salatalik":                "salatalik",
    "salcali-makarna":          "makarna",
    "sandvic":                  "sandvic",
    "seftali":                  None,        # şeftali listede yok — eklenebilir
    "sehriye-corbasi":          "sehriye_corbasi",
    "siyah-zeytin":             "zeytin",
    "su-boregi":                "su_boregi",
    "sucuklu-yumurta":          "yumurta",
    "sulu-bamya-yemegi":        "bamya",             # ← düzeltildi
    "sulu-barbunya-yemegi":     "barbunya",
    "sulu-bezelye-yemegi":      "bezelye",
    "sulu-kuru-fasulye-yemegi": "kuru_fasulye",
    "sulu-mercimek-yemegi":     "mercimek",
    "sulu-nohut-yemegi":        "nohut",
    "sulu-patates-yemegi":      "patates",
    "sutlac":                   "sutlac",            # ← düzeltildi
    "tantuni":                  "tantuni",
    "tarhana-corbasi":          "tarhana_corbasi",
    "tas-kebabi":               "tas_kebabi",
    "tavuk-sote":               "tavuk_sote",
    "tulumba-tatlisi":          "tulumba_tatlisi",
    "turk-kahvesi":             "turk_kahvesi",
    "tursu":                    None,        # tursu listede yok — eklenebilir
    "uzum":                     "uzum",
    "yaprak-sarma":             "sarma",
    "yayla-corbasi":            "yayla_corbasi",
    "yesil-zeytin":             "zeytin",
    "yogurt":                   "yogurt",
    "yogurtlu-makarna":         "makarna",
    "zeytinyagli-fasulye":      "zeytinyagli_fasulye",
}


def check():
    dataset_path = Path(DATASET_DIR)

    if not dataset_path.exists():
        print("HATA: Klasor bulunamadi: " + str(dataset_path.absolute()))
        return

    folders = sorted([f for f in dataset_path.iterdir() if f.is_dir()])
    total_images = 0
    matched = []
    unmatched = []
    skipped = []

    print("KAGGLE DATASET - DUZELTILMIS ESLESME")
    print("=" * 65)
    print("Kaggle Klasoru                  | Goruntu | Benim Etiketim")
    print("-" * 65)

    for folder in folders:
        images = (
            list(folder.glob("*.jpg")) +
            list(folder.glob("*.jpeg")) +
            list(folder.glob("*.png")) +
            list(folder.glob("*.JPG")) +
            list(folder.glob("*.PNG"))
        )
        count = len(images)
        total_images += count

        my_label = MANUAL_MAP.get(folder.name)

        if my_label is None and folder.name in MANUAL_MAP:
            status = "ATLA (listede yok)"
            skipped.append((folder.name, count))
        elif my_label:
            status = my_label
            matched.append((folder.name, my_label, count))
        else:
            status = "TANINMADI"
            unmatched.append((folder.name, count))

        print(folder.name[:32].ljust(32) + " | " + str(count).rjust(7) + " | " + status)

    print("=" * 65)
    print("TOPLAM KLASOR      : " + str(len(folders)))
    print("TOPLAM GORUNTU     : " + str(total_images))
    print("ESLESEN            : " + str(len(matched)))
    print("ATLANACAK          : " + str(len(skipped)))
    print("TANINMADI          : " + str(len(unmatched)))

    label_counts = {}
    for folder_name, my_label, count in matched:
        if my_label not in label_counts:
            label_counts[my_label] = 0
        label_counts[my_label] += count

    print("\nETİKET BAZINDA GORUNTU SAYISI:")
    print("-" * 40)
    for label, count in sorted(label_counts.items(), key=lambda x: x[1], reverse=True):
        print(label.ljust(25) + " : " + str(count))

    print("\n153+ LISTEDE OLUP KAGGLE DE OLMAYAN:")
    print("-" * 40)
    missing = [l for l in MY_FINAL_LABELS if l not in label_counts]
    for i, m in enumerate(missing):
        print(str(i + 1) + ". " + m)
    print("Toplam eksik: " + str(len(missing)))


if __name__ == "__main__":
    check()