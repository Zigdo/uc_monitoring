
from app.core.ssh.client import SSHClientManager
from app.core.config.deployment_secrets import get_cucm_ssh_credentials


def collect(node):

    username, password = get_cucm_ssh_credentials()

    ssh = SSHClientManager()

    ssh.connect(
        node.ip_address,
        username=username,
        password=password,
    )

    raw = ssh.execute(
        "utils ntp status"
    )

    ssh.close()

    return raw
