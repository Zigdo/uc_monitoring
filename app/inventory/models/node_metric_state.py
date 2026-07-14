from __future__ import annotations

from datetime import datetime, UTC
from typing import TYPE_CHECKING

import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import text

from sqlalchemy import (
    String,
    Text,
    ForeignKey,
    DateTime,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.base import Base

if TYPE_CHECKING:
    from app.inventory.models.node import NodeBase


class NodeMetricState(Base):

    __tablename__ = "node_metric_state"

    __table_args__ = (
        UniqueConstraint(
            "node_id",
            "metric_name",
            name="uq_node_metric_state"
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
        ForeignKey("node_base.id", ondelete="CASCADE"),
        index=True
    )

    #
    # Metric Information
    #

    metric_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )

    #
    # Raw parsed data
    #
    # Example:
    # {
    #   "synced": true,
    #   "stratum": 3,
    #   "reach": 377
    # }
    #

    metric_data: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False
    )

    #
    # Optional human message
    #

    message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    #
    # Tracking
    #

    collected_at: Mapped[datetime] = mapped_column(
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
        back_populates="metric_states"
    )