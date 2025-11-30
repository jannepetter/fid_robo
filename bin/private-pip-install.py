#! /usr/bin/env python

import os
import subprocess
import sys

from robocorp import vault

REQUIRED_SECRETS = {
    # "GITHUB_SSH": "ssh_key",
    "GITHUB_TOKEN": "token"
}


def pip_install(requirements_path, env=None):
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-Ur", requirements_path], env=env
    )


def save_ssh(private_key: str, key_filename: str, host: str = "github.com"):
    """
    Save an SSH private key to ~/.ssh and configure known_hosts.

    Args:
        private_key (str): The full private key string.
        key_filename (str): Name of the key file (default: id_ed25519).
        host (str): Host to add to known_hosts (default: github.com).
    """
    ssh_dir = os.path.expanduser("~/.ssh")
    os.makedirs(ssh_dir, exist_ok=True)

    # key_filename = "private_git_ssh_test"
    key_path = os.path.join(ssh_dir, key_filename)

    # Write the private key
    with open(key_path, "w") as f:
        f.write(private_key)

    # Set secure permissions
    os.chmod(key_path, 0o600)

    # Add host to known_hosts
    known_hosts_path = os.path.join(ssh_dir, "known_hosts")
    result = subprocess.run(
        ["ssh-keyscan", host],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    if result.stdout:
        with open(known_hosts_path, "a") as f:
            f.write(result.stdout)


def main(argv):
    if len(argv) != 3:
        print(f"usage: {argv[0]} VAULT_SECRETS_NAME REQUIREMENTS_PATH")
        return

    pip_env = os.environ.copy()
    secrets = vault.get_secret(argv[1])
    for env_var, secret_name in REQUIRED_SECRETS.items():
        #     # pip_env[env_var] = secrets[secret_name]
        # if env_var == "GITHUB_SSH":
        #     private_key_single_line = secrets[secret_name]
        #     private_key = private_key_single_line.replace("\\n", "\n")
        #     save_ssh(private_key, "id_ed25519")
        pip_env[env_var] = secrets[secret_name]

    pip_install(argv[2], env=pip_env)


if __name__ == "__main__":
    main(sys.argv)
