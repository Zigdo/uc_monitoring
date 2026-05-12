"""
from app.monitoring.collectors import ntp
from app.monitoring.collectors import show_status

METRIC_DISPATCH = {
    "ntp": ntp.collect,
    "show_status": show_status.collect,
    # "cpu_memory": system.collect,
    # "disk": disk.collect,
    # "replication": replication.collect,
}

"""
from app.core.logging.logger import logger

from app.core.scheduler.job_registry import (
    JOB_REGISTRY
)


def dispatch_job(
    node,
    group
):

    try:

        job = JOB_REGISTRY.get(group)

        if not job:

            logger.warning(
                f"No job registered for group '{group}'"
            )

            return

        logger.info(
            f"Running {group} on {node.hostname}"
        )

        job.run(node)

    except Exception as e:

        logger.error(
            f"Node {node.hostname} "
            f"group {group} failed: {e}"
        )