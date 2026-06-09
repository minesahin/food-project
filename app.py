import streamlit as st
import requests
from PIL import Image, ImageDraw, ImageFont
import io

API_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Tabak Uygunluk Uygulaması",
    page_icon="🍽️",
    layout="centered"
)

st.title("🍽️ Tabak İçeriği Uygunluk Tespiti")
st.write("Tabak fotoğrafınızı yükleyin, hastalığınıza uygun olup olmadığını öğrenin.")
st.divider()

hastalik = st.selectbox(
    "Hastalığınızı seçin:",
    ["diyabet", "hipertansiyon", "obezite", "bobrek"],
    format_func=lambda x: {
        "diyabet": "🩸 Tip 2 Diyabet",
        "hipertansiyon": "❤️ Hipertansiyon",
        "obezite": "⚖️ Obezite",
        "bobrek": "🫘 Kronik Böbrek Hastalığı"
    }[x]
)

foto = st.file_uploader("Tabak fotoğrafı yükleyin:", type=["jpg", "jpeg", "png"])

RENKLER = {
    "YASAK":   (220, 50,  50),
    "DIKKAT":  (255, 165,  0),
    "UYGUN":   (50,  180, 50),
    "default": (70,  130, 200)
}

def ciz_bbox(image, tespit, uyarilar_dict, uygun_dict):
    img = image.copy()

    max_size = 1200
    w, h = img.size
    if max(w, h) > max_size:
        scale = max_size / max(w, h)
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

    draw = ImageDraw.Draw(img)
    img_w, img_h = img.size

    for item in tespit:
        label = item["label"]
        bbox  = item["bbox"]
        conf  = item["confidence"]

        x1 = int(bbox["x"] / 100 * img_w)
        y1 = int(bbox["y"] / 100 * img_h)
        x2 = int((bbox["x"] + bbox["width"])  / 100 * img_w)
        y2 = int((bbox["y"] + bbox["height"]) / 100 * img_h)

        seviye = uyarilar_dict.get(label) or uygun_dict.get(label) or "default"
        renk   = RENKLER[seviye]


        for t in range(4):
            draw.rectangle([x1-t, y1-t, x2+t, y2+t], outline=renk)


        etiket_text = f"{label.replace('_',' ')} {int(conf*100)}%"
        font_size   = max(16, img_w // 40)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        bbox_text = draw.textbbox((x1, y1), etiket_text, font=font)
        tw = bbox_text[2] - bbox_text[0]
        th = bbox_text[3] - bbox_text[1]

        pad = 6
        label_y = max(0, y1 - th - pad * 2)
        draw.rectangle(
            [x1, label_y, x1 + tw + pad * 2, label_y + th + pad * 2],
            fill=renk
        )
        draw.text(
            (x1 + pad, label_y + pad),
            etiket_text,
            fill=(255, 255, 255),
            font=font
        )

    return img

if foto:
    image = Image.open(foto)
    st.image(image, caption="Yüklenen fotoğraf", use_container_width=True)

    if st.button("🔍 Analiz Et", type="primary", use_container_width=True):
        with st.spinner("Analiz ediliyor..."):
            try:
                foto.seek(0)
                response = requests.post(
                    API_URL + "/analyze",
                    files={"image": (foto.name, foto.getvalue(), "image/jpeg")},
                    data={"disease": hastalik},
                    timeout=30
                )
                result = response.json()

                if result.get("basarili"):
                    uygunluk = result["uygunluk"]
                    sonuc    = uygunluk["sonuc"]
                    tespit   = result["tespit"]

                    uyarilar_dict = {u["besin"]: u["seviye"] for u in uygunluk.get("uyarilar", [])}
                    uygun_dict    = {u["besin"]: "UYGUN"    for u in uygunluk.get("uygun_besinler", [])}


                    if tespit:
                        img_bbox = ciz_bbox(image, tespit, uyarilar_dict, uygun_dict)
                        st.image(img_bbox, caption="Tespit sonucu", use_container_width=True)
                    else:
                        st.image(image, caption="Tespit sonucu", use_container_width=True)


                    st.divider()
                    if sonuc == "UYGUN":
                        st.success(f"✅ {sonuc} — Skor: {uygunluk['skor']}/100")
                    elif sonuc == "KISMI UYGUN":
                        st.warning(f"⚠️ {sonuc} — Skor: {uygunluk['skor']}/100")
                    else:
                        st.error(f"❌ {sonuc} — Skor: {uygunluk['skor']}/100")

                    st.write(f"**{uygunluk['ozet']}**")
                    st.divider()


                    if tespit:
                        st.subheader("🔎 Tespit Edilen Yiyecekler")
                        unique = {d["label"]: d for d in tespit}
                        cols = st.columns(min(len(unique), 4))
                        for i, (lbl, item) in enumerate(unique.items()):
                            seviye = uyarilar_dict.get(lbl) or uygun_dict.get(lbl) or "default"
                            emoji  = {"YASAK": "🚫", "DIKKAT": "⚠️", "UYGUN": "✅", "default": "🔵"}[seviye]
                            with cols[i % 4]:
                                st.metric(
                                    label=f"{emoji} {lbl.replace('_', ' ').title()}",
                                    value=f"%{int(item['confidence']*100)}"
                                )
                    else:
                        st.info("Fotoğrafta yiyecek tespit edilemedi.")


                    uyarilar = uygunluk.get("uyarilar", [])
                    if uyarilar:
                        st.subheader("⚠️ Uyarılar")
                        for u in uyarilar:
                            if u["seviye"] == "YASAK":
                                st.error(f"🚫 {u['mesaj']}")
                            else:
                                st.warning(f"⚠️ {u['mesaj']}")


                    uygun = uygunluk.get("uygun_besinler", [])
                    if uygun:
                        st.subheader("✅ Uygun Besinler")
                        for u in uygun:
                            st.success(f"✅ {u['mesaj']}")


                    besin = result.get("besin_degerleri", {})
                    if besin:
                        st.subheader("📊 Besin Değerleri")
                        for isim, deger in besin.items():
                            with st.expander(isim.replace("_", " ").title()):
                                c1, c2, c3, c4 = st.columns(4)
                                c1.metric("Kalori",       f"{deger.get('kalori',0)} kcal")
                                c2.metric("Karbonhidrat", f"{deger.get('karbonhidrat',0)} g")
                                c3.metric("Protein",      f"{deger.get('protein',0)} g")
                                c4.metric("Yağ",          f"{deger.get('yag',0)} g")
                                c1.metric("Sodyum",       f"{deger.get('sodyum',0)} mg")
                                c2.metric("Potasyum",     f"{deger.get('potasyum',0)} mg")
                                kaynak = deger.get("kaynak", "")
                                st.caption(f"Kaynak: {'TürKomp' if kaynak == 'turkomp' else 'USDA FoodData Central'}")
                else:
                    st.error("Hata: " + result.get("hata", "Bilinmeyen hata"))

            except Exception as e:
                st.error(f"Bağlantı hatası: {e}")
                st.info("FastAPI backend çalışıyor mu? http://localhost:8000")