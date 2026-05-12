from sqlalchemy.orm import Session
from app.inventory.models.node import Node


def get_monitored_nodes(db: Session):

    return (
        db.query(Node)
        .filter(Node.monitoring_enabled == True)
        .all()
    )