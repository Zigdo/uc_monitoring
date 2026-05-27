from __future__ import annotations

import uuid
from typing import List

from sqlalchemy import ForeignKey, Enum, Index, UniqueConstraint, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

from .mixins import TimestampMixin
from .enums import ApplicationType

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.inventory.models.customer import Customer
    from app.inventory.models.node import NodeBase
    from app.inventory.models.monitoring.monitoring_profile import MonitoringProfile

# Add TimestampMixin
class System(Base,):
    __tablename__ = "systems"

    __table_args__ = (
        UniqueConstraint(
            "customer_id",
            "system_type",
            "sequence_number",
            name="uq_system_sequence"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customers.id"),
        nullable=False
    )

    type: Mapped[ApplicationType] = mapped_column(
        Enum(ApplicationType),
        nullable=False
    )

    sequence_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    monitoring_profile_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("monitoring_profiles.id"),
        nullable=False

    )

    # Generated automatically
    system_code: Mapped[String] = mapped_column(String, unique=True, nullable=False)

    # Relationships
    customer: Mapped["Customer"] = relationship(back_populates="systems")

    nodes: Mapped[List["NodeBase"]] = relationship(
        back_populates="system",
        cascade="all, delete-orphan"
    )

    monitoring_profile: Mapped["MonitoringProfile"] = relationship(
    back_populates="systems",
    )

    __table_args__ = (
        Index("idx_system_customer", "customer_id"),
    )