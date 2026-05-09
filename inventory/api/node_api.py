from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from uuid import UUID
from sqlalchemy import select

from typing import Annotated

from inventory.models.node import NodeBase, CUCM
from inventory.schemas.node_schema import NodeCreate, NodeResponse, CUCMNodeCreate, CUCMNodeUpdate

from inventory.database import get_db


router = APIRouter(prefix="/inventory/api/v1/nodes", tags=["Nodes"])

#Create CUCM Node

@router.post("/cucm")
def create_cucm_node(
    node_data: CUCMNodeCreate,
    db: Annotated [Session, Depends(get_db)]
):

    # -----------------------------------------
    # Create generic node
    # -----------------------------------------

    new_node = NodeBase(
        customer_id=node_data.customer_id,
        system_id=node_data.system_id,
        hostname=node_data.hostname,
        ip_address=node_data.ip_address,
        vendor=node_data.vendor,
        node_type="cucm"
    )

    db.add(new_node)

    db.flush()

    # -----------------------------------------
    # Create CUCM extension
    # -----------------------------------------

    cucm_extension = CUCM(
        node_id=new_node.id,
        role=node_data.role,
        version=node_data.version,
    )

    db.add(cucm_extension)

    db.commit()

    db.refresh(new_node)

    return {
        "node_id": str(new_node.id),
        "hostname": new_node.hostname,
        "cluster_role": cucm_extension.role
    }


#Get all Nodes

@router.get("/", response_model=list[NodeResponse])
def get_nodes(
    db: Session = Depends(get_db)
):

    nodes = db.query(NodeBase).all()

    return nodes

#Get one Node

@router.get("/{node_id}", response_model=NodeResponse)
def get_node(
    node_id: UUID,
    db: Session = Depends(get_db)
):

    node = db.query(NodeBase).filter(
        NodeBase.id == node_id
    ).first()

    if not node:
        raise HTTPException(
            status_code=404,
            detail="Node not found"
        )

    return node


#Get all cucm nodes
@router.get("/cucm/all")
def get_cucm_nodes(
    db: Session = Depends(get_db)
):

    cucm_nodes = (
        db.query(CUCM)
        .options(
            joinedload(CUCM.node)
            .joinedload(NodeBase.customer),

            joinedload(CUCM.node)
            .joinedload(NodeBase.system)
        )
        .all()
    )

    result = []

    for cucm in cucm_nodes:

        result.append({
            "cucm_details": cucm
        })

    return result


#Get one CUCM Node

@router.get("/cucm/{node_id}")
def get_cucm_node(
    node_id: UUID,
    db: Session = Depends(get_db)
):

    cucm = (
        db.query(CUCM)
        .options(
            joinedload(CUCM.node)
            .joinedload(NodeBase.customer),

            joinedload(CUCM.node)
            .joinedload(NodeBase.system)
        )
        .filter(CUCM.node_id == node_id)
        .first()
    )

    if not cucm:
        raise HTTPException(
            status_code=404,
            detail="CUCM node not found"
        )

    return {
        "cucm_details": cucm
    }



@router.put("/cucm/{node_id}")
def update_cucm_node(
    node_id: UUID,
    data: CUCMNodeUpdate,
    db: Session = Depends(get_db)
):

    cucm = db.query(CUCM).filter(
        CUCM.node_id == node_id
    ).first()

    if not cucm:
        raise HTTPException(404)

    node = cucm.node

    if data.hostname:
        node.hostname = data.hostname

    if data.ip_address:
        node.ip_address = data.ip_address

    db.commit()

    return {"message": "updated"}


@router.delete("/cucm/{node_id}")
def delete_cucm_node(
    node_id: UUID,
    db: Session = Depends(get_db)
):

    cucm = db.query(CUCM).filter(
        CUCM.node_id == node_id
    ).first()

    if not cucm:
        raise HTTPException(404)

    node = cucm.node

    db.delete(cucm)

    db.delete(node)

    db.commit()

    return {"message": "deleted"}


"""

# UPDATE
@router.put("/{system_id}")
def update_system(system_id: UUID, data: dict, db: Annotated [Session, Depends(get_db)]):
    system = db.query(NodeBase).get(system_id)

    for key, value in data.items():
        setattr(system, key, value)

    db.commit()
    return system


# DELETE
@router.delete("/{system_id}")
def delete_system(system_id: UUID, db: Annotated [Session, Depends(get_db)]):
    system = db.query(NodeBase).get(system_id)
    db.delete(system)
    db.commit()
    return {"status": "deleted"}

    """