import tempfile
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from PIL import UnidentifiedImageError

from src.models.vehicle import Vehicle
from src.models.part import PartRequest
from src.vehicle_detection.ocr import extract_text
from src.vehicle_detection.parser import extract_vehicle_info


app = FastAPI(
    title="AutoPartsAI API",
    description="Automotive Spare Parts Workflow Automation System",
    version="0.1.0",
)


@app.get("/chat", response_class=FileResponse, include_in_schema=False)
def chat_page():
    return FileResponse(Path(__file__).with_name("chat.html"))


@app.get("/")
def root():
    return {
        "message": "Welcome to AutoPartsAI API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "application": "AutoPartsAI"
    }


@app.post("/vehicles", response_model=Vehicle)
def create_vehicle(vehicle: Vehicle):
    # Araç bilgilerini doğrula ve geri döndür
    return vehicle


@app.post("/part-requests", response_model=PartRequest)
def create_part_request(request: PartRequest):
    # Parça talebini doğrula ve geri döndür
    return request


@app.post("/vehicles/upload-registration", response_model=Vehicle)
async def upload_registration(file: UploadFile = File(...)):
    # Yüklenen dosyanın görsel olup olmadığını kontrol et
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Please upload an image file")

    temp_path = None

    try:
        # Görseli geçici bir dosyaya kaydet
        with tempfile.NamedTemporaryFile(suffix=".img", delete=False) as temp_file:
            temp_file.write(await file.read())
            temp_path = Path(temp_file.name)

        # OCR ile görseldeki metinleri çıkar
        text = extract_text(str(temp_path))

        # Metinden araç bilgilerini çıkar ve doğrula
        vehicle = extract_vehicle_info(text)

        return vehicle

    except (ValueError, UnidentifiedImageError) as error:
        # Görsel okunamazsa veya araç bilgileri eksikse hata döndür
        raise HTTPException(status_code=422, detail=str(error))

    finally:
        # İşlem bitince geçici görsel dosyasını sil
        if temp_path and temp_path.exists():
            temp_path.unlink()

        await file.close()
