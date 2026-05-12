from collectors import ntp, show_status

METRIC_DISPATCH = {
    "ntp": ntp.collect,
    "show_status": show_status.collect,
    # "cpu_memory": system.collect,
    # "disk": disk.collect,
    # "replication": replication.collect,
}