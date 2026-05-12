from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import UUID

from inventory.models.service import Service

router = APIRouter(prefix="/inventory/api/v1/services", tags=["services"])