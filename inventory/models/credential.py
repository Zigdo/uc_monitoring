from __future__ import annotations


import uuid
from typing import List

from sqlalchemy import String, Enum, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

from inventory.database import Base
# from database import Base

from .enums import CredentialType

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.node import NodeBase


class Credential(Base):
    __tablename__ = "credentials"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    username: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[CredentialType] = mapped_column(
        Enum(CredentialType), nullable=False
    )

    # Relationships
    nodes: Mapped[List["NodeCredentialMapping"]] = relationship(
        back_populates="credential",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        Index("idx_credential_type", "type"),
    )


class NodeCredentialMapping(Base):
    __tablename__ = "node_credentials_mapping"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    node_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("node_base.id"), nullable=False
    )

    credential_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("credentials.id"), nullable=False
    )

    # Relationships
    node: Mapped["NodeBase"] = relationship(back_populates="credentials")
    credential: Mapped["Credential"] = relationship(back_populates="nodes")