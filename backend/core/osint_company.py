# core/osint_company.py
import os
from urllib.parse import urlparse
from core.osint_search import serpapi_search

INDIAN_HINTS = ["pvt ltd", "private limited", "india", "limited"]

def extract_company_name(url: str, title: str = "") -> str:
    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "").split(".")[0]
    if title:
        t = title.split("-")[0].strip()
        if 1 <= len(t.split()) <= 5:
            return t
    return domain.title()

def check_mca(company: str):
    links = serpapi_search(f"{company} MCA registration site mca.gov.in", max_results=6)
    return any("mca.gov.in" in l.lower() for l in links)

def check_gst(company: str):
    links = serpapi_search(f"{company} GSTIN GST number", max_results=6)
    return any("gst" in l.lower() or "gstin" in l.lower() for l in links)

def check_location_presence(company: str):
    links = serpapi_search(f"{company} office address google maps", max_results=6)
    return any("google.com/maps" in l.lower() or "maps" in l.lower() or "place" in l.lower() for l in links)

def full_company_osint(company: str, domain: str = "") -> dict:
    """
    Returns detailed OSINT about a company:
      - linkedin/glassdoor handled separately by analyze_presence()
      - mca/gst/location derived here
    """
    mca = check_mca(company)
    gst = check_gst(company)
    location = check_location_presence(company)

    return {
        "mca_found": mca,
        "gst_found": gst,
        "location_found": location,
        "raw": {
            "mca_links": serpapi_search(f"{company} MCA registration site mca.gov.in", max_results=6),
            "gst_links": serpapi_search(f"{company} GSTIN GST number", max_results=6),
            "location_links": serpapi_search(f"{company} office address google maps", max_results=6),
        }
    }
