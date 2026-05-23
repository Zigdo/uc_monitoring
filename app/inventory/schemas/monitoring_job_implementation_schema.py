from pydantic import BaseModel, ConfigDict
from uuid import UUID


class MonitoringJobImplementationBase(BaseModel):
    capability_id: UUID
    implementation_key: str
    platform: str

    collector_path: str
    parser_path: str | None = None
    writer_path: str | None = None


class MonitoringJobImplementationCreate(MonitoringJobImplementationBase):
    pass


class MonitoringJobImplementationUpdate(BaseModel):
    implementation_key: str | None = None
    platform: str | None = None
    collector_path: str | None = None
    parser_path: str | None = None
    writer_path: str | None = None


class MonitoringJobImplementationResponse(MonitoringJobImplementationBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)