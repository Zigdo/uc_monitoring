from pydantic import BaseModel, ConfigDict, Field, EmailStr
import uuid

class ContactsBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr = Field(min_length=1, max_length=100)
    title: str = Field(min_length=1, max_length=100)


class ContactsCreate(ContactsBase):
    pass

class ContactsResponse(ContactsBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID