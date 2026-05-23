from pydantic import BaseModel, ConfigDict
from uuid import UUID


class MonitoringProfileJobBase(BaseModel):
    profile_id: UUID
    implementation_id: UUID
    interval_seconds: int


class MonitoringProfileJobCreate(MonitoringProfileJobBase):
    pass


class MonitoringProfileJobUpdate(BaseModel):
    interval_seconds: int | None = None


class MonitoringProfileJobResponse(MonitoringProfileJobBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)