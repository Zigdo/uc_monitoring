from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Enum, ForeignKey, DateTime, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
# from database import Base

from .enums import EntityType, MaintenanceStatus

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.inventory.models.customer import Customer
    from app.inventory.models.user import User



class MaintenanceEvent(Base):
    __tablename__ = "maintenance_event"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customers.id"),
        nullable=False
    )

    entity_type: Mapped[EntityType] = mapped_column(
        Enum(EntityType),
        nullable=False
    )

    entity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        nullable=False
    )

    start_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    end_time: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False
    )

    reason: Mapped[Optional[str]] = mapped_column(String)

    status: Mapped[MaintenanceStatus] = mapped_column(
        Enum(MaintenanceStatus),
        nullable=False
    )

    created_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Relationships (optional but recommended)
    customer: Mapped["Customer"] = relationship()
    user: Mapped["User"] = relationship()

    __table_args__ = (
        Index("idx_entity", "entity_type", "entity_id"),
        Index("idx_customer", "customer_id"),
        Index("idx_time", "start_time", "end_time"),
        Index("idx_active_lookup", "entity_id", "start_time", "end_time"),
    )