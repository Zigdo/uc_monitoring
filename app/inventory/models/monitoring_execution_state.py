from datetime import datetime, UTC
from uuid import UUID as UUIDType, uuid4

from sqlalchemy import (
    String,
    Integer,
    DateTime,
    ForeignKey,
    Enum,
    Text,
    UniqueConstraint,
    BigInteger
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from sqlalchemy.dialects.postgresql import UUID

from app.db.base import Base

from app.inventory.models.enums import (
    ExecutionStatus,
    ExecutionStage
)


class MonitoringExecutionState(Base):

    __tablename__ = "monitoring_execution_state"

    #
    # Prevent duplicate state rows
    #
    __table_args__ = (
        UniqueConstraint(
            "node_id",
            "implementation_id",
            name="uq_node_implementation_state"
        ),
    )

    #
    # Primary Key
    #
    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid4())
    )

    #
    # Relationships
    #
    node_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("node_base.id"),
        nullable=False,
        index=True
    )

    system_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("systems.id"),
        nullable=False,
        index=True
    )

    customer_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customers.id"),
        nullable=False,
        index=True
    )

    implementation_id: Mapped[UUIDType] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("monitoring_job_implementations.id"),
        nullable=False,
        index=True
    )

    #
    # Current Operational State
    #
    current_status: Mapped[ExecutionStatus] = mapped_column(
        Enum(ExecutionStatus),
        default=ExecutionStatus.UNKNOWN,
        nullable=False
    )

    current_stage: Mapped[ExecutionStage] = mapped_column(
        Enum(ExecutionStage),
        default=ExecutionStage.COMPLETE,
        nullable=False
    )

    current_message: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    #
    # Last Execution
    #
    last_started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    last_finished_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    last_duration_ms: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )

    #
    # Last Success
    #
    last_success_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    #
    # Last Failure
    #
    last_failure_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )

    last_error_type: Mapped[str] = mapped_column(
        String(255),
        nullable=True
    )

    last_error_message: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    #
    # Counters
    #
    consecutive_failures: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    total_successes: Mapped[int] = mapped_column(
        BigInteger,
        default=0
    )

    total_failures: Mapped[int] = mapped_column(
        BigInteger,
        default=0
    )

    total_executions: Mapped[int] = mapped_column(
        BigInteger,
        default=0
    )

    #
    # Version Tracking
    #
    collector_version: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )

    parser_version: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )

    #
    # Audit
    #
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(UTC)
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.now(UTC),
        onupdate=datetime.now(UTC)
    )

    #
    # ORM Relationships
    #
    node = relationship("NodeBase")

    system = relationship("System")

    customer = relationship("Customer")

    implementation = relationship(
        "MonitoringJobImplementation"
    )
