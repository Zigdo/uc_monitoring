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


def write_ntp(node, system_synced, data):
    """
    Writes NTP status metrics to InfluxDB.
    This function must NEVER raise unless configuration is broken.
    """

    for peer in data:
        point = (
            Point("ntp_status")
            # ---- Identity (tags) ----
            .tag("customer", node["customer"])
            .tag("application", node["application"])
            .tag("hostname", node["hostname"])
            .tag("IpAddress", node["ip"])
            .tag("role", node["role"])
           
            .tag("server", peer.get("remote", "unknown"))
            .tag("refid", peer.get("refid", "unknown"))
            # ---- Metrics (fields) ----
            .field("synced", bool(peer.get(system_synced, False)))
            .field("type", peer.get("type", "u"))
            .field("offset_ms", float(peer.get("offset_ms", 0)))
            .field("delay_ms", float(peer.get("delay_ms", 0)))
            .field("jitter_ms", float(peer.get("jitter_ms", 0)))
            .field("stratum", int(peer.get("stratum", 0)))
            .field("reach", int(peer.get("reach", 0)))
            .field("when", int(peer.get("when", 0)))
            .field("poll", int(peer.get("poll", 0)))
            .field("sync_state", 1 if peer.get("system_peer") else 0)

        )

    write_api.write(bucket=bucket, record=point)
