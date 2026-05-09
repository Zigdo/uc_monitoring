import paramiko
paramiko.util.log_to_file("paramiko.log")
import time 
import re
import socket

"""
Runs a CUCM / UCCX CLI command over SSH and returns full raw output.

Why invoke_shell?
-----------------
CUCM does NOT behave like a standard Linux shell.
Most 'utils' commands require an interactive CLI session.
"""

# CUCM_PROMPT = re.compile(r"\nadmin:\s*$", re.IGNORECASE)


def run_ssh_command(host, username, password, command, timeout=60):
      
    """Connects to CUCM via SSH and retrieves raw license usage output."""

    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        ssh_client.connect(
            hostname = host,
            username = username,
            password = password,
            timeout=timeout,
            banner_timeout=60,
            auth_timeout=timeout,
            disabled_algorithms=None,
        )

        ssh_shell = ssh_client.invoke_shell()
        time.sleep(2)

        # clear banner
        while ssh_shell.recv_ready():
            ssh_shell.recv(1024)

        ssh_shell.send(command + "\n")
        time.sleep(2)

        recv_data = ""
        last_len = -1
        stable_count = 0
        # read until stable output
        while stable_count < 3:
            time.sleep(2)
            while ssh_shell.recv_ready():
                recv_data += ssh_shell.recv(4096).decode(errors="ignore")
            if len(recv_data) == last_len:
                stable_count += 1
            else:
                stable_count = 0
                last_len = len(recv_data)

        return recv_data

    except Exception as e:
        raise RuntimeError(f"SSH error {host}:22 - {e}")
    finally:
        try:
            ssh_client.close()
        except Exception:
            pass