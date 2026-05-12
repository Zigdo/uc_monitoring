import time

import paramiko

from app.core.logging.logger import logger

from app.core.config.settings import settings

from app.core.ssh.exceptions import (
    SSHConnectionError,
    SSHCommandError
)


class SSHClientManager:

    def __init__(self):

        self.client = None

        self.shell = None

    def connect(
        self,
        host,
        username,
        password
    ):

        try:

            self.client = paramiko.SSHClient()

            self.client.set_missing_host_key_policy(
                paramiko.AutoAddPolicy()
            )

            self.client.connect(
                hostname=host,
                username=username,
                password=password,
                timeout=settings.ssh_timeout,
                banner_timeout=60,
                auth_timeout=settings.ssh_timeout,
            )

            self.shell = self.client.invoke_shell()

            time.sleep(2)

            self._clear_banner()

            logger.info(f"SSH connected to {host}")

        except Exception as e:

            raise SSHConnectionError(
                f"SSH connection failed to {host}: {e}"
            )

    def execute(self, command):

        if not self.shell:
            raise SSHCommandError(
                "SSH shell not initialized"
            )

        try:

            self.shell.send(command + "\n")

            time.sleep(2)

            output = ""

            stable_count = 0

            last_len = -1

            while stable_count < 3:

                time.sleep(2)

                while self.shell.recv_ready():

                    output += self.shell.recv(
                        4096
                    ).decode(errors="ignore")

                if len(output) == last_len:

                    stable_count += 1

                else:

                    stable_count = 0

                    last_len = len(output)

            return output

        except Exception as e:

            raise SSHCommandError(
                f"SSH command failed: {e}"
            )

    def _clear_banner(self):

        while self.shell.recv_ready():

            self.shell.recv(1024)

    def close(self):

        try:

            if self.client:
                self.client.close()

        except Exception:
            pass