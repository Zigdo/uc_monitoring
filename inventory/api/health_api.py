from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID

from typing import Annotated

from inventory.schemas.customer_schema import CustomerCreate, CustomerResponse
from inventory.models.customer import Customer

from inventory.database import get_db

router = APIRouter(prefix="/inventory/api/v1/health", tags=["health"])


# Test Health
@router.get("/")
def test_health():
    # customers = db.query(Customer).order_by(Customer.code_name).all()
    return "ok"