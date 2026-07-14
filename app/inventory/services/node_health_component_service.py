from datetime import datetime, UTC

from sqlalchemy.orm import Session

from app.inventory.models.node_health_component import (
    NodeHealthComponent
)

from app.inventory.models.enums import (
    HealthStatus
)


def update_health_component(
    db: Session,
    node,
    component_name: str,
    status: HealthStatus,
    score: int,
    message: str | None = None,
):

    component = (
        db.query(NodeHealthComponent)
        .filter(
            NodeHealthComponent.node_id == node.id,
            NodeHealthComponent.component_name == component_name
        )
        .first()
    )

    if not component:

        component = NodeHealthComponent(
            node_id=node.id,
            component_name=component_name,
            status=status,
            score=score,
            message=message,
            evaluated_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )

        db.add(component)

    else:

        component.status = status

        component.score = score

        component.message = message

        component.evaluated_at = datetime.now(UTC)

        component.updated_at = datetime.now(UTC)

    db.commit()

    db.refresh(component)

    return component