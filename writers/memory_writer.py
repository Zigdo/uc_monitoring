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


def write_memory(node, data):
    """
    Writes memory status metrics to InfluxDB.
    This function must NEVER raise unless configuration is broken.
    """
    point = (
        Point("memory_status")
        # ---- Identity (tags) ----
        .tag("customer", node["customer"])
        .tag("application", node["application"])
        .tag("hostname", node["hostname"])
        .tag("IpAddress", node["ip"])
        .tag("role", node["role"])
        
        # ---- Metrics (fields) ----
        .field("mem_total_kb", int(data.get("mem_total_kb", 0)))
        .field("mem_used_kb", int(data.get("mem_used_kb", 0)))
        .field("mem_free_kb", int(data.get("mem_free_kb", 0)))
        .field("mem_cached_kb", int(data.get("mem_cached_kb", 0)))
        .field("mem_buffers_kb", int(data.get("mem_buffers_kb", 0)))
        .field("mem_usage_percent", float(data.get("mem_usage_percent", 0)))

    )

    write_api.write(bucket=bucket, record=point)
