import re

SUSPICIOUS_KEYWORDS = [
    "registration fee", "security deposit", "pay to apply",
    "pay to work", "payment required", "crypto", "urgent hiring",
    "100% job guarantee", "telegram", "whatsapp only",
    "investment required", "processing fee"
]

SAFE_DOMAINS = {
    "microsoft.com", "google.com", "amazon.com", "apple.com",
    "meta.com", "linkedin.com", "adobe.com", "oracle.com",
    "walmart.com", "flipkart.com", "tcs.com", "infosys.com",
}


def keyword_risk(text: str):
    text = (text or "").lower()

    # Remove hidden JS garbage
    text = re.sub(r"{.*?}", "", text)
    text = re.sub(r"\s+", " ", text)

    return [k for k in SUSPICIOUS_KEYWORDS if f" {k} " in f" {text} "]


def heuristic_risk(text, domain, osint_basic, osint_company, domain_health):
    score = 0
    risk_flags = []
    trust_flags = []

    # ---------------- SAFE BRANDS → skip risk rules ----------------
    if domain in SAFE_DOMAINS:
        return {
            "score": 0,
            "verdict": "Safe – Official Verified Company Website",
            "risk_flags": [],
            "trust_flags": [
                "Recognized global corporate domain",
                "Large/official brand — strong online presence expected",
                "Trusted based on official domain list"
            ]
        }

    # ---------------- KEYWORD CHECK ----------------
    suspicious = keyword_risk(text)
    if suspicious:
        score += 30
        risk_flags.append("Suspicious keywords: " + ", ".join(suspicious))
    else:
        trust_flags.append("No suspicious keywords found")

    # ---------------- CHECK SCAM REPORTS ----------------
    if osint_basic.get("scam_reports_found") and domain not in SAFE_DOMAINS:
        score += 20
        risk_flags.append("Scam reports detected online")
    else:
        trust_flags.append("No scam reports detected online")

    # ---------------- WHOIS AGE ----------------
    age = domain_health.get("domain_age_days")
    if age is None:
        risk_flags.append("Domain age unavailable")
        score += 5
    elif age < 60:
        score += 15
        risk_flags.append("Domain is newly created (<60 days)")
    else:
        trust_flags.append(f"Domain established ({age} days old)")

    # ---------------- SSL ----------------
    if domain_health.get("ssl_valid"):
        trust_flags.append("Valid SSL certificate detected")
    else:
        risk_flags.append("SSL invalid or missing")
        score += 10

    # ---------------- REDIRECTS ----------------
    redirects = domain_health.get("redirect_count", 0)
    if redirects > 3:
        score += 5
        risk_flags.append("Unusual number of redirects")
    else:
        trust_flags.append("Redirect count normal")

    # ---------------- CONTACTS ----------------
    contacts = domain_health.get("contacts", {})
    if contacts.get("emails") or contacts.get("phones"):
        trust_flags.append("Contact details found on page")
    else:
        risk_flags.append("No contact details on page")

    # ---------------- OSINT (LinkedIn, Glassdoor) ----------------
    if osint_basic.get("linkedin_found"):
        trust_flags.append("LinkedIn presence detected")
    else:
        risk_flags.append("No LinkedIn presence")

    if osint_basic.get("glassdoor_found"):
        trust_flags.append("Glassdoor presence detected")
    else:
        risk_flags.append("No Glassdoor presence")

    # ---------------- Final Verdict ----------------
    score = min(max(score, 0), 100)

    if score < 35:
        verdict = "Low Risk – Likely Safe"
    elif score < 70:
        verdict = "Medium Risk – Investigate Carefully"
    else:
        verdict = "High Risk – Potential Scam"

    return {
        "score": score,
        "verdict": verdict,
        "risk_flags": risk_flags,
        "trust_flags": trust_flags
    }
