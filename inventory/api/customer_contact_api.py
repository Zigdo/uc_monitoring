from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from inventory.database import SessionLocal
from inventory.models.customer import CustomerContact

router = APIRouter(prefix="/inventory/api/v1/customer_contact", tags=["customer_contacts"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Get API CLusters
@router.get("/", name="customer_contact")
def get_clusters(db: Session = Depends(get_db)):

    customer_contacts = db.query(CustomerContact).all()
    return customer_contacts

# Get One CLuster
@router.get("/{id}", name="customer_contact")
def get_clusters(id: UUID, db: Session = Depends(get_db)):
    return db.query(CustomerContact).get(id)