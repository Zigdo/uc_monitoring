from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session
from sqlalchemy import select

from uuid import UUID
from typing import Annotated

from app.db.session import get_db

from app.inventory.models.monitoring.monitoring_profile_job import (
    MonitoringProfileJob
)

from app.inventory.schemas.monitoring_profile_job_schema import (
    MonitoringProfileJobCreate,
    MonitoringProfileJobResponse
)


router = APIRouter(
    prefix="/inventory/api/v1/monitoring/profile-jobs",
    tags=["Monitoring Profile Jobs"]
)


# LIST ALL PROFILE JOBS
@router.get(
    "/",
    response_model=list[MonitoringProfileJobResponse]
)
def get_profile_jobs(
    db: Annotated[Session, Depends(get_db)]
):

    profile_jobs = db.query(
        MonitoringProfileJob
    ).all()

    return profile_jobs


# GET ONE PROFILE JOB
@router.get(
    "/{id}",
    response_model=MonitoringProfileJobResponse
)
def get_profile_job(
    id: UUID,
    db: Annotated[Session, Depends(get_db)]
):

    profile_job = db.query(
        MonitoringProfileJob
    ).get(id)

    if not profile_job:

        raise HTTPException(
            status_code=404,
            detail="Profile job not found"
        )

    return profile_job


# CREATE PROFILE JOB
@router.post(
    "/",
    response_model=MonitoringProfileJobResponse,
    status_code=status.HTTP_201_CREATED
)
def create_profile_job(
    profile_job: MonitoringProfileJobCreate,
    db: Annotated[Session, Depends(get_db)]
):

    # Prevent duplicate implementation assignment
    result = db.execute(
        select(MonitoringProfileJob).where(
            MonitoringProfileJob.profile_id
            == profile_job.profile_id,

            MonitoringProfileJob.implementation_id
            == profile_job.implementation_id
        )
    )

    existing = result.scalars().first()

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Implementation already assigned to profile"
        )

    new_profile_job = MonitoringProfileJob(
        **profile_job.model_dump()
    )

    db.add(new_profile_job)

    db.commit()

    db.refresh(new_profile_job)

    return new_profile_job


# UPDATE PROFILE JOB
@router.put("/{profile_job_id}")
def update_profile_job(
    profile_job_id: UUID,
    data: dict,
    db: Annotated[Session, Depends(get_db)]
):

    profile_job = db.query(
        MonitoringProfileJob
    ).get(profile_job_id)

    if not profile_job:

        raise HTTPException(
            status_code=404,
            detail="Profile job not found"
        )

    for key, value in data.items():

        setattr(profile_job, key, value)

    db.commit()

    db.refresh(profile_job)

    return profile_job


# DELETE PROFILE JOB
@router.delete("/{profile_job_id}")
def delete_profile_job(
    profile_job_id: UUID,
    db: Annotated[Session, Depends(get_db)]
):

    profile_job = db.query(
        MonitoringProfileJob
    ).get(profile_job_id)

    if not profile_job:

        raise HTTPException(
            status_code=404,
            detail="Profile job not found"
        )

    db.delete(profile_job)

    db.commit()

    return {"status": "deleted"}