from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class NodeHealthResponse(BaseModel):

    node_id: UUID

    score: int

    status: str

    message: str | None

    evaluated_at: datetime

    updated_at: datetime

    class Config:
        from_attributes = True