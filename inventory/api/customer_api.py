from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from uuid import UUID

from typing import Annotated

from inventory.schemas.customer_schema import CustomerCreate, CustomerResponse
from inventory.models.customer import Customer

from app.db.session import get_db

router = APIRouter(prefix="/inventory/api/v1/customers", tags=["Customers"])

# LIST CUSTOMERS
@router.get("/", response_model=list[CustomerResponse])
def get_customers(db: Annotated [Session, Depends(get_db)]):
    customers = db.query(Customer).order_by(Customer.code_name).all()
    return customers

# List one Customer
@router.get("/{id}", response_model=CustomerResponse)
def get_customer(id: UUID, db: Annotated [Session, Depends(get_db)]):
    customer = db.query(Customer).get(id)
    if not customer:
        raise HTTPException(status_code=404, detail="Node not found")
    return customer


# CREATE
@router.post("/", response_model=CustomerResponse, status_code=status.HTTP_201_CREATED,)
def create_customer(customer: CustomerCreate, db: Annotated [Session, Depends(get_db)]):

    #Check if customer already exist
    result = db.execute(select(Customer).where(Customer.code_name == customer.code_name),)
    existing_customer = result.scalars().first()

    if existing_customer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Customer already exists",)
    
    result = db.execute(select(Customer).where(Customer.display_name == customer.display_name),)
    existing_customer = result.scalars().first()

    if existing_customer:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Customer already exists",)
    
    new_customer = Customer(code_name=customer.code_name, display_name=customer.display_name, type=customer.type)
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    return new_customer



# UPDATE
@router.put("/{customer_id}")
def update_customer(customer_id: UUID, data: dict, db: Annotated [Session, Depends(get_db)]):
    customer = db.query(Customer).get(customer_id)

    for key, value in data.items():
        setattr(customer, key, value)

    db.commit()
    return customer


# DELETE
@router.delete("/{customer_id}")
def delete_customer(customer_id: UUID, db: Annotated [Session, Depends(get_db)]):
    customer = db.query(Customer).get(customer_id)
    db.delete(customer)
    db.commit()
    return {"status": "deleted"}