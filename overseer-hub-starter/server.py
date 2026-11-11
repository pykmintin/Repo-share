"""Portable, read-only MCP gateway based on Overseer's cloud auth boundary.

This is a teaching starter, not the production Overseer Bridge.
No host execution, browser access, Google tokens, or secret-bearing operations.
"""
from contextlib import asynccontextmanager
from hashlib import sha256
from urllib.parse import urlsplit

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from mcp.server.mcpserver import MCPServer
from mcp.server.streamable_http_manager import TransportSecuritySettings
from mcp.types import ToolAnnotations
from starlette.concurrency import run_in_threadpool

from cloud_auth import CloudAuthSettings, CloudTokenVerifier, unauthorized_header

PROTECTED_PATH = "/cloud/mcp"
METADATA_PATHS = {
    "/.well-known/oauth-protected-resource",
    "/.well-known/oauth-protected-resource/cloud/mcp",
}
READ_ONLY = ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=False)


def create_app(settings: CloudAuthSettings | None = None,
               verifier: CloudTokenVerifier | None = None) -> FastAPI:
    settings = settings or CloudAuthSettings.from_env()
    verifier = verifier or CloudTokenVerifier(settings)
    mcp = MCPServer(
        "overseer-hub-starter",
        description="Educational authenticated MCP gateway; read-only demo tools",
    )

    @mcp.tool(
        name="get_profile",
        description="Return an opaque profile ID based on the authorized Auth0 subject",
        annotations=READ_ONLY,
        meta={"openai/profile": True},
    )
    def get_profile() -> dict[str, str]:
        identity = sha256(f"{settings.issuer}\0{settings.subject}".encode()).hexdigest()[:32]
        return {"id": "prf_" + identity}

    @mcp.tool(
        name="fabric_read",
        description="Discover the one safe demonstration backend",
        annotations=READ_ONLY,
    )
    def fabric_read(tool: str = "") -> dict:
        if tool and tool != "echo":
            return {"ok": False, "error": "unknown backend"}
        return {
            "ok": True,
            "allowed_tools": ["echo"],
            "schema": {"echo": {"message": "string, maximum 1024 characters"}},
        }

    @mcp.tool(
        name="fabric_call",
        description="Execute the allowlisted read-only echo demonstration",
        annotations=READ_ONLY,
    )
    def fabric_call(tool: str, args: dict, maxChars: int = 4000) -> dict:
        if tool != "echo":
            return {"ok": False, "error": "unknown backend"}
        message = args.get("message")
        if not isinstance(message, str) or len(message) > 1024 or not 256 <= maxChars <= 16000:
            return {"ok": False, "error": "invalid input"}
        return {"ok": True, "tool": "echo", "output": message}

    host = urlsplit(settings.resource_url).netloc if settings.resource_url else ""
    mcp_app = mcp.streamable_http_app(
        streamable_http_path=PROTECTED_PATH,
        stateless_http=True,
        json_response=True,
        transport_security=TransportSecuritySettings(
            enable_dns_rebinding_protection=True,
            allowed_hosts=[host] if host else ["localhost:*", "127.0.0.1:*"],
            allowed_origins=[settings.resource_url.removesuffix(PROTECTED_PATH)] if host else [],
        ),
    )

    @asynccontextmanager
    async def lifespan(_app):
        async with mcp_app.router.lifespan_context(mcp_app):
            yield

    app = FastAPI(
        title="Overseer Hub Starter",
        docs_url=None, redoc_url=None, openapi_url=None,
        lifespan=lifespan,
    )

    @app.middleware("http")
    async def oauth_guard(request: Request, call_next):
        p = request.url.path
        if p in METADATA_PATHS:
            if not settings.ready:
                return JSONResponse({"error": "not configured"}, status_code=503)
            return await call_next(request)
        if p != PROTECTED_PATH:
            return JSONResponse({"error": "not found"}, status_code=404)
        if not settings.ready:
            return JSONResponse({"error": "not configured"}, status_code=503)
        try:
            selected = verifier.for_request(
                request.headers.get("host", ""), request.headers.get("origin"),
            )
            await run_in_threadpool(selected.verify, request.headers.get("authorization", ""))
        except (ValueError, RuntimeError):
            return JSONResponse(
                {"error": "unauthorized"}, status_code=401,
                headers={"WWW-Authenticate": unauthorized_header(settings.resource_url)},
            )
        return await call_next(request)

    @app.get("/.well-known/oauth-protected-resource")
    @app.get("/.well-known/oauth-protected-resource/cloud/mcp")
    async def resource_metadata():
        return settings.resource_metadata()

    app.mount("/", mcp_app)
    return app


app = create_app()
