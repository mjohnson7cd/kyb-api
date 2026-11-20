# RapidAPI Listing Guide

## 1. Prerequisites

- [x] API running on a public URL (Render deployment)
- [x] OpenAPI spec generated (`openapi.json`)
- [x] RapidAPI proxy secret configured in environment

## 2. Create RapidAPI Provider Account

1. Go to [rapidapi.com/developer](https://rapidapi.com/developer)
2. Sign up or log in
3. Navigate to "My APIs" → "Add New API"

## 3. Configure API Settings

### Basic Information
- **API Name**: European Company Registry & KYB API
- **Category**: Data / Business
- **Short Description**: "Company lookup in official EU registries: France, Norway, Finland, Czechia. No scraping."
- **Full Description**: (use from README.md)
- **Tags**: kyb, company-data, business-verification, compliance, due-diligence, registry, europe

### Base URL
- **Production URL**: `https://your-app.onrender.com`
- Replace with your actual Render URL after deployment

### Authentication
1. Select "API Key" authentication
2. Header name: `X-RapidAPI-Proxy-Secret`
3. RapidAPI will generate a secret — **copy this value**
4. Add it to your Render environment variables as `RAPIDAPI_PROXY_SECRET`

## 4. Upload OpenAPI Spec

1. In the RapidAPI dashboard, go to "Endpoints" tab
2. Click "Import" → "OpenAPI/Swagger"
3. Upload the `openapi.json` file from this repo
4. Review and confirm the imported endpoints

## 5. Test Endpoints

Before going live, test each endpoint:

### Test: Batch Lookup
```bash
curl -X POST "https://your-app.onrender.com/kyb/lookup" \
  -H "X-RapidAPI-Proxy-Secret: YOUR_SECRET" \
  -H "Content-Type: application/json" \
  -d '{
    "search_terms": ["Nokia", "552032534"],
    "countries": ["FI", "FR"],
    "max_results_per_query": 3,
    "validate_vat": true,
    "lookup_lei": true
  }'
```

### Test: Single Company
```bash
curl "https://your-app.onrender.com/kyb/company/FR/552032534?validate_vat=true&lookup_lei=true" \
  -H "X-RapidAPI-Proxy-Secret: YOUR_SECRET"
```

## 6. Pricing Configuration

Suggested pricing based on competitor research (B2BHint at $69.99 for similar data):

### Pricing Tiers

| Tier | Quota | Price | Target |
|---|---|---|---|
| **Basic** | 100 requests/month | $9.99 | Hobbyists, testing |
| **Pro** | 1,000 requests/month | $49.99 | Small businesses |
| **Business** | 5,000 requests/month | $199.99 | Mid-size companies |
| **Enterprise** | 25,000 requests/month | $799.99 | Large-scale integrations |

### Pricing Events
- Bill per successful company record returned (not per query)
- No charge for queries that return no match
- Enrichments (VAT check, LEI lookup) included in base price

**Your economics at $49.99/mo (Pro tier):**
- RapidAPI takes 25% = $12.50
- You receive 75% = $37.49
- Marginal cost: ~$0 (government APIs are free)
- Net profit: **$37.49/mo per Pro subscriber**

## 7. Marketing Copy

### Tagline
"Instant company verification from official EU registries. No scraping, no downtime."

### Key Differentiators
- ✅ **Official sources only** — direct from government APIs
- ✅ **Never breaks** — no HTML parsing, no site redesigns to track
- ✅ **Full audit trail** — every field includes source URL
- ✅ **GDPR compliant** — respects INSEE commercial use flags
- ✅ **Multi-country** — France, Norway, Finland, Czechia in one call

### Use Cases
- KYB / compliance checks
- Lead enrichment
- CRM data validation
- Financial due diligence
- Procurement verification
- Market research

## 8. Go Live Checklist

- [ ] Render deployment confirmed running
- [ ] `RAPIDAPI_PROXY_SECRET` set in Render env vars
- [ ] OpenAPI spec uploaded to RapidAPI
- [ ] All endpoints tested successfully
- [ ] Pricing tiers configured
- [ ] API description and docs filled in
- [ ] Category and tags set
- [ ] API set to "Public" (or "Private" for soft launch)

## 9. Post-Launch

### Monitor
- RapidAPI dashboard for usage metrics
- Render logs for errors
- Apify actor usage (stays within your plan limits)

### Support
- Respond to API questions in RapidAPI forums
- Update docs based on user feedback
- Monitor VIES/GLEIF uptime (rare downtime, but log when it happens)

### Growth
- Link from your GitHub profile
- Tweet about it with #KYB #API
- Add to Product Hunt / Indie Hackers
- Consider writing a blog post: "Why we built a no-scraping KYB API"

## 10. Expected Revenue Timeline

- **Month 1–2**: $0–50 (discovery phase)
- **Month 3–6**: $50–300 (early adopters, mostly Basic tier)
- **Month 6–12**: $300–1,000 (Pro tier conversions)
- **Month 12+**: $1,000+ (Enterprise traction if SEO/marketing scales)

RapidAPI median earning API: ~$200/mo. Top 20% clear $1,000+/mo. Price is the lever: APIs priced >$20/mo earn 10× more than <$5/mo with similar traffic.

## Troubleshooting

### "Unauthorized" errors
- Verify `RAPIDAPI_PROXY_SECRET` matches between Render and RapidAPI
- Check that the secret isn't expired (RapidAPI rotates these on API updates)

### "Actor execution failed"
- Check Apify actor is published and not archived
- Verify `APIFY_API_TOKEN` has sufficient permissions
- Check Apify usage limits (Free: 5 actors, $5 usage/mo)

### Slow responses
- First run is cold start (~2–5s for Apify actor spin-up)
- Registry APIs are fast but Norway's can hit 3–5s
- Consider caching results for 24h (requires Redis/DB, not in v1)
