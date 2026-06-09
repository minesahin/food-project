import json
import requests
import os

TURKOMP_PATH = os.path.join(os.path.dirname(__file__), "turkomp_db.json")
USDA_API_KEY = "r4rZFtVzUAY4OU7Pcw549b1BOuqFBdpb9VG2Qt8z"

TURKISH_TO_ENGLISH = {
    "avokado": "avocado raw",
    "baklava": "baklava",
    "lahmacun": "lahmacun turkish flatbread",
    "adana_kebap": "adana kebab grilled",
    "ayran": "ayran yogurt drink",
    "doner": "doner kebab",
    "mercimek_corbasi": "lentil soup",
    "sutlac": "rice pudding",
    "menemen": "menemen scrambled eggs tomato",
    "karniyarik": "stuffed eggplant",
    "su_boregi": "borek pastry cheese",
    "yogurt": "plain yogurt whole milk",
    "elma": "apple raw",
    "muz": "banana raw",
    "portakal": "orange raw",
    "domates": "tomato raw",
    "salatalik": "cucumber raw",
    "brokoli": "broccoli raw",
    "havuc": "carrot raw",
    "patates": "potato boiled",
    "beyaz_pilav": "white rice cooked",
    "bulgur_pilavi": "bulgur cooked",
    "makarna": "pasta cooked",
    "ekmek": "white bread",
    "beyaz_ekmek": "white bread",
    "simit": "sesame bread ring",
    "patates_kizartma": "french fries",
    "hamburger": "hamburger beef",
    "pizza": "pizza cheese",
    "hot_dog": "hot dog",
    "sandvic": "sandwich",
    "dondurma": "ice cream vanilla",
    "cay": "black tea",
    "turk_kahvesi": "turkish coffee",
    "cikolata": "dark chocolate",
    "biskuvi_kraker": "biscuit cracker",
    "peynir": "cheese white",
    "beyaz_peynir": "feta cheese",
    "kasar_peynir": "yellow cheese",
    "tereyagi": "butter",
    "sut": "whole milk",
    "karides": "shrimp cooked",
    "balik": "fish grilled",
    "hamsi": "anchovy",
    "levrek_cipura": "sea bass grilled",
    "tavuk": "chicken breast grilled",
    "et": "beef cooked",
    "kofte": "meatball beef",
    "ispanak": "spinach cooked",
    "kabak": "zucchini cooked",
    "patlican": "eggplant cooked",
    "mantar": "mushroom cooked",
    "karpuz": "watermelon",
    "uzum": "grapes",
    "cilek": "strawberry",
    "limon": "lemon",
    "incir": "fig fresh",
    "nar": "pomegranate",
    "kavun": "melon",
    "kivi": "kiwi",
    "kayisi": "apricot",
    "erik": "plum",
    "armut": "pear",
    "kuru_fasulye": "white beans cooked",
    "nohut": "chickpeas cooked",
    "mercimek": "lentils cooked",
    "barbunya": "borlotti beans cooked",
    "bezelye": "peas cooked",
    "zeytin": "olives",
    "cacik": "tzatziki yogurt cucumber",
    "humus": "hummus",
    "kisir": "bulgur salad",
    "coban_salatasi": "shepherd salad",
    "bamya": "okra cooked",
    "marul": "lettuce",
    "tursu": "pickles",
    "yumurta": "egg boiled",
    "omlet": "omelette",
    "kola_gazoz": "cola soda",
    "meyve_suyu": "fruit juice",
    "su": "water",
}

if os.path.exists(TURKOMP_PATH):
    with open(TURKOMP_PATH, encoding="utf-8") as f:
        TURKOMP = json.load(f)
else:
    TURKOMP = {}


def get_nutrition(food_name: str):
    if food_name in TURKOMP:
        return TURKOMP[food_name]

    query = TURKISH_TO_ENGLISH.get(food_name, food_name.replace("_", " "))

    try:
        url = "https://api.nal.usda.gov/fdc/v1/foods/search"
        params = {
            "query": query,
            "api_key": USDA_API_KEY,
            "pageSize": 1,
            "dataType": "SR Legacy,Foundation"
        }
        r = requests.get(url, params=params, timeout=5)
        data = r.json()

        if data.get("foods"):
            nutrients = data["foods"][0].get("foodNutrients", [])

            def get_val(name):
                for n in nutrients:
                    if name.lower() in n.get("nutrientName", "").lower():
                        return round(n.get("value", 0), 1)
                return 0

            return {
                "kalori": get_val("energy"),
                "karbonhidrat": get_val("carbohydrate"),
                "protein": get_val("protein"),
                "yag": get_val("total lipid"),
                "sodyum": get_val("sodium"),
                "potasyum": get_val("potassium"),
                "fosfor": get_val("phosphorus"),
                "seker": get_val("sugars"),
                "kaynak": "usda",
                "usda_isim": data["foods"][0].get("description", query)
            }

    except Exception as e:
        print("USDA hatasi: " + str(e))

    return None


def get_nutrition_list(food_names: list):
    result = {}
    for name in food_names:
        nutrition = get_nutrition(name)
        if nutrition:
            result[name] = nutrition
    return result