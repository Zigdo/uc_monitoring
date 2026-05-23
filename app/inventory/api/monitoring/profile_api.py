from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session
from sqlalchemy import select

from uuid import UUID
from typing import Annotated

from app.db.session import get_db

from app.inventory.models.monitoring.monitoring_profile import (
    MonitoringProfile
)

from app.inventory.schemas.monitoring_profile_schema import (
    MonitoringProfileCreate,
    MonitoringProfileResponse
)


router = APIRouter(
    prefix="/inventory/api/v1/monitoring/profiles",
    tags=["Monitoring Profiles"]
)


@router.get(
    "/",
    response_model=list[MonitoringProfileResponse]
)
def get_profiles(
    db: Annotated[Session, Depends(get_db)]
):

    return db.query(
        MonitoringProfile
    ).order_by(
        MonitoringProfile.name
    ).all()


@router.get(
    "/{id}",
    response_model=MonitoringProfileResponse
)
def get_profile(
    id: UUID,
    db: Annotated[Session, Depends(get_db)]
):

    profile = db.query(
        MonitoringProfile
    ).get(id)

    if not profile:

        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    return profile


@router.post(
    "/",
    response_model=MonitoringProfileResponse,
    status_code=status.HTTP_201_CREATED
)
def create_profile(
    profile: MonitoringProfileCreate,
    db: Annotated[Session, Depends(get_db)]
):

    result = db.execute(
        select(MonitoringProfile).where(
            MonitoringProfile.name == profile.name
        )
    )

    existing = result.scalars().first()

    if existing:

        raise HTTPException(
            status_code=400,
            detail="Profile already exists"
        )

    new_profile = MonitoringProfile(
        **profile.model_dump()
    )

    db.add(new_profile)

    db.commit()

    db.refresh(new_profile)

    return new_profile


@router.put("/{profile_id}")
def update_profile(
    profile_id: UUID,
    data: dict,
    db: Annotated[Session, Depends(get_db)]
):

    profile = db.query(
        MonitoringProfile
    ).get(profile_id)

    if not profile:

        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    for key, value in data.items():

        setattr(profile, key, value)

    db.commit()

    db.refresh(profile)

    return profile


@router.delete("/{profile_id}")
def delete_profile(
    profile_id: UUID,
    db: Annotated[Session, Depends(get_db)]
):

    profile = db.query(
        MonitoringProfile
    ).get(profile_id)

    if not profile:

        raise HTTPException(
            status_code=404,
            detail="Profile not found"
        )

    db.delete(profile)

    db.commit()

    return {"status": "deleted"}