from sqlalchemy.orm import Session
from app.inventory.models.node import NodeBase
from app.db.session import get_db
from fastapi import Depends



def get_monitored_nodes(db: Session):

    return (
        db.query(NodeBase)
        # .filter(NodeBase.monitoring_enabled == True)
        .all()
    )

def get_nodes(
    db: Session = Depends(get_db)
):

    nodes = db.query(NodeBase).all()

    return nodes