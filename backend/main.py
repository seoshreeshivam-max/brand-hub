import sys
import os

# Add the project root to sys.path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
import requests

# Absolute imports from the brand_hub package structure
from backend.auth_manager import auth_manager
from agents.monitor_agent import MonitorAgent
from agents.auditor_agent import auditor_agent
from agents.content_agent import content_agent

app = FastAPI(title="brandHub API", version="0.0.1")

# --- PRODUCTION CORS SETUP ---
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://hub.shreeshivam.com",
    "https://*.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CONFIG_PATH = os.path.join(BASE_DIR, "config", "brands.json")

def load_brands():
    if not os.path.exists(CONFIG_PATH):
        return []
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)["brands"]

@app.get("/")
async def root():
    return {"message": "Welcome to brandHub v.0.0 API"}

@app.get("/brands")
async def get_brands():
    return load_brands()

@app.get("/brands/{brand_id}")
async def get_brand(brand_id: str):
    brands = load_brands()
    brand = next((b for b in brands if b["id"] == brand_id), None)
    if not brand:
        raise HTTPException(status_code=404, detail="Brand not found")
    return brand

@app.get("/agents/monitor/audit")
async def run_monitor_audit():
    try:
        agent = MonitorAgent(CONFIG_PATH)
        report = agent.run_daily_audit()
        return report
    except Exception as e:
        print(f"Audit Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents/auditor/investigate/{brand_id}")
async def run_auditor_investigation(brand_id: str):
    try:
        brands = load_brands()
        brand = next((b for b in brands if b["id"] == brand_id), None)
        if not brand:
            raise HTTPException(status_code=404, detail="Brand not found")
            
        report = auditor_agent.investigate_anomaly(brand_id, brand)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents/content/draft-fix/{brand_id}/{product_id}")
async def draft_content_fix(brand_id: str, product_id: str):
    try:
        product_data = {"id": product_id, "title": "Sample Product"} 
        draft = content_agent.generate_product_fix(brand_id, product_data)
        return draft
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/agents/auditor/sync-status/{brand_id}")
async def sync_product_status(brand_id: str):
    try:
        from mcp_tools.shopify_audit_tool import shopify_audit_tool
        from mcp_tools.shopify_content_tool import shopify_content_tool
        
        # 1. Find mismatched products
        products = shopify_audit_tool.get_product_seo_health(brand_id)
        synced_count = 0
        
        for p in products:
            if "LIVE_BUT_OUT_OF_STOCK" in p["issues"]:
                shopify_content_tool.update_product_status(brand_id, p["id"], "draft")
                synced_count += 1
            elif "STOCK_AVAILABLE_BUT_DRAFT" in p["issues"]:
                shopify_content_tool.update_product_status(brand_id, p["id"], "active")
                synced_count += 1
                
        return {"status": "success", "synced_count": synced_count}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test/google")
async def test_google():
    try:
        creds = auth_manager.get_google_creds()
        return {"status": "success", "expired": creds.expired}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/test/shopify/{brand_id}")
async def test_shopify(brand_id: str):
    try:
        token = auth_manager.get_shopify_token(brand_id)
        brands = load_brands()
        brand = next((b for b in brands if b["id"] == brand_id), None)
        if not brand:
             raise HTTPException(status_code=404, detail="Brand not found")
             
        url = f"https://{brand['shopify_url']}/admin/api/2026-01/shop.json"
        headers = {"X-Shopify-Access-Token": token}
        response = requests.get(url, headers=headers)
        return {"status": "success", "shop": response.json().get("shop", {}).get("name")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
