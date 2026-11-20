# European Company Registry & KYB API 🏛️

A FastAPI-based KYB (Know Your Business) lookup service that fetches company data **directly from official government registries** across Europe — designed for deployment on **Render** and listing on **RapidAPI** marketplace.

## Features

Resolve a company name or national registry ID into clean, normalized records from:

- 🇫🇷 **France** — INSEE / RNE (SIREN) with revenue, net income, officers
- 🇳🇴 **Norway** — Brønnøysund (Org.nr) with employee count, website, bankruptcy flag
- 🇫🇮 **Finland** — PRH / YTJ (Y-tunnus) with trade names, former names
- 🇨🇿 **Czechia** — ARES (IČO) with VAT direct from registry

Plus EU VAT validation (VIES) and LEI lookup (GLEIF) for every country.

## Endpoints

| Endpoint | Description |
|---|---|
| `POST /kyb/lookup` | Batch company lookup (names or IDs) |
| `GET /kyb/company/{country}/{id}` | Single company by national ID |
| `GET /health` | Health check |

## Authentication

Provide one of these headers:
- `X-API-Key: ***` — custom key
- `X-RapidAPI-Proxy-Secret: your-secret` — set by RapidAPI proxy

Set keys via the `API_KEYS` and `RAPIDAPI_PROXY_SECRET` environment variables.

## Quick Start (Local)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Set your Apify API token
export APIFY_API_TOKEN=your_token_here

# No auth in dev mode (leave API_KEYS empty)
uvicorn app.main:app --reload --port 10000
```

Open http://localhost:10000/docs for interactive API docs.

## Deploy to Render

1. Push this repo to GitHub
2. Go to [render.com](https://render.com) → New → Web Service
3. Connect your repo
4. Render auto-detects `render.yaml` — or set:
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add env vars:
   - `APIFY_API_TOKEN` (required)
   - `API_KEYS` (optional, comma-separated)
   - `RAPIDAPI_PROXY_SECRET` (required for RapidAPI)

## List on RapidAPI

1. Create a RapidAPI Provider account at [rapidapi.com/developer](https://rapidapi.com/developer)
2. Add your Render URL as the backend
3. Upload the OpenAPI spec from `/openapi.json`
4. Set `X-RapidAPI-Proxy-Secret` in your Render env vars (use the value RapidAPI provides)
5. Define pricing tiers (suggested: $20–50 per 1,000 results)
6. Publish!

## Pricing & Economics

- **Marginal cost**: Near zero (government APIs are free)
- **RapidAPI fee**: 25% (you keep 75%)
- **Payout**: PayPal, end of following month (~45–60 day lag)
- **Competitive pricing**: B2BHint charges $69.99 for similar data

## Data Sources

- France: [recherche-entreprises.api.gouv.fr](https://recherche-entreprises.api.gouv.fr/)
- Norway: [data.brreg.no](https://data.brreg.no/enhetsregisteret/api/docs/index.html)
- Finland: [avoindata.prh.fi](https://avoindata.prh.fi/ytj_en.html)
- Czechia: [ares.gov.cz](https://ares.gov.cz/)
- EU VAT: [ec.europa.eu/vies](https://ec.europa.eu/taxation_customs/vies/)
- LEI: [gleif.org](https://www.gleif.org/en/lei-data/gleif-api)

## Tech Stack

- **Python 3.11+** / **FastAPI** / **uvicorn**
- **httpx** — async HTTP client
- **slowapi** — rate limiting
- **Apify API** — runs the company registry actor
- **Docker** ready

## Legal Notes

This API provides **access to data**, not stored datasets. Results are fetched on-demand from government registries for each request. No bulk retention or redistribution. Complies with GDPR by suppressing French officers when `opposition_diffusion_commerciale` is set.
