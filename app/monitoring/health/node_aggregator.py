from sqlalchemy.orm import Session

from app.inventory.models.node_health_component import NodeHealthComponent
from app.inventory.models.node_health import NodeHealth

from datetime import datetime, UTC


class NodeHealthAggregator:

    def evaluate_node(self, db: Session, node):

        components = (
            db.query(NodeHealthComponent)
            .filter(NodeHealthComponent.node_id == node.id)
            .all()
        )

        if not components:

            return None

        #
        # Weighted scoring
        #
        total_score = 0
        worst_status = "HEALTHY"
        messages = []

        for c in components:

            total_score += c.score

            messages.append(f"{c.component_name}: {c.status}")

            if c.status == "CRITICAL":
                worst_status = "CRITICAL"

            elif c.status == "WARNING" and worst_status != "CRITICAL":
                worst_status = "WARNING"

        #
        # Average score
        #
        avg_score = int(total_score / len(components))

        #
        # Summary message
        #
        message = " | ".join(messages)

        #
        # Upsert Node Health
        #
        node_health = (
            db.query(NodeHealth)
            .filter(NodeHealth.node_id == node.id)
            .first()
        )

        if not node_health:

            node_health = NodeHealth(
                node_id=node.id,
                score=avg_score,
                status=worst_status,
                message=message,
                evaluated_at=datetime.now(UTC),
                updated_at=datetime.now(UTC)
            )

            db.add(node_health)

        else:

            node_health.score = avg_score
            node_health.status = worst_status
            node_health.message = message
            node_health.evaluated_at = datetime.now(UTC)
            node_health.updated_at = datetime.now(UTC)

        db.commit()
        db.refresh(node_health)

        return node_health