from __future__ import annotations

import uuid
from typing import List

from sqlalchemy import String, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from app.db.base import Base
# from database import Base

from .mixins import TimestampMixin
from .enums import CustomerType

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.inventory.models.customer import Customer
    from app.inventory.models.system import System
    from app.inventory.models.node import NodeBase

class Customer(Base,TimestampMixin):
    __tablename__ = "customers"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    code_name: Mapped[str] = mapped_column(
        String, unique=True, nullable=False
    )

    display_name: Mapped[str | None] = mapped_column(String)

    type: Mapped[CustomerType | None] = mapped_column(
        Enum(CustomerType)
    )

    # Relationships
    systems: Mapped[List["System"]] = relationship(
        back_populates="customer",
        cascade="all, delete-orphan"
    )

    contacts: Mapped[List["CustomerContact"]] = relationship(
        back_populates="customer",
        cascade="all, delete-orphan"
    )

    nodes: Mapped[List["NodeBase"]] = relationship(
        back_populates="customer",
        cascade="all, delete-orphan"
    )


class CustomerContact(Base):
    __tablename__ = "customers_contacts"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    customer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("customers.id"),
        nullable=False
    )

    email: Mapped[str] = mapped_column(String, nullable=False)
    first_name: Mapped[str | None] = mapped_column(String)
    last_name: Mapped[str | None] = mapped_column(String)

    # Relationship
    customer: Mapped["Customer"] = relationship(
        back_populates="contacts"
    )

    __table_args__ = (
        UniqueConstraint("email", "customer_id"),
    )