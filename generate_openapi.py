#!/usr/bin/env python3
"""Generate OpenAPI spec for RapidAPI upload."""

import json
from app.main import app

if __name__ == "__main__":
    openapi_spec = app.openapi()
    
    # Add RapidAPI-specific extensions
    openapi_spec["info"]["x-logo"] = {
        "url": "https://example.com/logo.png",
        "altText": "KYB API Logo"
    }
    
    # Ensure security schemes are present
    if "components" not in openapi_spec:
        openapi_spec["components"] = {}
    if "securitySchemes" not in openapi_spec["components"]:
        openapi_spec["components"]["securitySchemes"] = {}
    
    openapi_spec["components"]["securitySchemes"]["RapidAPI"] = {
        "type": "apiKey",
        "in": "header",
        "name": "X-RapidAPI-Proxy-Secret",
        "description": "RapidAPI proxy secret (automatically set by RapidAPI)"
    }
    
    openapi_spec["components"]["securitySchemes"]["APIKey"] = {
        "type": "apiKey",
        "in": "header",
        "name": "X-API-Key",
        "description": "Custom API key for direct access"
    }
    
    # Apply security globally
    openapi_spec["security"] = [
        {"RapidAPI": []},
        {"APIKey": []}
    ]
    
    # Write to file
    with open("openapi.json", "w") as f:
        json.dump(openapi_spec, f, indent=2)
    
    print("✓ OpenAPI spec written to openapi.json")
    print(f"  Title: {openapi_spec['info']['title']}")
    print(f"  Version: {openapi_spec['info']['version']}")
    print(f"  Endpoints: {len(openapi_spec['paths'])}")
