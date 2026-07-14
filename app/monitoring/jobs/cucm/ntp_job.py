from app.monitoring.health.engine import HealthEngine
from app.inventory.services.node_health_component_service import (
    update_health_component
)
from app.monitoring.collectors.ssh.ntp_collector import (
    collect
)

from app.monitoring.parsers.cucm.ntp_parser import (
    parse_utils_ntp_status
)

from app.inventory.services.node_metric_state_service import update_metric_state

from app.monitoring.writers.cucm.ntp_writer import (
    write_ntp
)

from app.monitoring.health.node_aggregator import NodeHealthAggregator


class CUCMNTPJob:

    collector_version = "1.0.0"

    parser_version = "1.0.0"

    def run(self, db, node):

        raw = collect(node)

        parsed = parse_utils_ntp_status(raw)
        # print (parsed)

        #
        # 1. Store raw metric state
        #

        update_metric_state(
        db=db,
        node=node,
        metric_name="ntp",
        metric_data=parsed,
        )

        #
        # 2. Evaluate health
        #
        engine = HealthEngine()

        result = engine.evaluate(
            metric_name="ntp",
            node=node,
            data=parsed
        )

        #
        # 3. Store health result
        #
        update_health_component(
            db=db,
            node=node,
            component_name="ntp",
            status=result["status"],
            score=result["score"],
            message=result["message"]
        )


        aggregator = NodeHealthAggregator()

        aggregator.evaluate_node(db, node)
        
        #
        # 4. Write to InfluxDB (history)
        #
        write_ntp(node, parsed)