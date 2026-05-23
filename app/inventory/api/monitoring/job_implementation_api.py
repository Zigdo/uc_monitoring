from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session
from sqlalchemy import select

from uuid import UUID
from typing import Annotated

from app.db.session import get_db

from app.inventory.models.monitoring.monitoring_job_implementation import (
    MonitoringJobImplementation
)

from app.inventory.schemas.monitoring_job_implementation_schema import (
    MonitoringJobImplementationCreate,
    MonitoringJobImplementationResponse
)


router = APIRouter(
    prefix="/inventory/api/v1/monitoring/implementations",
    tags=["Monitoring Implementations"]
)


# LIST
@router.get(
    "/",
    response_model=list[MonitoringJobImplementationResponse]
)
def get_implementations(
    db: Annotated[Session, Depends(get_db)]
):

    return db.query(
        MonitoringJobImplementation
    ).order_by(
        MonitoringJobImplementation.implementation_key
    ).all()


# GET ONE
@router.get(
    "/{id}",
    response_model=MonitoringJobImplementationResponse
)
def get_implementation(
    id: UUID,
    db: Annotated[Session, Depends(get_db)]
):

    implementation = db.query(
        MonitoringJobImplementation
    ).get(id)

    if not implementation:

        raise HTTPException(
            status_code=404,
            detail="Implementation not found"
        )

    return implementation


# CREATE
@router.post(
    "/",
    response_model=MonitoringJobImplementationResponse,
    status_code=status.HTTP_201_CREATED
)
def create_implementation(
    implementation: MonitoringJobImplementationCreate,
    db: Annotated[Session, Depends(get_db)]
):

    result = db.execute(
        select(MonitoringJobImplementation).where(
            MonitoringJobImplementation.implementation_key
            == implementation.implementation_key
        )
    )

    existing = result.scalars().first()

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Implementation already exists"
        )

    new_implementation = MonitoringJobImplementation(
        **implementation.model_dump()
    )

    db.add(new_implementation)

    db.commit()

    db.refresh(new_implementation)

    return new_implementation


# UPDATE
@router.put("/{implementation_id}")
def update_implementation(
    implementation_id: UUID,
    data: dict,
    db: Annotated[Session, Depends(get_db)]
):

    implementation = db.query(
        MonitoringJobImplementation
    ).get(implementation_id)

    if not implementation:

        raise HTTPException(
            status_code=404,
            detail="Implementation not found"
        )

    for key, value in data.items():

        setattr(implementation, key, value)

    db.commit()

    db.refresh(implementation)

    return implementation


# DELETE
@router.delete("/{implementation_id}")
def delete_implementation(
    implementation_id: UUID,
    db: Annotated[Session, Depends(get_db)]
):

    implementation = db.query(
        MonitoringJobImplementation
    ).get(implementation_id)

    if not implementation:

        raise HTTPException(
            status_code=404,
            detail="Implementation not found"
        )

    db.delete(implementation)

    db.commit()

    return {"status": "deleted"}