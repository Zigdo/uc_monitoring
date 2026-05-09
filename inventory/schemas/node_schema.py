from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID
from datetime import datetime
from inventory.models.enums import CustomerType
from inventory.schemas.customer_schema import CustomerMini
from inventory.schemas.system_schema import SystemMini

class NodeBase(BaseModel):

    system_id: UUID | None = None

    hostname: str

    ip_address: str

    vendor: str

    node_type: str


class NodeCreate(NodeBase):
    pass

class NodeResponse(BaseModel):

    id: UUID

    hostname: str

    ip_address: str

    vendor: str

    node_type: str

    customer: CustomerMini

    system: SystemMini | None

    class Config:
        from_attributes = True


class NodeCreate(BaseModel):

    customer_id: UUID

    system_id: UUID | None = None

    hostname: str

    ip_address: str

    vendor: str

    #author: UserResponse - Example - option to validate also the user and return the data on the API response 



class CUCMNodeCreate(BaseModel):

    customer_id: UUID

    system_id: UUID

    hostname: str

    ip_address: str

    vendor: str

    version: str

    role: str


class CUCMDetailsResponse(BaseModel):

    cluster_role: str

    class Config:
        from_attributes = True

class CUCMNodeResponse(BaseModel):

    node: NodeResponse

    cucm_details: CUCMDetailsResponse

    class Config:
        from_attributes = True

class CUCMNodeUpdate(BaseModel):

    hostname: str | None = None

    ip_address: str | None = None