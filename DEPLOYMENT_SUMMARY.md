# KYB API - RapidAPI Listing Summary

## ✅ Completed

### 1. API Implementation
- FastAPI service wrapping the Apify EU Company Registry actor
- RapidAPI proxy secret authentication (X-RapidAPI-Proxy-Secret header)
- Custom API key support (X-API-Key header)
- Rate limiting (60 requests/minute via slowapi)
- Two endpoints:
  - `POST /kyb/lookup` - batch company lookup
  - `GET /kyb/company/{country}/{id}` - single company by ID
- OpenAPI spec generated and ready for upload

### 2. Repository
- GitHub: https://github.com/mjohnson7cd/kyb-api
- Includes:
  - Full FastAPI application
  - Render deployment config (`render.yaml`)
  - OpenAPI spec (`openapi.json`)
  - Detailed RapidAPI listing guide (`RAPIDAPI_GUIDE.md`)
  - Environment config example (`.env.example`)

### 3. Documentation
- README with deployment instructions
- RapidAPI listing guide with pricing strategy
- Competitor pricing research (B2BHint at $69.99)

## 📋 Next Steps (2–4 hours)

### Step 1: Deploy to Render (20 min)
```bash
# 1. Go to https://render.com
# 2. New → Web Service
# 3. Connect GitHub repo: mjohnson7cd/kyb-api
# 4. Render auto-detects render.yaml
# 5. Add environment variables:
#    - APIFY_API_TOKEN: <your Apify token>
#    - RAPIDAPI_PROXY_SECRET: <leave empty for now>
# 6. Deploy
# 7. Copy the Render URL (e.g., https://kyb-api-xyz.onrender.com)
```

### Step 2: Create RapidAPI Listing (30 min)
```bash
# 1. Go to https://rapidapi.com/developer
# 2. My APIs → Add New API
# 3. Fill in:
#    - Name: European Company Registry & KYB API
#    - Category: Data / Business
#    - Base URL: <your Render URL>
#    - Description: (copy from README)
# 4. Upload openapi.json from repo
# 5. Configure authentication:
#    - Type: API Key
#    - Header: X-RapidAPI-Proxy-Secret
# 6. RapidAPI generates a secret → COPY IT
```

### Step 3: Update Render Config (5 min)
```bash
# 1. Go back to Render dashboard
# 2. Find your kyb-api service
# 3. Environment → Add variable:
#    - RAPIDAPI_PROXY_SECRET: <paste the secret from RapidAPI>
# 4. Service will auto-redeploy
```

### Step 4: Test & Verify (15 min)
```bash
# Test via RapidAPI dashboard:
curl -X POST "https://your-app.onrender.com/kyb/lookup" \
  -H "X-RapidAPI-Proxy-Secret: YOUR_SECRET" \
  -H "Content-Type: application/json" \
  -d '{
    "search_terms": ["Nokia", "Danone"],
    "countries": ["FI", "FR"],
    "max_results_per_query": 2
  }'

# Should return company records from Finland and France
```

### Step 5: Configure Pricing (20 min)
Recommended tiers (see `RAPIDAPI_GUIDE.md` for detailed breakdown):
- **Basic**: 100 req/mo @ $9.99
- **Pro**: 1,000 req/mo @ $49.99 ⭐ (target tier)
- **Business**: 5,000 req/mo @ $199.99
- **Enterprise**: 25,000 req/mo @ $799.99

**Your take at Pro tier**: $37.49/mo per subscriber (75% after RapidAPI's 25% fee)

### Step 6: Publish (10 min)
1. Set API visibility to "Public"
2. Add tags: kyb, company-data, compliance, europe, registry
3. Add logo (optional, can use a simple icon)
4. Submit for listing

## 💰 Economics

### Cost Structure
- **Marginal cost per request**: ~$0 (government APIs are free)
- **Apify cost**: Free tier covers 5 actors + $5 usage/mo (plenty for MVP)
- **Render hosting**: Free tier (or $7/mo for always-on)
- **RapidAPI fee**: 25% of revenue

### Revenue Potential
- **Conservative (Month 6)**: 5 Basic + 2 Pro = $149.90/mo → **$112.43 to you**
- **Optimistic (Month 12)**: 10 Basic + 8 Pro + 1 Business = $699.80/mo → **$524.85 to you**
- **RapidAPI median earning API**: ~$200/mo
- **Top 20% of APIs**: $1,000+/mo

### Competitive Advantage
- **B2BHint** (competitor): $69.99 for similar data
- **Your pricing**: Undercuts by 30% at Pro tier ($49.99)
- **Your moat**: Near-zero marginal cost (they likely pay per lookup to aggregators)

## 🔧 Maintenance Expectations

### Low-Touch (2–3 hours/month)
- Check RapidAPI support questions (1–2/month initially)
- Monitor Render logs for errors
- Update docs if users request clarifications

### Zero-Touch
- Government API changes are extremely rare (they're stable public services)
- No scraping = no breakage from site redesigns
- Apify handles actor hosting and scaling

### High-Touch Only If...
- You want to add more countries (Spain, Germany, etc.) — requires new Apify actor code
- VIES or GLEIF have downtime (log it, they recover quickly)

## 📊 Success Metrics

### Week 1
- [ ] API live on RapidAPI
- [ ] First test call succeeds
- [ ] Pricing configured

### Month 1
- [ ] 5+ free tier sign-ups
- [ ] 1+ paid subscriber
- [ ] $0–50 revenue

### Month 3
- [ ] 20+ free tier users
- [ ] 3–5 paid subscribers
- [ ] $50–200 revenue

### Month 6
- [ ] 50+ free tier users
- [ ] 8–10 paid subscribers
- [ ] $200–500 revenue

## 🚀 Growth Tactics (Optional)

1. **SEO**: Write a blog post "Building a No-Scraping KYB API" with link to RapidAPI listing
2. **Community**: Share on /r/SideProject, Indie Hackers, Product Hunt
3. **B2B Outreach**: Find fintech/compliance startups on Twitter, offer free trial
4. **Content**: Create comparison table vs North Data scraping (reliability angle)
5. **Integrations**: Add to Zapier/Make.com (requires their integration process)

## 📞 Support

- **RapidAPI docs**: https://docs.rapidapi.com/docs/provider-quick-start-guide
- **Render docs**: https://render.com/docs
- **Apify docs**: https://docs.apify.com/

## ⚠️ Legal Notes (Critical)

Your memory notes emphasize: **We sell ACCESS, not stored data.**

✅ **This API complies**:
- Fetches data on-demand per request (not pre-cached)
- No bulk dataset retention
- No rehosting of government data
- Transient caching only (Apify actor run results, short TTL)
- Respects GDPR flags (French `opposition_diffusion_commerciale`)

This is load-bearing for the business model — especially with government APIs like PRH/YTJ.

---

**Total implementation time**: ~3 hours  
**Total listing time**: ~2 hours  
**Monthly maintenance**: ~2 hours  
**Passive income potential**: $200–1,000/mo by month 6–12
