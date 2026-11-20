"""KYB API — FastAPI application entry point."""

import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.middleware.auth import APIKeyMiddleware
from app.routes.kyb import router as kyb_router

# ── Rate limiter ────────────────────────────────────────────────────────────

limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])

# ── App ──────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="European Company Registry & KYB API",
    description=(
        "Resolve company names or national registry IDs into clean, normalized records "
        "pulled **directly from official government registries** across Europe. "
        "Covers France (INSEE/RNE), Norway (Brønnøysund), Finland (PRH/YTJ), "
        "and Czechia (ARES), plus EU VAT validation (VIES) and LEI lookup (GLEIF). "
        "Authenticate via `X-API-Key` or `X-RapidAPI-Proxy-Secret` header."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ── CORS ─────────────────────────────────────────────────────────────────────

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Auth middleware ─────────────────────────────────────────────────────────

app.add_middleware(APIKeyMiddleware)

# ── Routes ──────────────────────────────────────────────────────────────────

app.include_router(kyb_router)


# ── Health check ─────────────────────────────────────────────────────────────

@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok", "service": "kyb-api", "version": "1.0.0"}


# ── Root ─────────────────────────────────────────────────────────────────────

@app.get("/", tags=["System"])
async def root():
    return {
        "service": "European Company Registry & KYB API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "batch_lookup": "POST /kyb/lookup",
            "single_lookup": "GET /kyb/company/{country}/{id}",
        },
    }
