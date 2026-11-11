"""Owner-only cloud MCP authentication; fail closed until configured.

Auth0/another OIDC issuer may use Google as upstream login. Access *tokens*
must be issued for this MCP resource; Google login ID tokens are not accepted.
"""
import os
from dataclasses import dataclass, replace
from urllib.parse import urlsplit

import jwt
from jwt import PyJWKClient


@dataclass(frozen=True)
class CloudAuthSettings:
    issuer: str
    audience: str
    subject: str
    jwks_uri: str
    resource_url: str
    # Explicitly registered OAuth clients; no other Auth0 app is authorized.
    allowed_clients: tuple[str, ...] = ()
    additional_resource_urls: tuple[str, ...] = ()

    @classmethod
    def from_env(cls):
        issuer, audience, subject, jwks_uri, resource_url = (
            os.environ.get(name, "").strip() for name in (
                "CLOUD_MCP_ISSUER", "CLOUD_MCP_AUDIENCE",
                "CLOUD_MCP_SUBJECT", "CLOUD_MCP_JWKS_URI",
                "CLOUD_MCP_RESOURCE_URL",
            )
        )
        settings = cls(
            issuer=issuer, audience=audience, subject=subject,
            jwks_uri=jwks_uri, resource_url=resource_url,
            allowed_clients=tuple(x.strip() for x in os.environ.get(
                "CLOUD_MCP_ALLOWED_CLIENTS", "").split(",") if x.strip()),
            additional_resource_urls=tuple(x.strip() for x in os.environ.get(
                "CLOUD_MCP_ADDITIONAL_RESOURCE_URLS", "").split(",") if x.strip()),
        )
        settings.resources()
        return settings

    def resources(self):
        result = {}
        if not self.resource_url and not self.additional_resource_urls:
            return result
        for index, url in enumerate((self.resource_url, *self.additional_resource_urls)):
            parsed = urlsplit(url)
            if (parsed.scheme != "https" or not parsed.netloc
                    or parsed.hostname != parsed.netloc or parsed.port is not None
                    or parsed.path != "/cloud/mcp" or parsed.query or parsed.fragment):
                raise ValueError("invalid cloud resource URL")
            if parsed.netloc in result:
                raise ValueError("duplicate cloud resource host")
            result[parsed.netloc] = self if index == 0 else replace(
                self, resource_url=url, audience=url, additional_resource_urls=())
        return result

    @property
    def ready(self):
        return bool(
            all((self.issuer, self.audience, self.subject, self.jwks_uri,
                 self.resource_url, self.allowed_clients))
            and self.audience == self.resource_url
            and self.issuer.startswith("https://")
            and self.jwks_uri.startswith("https://")
            and self.resource_url.startswith("https://")
            and self.resource_url.endswith("/cloud/mcp")
        )

    def resource_metadata(self):
        return {
            "resource": self.resource_url,
            "authorization_servers": [self.issuer],
            "bearer_methods_supported": ["header"],
        }


class CloudTokenVerifier:
    def __init__(self, settings: CloudAuthSettings):
        self.settings = settings
        self._keys = None
        self._additional = {}

    def for_request(self, host, origin):
        settings = self.settings.resources().get(host)
        if settings is None or (origin is not None and origin !=
                                settings.resource_url.removesuffix("/cloud/mcp")):
            raise ValueError("unrecognized cloud host or origin")
        if settings is self.settings:
            return self
        if host not in self._additional:
            self._additional[host] = CloudTokenVerifier(settings)
        return self._additional[host]

    def verify(self, authorization: str):
        if not self.settings.ready:
            raise RuntimeError("cloud OAuth is not configured")
        if not authorization.startswith("Bearer "):
            raise ValueError("missing bearer token")
        token = authorization[7:]
        if not token or len(token) > 16_384:
            raise ValueError("invalid bearer token length")
        try:
            if self._keys is None:
                self._keys = PyJWKClient(self.settings.jwks_uri, cache_jwk_set=True, lifespan=300, timeout=5)
            signing_key = self._keys.get_signing_key_from_jwt(token)
            claims = jwt.decode(
                token, signing_key.key, algorithms=["RS256"],
                issuer=self.settings.issuer, audience=self.settings.audience,
                options={"require": ["exp", "iat", "iss", "aud", "sub"]},
                leeway=30,
            )
        except (jwt.PyJWTError, ValueError, OSError) as exc:
            raise ValueError("invalid access token") from exc
        if claims.get("sub") != self.settings.subject:
            raise ValueError("unauthorized account")
        if claims.get("azp") not in self.settings.allowed_clients:
            raise ValueError("unauthorized OAuth client")
        return claims


def unauthorized_header(resource_url: str):
    metadata_url = resource_url.removesuffix("/cloud/mcp") + "/.well-known/oauth-protected-resource/cloud/mcp"
    return f'Bearer resource_metadata="{metadata_url}"'
