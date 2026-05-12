from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID
from sqlalchemy import select


from typing import Annotated

from app.inventory.models.system import System
from app.inventory.schemas.system_schema import SystemCreate, SystemResponse

from app.db.session import get_db


router = APIRouter(prefix="/inventory/api/v1/systems", tags=["Systems"])

# LIST Systems
@router.get("/", response_model=list[SystemResponse])
def get_systems(db: Annotated [Session, Depends(get_db)]):
    systems = db.query(System).all()
    return systems

# Get One System
@router.get("/{id}", name="system")
def get_systems(id: UUID, db: Session = Depends(get_db)):
    return db.query(System).get(id)


# CREATE
@router.post("/", response_model=SystemResponse, status_code=status.HTTP_201_CREATED,)
def create_system(system: SystemCreate, db: Annotated [Session, Depends(get_db)]):

    # #Check if customer already exist
    # result = db.execute(select(System).where(System.id == System.id),)
    # existing_customer = result.scalars().first()

    # if existing_customer:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="System already exists",)
    
    new_system = System(customer_id=system.customer_id, type=system.type)
    db.add(new_system)
    db.commit()
    db.refresh(new_system)
    return new_system



# UPDATE
@router.put("/{system_id}")
def update_system(system_id: UUID, data: dict, db: Annotated [Session, Depends(get_db)]):
    system = db.query(System).get(system_id)

    for key, value in data.items():
        setattr(system, key, value)

    db.commit()
    return system


# DELETE
@router.delete("/{system_id}")
def delete_system(system_id: UUID, db: Annotated [Session, Depends(get_db)]):
    system = db.query(System).get(system_id)
    db.delete(system)
    db.commit()
    return {"status": "deleted"}