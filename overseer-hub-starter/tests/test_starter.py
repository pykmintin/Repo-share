"""Contract tests for the public read-only Hub example (no live Auth0 or network)."""
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import jwt
import pytest
from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cloud_auth import CloudAuthSettings, CloudTokenVerifier
from server import create_app


def settings():
    return CloudAuthSettings(
        issuer="https://tenant.example.auth0.com/",
        audience="https://hub.example.test/cloud/mcp",
        subject="auth0|cousin",
        jwks_uri="https://tenant.example.auth0.com/.well-known/jwks.json",
        resource_url="https://hub.example.test/cloud/mcp",
        allowed_clients=("chatgpt-app-id",),
    )


def signed_token(overrides=None):
    key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    claims = {
        "iss": settings().issuer,
        "aud": settings().audience,
        "sub": settings().subject,
        "azp": "chatgpt-app-id",
        "iat": int(time.time()),
        "exp": int(time.time()) + 3600,
    }
    claims.update(overrides or {})
    token = jwt.encode(claims, key, algorithm="RS256", headers={"kid": "test"})
    verifier = CloudTokenVerifier(settings())
    verifier._keys = SimpleNamespace(
        get_signing_key_from_jwt=lambda t: SimpleNamespace(key=key.public_key())
    )
    return token, verifier


def test_audience_must_equal_resource():
    wrong = CloudAuthSettings(
        issuer="https://tenant.example.auth0.com/",
        audience="https://another-api.example.test/cloud/mcp",
        subject="auth0|cousin",
        jwks_uri="https://tenant.example.auth0.com/.well-known/jwks.json",
        resource_url="https://hub.example.test/cloud/mcp",
        allowed_clients=("chatgpt-app-id",),
    )
    assert not wrong.ready
    with pytest.raises(RuntimeError):
        CloudTokenVerifier(wrong).verify("Bearer anything")


def test_configuration_fails_closed():
    empty = CloudAuthSettings("", "", "", "", "")
    assert not empty.ready
    with pytest.raises(RuntimeError):
        CloudTokenVerifier(empty).verify("Bearer anything")


def test_reject_wrong_subject_client_and_audience():
    for claim in [
        {"sub": "someone-else"},
        {"azp": "unregistered-client"},
        {"aud": "https://wrong.example/cloud/mcp"},
    ]:
        token, verifier = signed_token(claim)
        with pytest.raises(ValueError):
            verifier.verify("Bearer " + token)


def test_valid_token_and_missing_bearer():
    token, verifier = signed_token()
    assert verifier.verify("Bearer " + token)["sub"] == "auth0|cousin"
    with pytest.raises(ValueError):
        verifier.verify(token)


def test_public_metadata_and_unauthorized_mcp():
    with TestClient(create_app(settings()), base_url="https://hub.example.test") as client:
        meta = client.get("/.well-known/oauth-protected-resource")
        assert meta.status_code == 200
        assert meta.json()["authorization_servers"] == [settings().issuer]
        denied = client.post("/cloud/mcp", json={"jsonrpc": "2.0", "id": 1, "method": "tools/list"})
        assert denied.status_code == 401
        assert "resource_metadata=" in denied.headers.get("www-authenticate", "")


def test_valid_mcp_tool_discovery():
    token, verifier = signed_token()
    app = create_app(settings(), verifier=verifier)
    headers = {
        "authorization": "Bearer " + token,
        "accept": "application/json, text/event-stream",
        "content-type": "application/json",
        "mcp-protocol-version": "2025-06-18",
    }
    with TestClient(app, base_url="https://hub.example.test") as client:
        req = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-06-18",
                "capabilities": {},
                "clientInfo": {"name": "contract-test", "version": "1"},
            },
        }
        init = client.post("/cloud/mcp", headers=headers, json=req)
        assert init.status_code == 200, init.text
        result = client.post(
            "/cloud/mcp", headers=headers,
            json={"jsonrpc": "2.0", "id": 2, "method": "tools/list"},
        )
        assert result.status_code == 200, result.text
        names = {x["name"] for x in result.json()["result"]["tools"]}
        assert {"get_profile", "fabric_read", "fabric_call"} <= names
        call = client.post(
            "/cloud/mcp", headers=headers,
            json={"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                  "params": {"name": "fabric_call", "arguments": {
                      "tool": "echo", "args": {"message": "hello"}}}},
        )
        assert call.status_code == 200, call.text
        assert "hello" in call.text
        refused = client.post(
            "/cloud/mcp", headers=headers,
            json={"jsonrpc": "2.0", "id": 4, "method": "tools/call",
                  "params": {"name": "fabric_call", "arguments": {
                      "tool": "host_execute", "args": {"command": "whoami"}}}},
        )
        assert refused.status_code == 200, refused.text
        assert "unknown backend" in refused.text


def test_wrong_host_cannot_reach_mcp():
    token, verifier = signed_token()
    with TestClient(create_app(settings(), verifier=verifier), base_url="https://evil.example.test") as client:
        result = client.post("/cloud/mcp", headers={"authorization": "Bearer " + token}, json={})
        assert result.status_code in (401, 403)


def test_unconfigured_app_refuses_public_access():
    blank = CloudAuthSettings("", "", "", "", "")
    with TestClient(create_app(blank), base_url="https://hub.example.test") as client:
        assert client.get("/.well-known/oauth-protected-resource").status_code == 503
        assert client.post("/cloud/mcp", json={}).status_code == 503


def test_token_check_runs_off_async_event_loop():
    import asyncio
    import threading
    import httpx

    token, verifier = signed_token()
    seen_threads = []
    original_verify = verifier.verify

    def tracked_verify(header):
        seen_threads.append(threading.get_ident())
        return original_verify(header)

    verifier.verify = tracked_verify
    app = create_app(settings(), verifier=verifier)

    async def request():
        async with app.router.lifespan_context(app):
            async with httpx.AsyncClient(
                transport=httpx.ASGITransport(app=app),
                base_url="https://hub.example.test",
            ) as client:
                event_loop_thread = threading.get_ident()
                response = await client.post(
                    "/cloud/mcp",
                    headers={"authorization": "Bearer " + token},
                    json={"jsonrpc": "2.0", "id": 1, "method": "ping"},
                )
                assert response.status_code != 401
                return event_loop_thread

    event_loop_thread = asyncio.run(request())
    assert seen_threads and all(t != event_loop_thread for t in seen_threads)
