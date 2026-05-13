from app.monitoring.collectors.ssh.ntp_collector import (
    collect
)

from app.monitoring.parsers.ntp_parser import (
    parse_utils_ntp_status
)

from app.monitoring.writers.ntp_influx import (
    write_ntp
)


class CUCMNTPJob:

    def run(self, node):

        raw = collect(node)

        parsed = parse_utils_ntp_status(raw)

        write_ntp(
            node,
            parsed
        )