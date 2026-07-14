from app.inventory.models.enums import HealthStatus


class NTPHealthEvaluator:

    metric_name = "ntp"

    def evaluate(self, node, data: dict) -> dict:

        active_peer = next(
            (
                peer
                for peer in data.get("peers", [])
                if peer.get("sync_state") == "system_peer"
            ),
            None
        )

        backup_peers = next(
            (
                peer
                for peer in data.get("peers", [])
                if peer.get("sync_state") == "candidate"
            ),
            None
        )


        if not data.get("system_synced"):
            return {
                "status": HealthStatus.CRITICAL,
                "score": 0,
                "message": "System not synchronized"
            }

        if not active_peer:
            return {
                "status": HealthStatus.CRITICAL,
                "score": 0,
                "message": "No active NTP peer"
            }

        remote = active_peer.get("remote")
        stratum = active_peer.get("stratum")
        offset = active_peer.get("offset_ms", 0)
        reach = active_peer.get("reach", 0)
        jitter = active_peer.get("jitter_ms", 0)

        #
        # CRITICAL RULES
        #

        if reach == 0:
            return {
                "status": HealthStatus.CRITICAL,
                "score": 0,
                "message": "No NTP reachability"
            }

        #
        # WARNING RULES
        #
        if stratum > 4:
            return {
                "status": HealthStatus.WARNING,
                "score": 60,
                "message": f"High stratum: {stratum}"
            }

        if abs(offset) > 100:
            return {
                "status": HealthStatus.WARNING,
                "score": 70,
                "message": f"High offset: {offset}ms"
            }

        if jitter > 10:
            return {
                "status": HealthStatus.WARNING,
                "score": 75,
                "message": f"High jitter: {jitter}ms"
            }
        
        if not backup_peers:
            return {
                "status": HealthStatus.WARNING,
                "score": 90,
                "message": f"NTP synchronized but no backup peers available"
            }
        


        #
        # HEALTHY
        #
        return {
            "status": HealthStatus.HEALTHY,
            "score": 100,
            "message": f"Sync to {remote} stratum {stratum}"
        }