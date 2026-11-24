import re
from typing import Optional

from src.models.vehicle import Vehicle


def extract_vin(text: str) -> Optional[str]:
    """OCR metninden 17 karakterli VIN numarasini cikarir."""

    # VIN veya Sasi No etiketinden sonraki numarayi ara
    patterns = [
        r"VIN\)?\s*[:|]?\s*([A-HJ-NPR-Z0-9]{17})\b",
        r"SASI\s*NO\s*[:|]?\s*([A-HJ-NPR-Z0-9]{17})\b"
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).upper()

    # VIN bulunamazsa None dondur
    return None


def extract_vehicle_info(text: str) -> Vehicle:
    """OCR metninden arac bilgilerini cikarir ve Vehicle nesnesi olusturur."""

    # Hem sentetik belge hem ruhsat formatindaki alanlari tanimla
    vin = extract_vin(text)
    brand_match = re.search(
        r"(?:Marka\s*:|MARKA)\s*([A-Za-zÇĞİÖŞÜçğıöşü-]+)",
        text,
        re.IGNORECASE
    )
    model_match = re.search(
        r"(?:Model\s*:|TIP)\s*([A-Za-z0-9-]+)",
        text,
        re.IGNORECASE
    )
    year_match = re.search(
        r"(?:Yil\s*:|MODEL\s*YILI)\s*(\d{4})",
        text,
        re.IGNORECASE
    )

    # Gerekli bilgilerden biri eksikse hata ver
    if not all([vin, brand_match, model_match, year_match]):
        raise ValueError("Vehicle information is incomplete")

    # Bilgileri Vehicle modeline aktar ve dogrula
    return Vehicle(
        vin=vin,
        brand=brand_match.group(1).strip(),
        model=model_match.group(1).strip(),
        year=int(year_match.group(1))
    )
