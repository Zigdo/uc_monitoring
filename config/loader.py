import yaml

def load_nodes(config_path="config/nodes.yaml"):
    """
    Load full configuration:
    - polling_groups
    - application_profiles
    - nodes
    Attach resolved polling intervals to each node.
    """

    with open(config_path) as f:
        config = yaml.safe_load(f)

    polling_groups = config["polling_groups"]
    app_profiles = config["application_profiles"]
    nodes = config["nodes"]

    for node in nodes:

        app = node["application"]

        if app not in app_profiles:
            raise ValueError(f"Application profile missing: {app}")

        resolved_groups = {}

        for group_name in app_profiles[app]["groups"]:

            if group_name not in polling_groups:
                raise ValueError(f"Polling group missing: {group_name}")

            interval = polling_groups[group_name]["interval"]

            resolved_groups[group_name] = interval

        # Attach groups to node dynamically
        node["groups"] = resolved_groups

    return nodes