"""Pydantic models for validating HCGateway steps data."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, field_validator


class StepsData(BaseModel):  # type: ignore[misc]
    """Model for the 'data' field in a step record."""

    count: int = Field(..., ge=0, description="Step count, must be non-negative")


class StepsRecord(BaseModel):  # type: ignore[misc]
    """Model for a single step record from the HCGateway API."""

    _id: str
    app: str
    data: StepsData
    end: str
    id: str
    start: str

    @field_validator("end", "start")  # type: ignore[misc]
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

    @property
    def end_dt(self) -> datetime | None:
        """Return the 'end' field as a datetime object, or None if invalid."""
        v = self.end
        if v.endswith("Z"):
            v = v[:-1] + "+00:00"
        try:
            return datetime.fromisoformat(v)
        except (ValueError, TypeError):
            return None

    @property
    def start_dt(self) -> datetime | None:
        """Return the 'start' field as a datetime object, or None if invalid."""
        v = self.start
        if v.endswith("Z"):
            v = v[:-1] + "+00:00"
        try:
            return datetime.fromisoformat(v)
        except (ValueError, TypeError):
            return None


def validate_steps_list(steps: list[dict[str, Any]]) -> list[StepsRecord]:
    """Validate a list of step dicts, returning StepRecord objects or raising ValidationError."""
    return [StepsRecord.model_validate(item) for item in steps]
