# backend/routes/verify.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, HttpUrl
from datetime import datetime

from core.scraper import (
    fetch_page_text,
    extract_basic_info,
    get_domain_info,
    get_whois,
    check_ssl,
    check_redirects,
    extract_contacts
)

from core.osint_search import analyze_presence
from core.osint_company import extract_company_name, full_company_osint
from core.risk import heuristic_risk
from database import db, to_obj
import tldextract

router = APIRouter()


class LinkRequest(BaseModel):
    url: HttpUrl


@router.post("/link")
async def verify_link(payload: LinkRequest):
    url = str(payload.url)

    # 1. FETCH HTML
    html = fetch_page_text(url)
    if not html:
        raise HTTPException(status_code=400, detail="Unable to fetch the URL")

    # 2. EXTRACT TEXT + TITLE
    info = extract_basic_info(html)
    title = info.get("title") or ""
    text = info.get("text") or ""

    # 3. COMPANY NAME
    company = extract_company_name(url, title)

    # 4. BASIC OSINT
    osint_basic = analyze_presence(company)

    # 5. DEEP COMPANY OSINT
    osint_company = full_company_osint(company)

    # 6. DOMAIN NORMALIZATION (IMPORTANT FIX)
    ext = tldextract.extract(url)
    root_domain = f"{ext.domain}.{ext.suffix}"   # microsoft.com

    # 7. DOMAIN HEALTH (WHOIS -> on root domain only)
    whois_info = get_whois(root_domain)
    redirects = check_redirects(url)
    ssl_info = check_ssl(root_domain)
    contacts = extract_contacts(text)

    domain_health = {
        "registered_domain": root_domain,
        "domain_age_days": whois_info["domain_age_days"],
        "whois_found": whois_info["whois_found"],
        "ssl_valid": ssl_info["ssl_valid"],
        "redirect_count": redirects["redirects"],
        "contacts": contacts
    }

    # 8. RISK SCORE
    risk = heuristic_risk(
        text=text,
        domain=root_domain,
        osint_basic=osint_basic,
        osint_company=osint_company,
        domain_health=domain_health
    )

    # 9. Return Combined Result
    record = {
        "url": url,
        "domain": root_domain,
        "company": company,
        "risk_score": risk["score"],
        "verdict": risk["verdict"],
        "risk_flags": risk["risk_flags"],
        "trust_flags": risk["trust_flags"],
        "domain_info": domain_health,
        "osint_basic": osint_basic,
        "osint_company": osint_company,
        "timestamp": datetime.utcnow()
    }

    res = await db.checks.insert_one(record)
    saved = await db.checks.find_one({"_id": res.inserted_id})
    return to_obj(saved)



@router.get("/history")
async def get_history(limit: int = 20):
    cursor = db.checks.find().sort("timestamp", -1).limit(limit)
    res = []

    async for doc in cursor:
        obj = to_obj(doc)

        # FIX: Convert BSON datetime → string
        if isinstance(obj.get("timestamp"), datetime):
            obj["timestamp"] = obj["timestamp"].isoformat()

        res.append(obj)

    return res
