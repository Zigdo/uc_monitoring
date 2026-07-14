import unittest
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from app.monitoring.collectors.ssh.ntp_collector import collect


class NTPCollectorSecretTests(unittest.TestCase):
    @patch("app.monitoring.collectors.ssh.ntp_collector.SSHClientManager")
    @patch(
        "app.monitoring.collectors.ssh.ntp_collector.get_cucm_ssh_credentials"
    )
    def test_collector_uses_deployment_credentials(
        self,
        get_credentials,
        ssh_manager,
    ):
        get_credentials.return_value = ("runtime-user", "runtime-password")
        ssh = MagicMock()
        ssh.execute.return_value = "ntp output"
        ssh_manager.return_value = ssh
        node = SimpleNamespace(ip_address="192.0.2.10")

        result = collect(node)

        ssh.connect.assert_called_once_with(
            node.ip_address,
            username="runtime-user",
            password="runtime-password",
        )
        ssh.execute.assert_called_once_with("utils ntp status")
        ssh.close.assert_called_once_with()
        self.assertEqual(result, "ntp output")


if __name__ == "__main__":
    unittest.main()
