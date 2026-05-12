import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from config.loader import load_nodes
from app.core.dispatcher import METRIC_DISPATCH

from app.inventory.services import inventory_service

def safe_run_group(node, group):
    """
    Wrapper to safely execute a metric group collector.
    Prevents scheduler crash if one node fails.
    """
    try:
        collect_function = METRIC_DISPATCH.get(group)

        if not collect_function:
            print(f"[WARN] No collector found for group '{group}'")
            return

        collect_function(node)

    except Exception as e:
        print(f"[ERROR] Node {node['hostname']} group {group} failed: {e}")

def run_scheduler(max_workers=100, loop_interval=5):
    """
    Main scheduler loop.

    :param nodes: List of node dictionaries.
    :param max_workers: Maximum concurrent threads.
    :param loop_interval: How often scheduler checks (seconds).
    """

    # Dictionary to track last execution time per host per group
    # Structure:
    # {
    #   "host1": {"performance": 1709350000, "ntp": 1709350020},
    #   "host2": {"services": 1709350010}
    # }
    last_run = {}

    # Create ONE persistent thread pool (important for performance)
    executor = ThreadPoolExecutor(max_workers=max_workers)

    print(f"[INFO] Scheduler started with {max_workers} workers.")

    while True:

        #Capture current timestamp once per loop
        now = time.time()
        # nodes = load_nodes()
        nodes = inventory_service.get_monitored_nodes()
        # print(nodes)
        print(f"🔄 Polling {len(nodes)} nodes")

        # Iterate over all monitored nodes
        for node in nodes:

            host = node["hostname"]
            # Ensure host entry exists in last_run dictionary
            if host not in last_run:
                last_run[host] = {}

            # Iterate over polling groups defined for this node
            for group, interval in node["groups"].items():

                # Get last execution time of this group for this host
                last_time = last_run[host].get(group, 0)

                # Check if enough time has passed
                if now - last_time >= interval:

                    # Submit polling task to thread pool
                    executor.submit(safe_run_group, node, group)

                    # Update last execution time immediately
                    # (prevents duplicate scheduling)
                    last_run[host][group] = now

        # Sleep before next scheduler cycle
        time.sleep(loop_interval)


