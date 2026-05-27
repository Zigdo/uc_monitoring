import time
import signal
import sys

from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from app.db.session import SessionLocal

from app.core.logging.logger import logger

from app.core.scheduler.worker_pool import executor

from app.core.dispatcher.metric_dispatcher import dispatch_job

from app.inventory.models.node import NodeBase
from app.inventory.models.system import System
from app.inventory.models.monitoring.monitoring_profile import MonitoringProfile
from app.inventory.models.monitoring.monitoring_profile_job import MonitoringProfileJob
from app.inventory.models.monitoring.node_monitoring_override import (
    NodeMonitoringOverride
)

def run_scheduler():

    logger.info("Scheduler started")

    # Track last execution time
    # Structure:
    #
    # {
    #   "node-hostname": {
    #       "implementation_key": timestamp
    #   }
    # }
    #
    last_run = {}

    while True:
    # while not stop_event.is_set():
        
        db: Session = SessionLocal()

        try:

            now = time.time()

            # Eager load relationships
            nodes = (
                db.query(NodeBase)
                .options(

                    #
                    # Direct node relationships
                    #
                    joinedload(NodeBase.customer),

                    joinedload(NodeBase.system),

                    joinedload(NodeBase.monitoring_overrides)
                    .joinedload(
                        NodeMonitoringOverride.implementation
                    ),

                    #
                    # System -> Monitoring Profile
                    #
                    joinedload(NodeBase.system)
                    .joinedload(System.monitoring_profile)

                    .joinedload(MonitoringProfile.jobs)

                    .joinedload(
                        MonitoringProfileJob.implementation
                    )

                )
                .all()
            )

            logger.info(
                f"Polling {len(nodes)} nodes"
            )

            for node in nodes:

                host = node.hostname

                if host not in last_run:

                    last_run[host] = {}

                # Skip nodes without system
                if not node.system:
                    continue

                # Skip systems without monitoring profile
                if not node.system.monitoring_profile:
                    continue

                profile = node.system.monitoring_profile

                # Convert overrides to dictionary
                # Key:
                # implementation_id
                overrides = {}

                for override in node.monitoring_overrides or []:
                    overrides[override.implementation_id] = override

                # Iterate profile jobs
                for profile_job in profile.jobs:

                    implementation = (
                        profile_job.implementation
                    )

                    override = overrides.get(
                        implementation.id
                    )

                    # Disabled by override
                    if (
                        override
                        and override.enabled is False
                    ):
                        continue

                    # Use override interval if exists
                    interval = (
                        override.interval_seconds
                        if (
                            override
                            and override.interval_seconds
                        )
                        else profile_job.interval_seconds
                    )

                    implementation_key = (
                        implementation.implementation_key
                    )

                    last_time = last_run[host].get(
                        implementation_key,
                        0
                    )

                    # Check interval
                    if now - last_time >= interval:

                        logger.info(
                            f"Scheduling "
                            f"{host} -> "
                            f"{implementation_key}"
                        )

                        executor.submit(
                            dispatch_job,
                            node,
                            implementation_key
                        )

                        # Update last run
                        last_run[host][
                            implementation_key
                        ] = now
        
        except KeyboardInterrupt:

            logger.info(
                "Scheduler stopped by user"
            )

            break

        except Exception as e:

            logger.error(
                f"Scheduler loop failed: {e}"
            )

        finally:

            db.close()

        time.sleep(5)