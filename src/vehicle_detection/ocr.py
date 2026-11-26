from pathlib import Path

import os

import pytesseract
from dotenv import load_dotenv
from PIL import Image

# Proje kökündeki .env dosyası varsa yükle. TESSERACT_CMD tanımlı değilse
# pytesseract, sistem PATH'indeki `tesseract` komutunu kullanır.
load_dotenv(Path(__file__).resolve().parents[2] / ".env")
tesseract_cmd = os.getenv("TESSERACT_CMD")
if tesseract_cmd:
    pytesseract.pytesseract.tesseract_cmd = tesseract_cmd


def extract_text(image_path: str) -> str:
    # Gorsel dosyasinin varligini kontrol et
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    with Image.open(path) as image:
        # Önce görselin tamamını oku.
        text = pytesseract.image_to_string(image, lang="tur", config="--psm 6")
        upper_text = text.upper()

        # Etiketlerden biri eksikse sol taraftaki araç tablosunun tamamını yeniden tara.
        field_labels = (
            ("VIN", "SASI", "ŞASİ"),
            ("MARKA",),
            ("TİP", "TIP", "MODEL:"),
            ("MODEL YILI", "YIL:"),
            ("MOTOR HACMİ", "MOTOR HACMI"),
            ("YAKIT",),
        )
        if not all(any(label in upper_text for label in labels) for labels in field_labels):
            width, height = image.size
            strip_height = max(1, int(height * 0.075))
            step = max(1, int(height * 0.05))
            target_width = min(width, 2000)
            strips = []

            # Biraz üst üste gelen şeritler satırların kesilmesini önler.
            for top in range(0, height, step):
                strip = image.crop((0, top, width // 2, min(top + strip_height, height))).convert("L")
                resized_height = max(1, int(strip.height * target_width / strip.width))
                strips.append(strip.resize((target_width, resized_height)))

            gap = max(4, target_width // 150)
            montage_height = sum(strip.height for strip in strips) + gap * (len(strips) - 1)
            montage = Image.new("L", (target_width, montage_height), color=255)
            top = 0
            for strip in strips:
                montage.paste(strip, (0, top))
                top += strip.height + gap

            # Tüm şeritleri tek ek Tesseract çağrısında oku.
            extra_text = pytesseract.image_to_string(montage, lang="tur", config="--psm 6")
            text = f"{text}\n{extra_text}"

    return text.strip()
