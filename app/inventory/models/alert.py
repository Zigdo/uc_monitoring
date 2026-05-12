from __future__ import annotations


from datetime import datetime
import uuid
from typing import Optional, List

from sqlalchemy import String, Enum, ForeignKey, DateTime, Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

# from database import Base
from app.db.base import Base

from .enums import SeverityType, StatusType

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from app.inventory.models.service import Service
    from app.inventory.models.alert import Alert
    from app.inventory.models.node import NodeBase


class Alert(Base):
    __tablename__ = "alerts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False
    )

    node_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("node_base.id"), nullable=False
    )

    service_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("services.id"), nullable=True
    )

    severity: Mapped[SeverityType] = mapped_column(Enum(SeverityType), nullable=False)
    status: Mapped[StatusType] = mapped_column(Enum(StatusType), nullable=False)

    message: Mapped[Optional[str]] = mapped_column(String)

    triggered_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    resolved_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    # Relationships
    node: Mapped["NodeBase"] = relationship(back_populates="alerts")
    service: Mapped[Optional["Service"]] = relationship()

    __table_args__ = (
        Index("idx_alert_node", "node_id"),
        Index("idx_alert_status", "status"),
        Index("idx_alert_customer", "customer_id"),
    )


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("customers.id"), nullable=False
    )

    title: Mapped[str] = mapped_column(String, nullable=False)

    severity: Mapped[SeverityType] = mapped_column(Enum(SeverityType), nullable=False)
    status: Mapped[StatusType] = mapped_column(Enum(StatusType), nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    closed_at: Mapped[Optional[datetime]] = mapped_column(DateTime)

    # Relationships
    alerts: Mapped[List["IncidentAlert"]] = relationship(back_populates="incident")


class IncidentAlert(Base):
    __tablename__ = "incident_alert"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    incident_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("incidents.id"), nullable=False
    )

    alert_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("alerts.id"), nullable=False
    )

    # Relationships
    incident: Mapped["Incident"] = relationship(back_populates="alerts")
    alert: Mapped["Alert"] = relationship()

    __table_args__ = (
        UniqueConstraint("incident_id", "alert_id"),
    )