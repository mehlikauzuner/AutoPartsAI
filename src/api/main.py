from fastapi import FastAPI

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
