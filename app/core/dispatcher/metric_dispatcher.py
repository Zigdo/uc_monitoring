from app.core.logging.logger import logger
from app.db.session import SessionLocal
from app.inventory.services.execution_state_service import start_execution, execution_success, execution_failed
from app.monitoring.writers.telemetry.execution_writer import write_execution_metric
import time

from app.core.scheduler.job_registry import (
    JOB_REGISTRY
)

def dispatch_job(
    node,
    implementation
):

    with SessionLocal() as db:


        try:

            job = JOB_REGISTRY.get(implementation.implementation_key)

            if not job:
                logger.warning(
                    f"No job registered for group '{implementation.implementation_key}'"
                )
                return
            
            state = start_execution(db, node, implementation)

            
            state.collector_version = job.collector_version
            state.parser_version = job.parser_version

            start_time = time.time()
            try:

                logger.info(
                    f"Running {implementation.implementation_key} on {node.hostname}"
                )

                job.run(db, node)

                duration = int((time.time() - start_time) * 1000)

                execution_success(db, state, duration)

                write_execution_metric(
                node=node,
                implementation=implementation,
                duration_ms=duration,
                success=True
)

            except Exception as e:

                execution_failed(db, state, e)

                logger.error(
                    f"Node {node.hostname} "
                    f"group {implementation.implementation_key} failed: {e}"
                )

                raise
        
        except Exception as e:

            execution_failed(db, state, e)

            logger.error(
                f"Node {node.hostname} "
                f"group {implementation} failed: {e}"
            )

            raise
