from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session
from sqlalchemy import select

from uuid import UUID
from typing import Annotated

from app.db.session import get_db

from app.inventory.models.monitoring.monitoring_capability import (
    MonitoringCapability
)

from app.inventory.schemas.monitoring_capability_schema import (
    MonitoringCapabilityCreate,
    MonitoringCapabilityResponse
)


router = APIRouter(
    prefix="/inventory/api/v1/monitoring/capabilities",
    tags=["Monitoring Capabilities"]
)


# LIST
@router.get(
    "/",
    response_model=list[MonitoringCapabilityResponse]
)
def get_capabilities(
    db: Annotated[Session, Depends(get_db)]
):

    capabilities = db.query(
        MonitoringCapability
    ).order_by(
        MonitoringCapability.name
    ).all()

    return capabilities


# GET ONE
@router.get(
    "/{id}",
    response_model=MonitoringCapabilityResponse
)
def get_capability(
    id: UUID,
    db: Annotated[Session, Depends(get_db)]
):

    capability = db.query(
        MonitoringCapability
    ).get(id)

    if not capability:

        raise HTTPException(
            status_code=404,
            detail="Capability not found"
        )

    return capability


# CREATE
@router.post(
    "/",
    response_model=MonitoringCapabilityResponse,
    status_code=status.HTTP_201_CREATED
)
def create_capability(
    capability: MonitoringCapabilityCreate,
    db: Annotated[Session, Depends(get_db)]
):

    result = db.execute(
        select(MonitoringCapability).where(
            MonitoringCapability.name == capability.name
        )
    )

    existing = result.scalars().first()

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Capability already exists"
        )

    new_capability = MonitoringCapability(
        name=capability.name,
        description=capability.description
    )

    db.add(new_capability)

    db.commit()

    db.refresh(new_capability)

    return new_capability


# UPDATE
@router.put("/{capability_id}")
def update_capability(
    capability_id: UUID,
    data: dict,
    db: Annotated[Session, Depends(get_db)]
):

    capability = db.query(
        MonitoringCapability
    ).get(capability_id)

    if not capability:

        raise HTTPException(
            status_code=404,
            detail="Capability not found"
        )

    for key, value in data.items():

        setattr(capability, key, value)

    db.commit()

    db.refresh(capability)

    return capability


# DELETE
@router.delete("/{capability_id}")
def delete_capability(
    capability_id: UUID,
    db: Annotated[Session, Depends(get_db)]
):

    capability = db.query(
        MonitoringCapability
    ).get(capability_id)

    if not capability:

        raise HTTPException(
            status_code=404,
            detail="Capability not found"
        )

    db.delete(capability)

    db.commit()

    return {"status": "deleted"}