# Overseer Hub Starter — your own ChatGPT MCP backend

**Want to learn both KGO and Overseer together?** Use the [guided ChatGPT starter prompt](../START-HERE.md) before tackling individual setup or installation.

A **working, read-only teaching implementation** of the key public-facing Overseer Hub pattern: an HTTPS-reachable MCP endpoint, Auth0 access-token verification, identity-aware tool discovery, and a tiny allowlisted backend. It is designed to be understandable and independently deployable without connecting to the maintainer's infrastructure.

**Start with an AI agent:** Open the public repository in a coding agent with file and terminal access. Paste the [agent handoff prompt](#agent-handoff-prompt), and let it inspect your operating system and available services before proposing setup changes. A chat-only agent can explain the files but cannot install or deploy them without appropriate tools.

**This is not the full private Overseer Hub.** The production Hub includes a private Bridge, browser sessions, host execution, provider registries and multiple owner-scoped integrations. Those are intentionally absent. The starter runs only `get_profile`, `fabric_read`, and a harmless `fabric_call("echo", ...)`. Do not claim the full Overseer stack is installed.

## Code and architecture

- [`server.py`](server.py) — runnable MCP v2 server, fail-closed HTTP auth middleware, read-only tools, and OAuth resource metadata.
- [`cloud_auth.py`](cloud_auth.py) — **verbatim copy** of the canonical Overseer Cloud Auth0 JWT guard (issuer, audience, subject, allowed OAuth clients, RS256/JWKS); no credentials are embedded.
- [`tests/test_starter.py`](tests/test_starter.py) — isolated contract tests for JWT authorization, host isolation, OAuth discovery and actual MCP tool calls.
- [`ARCHITECTURE.md`](ARCHITECTURE.md) — what maps to the real production architecture and what was deliberately excluded.
- [`.env.example`](.env.example) — safe environment-variable template, not credentials.
- [`Caddyfile.example`](Caddyfile.example) — optional public HTTPS reverse proxy once you own a resolvable hostname.

## What you need

Python 3.11 or newer, permission to run a server, and (to connect from ChatGPT) access to the custom MCP plugin feature in your ChatGPT plan/workspace. A live OAuth connection additionally requires your **own Auth0 tenant** and a stable publicly reachable HTTPS endpoint. You do *not* need the maintainer's Auth0 tenant, GitHub private repository, browser accounts, APIs, or OAuth secrets.

**ChatGPT entitlement caveat:** As documented in November 2026, full MCP actions are available to Business and Enterprise/Edu workspaces with appropriate permissions; Pro has more limited read/fetch access. Other plans may not offer custom MCP connections. Check [current official connection guidance](https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt) inside your own account before paying for or provisioning infrastructure.

## Local setup

Clone the public repository, open this folder, and create an isolated Python environment. No installations or account registrations are performed by these instructions automatically.

```sh
git clone https://github.com/pykmintin/Repo-share.git
cd Repo-share/overseer-hub-starter
python -m venv .venv
# Activate .venv using your OS's documented command.
python -m pip install -r requirements.txt
python -m pytest -q tests/test_starter.py
```

Copy `.env.example` to `.env` (ignored by Git). Obtain all values from **your own** Auth0 tenant and chosen HTTPS hostname, then start:

```sh
python -m uvicorn server:app --env-file .env --host 127.0.0.1 --port 7701
```

The service deliberately returns HTTP **503** until the required OAuth variables are present; it never falls back to anonymous access. Once configured, its public resource metadata responds at `/.well-known/oauth-protected-resource`; an unauthenticated `POST /cloud/mcp` responds **401**, with a resource-metadata challenge. A successful local test is not proof of a completed ChatGPT login.

## Setup sequence for your own backend

1. **Choose the deployment machine.** It must keep a Python process running and accept inbound HTTPS through a reverse proxy/tunnel. A VPS or home server can work; hosting may cost money even when DNS and Auth0 have free tiers. Bind Python only to `127.0.0.1:7701`.
2. **Choose a public hostname.** For quick development, [Cloudflare Quick Tunnel](https://developers.cloudflare.com/tunnel/get-started/quick-tunnels/) gives a temporary `trycloudflare.com` URL; it changes when restarted and is *not* a stable connector address. For a persistent free hostname, a provider such as [dynv6](https://dynv6.com/) offers a free dynamic DNS hostname. If that hostname points to your reachable server and you have ports 80/443, [Caddy automatic HTTPS](https://caddyserver.com/docs/quick-starts/https) can provide the TLS reverse proxy in `Caddyfile.example`. A [named Cloudflare Tunnel](https://developers.cloudflare.com/tunnel/get-started/) is an alternative when you have a domain managed in a Cloudflare zone; do not assume Cloudflare provides a free permanent domain for a Python origin.
3. **Create your own Auth0 Free tenant.** In Auth0, create an API (resource server) whose identifier/audience matches your final **`https://YOUR-HOST/cloud/mcp`**. Use RS256. Create a Regular Web Application for the ChatGPT OAuth client. Enable Authorization Code and Refresh Token grants; configure **only the callback URL shown by ChatGPT's plugin setup UI**. Make sure the OAuth provider advertises `offline_access` and can issue refresh tokens. Do not enable open Dynamic Client Registration by default; Auth0 warns that open DCR permits public registration.
4. **Fill `.env` without sharing credentials in chat.** The issuer (including trailing slash), JWKS URI, audience, resource URL, subject (from your permitted Auth0 User ID), and OAuth client ID must match your actual tenant. No ChatGPT OAuth client secret belongs in this server's code or environment. Enter it only into a suitable secure connection UI if the chosen client-registration mode requires one.
5. **Verify server behavior without ChatGPT.** Run the included tests, verify public `https://YOUR-HOST/.well-known/oauth-protected-resource` returns the expected resource and issuer, then verify an unauthenticated MCP request is **401**, *not* a tool list or a 200. A verified Auth0 login must also produce a signed access token for this precise API audience; a Google ID token is not valid here. Do not paste bearer tokens into the chat or logs.
6. **Connect ChatGPT.** On the ChatGPT web interface, open **Plugins → Add custom MCP server** (or its current equivalent). Supply your **`https://YOUR-HOST/cloud/mcp`** URL, select OAuth, and use the Auth0 application registration details. Complete the consent flow with the authorized Auth0 account; review discovered tools. Test `get_profile`, `fabric_read` and `fabric_call` with `{"tool":"echo","args":{"message":"hello"}}`. If your plan only permits read/fetch actions, a `fabric_call` may not be available even though this example is non-mutating.
7. **Accept only evidence.** Confirm HTTPS externally, OAuth issuer/audience/client checks, no anonymous MCP tools, successful tool discovery, and a **real native ChatGPT tool call**. Server health, successful Auth0 login, and agent-written “it works” do not substitute for an observed call.

No public host execution, filesystem access, browser control, arbitrary provider calls, or secret-bearing tools exist in this starter. Adding one later requires an explicit authorization model, allowlist, user-scoped isolation, misuse analysis, and tests. **Do not point this example at the maintainer's live private Bridge.**

## Security checks before internet exposure

- **Treat the HTTP edge as an untrusted internet-facing API.** Auth0 is mandatory, not a substitute for perimeter protection. The MCP audience must **exactly equal** the public `CLOUD_MCP_RESOURCE_URL`; the starter now refuses mismatches. JWT checks run in a worker thread with a five-second JWKS fetch timeout.
- **Restrict ingress.** Only expose `/cloud/mcp` plus the two `/.well-known/oauth-protected-resource*` discovery endpoints. Never proxy the private Bridge port or the wider Overseer daemon. Keep Uvicorn bound to loopback, use TLS, and avoid logging Authorization headers, bearer tokens, query strings containing credentials, or sensitive MCP tool inputs.
- **Rate-limit at the public edge before production use.** If your hostname uses a Cloudflare-managed zone, configure a rate-limiting rule for the MCP path; start in log/monitor mode, observe legitimate traffic and tune the threshold before blocking. Verify both an ordinary OAuth request and a burst of unauthenticated traffic. Avoid JavaScript challenges or interstitial login pages on MCP or OAuth discovery: machine clients need API responses, not browser puzzles. Cloudflare **Quick Tunnels do not imply that you control a zone/WAF**. If you expose the service directly through Caddy, the example Caddyfile **does not provide rate limiting**: arrange a suitable reverse-proxy, firewall or upstream limit. Check your provider's available features before relying on them.
- **Do not bypass cryptographic checks at the edge.** Cloudflare Access, a tunnel, a Cloudflare rule or a successful Auth0 dashboard login is not an MCP authorization decision. Reject incorrect JWT issuer, audience, subject, client, signature and expiry in Python, even if the edge allows the request through.
- **Verify DNS/TLS and rate policies independently.** Check a real public HTTPS request, the exact OAuth resource metadata, anonymous 401s, token-based discovery and a real ChatGPT tool call. Run the smoke tests again after changing tunneling, proxy headers, OAuth grants or edge rules. The example is not a certified production deployment.

## Agent handoff prompt

Paste this into a coding agent with access to your downloaded repository:

```text
You are my setup and learning assistant for the public Overseer Hub Starter.
Read overseer-hub-starter/README.md, ARCHITECTURE.md, server.py,
cloud_auth.py, .env.example and tests/test_starter.py before making changes.

My goal is to understand and deploy my OWN read-only MCP server using my
OWN Auth0 tenant and my OWN public HTTPS hostname, then connect it to
my ChatGPT account if that account supports custom MCP servers.

First inspect my OS, available Python and hosting environment, and
the ChatGPT feature/permission constraints. Explain the architecture
in plain language and show the exact testable steps. Before installs,
signups, billing, DNS/firewall changes, account/OAuth configuration,
external exposure, or publication: tell me the specific changes,
costs/permissions, and security consequences; request my approval.

Do not use the maintainer's credentials, tenant, API accounts, private Bridge,
browser profiles or live infrastructure. Do not ask me to paste secrets
into this chat, Git, scripts or logs. If you encounter an MFA/passkey
or payment step, have me perform it in the provider's secure interface.

Perform approved steps using my tools. Run local tests and then check
the real deployed URL and real ChatGPT plugin call. Return actual
commands/results, unresolved blockers, and what remains unverified.
Never claim the production Overseer Hub was installed.
```

## Related official references

- [ChatGPT custom MCP connections](https://help.openai.com/en/articles/12584461-connecting-custom-mcp-servers-in-chatgpt)
- [OpenAI MCP authentication](https://developers.openai.com/plugins/build/auth)
- [Auth0 pricing and Free tier](https://auth0.com/pricing)
- [Cloudflare Tunnel documentation](https://developers.cloudflare.com/tunnel/get-started/)
- [Caddy HTTPS quick start](https://caddyserver.com/docs/quick-starts/https)

This project is an educational reference and must be security reviewed before exposure to unrelated users or privileged tools.
