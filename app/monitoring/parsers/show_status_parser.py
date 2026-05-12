import re

def parse_show_status(output: str) -> dict:
    cpu = {}
    memory = {}
    disk = {}
    system = {}

    # Hostname
    hostname_match = re.search(r"Host Name\s+:\s+(.+)", output)
    if hostname_match:
        system["hostname"] = hostname_match.group(1).strip()

    # Product Version
    version_match = re.search(r"Product Ver\s+:\s+(.+)", output)
    if version_match:
        system["product_version"] = version_match.group(1).strip()

    # Uptime & Load
    uptime_match = re.search(r"up\s+(\d+)\s+days.*load average:\s+([\d.]+),\s+([\d.]+),\s+([\d.]+)", output)
    if uptime_match:
        system["uptime_days"] = int(uptime_match.group(1))
        cpu["load_1m"] = float(uptime_match.group(2))
        cpu["load_5m"] = float(uptime_match.group(3))
        cpu["load_15m"] = float(uptime_match.group(4))

    # CPU
    cpu_match = re.search(
        r"CPU Idle:\s+([\d.]+)%\s+System:\s+([\d.]+)%\s+User:\s+([\d.]+)%.*IOWAIT:\s+([\d.]+)%",
        output,
        re.DOTALL
    )
    if cpu_match:
        idle = float(cpu_match.group(1))
        cpu["cpu_idle"] = idle
        cpu["cpu_system"] = float(cpu_match.group(2))
        cpu["cpu_user"] = float(cpu_match.group(3))
        cpu["cpu_iowait"] = float(cpu_match.group(4))
        cpu["cpu_usage"] = 100 - idle

    # Memory
    mem_total = re.search(r"Memory Total:\s+(\d+)K", output)
    mem_free = re.search(r"Free:\s+(\d+)K", output)
    mem_used = re.search(r"Used:\s+(\d+)K", output)
    mem_cached = re.search(r"Cached:\s+(\d+)K", output)
    mem_buffers = re.search(r"Buffers:\s+(\d+)K", output)

    if mem_total:
        total = int(mem_total.group(1))
        used = int(mem_used.group(1))
        memory["mem_total_kb"] = total
        memory["mem_used_kb"] = used
        memory["mem_free_kb"] = int(mem_free.group(1))
        memory["mem_cached_kb"] = int(mem_cached.group(1))
        memory["mem_buffers_kb"] = int(mem_buffers.group(1))
        memory["mem_usage_percent"] = round((used / total) * 100, 2)

    # Disk Active
    disk_active = re.search(r"Disk/active.*\((\d+)%\)", output)
    if disk_active:
        disk["disk_active_percent"] = int(disk_active.group(1))

    # Disk Logging
    disk_logging = re.search(r"Disk/logging.*\((\d+)%\)", output)
    if disk_logging:
        disk["disk_logging_percent"] = int(disk_logging.group(1))

    return cpu, memory, disk, system