import time

from sqlalchemy.orm import Session

from app.db.session import SessionLocal

from app.core.logging.logger import logger

from app.core.scheduler.worker_pool import executor

from app.core.dispatcher.metric_dispatcher import (
    dispatch_job
)

from app.inventory.services.node_service import (
    get_nodes
)


def run_scheduler():

    logger.info("Scheduler started")
    db: Session = SessionLocal()
    nodes = get_nodes(db)
    for node in nodes:
        print(node.hostname)
"""
    last_run = {}

    while True:

        db: Session = SessionLocal()

        try:

            now = time.time()

            nodes = get_monitored_nodes(db)

            logger.info(
                f"Polling {len(nodes)} nodes"
            )

            for node in nodes:

                host = node.hostname

                if host not in last_run:

                    last_run[host] = {}

                for assignment in node.monitoring_assignments:

                    group = assignment.group_name

                    interval = assignment.interval

                    last_time = last_run[host].get(
                        group,
                        0
                    )

                    if now - last_time >= interval:

                        executor.submit(
                            dispatch_job,
                            node,
                            group
                        )

                        last_run[host][group] = now

        except Exception as e:

            logger.error(
                f"Scheduler loop failed: {e}"
            )

        finally:

            db.close()

        time.sleep(5)

"""