import uuid

from sqlalchemy import Integer
from sqlalchemy import ForeignKey

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.inventory.models.monitoring.monitoring_profile_job import MonitoringProfile
    from app.inventory.models.monitoring.monitoring_job_implementation import MonitoringJobImplementation

class MonitoringProfileJob(Base):

    __tablename__ = "monitoring_profile_jobs"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "monitoring_profiles.id"
        ),
        nullable=False
    )

    implementation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "monitoring_job_implementations.id"
        ),
        nullable=False
    )

    interval_seconds: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )


    #Relationships

    profile: Mapped["MonitoringProfile"] = relationship(
        back_populates="jobs"
    )

    implementation: Mapped["MonitoringJobImplementation"] = relationship(
        back_populates="profile_assignments"
    )