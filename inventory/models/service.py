from __future__ import annotations

import uuid
from typing import Optional, List

from sqlalchemy import String, Enum, ForeignKey, Boolean, Integer, UniqueConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from inventory.database import Base
# from database import Base

from .enums import ServiceType

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.alert import Alert
    from models.node import NodeBase


class Service(Base):
    __tablename__ = "services"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    node_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("node_base.id"),
        nullable=False
    )

    service_name: Mapped[str] = mapped_column(String, nullable=False)

    type: Mapped[ServiceType] = mapped_column(
        Enum(ServiceType),
        nullable=False
    )

    is_enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    check_interval: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    # Relationships
    node: Mapped["NodeBase"] = relationship(back_populates="services")

    alerts: Mapped[List["Alert"]] = relationship(
        back_populates="service",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("node_id", "service_name"),
        Index("idx_service_node", "node_id"),
    )