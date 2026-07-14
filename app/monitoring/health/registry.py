from app.monitoring.health.evaluators.ntp_evaluator import NTPHealthEvaluator


HEALTH_REGISTRY = {
    "ntp": NTPHealthEvaluator(),
}