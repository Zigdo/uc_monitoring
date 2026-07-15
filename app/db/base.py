"""Canonical SQLAlchemy declarative Base for all Leolan ORM models."""

from sqlalchemy.orm import declarative_base

Base = declarative_base()

__all__ = ["Base"]
