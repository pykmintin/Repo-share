# Working NotebookLM CLI workflows (v0.8.6)

These examples assume the user approved setup, `scripts/bootstrap.py check --profile personal` passed, and the current directory is `notebooklm-starter/`. The commands below use the installed CLI from this folder's isolated `.venv`; other operating systems substitute their executable path.

## Step 1 — confirm the chosen account

On Windows:

```powershell
.\.venv\Scripts\notebooklm.exe profile list
.\.venv\Scripts\notebooklm.exe -p personal auth check --test --passive
.\.venv\Scripts\notebooklm.exe -p personal list
```

On macOS/Linux:

```bash
./.venv/bin/notebooklm profile list
./.venv/bin/notebooklm -p personal auth check --test --passive
./.venv/bin/notebooklm -p personal list
```

The account list or `list` output may include personal information. Keep it local and avoid pasting identities, notebook titles, raw auth JSON or cookies into public logs. The initial `auth check` is read-only; it contacts Google, does **not** refresh cookies, and does not write saved auth state.

## Step 2 — create a notebook only when requested

The following examples use Windows `notebooklm.exe`. On macOS/Linux replace that executable with `./.venv/bin/notebooklm`.

```powershell
.\.venv\Scripts\notebooklm.exe -p personal create "Learning notes"
```

Save the **notebook ID returned by the command** before continuing. The CLI might save an active notebook context, but that context is not a safe substitute for passing an ID explicitly.

## Step 3 — add a source with specific approval

```powershell
.\.venv\Scripts\notebooklm.exe -p personal source add -n NOTEBOOK_ID --type url "https://example.org/intro"
.\.venv\Scripts\notebooklm.exe -p personal source list -n NOTEBOOK_ID
```

Do not use URLs containing sensitive bearer tokens or signed private query parameters. Check the source is something the owner has the right to upload and the URL is public/safe. Never automatically use `--allow-internal`; that bypasses protections intended to avoid local-network and intranet fetches.

## Step 4 — ask a source-grounded question

```powershell
.\.venv\Scripts\notebooklm.exe -p personal ask -n NOTEBOOK_ID --new "Summarise the main ideas and cite the sources."
```

Read-only as to notebook source material, but it sends a question to the Google service and may consume usage. Check citations and results; don't treat generated content as authoritative without review.

## Step 5 — optionally generate audio, video or slides

Only after confirming the requested content and quota implications:

```powershell
.\.venv\Scripts\notebooklm.exe -p personal generate audio -n NOTEBOOK_ID "Explain the essentials to a beginner" --wait
```

A command can start an asynchronous generation without returning a finished artifact. Do not claim a media file is complete until the tool actually verifies the artifact and any download. The CLI has `generate audio`, `generate video`, `generate slide-deck`, and other commands; use `<subcommand> --help` to check options before running. The `--later` option for supported media is **not** a completed output and cannot be combined with `--wait`.

## Optional second account

Each CLI profile has its own saved session, usually under `~/.notebooklm/profiles/<profile>/storage_state.json` (or `NOTEBOOKLM_HOME`). Labels may be anything path-safe such as `personal` and `work`; `P` or `V` are not special.

```powershell
py -3 scripts/bootstrap.py login --profile work
py -3 scripts/bootstrap.py check --profile work
.\.venv\Scripts\notebooklm.exe -p work list
```

Verify the actual Google account before storing or modifying anything. Don't clone one profile's cookies into another; simultaneous cookie rotation can invalidate sessions. If a different browser is already authenticated, using that **browser directly** may be simpler than establishing a new CLI login. A browser-only login is not proof that the CLI is authenticated. Always preserve the selected account throughout the workflow.

## Troubleshooting safely

| Symptom | What to do |
|---|---|
| Python executable not found | Install Python 3.10+ on the owner's machine, then rerun the approved installer |
| `.venv` CLI missing | Rerun `bootstrap.py install` with approval; never fall back to an unrelated global CLI |
| `auth check` fails | Confirm named profile and network. Verify any existing browser access before requesting another Google login |
| Browser doesn't open | Ensure the login command runs on a real desktop. Avoid headless identity challenges; use an owner-visible session |
| Multiple accounts in Google chooser | Owner selects the intended identity; verify NotebookLM account and notebooks before writing |
| Frequent cookie expiration | After successful login, consider the approved `refresh.py` one-shot and optional 15–20-minute scheduler while PC is awake and logged in |
| Rate limit / quota | Stop or defer. Free-tier limits vary; never claim that a quota is fixed or guarantee regeneration |
| Google changes site/API | `notebooklm-py` is unofficial. Recheck current release docs/CLI help and update this package through a reviewed change |
