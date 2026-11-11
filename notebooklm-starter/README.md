# NotebookLM starter — get one working account, then optionally more

This folder gives an AI assistant everything it needs to help you set up **Google NotebookLM** on **your own computer**. It contains an agent-readable skill, pinned installer, safe authentication checks, a one-shot session refresh, an optional Windows scheduler, and offline tests.

**Default: one account named `personal`.** Multiple accounts are optional. You do not need an MCP server, VPS, cloud deployment, API key, or a second browser profile just to begin.

The CLI is provided upstream at [`teng-lin/notebooklm-py`](https://github.com/teng-lin/notebooklm-py) and is installed from PyPI, not copied into this repository.

NotebookLM itself is Google's service; the `notebooklm-py` CLI used here is **unofficial**, can break when Google changes its site, and must be used with an account you control. We tested this package's CLI at **0.8.6** (11 November 2026); newer releases may require reviewing commands and compatibility.

## Give this folder to your AI agent

Copy the following into a ChatGPT, Codex, Claude, or other agent session that can actually read the downloaded files:

> **Set up NotebookLM with me using the `notebooklm-starter/` folder in this repository.** Read `SKILL.md`, `README.md`, and `references/SECURITY.md` before taking action. Verify what you can access; if the repository is not accessible, ask me to upload the folder. Assume I want **one account named `personal`** unless I ask for more. Check my platform, installed Python and any already-working NotebookLM login first. Show me the commands and obtain my approval **before** installing anything, opening a sign-in window, setting up a background task, or writing to my NotebookLM account. Use the normal visible Google login with me only if necessary—never ask me to send passwords or session cookies through chat. After setup, run a passive authenticated check and show me one read-only notebook listing. Explain what you verified and what remains untested. Do not delegate or connect external services without my approval.

The agent should identify the account, attempt a read-only preflight, and only then use the installer if approved. **If you already have a NotebookLM browser session, the agent should inspect whether that is sufficient for your requested task before asking you to log in again.** A browser account is not automatically a CLI account.

## Quick start (Windows PowerShell)

From the downloaded repository's `notebooklm-starter` folder, after approving the installation:

```powershell
py -3 scripts/bootstrap.py install
py -3 scripts/bootstrap.py login --profile personal
py -3 scripts/bootstrap.py check --profile personal
.\.venv\Scripts\notebooklm.exe -p personal list
```

The installer creates **`.venv/` inside this folder**, installs the pinned `notebooklm-py[browser]` and downloads Playwright Chromium in visible-browser mode without the unused headless shell. It does **not** capture a password, touch a pre-existing Google Chrome profile, or install a background scheduler. The login step may open a browser for you to finish Google sign-in, then saves an authenticated session locally. The check is a **network-based, read-only** token probe; the final `list` reads notebook titles from your account.

Use Python **3.10+**. If `py -3` is unavailable, use your installed `python` executable. Run the login command on your **visible local desktop**, not an invisible remote build runner.

## Quick start (macOS / Linux)

From `notebooklm-starter/`:

```bash
python3 scripts/bootstrap.py install
python3 scripts/bootstrap.py login --profile personal
python3 scripts/bootstrap.py check --profile personal
./.venv/bin/notebooklm -p personal list
```

On an OS without a supported graphical browser environment, perform first-time login on a computer with a visible browser. **Do not export or copy Google cookies between machines as a workaround.** The installer needs internet access, space for a browser download and permission to create a local `.venv`.

## How to add a second account (optional)

Repeat the login and check under a different explicit label. Example:

```powershell
py -3 scripts/bootstrap.py login --profile work
py -3 scripts/bootstrap.py check --profile work
.\.venv\Scripts\notebooklm.exe -p work list
```

Each label has its **own local saved Google session**; you must verify which Google account actually signed in. Label names are not proof of identity. Ask the assistant **which account** to use before each new multi-account task if not already specified. Never copy one account's `storage_state.json` to another, and never silently substitute an account that happens to be logged in. Additional profiles are not needed for a single account.

## Files in this folder

| File | Purpose |
|---|---|
| [`SKILL.md`](SKILL.md) | Agent decision flow, approvals and safe CLI usage |
| [`references/WORKFLOWS.md`](references/WORKFLOWS.md) | Working, reviewed example commands and account routing |
| [`references/SECURITY.md`](references/SECURITY.md) | Credential handling, privacy, browser and refresh precautions |
| [`scripts/bootstrap.py`](scripts/bootstrap.py) | Create isolated environment, install, log in, verify |
| [`scripts/refresh.py`](scripts/refresh.py) | One-shot verified cookie refresh for a named authenticated profile |
| [`scripts/register_keepalive.ps1`](scripts/register_keepalive.ps1) | Optional Windows 20-minute refresh task (requires separate approval) |
| [`requirements.txt`](requirements.txt) | Reviewed dependency constraint |
| [`tests/test_starter.py`](tests/test_starter.py) | Offline, no-account contract and safety tests |

Run the offline suite from this folder:

```bash
python -m unittest discover -s tests -v
```

These tests verify installer and account isolation logic **without logging into Google**. A real account is verified separately using `bootstrap.py check`.

## Session longevity: opt in, don't assume

Google authentication can become stale when a CLI account sits idle. The one-shot `python scripts/refresh.py --profile personal` uses the CLI's supported cookie rotation and passive verification. It is **state-changing**, so only use it for your account.

If you want Windows to attempt this every ~20 minutes **after you have an authenticated session and with your approval**, read [`references/SECURITY.md`](references/SECURITY.md) and run:

```powershell
.\scripts\register_keepalive.ps1 -Profile personal -DryRun
.\scripts\register_keepalive.ps1 -Profile personal
```

It creates a **per-profile** Windows task, only while that Windows user is logged in. It cannot keep a powered-off or offline machine authenticated indefinitely. For a second profile, register separately **after** verifying its own login. No task is created by the installer.

Unregister only the specific task when desired:

```powershell
Unregister-ScheduledTask -TaskName 'NotebookLM-Starter-personal' -Confirm:$false
```

## What "working" means

A successful install is **not** proof of authentication. A successful file check is **not** proof of live Google access. Setup acceptance is: CLI exists in `.venv`, the intended Google account is confirmed, `bootstrap.py check` exits 0 using a passive server token check, and `-p <profile> list` can read the expected notebooks. Generating audio, video or slide decks is optional, spends quota and requires separate authorization.

**No authentication material, local computer paths, Google account addresses or private automation configurations are included in this release.** Source files are usable without the author's private infrastructure.
