"""API key authentication middleware for RapidAPI and custom key support."""

import os
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

# Comma-separated valid keys from env
VALID_API_KEYS = {k.strip() for k in os.getenv("API_KEYS", "").split(",") if k.strip()}
RAPIDAPI_PROXY_SECRET = os.getenv("RAPIDAPI_PROXY_SECRET", "")


class APIKeyMiddleware(BaseHTTPMiddleware):
    """
    Authenticates requests via:
      1. X-RapidAPI-Proxy-Secret header (set by RapidAPI when proxying)
      2. X-API-Key header (custom key for direct access)
    Skips auth for /docs, /openapi.json, /health, and OPTIONS requests.
    """

    PUBLIC_PATHS = {"/docs", "/openapi.json", "/redoc", "/health", "/"}

    async def dispatch(self, request: Request, call_next):
        # Allow preflight
        if request.method == "OPTIONS":
            return await call_next(request)

        path = request.url.path
        if path in self.PUBLIC_PATHS or path.startswith("/docs"):
            return await call_next(request)

        # If no keys configured, allow all (dev mode)
        if not VALID_API_KEYS and not RAPIDAPI_PROXY_SECRET:
            return await call_next(request)

        rapid_secret = request.headers.get("X-RapidAPI-Proxy-Secret", "")
        api_key = request.headers.get("X-API-Key", "")

        # Check RapidAPI proxy secret
        if RAPIDAPI_PROXY_SECRET and rapid_secret == RAPIDAPI_PROXY_SECRET:
            return await call_next(request)

        # Check custom API key
        if VALID_API_KEYS and api_key in VALID_API_KEYS:
            return await call_next(request)

        return JSONResponse(
            status_code=401,
            content={"error": "Unauthorized. Provide X-API-Key or X-RapidAPI-Proxy-Secret header."},
        )
