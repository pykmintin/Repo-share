# How the starter maps to Overseer Hub

This document describes **architecture**, not a deployment of the maintainer's private source. The production source was inspected on 11 November 2026 in `Overseer/services/mcp_manager/`.

## Actual Overseer topology

```text
ChatGPT custom MCP plugin
   │ OAuth2 authorization-code / PKCE with Auth0
   ▼
Public HTTPS hostname (Cloudflare ingress)
   │ only /cloud/mcp and OAuth resource metadata
   ▼
Restricted loopback ingress (cloud_ingress.py, port 7701)
   │ forwards selected headers; never points public traffic to Bridge directly
   ▼
Private Bridge MCP process (main.py, loopback port 7700)
   │ cloud_auth.py: JWT signature / issuer / audience / subject / client guard
   │ cloud_facade.py: MCP tool contract and trusted owner context
   ▼
Cloud Fabric (cloud_fabric.py)
   │ explicit backend allowlist, bounded results and batch semantics
   ▼
Internal Router / provider registry / private tools
```

The full Overseer deployment also includes a separate daemon, browser/session system, host tools, permissions and secrets held only on the maintainer's machines. Merely cloning the source would not reproduce those services.

## Public starter topology

```text
Your ChatGPT → your Auth0 (authorizes client and user)
      │
      ▼
Your public HTTPS host /cloud/mcp
      │ Caddy (or an approved tunnel to the loopback app)
      ▼
server.py on 127.0.0.1:7701
      │ cloud_auth.py validates each access token
      │ MCPServer exposes get_profile, fabric_read, fabric_call
      ▼
Allowlisted echo-only demonstration (no network/provider/OS effects)
```

**Fidelity:** `cloud_auth.py` is an unmodified copy of the canonical production JWT verifier. `server.py` is a small v2-SDK teaching implementation of the same *boundary pattern*, **not** a byte-for-byte production facade. It combines TLS ingress and MCP routing to reduce installation dependencies, and replaces the private Router with a single safe demonstration backend. Its public tool names are representative, but not full production capabilities.

## Trust boundaries

1. **HTTPS/TLS** authenticates the public hostname and encrypts traffic. A free DNS name does not provide a running server or TLS by itself.
2. **Auth0** authenticates a user and issues an **access token for this specific MCP API audience**. ChatGPT is a client; OAuth client registration and callbacks belong to that client, not to the backend's API code.
3. **`cloud_auth.py`** independently verifies RS256 signature/JWKS, expiry, issuer, exact audience, allowed subject and authorized client (`azp`). Absence of configuration fails closed; the production file also checks Host and Origin against the configured resource URL.
4. **MCP boundary** exposes only three read-only tools. `fabric_call` is **not** a remote code runner; it accepts only `echo`. Its bounds are independently checked.
5. **No private bridge trust is inherited.** An authenticated connection is not authorization to execute arbitrary commands, use unrelated accounts or forward tools into an owner's computer.

The token verifier rejects mismatches between the configured OAuth audience and public resource URL. Signing-key retrieval uses a bounded timeout and executes outside the HTTP event loop. Edge rate limits are deployment-specific and **not** provided by the Python starter.

## Source provenance

Maintained implementation locations used for this educational adaptation:
- `Overseer/services/mcp_manager/cloud_auth.py` → this package's `cloud_auth.py`, exact contents.
- `Overseer/services/mcp_manager/cloud_ingress.py` → concept of a path-restricted public ingress; excluded here as a separate service.
- `Overseer/services/mcp_manager/cloud_facade.py` → real MCP tool schema / identity design; replaced by standalone MCP v2 tool declarations.
- `Overseer/services/mcp_manager/cloud_fabric.py` and `router.py` → real provider dispatch; **not public** in this starter.
- `Overseer/services/mcp_manager/main.py` → real private Bridge process; **not public** in this starter.

These project paths describe architecture only; they are not part of the public repository and do not imply that a new user has permission to access the maintainer's private worktree.

## Testing and expected behavior

`python -m pytest -q tests/test_starter.py` checks real locally signed RS256 claims and the actual MCP HTTP endpoint. No external Auth0 tenant, network, hosting service or ChatGPT account is contacted during these tests. A real deploy must pass separate **public HTTPS → Auth0 consent → ChatGPT tool call** acceptance.

The starter deliberately does not include Auth0 client registration automation, DNS mutation, installer scripts, a background daemon, or infrastructure-as-code; the accompanying setup agent should inspect the user's own target machine and ask approval before creating those resources.
