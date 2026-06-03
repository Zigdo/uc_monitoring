from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from app.inventory.models.enums import (
    ExecutionStatus,
    ExecutionStage
)


class MonitoringExecutionStateResponse(BaseModel):

    id: UUID

    node_id: UUID

    implementation_id: UUID

    current_status: ExecutionStatus

    current_stage: ExecutionStage

    current_message: str | None

    last_started_at: datetime | None

    last_finished_at: datetime | None

    last_duration_ms: int | None

    last_success_at: datetime | None

    last_failure_at: datetime | None

    last_error_type: str | None

    last_error_message: str | None

    consecutive_failures: int

    total_successes: int

    total_failures: int

    total_executions: int

    class Config:

        from_attributes = True