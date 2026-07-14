from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import text

from sqlalchemy import (
    String,
    Text,
    Integer,
    DateTime,
    ForeignKey,
    UniqueConstraint,
    Enum,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.base import Base

from app.inventory.models.enums import (
    HealthStatus
)

if TYPE_CHECKING:
    from app.inventory.models.node import NodeBase

class NodeHealthComponent(Base):

    __tablename__ = "node_health_component"

    __table_args__ = (
        UniqueConstraint(
            "node_id",
            "component_name",
            name="uq_node_health_component"
        ),
    )

    #
    # Identity
    #

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,   # ✅ IMPORTANT
    )

    node_id: Mapped[UUID] = mapped_column(
        ForeignKey(
            "node_base.id",
            ondelete="CASCADE"
        ),
        index=True
    )

    #
    # Component
    #

    component_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )

    #
    # Health
    #

    status: Mapped[HealthStatus] = mapped_column(
        Enum(HealthStatus),
        nullable=False
    )

    score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=100
    )

    #
    # Human explanation
    #

    message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    #
    # Tracking
    #

    evaluated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    #
    # Relationships
    #

    node: Mapped["NodeBase"] = relationship(
        back_populates="health_components"
    )