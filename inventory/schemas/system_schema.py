from pydantic import BaseModel
from uuid import UUID

from inventory.models.enums import ApplicationType



class SystemCreate(BaseModel):
    customer_id: UUID
    type: ApplicationType

class SystemResponse(BaseModel):
    id: UUID

    customer_id: UUID

    type: ApplicationType

    sequence_number: int

    system_code: str

    class Config:
        from_attributes = True


class SystemMini(BaseModel):
    id: UUID
    system_code: str
    type: ApplicationType

    class Config:
        from_attributes = True