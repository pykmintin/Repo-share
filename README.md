# Public AI learning starters — KGO, Overseer Hub and NotebookLM

**New to both projects?** Start with the [copyable ChatGPT learning prompt](START-HERE.md). It teaches KGO and the read-only Overseer Hub example step by step, asks questions, practises with your own prompts, and generates a portable **Learning Passport** for future chats. No installation is required to begin.

One maintained version of the **Kimi Genesis Orchestrator** (KGO) skill, supplied for learning and installing into your own AI agent.

**[Start with the README in `kimi-genesis-orch/`](kimi-genesis-orch/README.md).** It contains a copyable teaching/setup prompt, installation instructions, an example exercise, and a verification checklist.

- [Core skill](kimi-genesis-orch/SKILL.md) — read this in full first. It only activates by explicit request.
- [Strategy catalog](kimi-genesis-orch/references/strategies.md) — read the complete entries relevant to your task.
- [Failure modes](kimi-genesis-orch/references/failure-modes.md) — common mistakes and how to avoid them.
- [Worker-prompt slots](kimi-genesis-orch/references/slots.md) — use only when you want to write instructions for another agent.

To get the files, use GitHub **Code → Download ZIP**, or run `git clone https://github.com/pykmintin/Repo-share.git`. Keep the complete `kimi-genesis-orch/` directory together.

This release preserves the canonical `SKILL.md`, three reference files, and `agents/openai.yaml` byte-for-byte. The README is a portable onboarding adaptation; maintainer-specific retrieval configuration is omitted. Historical v3/v4 editions were retired from this public repository and archived offline.

**No API keys or special orchestration backend are needed to read and understand KGO.** Access to files, tool calls, and other agents depends on your chosen AI client.

## NotebookLM starter — install a working local account

**[Open the NotebookLM starter](notebooklm-starter/README.md)** for a copyable agent prompt, local installation scripts, normal Google browser login, server-verified authentication checks and an optional cookie keepalive. One account is the default; independent named profiles support multiple accounts if you need them. This is a **self-contained public example** and needs none of the maintainer's private accounts, Overseer Hub or KeyHub services. It installs the [unofficial notebooklm-py CLI](https://github.com/teng-lin/notebooklm-py) with the upstream browser integration instead of distributing Google credentials or copied upstream code.

## Overseer Hub Starter — public OAuth/MCP backend

**[Read the Overseer Hub starter guide](overseer-hub-starter/README.md)** to learn and deploy a separate, read-only MCP backend using **your own Auth0 tenant, HTTPS hostname and ChatGPT custom MCP connection**. The [architecture explanation](overseer-hub-starter/ARCHITECTURE.md) maps it to the real Overseer design. It includes source, environment template and executable tests; it does **not** include the private production Bridge, browser sessions, host tools or credentials.
