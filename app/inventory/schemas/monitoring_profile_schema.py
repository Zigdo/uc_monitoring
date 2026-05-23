from pydantic import BaseModel, ConfigDict
from uuid import UUID


class MonitoringProfileBase(BaseModel):
    name: str
    description: str | None = None


class MonitoringProfileCreate(MonitoringProfileBase):
    pass


class MonitoringProfileUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


class MonitoringProfileResponse(MonitoringProfileBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)