
from app.core.ssh.client import SSHClientManager


def collect(node):

    ssh = SSHClientManager()

    ssh.connect(
        node.ip_address,
        username="admin",
        password="Ahrkh8080!@"
        # node.username,
        # node.password
    )

    raw = ssh.execute(
        "utils ntp status"
    )

    ssh.close()

    return raw