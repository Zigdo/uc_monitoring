from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class NodeMetricStateResponse(BaseModel):

    id: UUID

    node_id: UUID

    metric_name: str

    metric_data: dict

    message: str | None

    collected_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True