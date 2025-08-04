"""Generic base model for HCGateway records with flexible data field."""

from datetime import datetime

from pydantic import BaseModel, field_validator


class GatewayRecord[T: BaseModel](BaseModel):
    """Generic model for a single record from the HCGateway API."""

    _id: str
    app: str
    data: T
    end: str
    id: str
    start: str

    @field_validator("end", "start")
    @classmethod
    def validate_datetime(cls, v: str) -> str:
        """Validate that the datetime string is in ISO 8601 format (with or without Z)."""
        if v.endswith("Z"):
            v = v[:-1] + "+00:00"
        try:
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
