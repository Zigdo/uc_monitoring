from pydantic import BaseModel, ConfigDict
from uuid import UUID


# Base shared fields
class MonitoringCapabilityBase(BaseModel):
    name: str
    description: str | None = None


# CREATE
class MonitoringCapabilityCreate(MonitoringCapabilityBase):
    pass


# UPDATE
class MonitoringCapabilityUpdate(BaseModel):
    name: str | None = None
    description: str | None = None


# RESPONSE
class MonitoringCapabilityResponse(MonitoringCapabilityBase):
    id: UUID

    model_config = ConfigDict(from_attributes=True)