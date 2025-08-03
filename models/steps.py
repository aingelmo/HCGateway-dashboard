"""Pydantic models for validating HCGateway steps data."""

from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class StepsData(BaseModel):
    """Model for the 'data' field in a step record."""

    count: int = Field(..., ge=0, description="Step count, must be non-negative")


class StepsRecord(BaseModel):
    """Model for a single step record from the HCGateway API."""

    _id: str
    app: str
    data: StepsData
    end: str
    id: str
    start: str

    @field_validator("end", "start")
    @classmethod
    def validate_datetime(cls, v: str) -> str:
        """Validate that the datetime string is in ISO 8601 format (with or without Z)."""
        try:
            # Accepts both 'Z' and offset
            if v.endswith("Z"):
                # Replace 'Z' with '+00:00' for fromisoformat compatibility
                v = v[:-1] + "+00:00"
            datetime.fromisoformat(v)
        except ValueError as err:
            msg = f"Invalid ISO 8601 datetime: {v}"
            raise ValueError(msg) from err
        return v


def validate_steps_list(steps: list[dict]) -> list[StepsRecord]:
    """Validate a list of step dicts, returning StepRecord objects or raising ValidationError."""
    return [StepsRecord.model_validate(item) for item in steps]
