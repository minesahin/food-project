# label_mapping.py
# Proje klasörüne bu dosyayı oluştur

# Open Images adı → Senin etiket adın
OPENIMAGES_TO_MINE = {
    # MEYVELER
    "Apple":          "elma",
    "Orange":         "portakal",
    "Banana":         "muz",
    "Lemon":          "limon",
    "Strawberry":     "çilek",
    "Grape":          "üzüm",
    "Watermelon":     "karpuz",
    "Pineapple":      "ananas",
    "Mango":          "mango",
    "Pomegranate":    "nar",
    "Peach":          "şeftali",
    "Pear":           "armut",
    "Coconut":        "hindistan_cevizi",

    # SEBZELER
    "Tomato":         "domates",
    "Carrot":         "havuç",
    "Cucumber":       "salatalık",
    "Potato":         "patates",
    "Onion":          "soğan",
    "Broccoli":       "brokoli",
    "Mushroom":       "mantar",
    "Garlic":         "sarımsak",
    "Cabbage":        "lahana",
    "Pepper":         "biber",
    "Zucchini":       "kabak",
    "Asparagus":      "kuşkonmaz",
    "Corn":           "mısır",
    "Artichoke":      "enginar",

    # PROTEİN
    "Chicken egg": "yumurta",
    "Cheese":         "peynir",
    "Shrimp":         "karides",
    "Lobster":        "ıstakoz",
    "Squid":          "kalamar",
    "Salmon":         "somon",
    "Fish":           "balık",
    "Chicken":        "tavuk",
    "Turkey":         "hindi",
    "Sausage":        "sosis",

    # HAZIR / FAST FOOD
    "Pizza":          "pizza",
    "Hamburger":      "hamburger",
    "Hot dog":        "hot_dog",
    "Taco":           "taco",
    "Sushi":          "sushi",
    "Pretzel":        "simit",   # yakın karşılık

    # TATLI / EKMEK
    "Bread":          "ekmek",
    "Cake":           "pasta",
    "Cookie":         "kurabiye",
    "Muffin":         "muffin",
    "Waffle":         "waffle",
    "Pancake":        "gözleme",  # yakın karşılık
    "Ice cream":      "dondurma",
    "Chocolate":      "çikolata",

    # İÇECEK
    "Coffee":         "kahve",
    "Tea":            "çay",
    "Juice":          "meyve_suyu",
    "Wine":           "şarap",
    "Beer":           "bira",
}

# Sadece Open Images adlarının listesi (download için)
OPENIMAGES_CLASSES = list(OPENIMAGES_TO_MINE.keys())

print(f"Toplam {len(OPENIMAGES_CLASSES)} kategori Open Images'tan indirilecek")