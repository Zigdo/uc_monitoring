from pydantic import BaseModel
from uuid import UUID

from app.inventory.models.enums import ApplicationType



class SystemCreate(BaseModel):
    customer_id: UUID
    type: ApplicationType
    monitoring_profile_id: UUID

class SystemResponse(BaseModel):
    id: UUID

    customer_id: UUID

    type: ApplicationType

    sequence_number: int

    system_code: str

    monitoring_profile_id: UUID

    class Config:
        from_attributes = True


class SystemMini(BaseModel):
    id: UUID
    system_code: str
    type: ApplicationType

    class Config:
        from_attributes = True