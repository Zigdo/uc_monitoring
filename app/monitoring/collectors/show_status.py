from core.ssh_client import run_ssh_command
from parsers.show_status_parser import parse_show_status
from writers.cpu_writer import write_cpu
from writers.memory_writer import write_memory
from writers.disk_writer import write_disk
from writers.system_writer import write_system


def collect(node):

    raw = run_ssh_command(
        node["ip"],
        node["username"],
        node["password"],
        "show status"
    )

    cpu, memory, disk, system = parse_show_status(raw)

    # Write cpu metrics
    write_cpu(node, cpu)

    # # Write memory metrics
    write_memory(node, memory)

    # # # Write disk metrics
    write_disk(node, disk)

    # # Write system information
    write_system(node, system)