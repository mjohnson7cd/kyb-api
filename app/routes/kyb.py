"""KYB (Know Your Business) lookup routes."""

import os
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from apify_client import ApifyClient

router = APIRouter(prefix="/kyb", tags=["KYB Lookup"])

# Apify client
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
if not APIFY_API_TOKEN:
    raise ValueError("APIFY_API_TOKEN environment variable is required")

apify_client = ApifyClient(APIFY_API_TOKEN)

# Apify actor ID
ACTOR_ID = "mjohnson7cd/eu-company-registry-kyb"


# ── Request/Response Models ──────────────────────────────────────────────────


class LookupRequest(BaseModel):
    """Batch company lookup request."""

    search_terms: List[str] = Field(
        ...,
        description="Company names or national registry IDs",
        examples=[["Danone", "Equinor", "0112038-9", "04788290"]],
    )
    countries: Optional[List[str]] = Field(
        None,
        description="ISO 3166-1 alpha-2 country codes (FR, NO, FI, CZ). If omitted, searches all.",
        examples=[["FR", "NO", "FI", "CZ"]],
    )
    max_results_per_query: int = Field(
        5, ge=1, le=20, description="Maximum results per search term (1-20)"
    )
    validate_vat: bool = Field(True, description="Check VAT numbers via EU VIES")
    lookup_lei: bool = Field(True, description="Fetch LEI (Legal Entity Identifier) from GLEIF")


class Address(BaseModel):
    """Company address."""

    street: Optional[str] = None
    postal_code: Optional[str] = None
    city: Optional[str] = None
    country_code: Optional[str] = None
    formatted: Optional[str] = None


class IndustryCode(BaseModel):
    """Industry classification code."""

    scheme: str
    code: str
    description: Optional[str] = None


class Financials(BaseModel):
    """Financial data (France only)."""

    year: int
    revenue: Optional[float] = None
    net_income: Optional[float] = None
    currency: str = "EUR"


class CompanyRecord(BaseModel):
    """Normalized company record."""

    query: str
    matched: bool
    country: Optional[str] = None
    company_id: Optional[str] = None
    company_id_type: Optional[str] = None
    legal_name: Optional[str] = None
    previous_names: Optional[List[str]] = None
    status: Optional[str] = None
    legal_form: Optional[str] = None
    registration_date: Optional[str] = None
    address: Optional[Address] = None
    industry_codes: Optional[List[IndustryCode]] = None
    employee_range: Optional[str] = None
    financials: Optional[Financials] = None
    vat_number: Optional[str] = None
    vat_valid: Optional[bool] = None
    lei: Optional[str] = None
    lei_status: Optional[str] = None
    source: Optional[str] = None
    source_url: Optional[str] = None
    error: Optional[str] = None


class LookupResponse(BaseModel):
    """Batch lookup response."""

    results: List[CompanyRecord]
    total_matches: int
    total_queries: int


# ── Routes ───────────────────────────────────────────────────────────────────


@router.post("/lookup", response_model=LookupResponse)
async def batch_lookup(request: LookupRequest):
    """
    Batch company lookup by name or national registry ID.

    Fetches data directly from official government registries across Europe:
    - France: INSEE / RNE (SIREN)
    - Norway: Brønnøysund (Org.nr)
    - Finland: PRH / YTJ (Y-tunnus)
    - Czechia: ARES (IČO)

    Plus EU VAT validation (VIES) and LEI lookup (GLEIF).
    """
    try:
        # Prepare Apify actor input
        actor_input = {
            "searchTerms": request.search_terms,
            "maxResultsPerQuery": request.max_results_per_query,
            "validateVat": request.validate_vat,
            "lookupLei": request.lookup_lei,
        }
        if request.countries:
            actor_input["countries"] = request.countries

        # Run the actor and wait for results
        run = apify_client.actor(ACTOR_ID).call(run_input=actor_input)

        # Fetch results from dataset
        results = []
        for item in apify_client.dataset(run["defaultDatasetId"]).iterate_items():
            results.append(CompanyRecord(**item))

        return LookupResponse(
            results=results,
            total_matches=sum(1 for r in results if r.matched),
            total_queries=len(request.search_terms),
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Actor execution failed: {str(e)}")


@router.get("/company/{country}/{company_id}", response_model=CompanyRecord)
async def single_lookup(
    country: str,
    company_id: str,
    validate_vat: bool = Query(True, description="Check VAT number via EU VIES"),
    lookup_lei: bool = Query(True, description="Fetch LEI from GLEIF"),
):
    """
    Lookup a single company by country and national registry ID.

    Example:
    - GET /kyb/company/FR/552032534  (Danone)
    - GET /kyb/company/NO/916385699  (Equinor)
    - GET /kyb/company/FI/0112038-9  (Nokia)
    """
    try:
        actor_input = {
            "searchTerms": [company_id],
            "countries": [country.upper()],
            "maxResultsPerQuery": 1,
            "validateVat": validate_vat,
            "lookupLei": lookup_lei,
        }

        run = apify_client.actor(ACTOR_ID).call(run_input=actor_input)

        # Get first result
        for item in apify_client.dataset(run["defaultDatasetId"]).iterate_items():
            return CompanyRecord(**item)

        raise HTTPException(status_code=404, detail="Company not found")

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Actor execution failed: {str(e)}")
