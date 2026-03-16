def calculate_risk(cvss_score):
    try:
        score = float(cvss_score)
        if score >= 9.0:
            return "Critical"
        elif score >= 7.0:
            return "High"
        elif score >= 4.0:
            return "Medium"
        elif score > 0:
            return "Low"
        else:
            return "None"
    except (ValueError, TypeError):
        return "Unknown"
