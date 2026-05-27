from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
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

    monitoring_profile_id: UUID

    # created_at: datetime
    # updated_at: datetime

    class Config:
        from_attributes = True


class SystemMini(BaseModel):
    id: UUID
    system_code: str
    type: ApplicationType

    class Config:
        from_attributes = True