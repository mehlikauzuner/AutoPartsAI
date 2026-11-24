from fastapi import FastAPI
from src.models.vehicle import Vehicle
from src.models.part import PartRequest

app = FastAPI(
    title="AutoPartsAI API",
    description="Automotive Spare Parts Workflow Automation System",
    version="0.1.0",
)


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
