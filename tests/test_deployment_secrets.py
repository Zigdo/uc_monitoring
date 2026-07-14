import os
import unittest
from unittest.mock import patch

from app.core.config.deployment_secrets import (
    DeploymentSecretError,
    get_cucm_ssh_credentials,
)


class DeploymentSecretsTests(unittest.TestCase):
    def test_returns_credentials_from_process_environment(self):
        environment = {
            "CUCM_SSH_USERNAME": "test-user",
            "CUCM_SSH_PASSWORD": "test-password",
        }

        with patch.dict(os.environ, environment, clear=True), patch(
            "app.core.config.deployment_secrets.load_dotenv"
        ):
            self.assertEqual(
                get_cucm_ssh_credentials(),
                ("test-user", "test-password"),
            )

    def test_process_environment_takes_precedence_over_dotenv(self):
        environment = {
            "CUCM_SSH_USERNAME": "process-user",
            "CUCM_SSH_PASSWORD": "process-password",
        }

        def simulate_dotenv(*, override=False):
            self.assertFalse(override)
            os.environ.setdefault("CUCM_SSH_USERNAME", "file-user")
            os.environ.setdefault("CUCM_SSH_PASSWORD", "file-password")

        with patch.dict(os.environ, environment, clear=True), patch(
            "app.core.config.deployment_secrets.load_dotenv",
            side_effect=simulate_dotenv,
        ):
            self.assertEqual(
                get_cucm_ssh_credentials(),
                ("process-user", "process-password"),
            )

    def test_missing_username_is_rejected(self):
        environment = {"CUCM_SSH_PASSWORD": "configured-password"}

        with patch.dict(os.environ, environment, clear=True), patch(
            "app.core.config.deployment_secrets.load_dotenv"
        ):
            with self.assertRaisesRegex(
                DeploymentSecretError, "CUCM_SSH_USERNAME"
            ):
                get_cucm_ssh_credentials()

    def test_missing_password_is_rejected(self):
        environment = {"CUCM_SSH_USERNAME": "configured-user"}

        with patch.dict(os.environ, environment, clear=True), patch(
            "app.core.config.deployment_secrets.load_dotenv"
        ):
            with self.assertRaisesRegex(
                DeploymentSecretError, "CUCM_SSH_PASSWORD"
            ):
                get_cucm_ssh_credentials()

    def test_blank_values_are_rejected(self):
        environment = {
            "CUCM_SSH_USERNAME": "   ",
            "CUCM_SSH_PASSWORD": "   ",
        }

        with patch.dict(os.environ, environment, clear=True), patch(
            "app.core.config.deployment_secrets.load_dotenv"
        ):
            with self.assertRaises(DeploymentSecretError) as raised:
                get_cucm_ssh_credentials()

        self.assertIn("CUCM_SSH_USERNAME", str(raised.exception))
        self.assertIn("CUCM_SSH_PASSWORD", str(raised.exception))

    def test_error_does_not_contain_configured_secret(self):
        secret = "value-that-must-not-appear"
        environment = {"CUCM_SSH_PASSWORD": secret}

        with patch.dict(os.environ, environment, clear=True), patch(
            "app.core.config.deployment_secrets.load_dotenv"
        ):
            with self.assertRaises(DeploymentSecretError) as raised:
                get_cucm_ssh_credentials()

        self.assertNotIn(secret, str(raised.exception))


if __name__ == "__main__":
    unittest.main()
