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
bucket = os.getenv("INFLUX_BUCKET")


def write_system(node, data):
    """
    Writes disk status metrics to InfluxDB.
    This function must NEVER raise unless configuration is broken.
    """
    point = (
        Point("system_status")
        # ---- Identity (tags) ----
        .tag("customer", node["customer"])
        .tag("application", node["application"])
        .tag("hostname", node["hostname"])
        .tag("IpAddress", node["ip"])
        .tag("role", node["role"])
        
        # ---- Metrics (fields) ----
        .field("hostname", data["hostname"])
        .field("product_version", data["product_version"])
        .field("uptime_days", int(data.get("uptime_days", 0)))
    )

    write_api.write(bucket=bucket, record=point)
