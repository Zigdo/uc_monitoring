import uuid

from sqlalchemy import String
from sqlalchemy import ForeignKey

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base


class MonitoringJobImplementation(Base):

    __tablename__ = "monitoring_job_implementations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    capability_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "monitoring_capabilities.id"
        ),
        nullable=False
    )

    implementation_key: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )

    platform: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    collector_path: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    parser_path: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    writer_path: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    capability = relationship(
        "MonitoringCapability",
        back_populates="implementations"
    )

    profile_assignments = relationship(
        "MonitoringProfileJob",
        back_populates="implementation"
    )