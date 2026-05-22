import uuid

from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.db.base import Base


class NodeMonitoringOverride(Base):

    __tablename__ = "node_monitoring_overrides"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    node_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("node_base.id"),
        nullable=False
    )

    implementation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey(
            "monitoring_job_implementations.id"
        ),
        nullable=False
    )

    enabled: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    interval_seconds: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    node = relationship(
        "Node",
        back_populates="monitoring_overrides"
    )

    implementation = relationship(
        "MonitoringJobImplementation"
    )