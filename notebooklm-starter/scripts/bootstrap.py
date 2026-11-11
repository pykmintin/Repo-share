#!/usr/bin/env python3
"""Safe, portable, agent-readable setup for the unofficial NotebookLM CLI.

Only "install" downloads/installs software. "login" uses normal visible browser
authentication; never accepts passwords or raw Google cookies in arguments.
"check" performs a passive, read-only server token check and redacts output.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import subprocess
import sys
import venv


ROOT = Path(__file__).resolve().parents[1]
REQUIREMENT = "notebooklm-py[browser]==0.8.6"


def valid_profile(value: str) -> str:
    if not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{0,31}", value):
        raise ValueError("Profile must be 1-32 characters: start with a letter, then letters, digits, _ or -.")
    return value


def venv_python(project: Path) -> Path:
    suffix = Path("Scripts/python.exe") if os.name == "nt" else Path("bin/python")
    return project / ".venv" / suffix


def venv_cli(project: Path) -> Path:
    suffix = Path("Scripts/notebooklm.exe") if os.name == "nt" else Path("bin/notebooklm")
    return project / ".venv" / suffix


def cli_command(project: Path, profile: str, *arguments: str) -> list[str]:
    return [str(venv_cli(project)), "-p", valid_profile(profile), *arguments]


def cli_env(base: dict[str, str] | None = None) -> dict[str, str]:
    env = dict(os.environ if base is None else base)
    # NOTEBOOKLM_AUTH_JSON bypasses named-profile storage, even if set to "".
    env.pop("NOTEBOOKLM_AUTH_JSON", None)
    # Prevent arbitrary external hook invocation during our simple healthcheck.
    env.pop("NOTEBOOKLM_REFRESH_CMD", None)
    return env


def auth_storage(profile: str) -> Path:
    home = Path(os.environ.get("NOTEBOOKLM_HOME") or (Path.home() / ".notebooklm")).expanduser()
    return home / "profiles" / valid_profile(profile) / "storage_state.json"


def ensure_install(project: Path) -> None:
    if sys.version_info < (3, 10):
        raise RuntimeError("Python 3.10+ is required.")
    requirement_file = (project / "requirements.txt").read_text(encoding="utf-8")
    if REQUIREMENT not in requirement_file:
        raise RuntimeError("Pinned requirements.txt does not match the tested setup.")
    if not venv_python(project).is_file():
        print("Creating a local Python virtual environment (no global Python changes)...")
        venv.EnvBuilder(with_pip=True, clear=False).create(project / ".venv")
    interpreter = str(venv_python(project))
    print("Installing the pinned NotebookLM CLI and browser integration...")
    subprocess.run(
        [interpreter, "-m", "pip", "install", "--disable-pip-version-check", "-r", str(project / "requirements.txt")],
        check=True,
    )
    print("Installing Playwright's Chromium browser for normal visible Google login...")
    subprocess.run([interpreter, "-m", "playwright", "install", "chromium", "--no-shell"], check=True)
    if not venv_cli(project).is_file():
        raise RuntimeError("Installation finished but the NotebookLM CLI executable was not found.")
    print("INSTALL OK. Next: python scripts/bootstrap.py login --profile personal")


def check_auth(project: Path, profile: str) -> bool:
    command = cli_command(project, profile, "auth", "check", "--test", "--passive")
    # Capture and discard sensitive diagnostic fields such as account metadata.
    result = subprocess.run(command, capture_output=True, text=True, env=cli_env(), check=False)
    if result.returncode == 0:
        print(f"PASS: NotebookLM profile '{profile}' authenticated with Google (passive check).")
        return True
    print(f"NOT READY: NotebookLM profile '{profile}' is not verified. Check the account or sign in using 'login'.")
    return False


def login(project: Path, profile: str) -> bool:
    valid_profile(profile)
    if auth_storage(profile).is_file() and check_auth(project, profile):
        print("Existing session works. No new browser login was needed.")
        return True
    print(f"Opening a local browser for profile '{profile}'. Sign in yourself; never give an agent your password.")
    result = subprocess.run(
        cli_command(project, profile, "login", "--browser-timeout", "900"),
        env=cli_env(), check=False,
    )
    if result.returncode != 0:
        print("Login did not complete. The existing profile was not deleted.")
        return False
    print("Login saved; verifying with a passive server-side token check...")
    return check_auth(project, profile)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Set up a private local NotebookLM CLI. Nothing installs or logs in until you choose that action."
    )
    actions = parser.add_subparsers(dest="action", required=True)
    actions.add_parser("install", help="Create .venv, install pinned CLI and Playwright Chromium.")
    login_parser = actions.add_parser("login", help="Reuse saved session or request normal interactive Google sign-in.")
    login_parser.add_argument("--profile", default="personal", type=valid_profile)
    check_parser = actions.add_parser("check", help="Read-only live authentication check.")
    check_parser.add_argument("--profile", default="personal", type=valid_profile)
    actions.add_parser("profiles", help="List existing CLI profiles (may show locally configured account labels).")
    args = parser.parse_args(argv)
    try:
        if args.action == "install":
            ensure_install(ROOT)
            return 0
        if not venv_cli(ROOT).is_file():
            print("CLI not installed in this folder. Run: python scripts/bootstrap.py install")
            return 2
        if args.action == "login":
            return 0 if login(ROOT, args.profile) else 1
        if args.action == "check":
            return 0 if check_auth(ROOT, args.profile) else 1
        if args.action == "profiles":
            return subprocess.run([str(venv_cli(ROOT)), "profile", "list"], env=cli_env(), check=False).returncode
    except (OSError, subprocess.CalledProcessError, RuntimeError) as exc:
        print(f"Setup failed ({type(exc).__name__}); check Python, network access, and this folder's permissions.")
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
