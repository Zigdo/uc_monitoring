from __future__ import annotations

import uuid
from typing import List, Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, INET
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
# from database import Base


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.inventory.models.service import Service
    from app.inventory.models.alert import Alert
    from app.inventory.models.credential import NodeCredentialMapping
    from app.inventory.models.system import System
    from app.inventory.models.customer import Customer
    from app.inventory.models.monitoring.monitoring_profile import MonitoringProfile
    from app.inventory.models.monitoring.node_monitoring_override import NodeMonitoringOverride




class NodeBase(Base):
    __tablename__ = "node_base"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customers.id"),
        nullable=False
    )

    system_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("systems.id"),
        nullable=False
    )

    monitoring_profile_id: Mapped[uuid.UUID | None] = mapped_column(
    UUID(as_uuid=True),
    ForeignKey("monitoring_profiles.id"),
    nullable=True
    )

    ip_address: Mapped[Optional[str]] = mapped_column(INET)
    hostname: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    vendor: Mapped[str] = mapped_column(String, nullable=False)
    node_type: Mapped[str] = mapped_column(String, nullable=False)


    # Relationships

    customer: Mapped["Customer"] = relationship(back_populates="nodes")
    system: Mapped["System"] = relationship(back_populates="nodes")

    services: Mapped[List["Service"]] = relationship(
        back_populates="node",
        cascade="all, delete-orphan"
    )

    alerts: Mapped[List["Alert"]] = relationship(
        back_populates="node",
        cascade="all, delete-orphan"
    )

    credentials: Mapped[List["NodeCredentialMapping"]] = relationship(
        back_populates="node",
        cascade="all, delete-orphan"
    )

    cucm: Mapped[Optional["CUCM"]] = relationship(
        back_populates="node",
        uselist=False
    )

    monitoring_profile: Mapped["MonitoringProfile"] = relationship(
    back_populates="nodes",
    cascade="all, delete-orphan"

    )

    monitoring_overrides: Mapped["NodeMonitoringOverride"] = relationship(
    back_populates="node",
    cascade="all, delete-orphan"
    )


class CUCM(Base):
    __tablename__ = "cucm"

    node_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("node_base.id"),
        primary_key=True
    )

    role: Mapped[Optional[str]] = mapped_column(String)
    version: Mapped[Optional[str]] = mapped_column(String)

    # Relationship
    node: Mapped["NodeBase"] = relationship(
        back_populates="cucm"
    )