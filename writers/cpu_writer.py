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


def write_cpu(node, data):
    """
    Writes cpu status metrics to InfluxDB.
    This function must NEVER raise unless configuration is broken.
    """
    point = (
        Point("cpu_status")
        # ---- Identity (tags) ----
        .tag("customer", node["customer"])
        .tag("application", node["application"])
        .tag("hostname", node["hostname"])
        .tag("IpAddress", node["ip"])
        .tag("role", node["role"])
        
        # ---- Metrics (fields) ----
        .field("load_1m", float(data.get("load_1m", 0)))
        .field("load_5m", float(data.get("load_5m", 0)))
        .field("load_15m", float(data.get("load_15m", 0)))
        .field("cpu_idle", float(data.get("cpu_idle", 0)))
        .field("cpu_system", float(data.get("cpu_system", 0)))
        .field("cpu_user", float(data.get("cpu_user", 0)))
        .field("cpu_iowait", float(data.get("cpu_iowait", 0)))
        .field("cpu_usage", float(data.get("cpu_usage", 0)))

    )

    write_api.write(bucket=bucket, record=point)
