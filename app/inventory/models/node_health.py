from __future__ import annotations

from datetime import datetime
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import text

from sqlalchemy import (
    Integer,
    String,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.db.base import Base


class NodeHealth(Base):

    __tablename__ = "node_health"

    __table_args__ = (
        UniqueConstraint("node_id", name="uq_node_health_node"),
    )


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
    # Overall score (0–100)
    #
    score: Mapped[int] = mapped_column(
        Integer,
        default=100,
        nullable=False
    )

    #
    # Status
    #
    status: Mapped[str] = mapped_column(
        String(20),
        default="HEALTHY"
    )

    #
    # Summary message
    #
    message: Mapped[str | None] = mapped_column(
        String(255),
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