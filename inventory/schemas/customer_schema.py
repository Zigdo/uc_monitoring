from pydantic import BaseModel, ConfigDict, Field
import uuid
# from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from inventory.models.enums import CustomerType

class CustomerBase(BaseModel):
    code_name: str = Field(pattern="^[a-z0-9_]+$", min_length=1, max_length=100)
    display_name: str = Field(min_length=1, max_length=100)
    type: CustomerType


class CustomerCreate(CustomerBase):
    pass

class CustomerResponse(CustomerBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    code_name: str
    display_name: str
    type: CustomerType
    created_at: datetime
    updated_at: datetime
    #author: UserResponse - Example - option to validate also the user and return the data on the API response 


class CustomerMini(BaseModel):
    id: uuid.UUID
    display_name: str

    class Config:
        from_attributes = True