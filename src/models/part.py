from typing import Optional
from pydantic import BaseModel, Field, field_validator


class PartRequest(BaseModel):
    """Represent a spare part request submitted by a user."""

    part_name: str = Field(..., min_length=1, description="Requested spare part name")
    brand_preference: Optional[str] = None
    quantity: int = Field(default=1, ge=1)
    notes: Optional[str] = None

    @field_validator("part_name")
    @classmethod
    def validate_part_name(cls, value: str) -> str:
        """Prevent empty part names."""
        value = value.strip()
        if not value:
            raise ValueError("Part name cannot be empty")
        return value

    @field_validator("brand_preference", "notes")
    @classmethod
    def clean_optional_text(cls, value: Optional[str]) -> Optional[str]:
        """Normalize optional text fields."""
        if value is not None:
            return value.strip() or None
        return value
