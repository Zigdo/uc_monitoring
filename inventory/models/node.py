from __future__ import annotations

import uuid
from typing import List, Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, INET
from sqlalchemy.orm import Mapped, mapped_column, relationship

from inventory.database import Base
# from database import Base


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.service import Service
    from models.alert import Alert
    from models.credential import NodeCredentialMapping
    from models.system import System
    from models.customer import Customer




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