from influxdb_client import InfluxDBClient, Point

from influxdb_client.client.write_api import SYNCHRONOUS
import os
from dotenv import load_dotenv
load_dotenv()

client = InfluxDBClient(
    url=os.getenv("INFLUX_URL"),
    token=os.getenv("INFLUX_TOKEN"),
    org=os.getenv("INFLUX_ORG")
)

write_api = client.write_api(write_options=SYNCHRONOUS)
bucket = os.getenv("INFLUX_platform_BUCKET")


# from app.monitoring.influx.client import write_api


def write_execution_metric(
    node,
    implementation,
    duration_ms,
    success
):

    point = (
        Point("monitoring_execution")
        .tag(
            "customer",
            node.customer.display_name
        )
        .tag(
            "system",
            node.system.type.value
        )
        .tag(
            "node",
            node.hostname
        )
        .tag(
            "job",
            implementation.implementation_key
        )
        .field(
            "duration_ms",
            duration_ms
        )
        .field(
            "success",
            int(success)
        )
    )

    write_api.write(
        bucket=bucket,
        record=point
    )