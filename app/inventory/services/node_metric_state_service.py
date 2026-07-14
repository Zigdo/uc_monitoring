from datetime import datetime, UTC

from sqlalchemy.orm import Session

from app.inventory.models.node_metric_state import (
    NodeMetricState
)


def update_metric_state(
    db: Session,
    node,
    metric_name: str,
    metric_data: dict,
    message: str | None = None,
):
    print("🔥 update_metric_state CALLED", node.id, metric_name)
    state = (
        db.query(NodeMetricState)
        .filter(
            NodeMetricState.node_id == node.id,
            NodeMetricState.metric_name == metric_name,
        )
        .first()
    )

    #
    # First metric creation
    #

    if not state:

        state = NodeMetricState(
            node_id=node.id,
            metric_name=metric_name,
            metric_data=metric_data,
            message=message,
            collected_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
        )

        db.add(state)

    #
    # Existing metric
    #

    else:

        state.metric_data = metric_data

        state.message = message

        state.collected_at = datetime.now(UTC)

        state.updated_at = datetime.now(UTC)

    db.commit()

    db.refresh(state)

    return state