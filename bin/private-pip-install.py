#! /usr/bin/env python

import os
import subprocess
import sys

from robocorp import vault

REQUIRED_SECRETS = {"GITHUB_TOKEN": "token"}


def pip_install(requirements_path, env=None):
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-Ur", requirements_path], env=env
    )


def main(argv):
    if len(argv) != 3:
        print(f"usage: {argv[0]} VAULT_SECRETS_NAME REQUIREMENTS_PATH")
        return

    pip_env = os.environ.copy()
    secrets = vault.get_secret(argv[1])
    for env_var, secret_name in REQUIRED_SECRETS.items():
        pip_env[env_var] = secrets[secret_name]

    pip_install(argv[2], env=pip_env)


if __name__ == "__main__":
    main(sys.argv)
