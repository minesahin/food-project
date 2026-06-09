# ============================================================
# rules.py — Hastalığa Göre Besin Uygunluk Kural Motoru
# ============================================================
# Kaynaklar:
#   Diyabet       : ADA Standards of Medical Care 2024
#   Hipertansiyon : AHA / DASH Diet Guidelines 2023
#   Obezite       : WHO Healthy Diet Fact Sheet 2023
#   Böbrek        : KDIGO Clinical Practice Guidelines 2024


RULES = {

    "diyabet": {
        "aciklama": "Tip 2 Diyabet",
        "kaynak": "ADA Standards of Medical Care 2024",
        "yasak": [
            "baklava", "sutlac", "tulumba_tatlisi",
            "pasta_kek", "kurabiye", "waffle", "dondurma",
            "beyaz_pilav", "patates",
            "pizza", "hamburger", "hot_dog",
        ],
        "dikkat": [
            "ekmek", "simit", "makarna", "bulgur_pilavi", "pogaca",
            "muz", "karpuz", "ananas", "mango",
            "adana_kebap", "doner", "kofte", "et_sote",
            "su_boregi", "lahmacun", "sarma", "dolma",
            "cig_kofte", "sandvic", "yumurta", "ayran",
        ],
        "uygun": [
            "domates", "salatalik", "brokoli", "kabak", "lahana",
            "ispanak", "patlican", "biber", "havuc", "mantar",
            "kuru_fasulye", "nohut", "mercimek", "barbunya",
            "tavuk", "hindi", "karides", "hamsi",
            "yogurt", "beyaz_peynir",
            "zeytin", "avokado",
            "elma", "armut", "cilek", "seftali", "limon",
            "portakal", "uzum", "kayisi", "erik",
            "kisir", "cacik", "coban_salatasi",
            "mercimek_corbasi", "karniyarik", "menemen",
            "cay", "turk_kahvesi",
        ],
        "mesajlar": {
            "yasak": " yüksek şeker/glisemik indeks içeriği nedeniyle diyabet hastaları için uygun değildir.",
            "dikkat": " karbonhidrat içeriği nedeniyle porsiyon kontrolü önerilir.",
            "uygun": " diyabet hastaları için uygundur.",
        }
    },

    "hipertansiyon": {
        "aciklama": "Hipertansiyon (Yüksek Tansiyon)",
        "kaynak": "AHA / DASH Diet Guidelines 2023",
        "yasak": [
            "pizza", "hamburger", "hot_dog",
            "beyaz_peynir",
        ],
        "dikkat": [
            "ekmek", "simit", "pogaca",
            "doner", "adana_kebap", "kofte", "et_sote",
            "sandvic", "su_boregi", "lahmacun", "sarma", "dolma",
            "karniyarik", "cig_kofte",
            "turk_kahvesi", "cay",
            "avokado", "zeytin",
        ],
        "uygun": [
            "muz", "portakal", "elma", "armut", "karpuz",
            "cilek", "mango", "ananas", "seftali", "uzum", "limon",
            "domates", "salatalik", "brokoli", "kabak", "ispanak",
            "patlican", "biber", "havuc", "mantar", "lahana",
            "kuru_fasulye", "nohut", "mercimek", "barbunya",
            "bulgur_pilavi",
            "tavuk", "hindi", "karides", "hamsi", "yumurta",
            "yogurt", "ayran",
            "kisir", "cacik", "coban_salatasi", "mercimek_corbasi",
        ],
        "mesajlar": {
            "yasak": " yüksek sodyum içeriği nedeniyle hipertansiyon hastaları için uygun değildir.",
            "dikkat": " sodyum/kafein içeriği nedeniyle dikkatli tüketilmelidir.",
            "uygun": " hipertansiyon hastaları için uygundur.",
        }
    },

    "obezite": {
        "aciklama": "Obezite",
        "kaynak": "WHO Healthy Diet Fact Sheet 2023",
        "yasak": [
            "baklava", "sutlac", "tulumba_tatlisi",
            "pasta_kek", "kurabiye", "waffle", "dondurma",
            "pizza", "hamburger", "hot_dog",
        ],
        "dikkat": [
            "beyaz_pilav", "ekmek", "simit", "makarna", "pogaca",
            "et_sote", "doner", "adana_kebap", "kofte",
            "su_boregi", "lahmacun", "sarma", "dolma",
            "avokado", "zeytin",
            "muz", "karpuz", "ananas", "mango",
            "sandvic", "patates", "beyaz_peynir", "cig_kofte",
        ],
        "uygun": [
            "domates", "salatalik", "brokoli", "kabak", "lahana",
            "ispanak", "patlican", "biber", "havuc", "mantar",
            "kuru_fasulye", "nohut", "mercimek", "barbunya",
            "tavuk", "hindi", "karides", "hamsi", "yumurta",
            "bulgur_pilavi",
            "elma", "armut", "cilek", "seftali", "portakal",
            "limon", "uzum",
            "yogurt", "ayran",
            "kisir", "cacik", "coban_salatasi",
            "mercimek_corbasi", "menemen", "karniyarik",
            "cay", "turk_kahvesi",
        ],
        "mesajlar": {
            "yasak": " yüksek kalori içeriği nedeniyle obezite hastaları için uygun değildir.",
            "dikkat": " kalori/karbonhidrat içeriği nedeniyle porsiyon kontrolü önerilir.",
            "uygun": " obezite hastaları için uygundur.",
        }
    },

    "bobrek": {
        "aciklama": "Kronik Böbrek Hastalığı",
        "kaynak": "KDIGO Clinical Practice Guidelines 2024",
        "yasak": [
            "muz", "portakal", "karpuz", "avokado",
            "mango", "ananas",
            "ispanak", "domates", "patates", "brokoli",
            "kuru_fasulye", "nohut", "mercimek", "barbunya",
        ],
        "dikkat": [
            "tavuk", "hindi", "et_sote", "adana_kebap",
            "kofte", "doner", "hamsi", "karides",
            "beyaz_peynir", "yogurt", "ayran",
            "pizza", "hamburger", "hot_dog", "sandvic",
            "ekmek", "simit", "pogaca",
            "mantar", "lahana", "havuc",
            "yumurta", "turk_kahvesi", "cig_kofte",
        ],
        "uygun": [
            "elma", "armut", "cilek", "limon", "seftali",
            "salatalik", "biber", "kabak",
            "makarna", "beyaz_pilav", "ekmek", "simit",
            "cacik", "menemen",
            "cay",
        ],
        "mesajlar": {
            "yasak": " yüksek potasyum/fosfor içeriği nedeniyle böbrek hastaları için uygun değildir.",
            "dikkat": " böbrek hastaları doktor kontrolünde sınırlı tüketmelidir.",
            "uygun": " kronik böbrek hastalığı için uygundur.",
        }
    },
}


def check_suitability(detected_foods: list, disease: str) -> dict:
    if disease not in RULES:
        return {
            "sonuc": "HATA",
            "mesaj": f"Geçersiz hastalık: {disease}",
            "desteklenen": list(RULES.keys()),
        }

    kural = RULES[disease]
    unique_foods = list(set(detected_foods))
    uyarilar = []
    uygun_besinler = []
    belirsiz = []

    for food in unique_foods:
        if food in kural["yasak"]:
            uyarilar.append({
                "besin": food,
                "seviye": "YASAK",
                "mesaj": food.replace("_", " ").title() + kural["mesajlar"]["yasak"],
            })
        elif food in kural["dikkat"]:
            uyarilar.append({
                "besin": food,
                "seviye": "DIKKAT",
                "mesaj": food.replace("_", " ").title() + kural["mesajlar"]["dikkat"],
            })
        elif food in kural["uygun"]:
            uygun_besinler.append({
                "besin": food,
                "seviye": "UYGUN",
                "mesaj": food.replace("_", " ").title() + kural["mesajlar"]["uygun"],
            })
        else:
            belirsiz.append(food)

    yasak_sayisi  = sum(1 for u in uyarilar if u["seviye"] == "YASAK")
    dikkat_sayisi = sum(1 for u in uyarilar if u["seviye"] == "DIKKAT")
    uygun_sayisi  = len(uygun_besinler)

    if yasak_sayisi > 0:
        sonuc = "UYGUN DEGİL"
        skor  = max(0, 40 - yasak_sayisi * 10 - dikkat_sayisi * 5)
    elif dikkat_sayisi > 0:
        sonuc = "KISMI UYGUN"
        skor  = max(41, 80 - dikkat_sayisi * 15)
    else:
        sonuc = "UYGUN"
        skor  = 100

    return {
        "hastalik"      : kural["aciklama"],
        "kaynak"        : kural["kaynak"],
        "sonuc"         : sonuc,
        "skor"          : skor,
        "tespit_edilen" : unique_foods,
        "uyarilar"      : uyarilar,
        "uygun_besinler": uygun_besinler,
        "belirsiz"      : belirsiz,
        "ozet"          : (
            f"{len(unique_foods)} yiyecek tespit edildi. "
            f"{yasak_sayisi} yasak, "
            f"{dikkat_sayisi} dikkat gerektiren, "
            f"{uygun_sayisi} uygun."
        ),
    }


