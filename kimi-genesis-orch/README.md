# Kimi Genesis Orchestrator (KGO)

**A practical guide to reasoning through work and designing instructions for AI agents.** This is a skill (a set of Markdown instructions), not an AI model, app, or autonomous agent service. You can use it to improve an agent's *own approach* to a task, or to prepare a more reliable prompt for a separate worker agent.

This public package is synchronized from the maintainer's current canonical skill. Its core skill, references, and invocation policy are preserved verbatim. The source files below, not this overview, define the method.

## Start here: ask an agent to teach you

Open an AI agent that can read GitHub pages or attached files, and paste the following. Replace `[your small task]` with a real example, such as "compare two study options" or "organize a few project notes." If the agent cannot access GitHub, download this directory and attach the files; don't let it guess their contents.

```text
You are my Kimi Genesis Orchestrator (KGO) guide and setup assistant.
Source: https://github.com/pykmintin/Repo-share/tree/main/kimi-genesis-orch

Read SKILL.md in full before explaining or using this skill. Then read the
complete relevant entries in references/strategies.md and applicable
references/failure-modes.md. Read references/slots.md if we draft a prompt
for another agent. If you cannot access those files, tell me which files to
attach instead of inventing their contents.

My goal: understand KGO, learn how to invoke it deliberately, and try it
on this task: [your small task].

After reading, first surface the Phase 0 articulation for this task:
who receives the result, what context is verified or unknown, what
inspectable output is intended, and the smallest next action. Do not
claim the skill is loaded before that articulation.

First establish what AI agent/app and operating system I'm using, if they
aren't already known. Explain in plain language KGO's two uses (your own
task reasoning versus creating worker prompts), Phase 0, the four forcing
questions, and the five audit checks. Show one concrete example grounded
in the actual source files.

If my agent supports installed skills, identify its documented skills
directory and help me install this entire folder without changing or
overwriting any existing installation silently. Verify the installed
SKILL.md and relative references can be opened, and test explicit
invocation. If my agent does not support skill discovery, show how to use
the supplied files directly.

Before any setup changes, explain exactly what you plan to change and
get my approval. Do not install other software, use my accounts, or
launch another agent without asking.

Return: (1) what KGO does, (2) what files you actually read,
(3) what is installed or what remains uninstalled, (4) one worked
example with a specific success artifact and verification test, and
(5) my next practical step. Distinguish verified facts from assumptions.
```

You can use this learning prompt without installing anything. The agent must actually be able to read the files: a repository URL alone does not supply source contents to every chat app.

## What the skill changes

KGO makes the agent ask *what output must exist*, *what it needs to read*, *where the boundary is*, and *which decisions require the user*. Before a substantial action, it checks whether the intended recipient can use the result and whether the success condition is observable. It then selects only the relevant prompting/reasoning strategies.

There are **two distinct modes**:

1. **Own-work mode:** an agent applies the strategies to its own task. There is no requirement to launch other agents or build an eight-slot worker prompt.
2. **Worker-prompt mode:** an agent designs instructions for another agent. The [eight slots](references/slots.md) help specify its role, read set, project context, mission, constraints, success criteria, return format, and (where useful) self-check.

The skill requires a **Phase 0 preflight**: read `SKILL.md`, consult the relevant complete reference entries, and articulate the recipient, known and unknown context, intended result, and next inspectable action. It is designed to be **explicitly invoked**, not to run automatically on every conversation.

## Files and reading order

| File | Purpose |
| --- | --- |
| [`SKILL.md`](SKILL.md) | Core contract, Phase 0, four forcing questions, five audit checks, and the strategy index. **Read this first, in full.** |
| [`references/strategies.md`](references/strategies.md) | Strategy catalog. Read full entries relevant to the current behavior; do not treat the index as a substitute. |
| [`references/failure-modes.md`](references/failure-modes.md) | Common mistakes and counter-patterns. Read those relevant to the current task. |
| [`references/slots.md`](references/slots.md) | The eight-slot template **only when constructing a worker prompt**. |
| [`agents/openai.yaml`](agents/openai.yaml) | Declares that implicit invocation is not allowed. |

## Get the files and install (optional)

You can browse the folder on GitHub, download the repository as a ZIP, or clone it:

```sh
git clone https://github.com/pykmintin/Repo-share.git
```

The files will be under `skills/kimi-genesis-orch/` if you cloned into the default directory. **Keep the complete `kimi-genesis-orch` folder together**: the relative `references/` files are part of the skill.

For an agent that supports skills, ask it to check its **current, documented** skills directory, copy this entire folder there, restart or refresh skill discovery if required, and explicitly invoke `kimi-genesis-orch`. Skill paths and invocation syntax differ by product. Do not assume the maintainer's paths are correct for your computer. Compare and back up an existing same-name directory before replacing it.

If your agent doesn't support installed skills, give it the folder's files as attachments or an accessible local workspace path and use the teaching prompt above. The core method is written in Markdown; no separate Kimi model, API key, or special orchestration service is required *to read and learn the skill*. Your chosen AI agent may itself require a subscription or login.

### Verify it works

Ask your agent to:

1. Open its installed or attached `SKILL.md` and identify the explicit-invocation rule.
2. State the difference between own-work and worker-prompt use.
3. Read one **complete** relevant entry from `references/strategies.md` and name why it was chosen.
4. Apply KGO to your small task, naming the recipient, source material, concrete output, and a falsifiable check. If drafting a worker prompt, also consult `references/slots.md`.
5. Report what it actually read and tested. An answer based solely on the directory name is **not** verification.

Example explicit request: `Use kimi-genesis-orch on my task of organizing three research notes. Show the Phase 0 articulation and the smallest verifiable result. Do not delegate.`

## Portability and safety

- The maintainer's optional, host-specific Codex retrieval adapter is not included in this portable package. Read the Markdown files directly; no special local index is required.
- KGO is an instruction framework; it does not automatically grant access to local files, GitHub, terminals, credentials, or other agents. Access depends on the client and your permissions.
- Don't give an agent passwords or tokens to make this work. Require confirmation before edits, installation, delegation, or account actions.
- For updates, pull the canonical repository again (`git pull --ff-only` in a clean clone) and compare changes before refreshing your installed copy. Do not silently overwrite personal edits.

## Troubleshooting

**"Skill not found."** Check whether your agent supports skill folders, where it discovers them, and whether the directory name and `SKILL.md` are in the expected location. Otherwise use the Markdown files directly.

**"The agent explains it but can't cite a source."** Ask it to read `SKILL.md` and the relevant full reference entry first, or attach those files. Do not accept a summary guessed from the name.

**"My agent asks for an unavailable file or host-specific tool."** Use direct reads of the relative files shipped here. Do not recreate the maintainer's tool setup to learn KGO.
