#!/usr/bin/env python3
"""Optional one-shot, account-scoped NotebookLM cookie refresh.

Schedule only with the owner's approval. The script refuses to initialize
a missing profile or expose saved session cookies / raw CLI output.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import subprocess

from bootstrap import ROOT, auth_storage, cli_command, cli_env, valid_profile, venv_cli


def refresh(project: Path, profile: str) -> bool:
    valid_profile(profile)
    storage = auth_storage(profile)
    if not storage.is_file():
        print(f"SKIPPED: profile '{profile}' has no saved NotebookLM session.")
        return False
    if not venv_cli(project).is_file():
        print("SKIPPED: NotebookLM CLI not installed in this folder.")
        return False
    result = subprocess.run(
        cli_command(project, profile, "auth", "refresh", "--verify", "--quiet"),
        env=cli_env(), capture_output=True, text=True, check=False,
    )
    if result.returncode == 0:
        print(f"PASS: profile '{profile}' refresh and verification succeeded.")
        return True
    print(f"FAILED: profile '{profile}' refresh. It may need interactive Google recovery; no browser login was attempted.")
    return False


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="One verified refresh of one existing NotebookLM login.")
    parser.add_argument("--profile", required=True, type=valid_profile)
    args = parser.parse_args(argv)
    try:
        return 0 if refresh(ROOT, args.profile) else 1
    except (OSError, ValueError):
        print("FAILED: local NotebookLM refresh could not run; no credentials were displayed.")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
