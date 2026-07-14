import os

from dotenv import load_dotenv


class DeploymentSecretError(RuntimeError):
    """Raised when a required deployment secret is not configured."""


def get_cucm_ssh_credentials() -> tuple[str, str]:
    """Return the temporary deployment-level CUCM SSH credentials.

    Process environment variables take precedence over values in the local
    ``.env`` file because ``load_dotenv`` does not override existing values.
    This shared credential interface is intentionally temporary; per-node
    encrypted credential selection is deferred to PR 15.
    """

    load_dotenv(override=False)

    username = os.getenv("CUCM_SSH_USERNAME", "").strip()
    password = os.getenv("CUCM_SSH_PASSWORD", "")

    missing = []
    if not username:
        missing.append("CUCM_SSH_USERNAME")
    if not password.strip():
        missing.append("CUCM_SSH_PASSWORD")

    if missing:
        variable_names = ", ".join(missing)
        raise DeploymentSecretError(
            f"Required deployment secret variables are not configured: {variable_names}"
        )

    return username, password
