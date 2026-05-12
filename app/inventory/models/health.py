from __future__ import annotations

import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import Integer, DateTime, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
# from database import Base


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.inventory.models.customer import Customer
    from app.inventory.models.node import NodeBase

class HealthScore(Base):
    __tablename__ = "health_score"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customers.id"),
        nullable=False
    )

    node_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("node_base.id"),
        nullable=False
    )

    score: Mapped[int] = mapped_column(Integer, nullable=False)

    calculated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Relationships (optional but recommended)
    customer: Mapped["Customer"] = relationship()
    node: Mapped["NodeBase"] = relationship()

    __table_args__ = (
        Index("idx_health_node", "node_id"),
    )