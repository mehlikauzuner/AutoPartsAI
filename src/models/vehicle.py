from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, field_validator


class Vehicle(BaseModel):
    """Represent a vehicle and its identification information."""

    vin: str = Field(..., min_length=17, max_length=17)
    brand: str = Field(..., min_length=1)
    model: str = Field(..., min_length=1)
    year: int = Field(..., ge=1900, le=date.today().year)
    engine: Optional[str] = None
    fuel_type: Optional[str] = None

    @field_validator("vin")
    @classmethod
    def validate_vin(cls, value: str) -> str:
        """Validate the VIN format."""
        value = value.strip().upper()
        if len(value) != 17:
            raise ValueError("VIN must contain exactly 17 characters")
        if not value.isalnum() or any(char in value for char in "IOQ"):
            raise ValueError("VIN contains invalid characters")
        return value

    @field_validator("brand", "model")
    @classmethod
    def validate_required_text(cls, value: str) -> str:
        """Prevent empty brand and model values."""
        value = value.strip()
        if not value:
            raise ValueError("This field cannot be empty")
        return value
