# backend/core/osint_search.py
import os
import requests

SERPAPI_KEY = os.getenv("SERPAPI_KEY")
SERPAPI_URL = "https://serpapi.com/search.json"

def serpapi_search(query: str, max_results: int = 10):
    """Search via SerpAPI (Google engine). Returns list of result links."""
    if not SERPAPI_KEY:
        return []
    params = {
        "engine": "google",
        "q": query,
        "api_key": SERPAPI_KEY,
        "num": max_results
    }
    try:
        r = requests.get(SERPAPI_URL, params=params, timeout=12)
        data = r.json()
        links = []
        for r in data.get("organic_results", [])[:max_results]:
            link = r.get("link")
            if link:
                links.append(link)
        return links
    except Exception:
        return []


def analyze_presence(company: str):
    """Return core OSINT presence signals using SerpAPI."""
    queries = {
        "linkedin": f"{company} LinkedIn company",
        "instagram": f"{company} Instagram",
        "glassdoor": f"{company} Glassdoor reviews",
        "scam": f"{company} scam fraud complaint",
        "reviews": f"{company} employee reviews"
    }

    raw = {}
    for key, q in queries.items():
        raw[key] = serpapi_search(q, max_results=8)

    return {
        "linkedin_found": any("linkedin.com/company" in l for l in raw["linkedin"]),
        "instagram_found": any("instagram.com" in l for l in raw["instagram"]),
        "glassdoor_found": any("glassdoor.com" in l.lower() for l in raw["glassdoor"]),
        "scam_reports_found": any("scam" in (l.lower()) or "complaint" in (l.lower()) or "fraud" in (l.lower())
                                  for l in raw["scam"]),
        "review_presence": len(raw["reviews"]) > 0,
        "raw": raw
    }
