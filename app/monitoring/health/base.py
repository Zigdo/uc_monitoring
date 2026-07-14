from abc import ABC, abstractmethod


class BaseHealthEvaluator(ABC):

    metric_name: str

    @abstractmethod
    def evaluate(self, node, data: dict) -> dict:
        """
        Must return:
        {
            "status": "HEALTHY|WARNING|CRITICAL|UNKNOWN",
            "score": int,
            "message": str
        }
        """
        pass