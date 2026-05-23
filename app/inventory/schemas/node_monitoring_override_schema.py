from pydantic import BaseModel, ConfigDict
from uuid import UUID


class NodeMonitoringOverrideBase(BaseModel):
    node_id: UUID
    implementation_id: UUID
    enabled: bool = True
    interval_seconds: int | None = None


class NodeMonitoringOverrideCreate(NodeMonitoringOverrideBase):
    pass


class NodeMonitoringOverrideUpdate(BaseModel):
    enabled: bool | None = None
    interval_seconds: int | None = None


class NodeMonitoringOverrideResponse(NodeMonitoringOverrideBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)