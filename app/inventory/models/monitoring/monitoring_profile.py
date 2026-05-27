from __future__ import annotations

import uuid
from typing import List

from sqlalchemy import String

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.inventory.models.node import NodeBase
    from app.inventory.models.system import System
    from app.inventory.models.monitoring.monitoring_profile_job import MonitoringProfileJob

class MonitoringProfile(Base):

    __tablename__ = "monitoring_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )


    #Relationships
    #  nodes: Mapped[List["NodeBase"]] = relationship(
    jobs: Mapped[List["MonitoringProfileJob"]] = relationship(
        back_populates="profile",
        cascade="all, delete-orphan",
        lazy="selectin"
    )

    systems: Mapped["System"] = relationship(
        back_populates="monitoring_profile"
    )

