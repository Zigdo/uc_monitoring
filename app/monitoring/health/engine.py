from app.monitoring.health.registry import HEALTH_REGISTRY


class HealthEngine:

    def evaluate(self, metric_name: str, node, data: dict):

        evaluator = HEALTH_REGISTRY.get(metric_name)

        if not evaluator:

            return {
                "status": "UNKNOWN",
                "score": -1,
                "message": f"No evaluator for {metric_name}"
            }

        return evaluator.evaluate(node, data)