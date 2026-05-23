from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session
from sqlalchemy import select

from uuid import UUID
from typing import Annotated

from app.db.session import get_db

from app.inventory.models.monitoring.node_monitoring_override import (
    NodeMonitoringOverride
)

from app.inventory.schemas.node_monitoring_override_schema import (
    NodeMonitoringOverrideCreate,
    NodeMonitoringOverrideResponse
)


router = APIRouter(
    prefix="/inventory/api/v1/monitoring/overrides",
    tags=["Node Monitoring Overrides"]
)


# LIST ALL OVERRIDES
@router.get(
    "/",
    response_model=list[NodeMonitoringOverrideResponse]
)
def get_overrides(
    db: Annotated[Session, Depends(get_db)]
):

    overrides = db.query(
        NodeMonitoringOverride
    ).all()

    return overrides


# GET ONE OVERRIDE
@router.get(
    "/{id}",
    response_model=NodeMonitoringOverrideResponse
)
def get_override(
    id: UUID,
    db: Annotated[Session, Depends(get_db)]
):

    override = db.query(
        NodeMonitoringOverride
    ).get(id)

    if not override:

        raise HTTPException(
            status_code=404,
            detail="Override not found"
        )

    return override


# CREATE OVERRIDE
@router.post(
    "/",
    response_model=NodeMonitoringOverrideResponse,
    status_code=status.HTTP_201_CREATED
)
def create_override(
    override: NodeMonitoringOverrideCreate,
    db: Annotated[Session, Depends(get_db)]
):

    # Prevent duplicate override
    result = db.execute(
        select(NodeMonitoringOverride).where(
            NodeMonitoringOverride.node_id
            == override.node_id,

            NodeMonitoringOverride.implementation_id
            == override.implementation_id
        )
    )

    existing = result.scalars().first()

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Override already exists for node"
        )

    new_override = NodeMonitoringOverride(
        **override.model_dump()
    )

    db.add(new_override)

    db.commit()

    db.refresh(new_override)

    return new_override


# UPDATE OVERRIDE
@router.put("/{override_id}")
def update_override(
    override_id: UUID,
    data: dict,
    db: Annotated[Session, Depends(get_db)]
):

    override = db.query(
        NodeMonitoringOverride
    ).get(override_id)

    if not override:

        raise HTTPException(
            status_code=404,
            detail="Override not found"
        )

    for key, value in data.items():

        setattr(override, key, value)

    db.commit()

    db.refresh(override)

    return override


# DELETE OVERRIDE
@router.delete("/{override_id}")
def delete_override(
    override_id: UUID,
    db: Annotated[Session, Depends(get_db)]
):

    override = db.query(
        NodeMonitoringOverride
    ).get(override_id)

    if not override:

        raise HTTPException(
            status_code=404,
            detail="Override not found"
        )

    db.delete(override)

    db.commit()

    return {"status": "deleted"}