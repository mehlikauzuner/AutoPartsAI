from pathlib import Path

import pytesseract
from PIL import Image

# Tesseract motorunun Windows konumu
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def extract_text(image_path: str) -> str:
    # Gorsel dosyasinin varligini kontrol et
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")

    # Orijinal gorseli OCR ile oku
    with Image.open(path) as image:
        text = pytesseract.image_to_string(
            image,
            lang="eng+tur",
            config="--psm 6"
        )

    return text.strip()
