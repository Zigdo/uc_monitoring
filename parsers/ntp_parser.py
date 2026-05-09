import re

def parse_utils_ntp_status(output_string):
    peers = []

    if not output_string:
        return {"peers": [], "system_synced": False}

    lines = output_string.splitlines()
    start_idx = None

    for i, line in enumerate(lines):
        if "remote" in line.lower():
            start_idx = i + 2
            break

    if start_idx is not None:
        for line in lines[start_idx:]:
            if not line.strip():
                continue
            try:
                remote = line[:16].strip()
                rest = line[16:].split()

                if len(rest) < 8:
                    continue

                refid, st, t, when, poll, reach, delay, offset, *jitter = rest

                def to_float(v):
                    try:
                        return float(v)
                    except ValueError:
                        return None

                peer = {
                    "remote": remote.lstrip("*+-"),
                    "refid": refid,
                    "stratum": int(st),
                    "type": t,
                    "when": when,
                    "poll": int(poll),
                    "reach": int(reach, 8),
                    "delay_ms": to_float(delay),
                    "offset_ms": to_float(offset),
                    "jitter_ms": to_float(jitter[0]) if jitter else None,
                    "sync_state": (
                        "system_peer" if remote.startswith("*")
                        else "candidate" if remote.startswith("+")
                        else "discarded"
                    )
                }

                peers.append(peer)

            except Exception:
                continue

    return {
        "peers": peers,
        "system_synced": any(p["sync_state"] == "system_peer" for p in peers)
    }