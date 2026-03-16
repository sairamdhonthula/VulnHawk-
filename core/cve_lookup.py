import requests
from core.risk_scoring import calculate_risk

def get_cve_info(cve_id):
    url = f"https://cve.circl.lu/api/cve/{cve_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (VulnHawk)"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"[DEBUG] {cve_id} → HTTP {response.status_code}")

        if response.status_code != 200:
            return None

        data = response.json()

        # Extract info
        description = data.get("summary", "No description available.")
        cvss_score = data.get("cvss", "Unknown")

        # Convert score to rough severity using risk scoring module
        severity = calculate_risk(cvss_score)

        return {
            "description": description,
            "severity": severity,
            "cvss_score": cvss_score
        }

    except Exception as e:
        print(f"[!] CIRCL lookup failed for {cve_id}: {e}")
        return None
