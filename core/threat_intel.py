from core.logger import log_event

def check_ip_reputation(ip):
    log_event(f"Checking Threat Intelligence for IP: {ip}")
    # Simulating API calls to AbuseIPDB, Shodan, or VirusTotal
    # In a real environment, you would use requests.get() with proper API keys here.
    
    # Mocking a response
    suspicious_ips = ["192.168.1.15", "10.0.0.5", "192.168.1.10"]
    
    if ip in suspicious_ips:
        return {
            "ip": ip,
            "reputation": "Suspicious",
            "botnet_activity": "Yes",
            "details": "Known malicious IP observed in local botnet simulations."
        }
    else:
        return {
            "ip": ip,
            "reputation": "Clean",
            "botnet_activity": "No",
            "details": "No immediate threats detected."
        }
