"""Models for steps data in the HCGateway dashboard."""

from typing import Any

from pydantic import BaseModel, Field

from hcgateway_dashboard.models.common import GatewayRecord


class StepsData(BaseModel):
    """Model for the 'data' field in a step record."""

    count: int = Field(..., ge=0, description="Step count, must be non-negative")


class StepsRecord(GatewayRecord[StepsData]):
    """Model for a single step record from the HCGateway API (specialized GatewayRecord)."""


def validate_steps_list(steps: list[dict[str, Any]]) -> list[StepsRecord]:
    """Validate a list of step dicts, returning StepRecord objects or raising ValidationError."""
    return [StepsRecord.model_validate(item) for item in steps]
