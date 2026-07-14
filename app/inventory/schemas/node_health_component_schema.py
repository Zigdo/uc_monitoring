from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.inventory.models.enums import (
    HealthStatus
)


class NodeHealthComponentResponse(BaseModel):

    id: UUID

    node_id: UUID

    component_name: str

    status: HealthStatus

    score: int

    message: str | None

    evaluated_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True