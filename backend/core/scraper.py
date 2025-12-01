import requests
import re
import ssl
import socket
import whois
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import urlparse


# -------------------------
# FETCH PAGE CONTENT
# -------------------------
def fetch_page_text(url: str):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code != 200:
            return None
        return res.text
    except:
        return None


# -------------------------
# EXTRACT BASIC INFO
# -------------------------
def extract_basic_info(html: str):
    soup = BeautifulSoup(html, "html.parser")

    title = soup.title.string if soup.title else ""
    text = soup.get_text(separator=" ", strip=True)

    return {"title": title, "text": text}


# -------------------------
# DOMAIN INFO HELPER
# -------------------------
def get_domain_info(url: str):
    domain = urlparse(url).netloc.replace("www.", "")
    return {"registered_domain": domain}


# -------------------------
# WHOIS (FIXED)
# -------------------------
def get_whois(domain: str):
    try:
        w = whois.whois(domain)
        created = w.creation_date

        # Handle lists
        if isinstance(created, list):
            created = created[0]

        # Handle timezone-aware datetime
        if isinstance(created, datetime):
            created = created.replace(tzinfo=None)

        age_days = (datetime.utcnow() - created).days if created else None

        return {
            "whois_found": True,
            "domain_age_days": age_days
        }

    except Exception as e:
        print("WHOIS ERROR:", e)
        return {
            "whois_found": False,
            "domain_age_days": None
        }



# -------------------------
# SSL CHECK
# -------------------------
def check_ssl(domain: str):
    ctx = ssl.create_default_context()

    try:
        with socket.create_connection((domain, 443), timeout=5) as sock:
            with ctx.wrap_socket(sock, server_hostname=domain):
                return {"ssl_valid": True}
    except:
        return {"ssl_valid": False}


# -------------------------
# REDIRECT CHECK
# -------------------------
def check_redirects(url: str):
    try:
        r = requests.get(url, allow_redirects=True, timeout=8)
        return {"redirects": len(r.history)}
    except:
        return {"redirects": 0}


# -------------------------
# CONTACT EXTRACTION (FIXED)
# -------------------------
def extract_contacts(text: str):
    if not text:
        return {"emails": [], "phones": []}

    # Email regex
    emails = list(set(re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)))

    # Phone regex (fixed)
    phones = list(set(
        re.findall(
            r"(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{2,4}\)?[\s.-]?)\d{3,4}[\s.-]?\d{3,4}",
            text
        )
    ))

    return {
        "emails": emails[:10],
        "phones": phones[:10]
    }
