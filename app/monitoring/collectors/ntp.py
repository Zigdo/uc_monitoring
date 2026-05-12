
from core.ssh_client import run_ssh_command
from parsers.ntp_parser import parse_utils_ntp_status
from writers.ntp_influx import write_ntp

def collect(node):

    raw = run_ssh_command(
        node["ip"],
        node["username"],
        node["password"],
        "utils ntp status",
    )
    
    parsed = parse_utils_ntp_status(raw)

    write_ntp(
        node,
        parsed["system_synced"],
        parsed["peers"]
    )