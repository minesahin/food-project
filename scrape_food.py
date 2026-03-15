from ddgs import DDGS
from pathlib import Path
import requests
import time
from PIL import Image
import io

OUTPUT_BASE = "./dataset/test_scraped"

def scrape(label, query, count=10):
    save_dir = Path(OUTPUT_BASE) / label
    save_dir.mkdir(parents=True, exist_ok=True)

    downloaded = 0
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        time.sleep(3)
        with DDGS() as ddgs:
            results = list(ddgs.images(
               query,
                region="tr-tr",
                safesearch="moderate",
                size="Medium",
                type_image="photo",
                max_results=count * 3,
            ))
    except Exception as e:
        print("HATA: " + str(e))
        return 0

    for result in results:
        if downloaded >= count:
            break
        try:
            response = requests.get(result["image"], timeout=5, headers=headers)
            if response.status_code != 200:
                continue
            img = Image.open(io.BytesIO(response.content))
            if img.width < 150 or img.height < 150:
                continue
            img = img.convert("RGB")
            save_path = save_dir / (label + "_" + str(downloaded).zfill(4) + ".jpg")
            img.save(save_path, "JPEG", quality=90)
            downloaded += 1
        except Exception:
            continue
        time.sleep(0.2)

    print(label + " -> " + str(downloaded) + " goruntu indirildi")
    return downloaded


if __name__ == "__main__":
    scrape("baklava", "baklava turkish dessert", count=5)
    scrape("kofte", "kofte turkish meatball", count=5)
    scrape("ayran", "ayran yogurt drink turkish", count=5)
    print("Test tamamlandi!")
    print("Kontrol: " + str(Path(OUTPUT_BASE).absolute()))