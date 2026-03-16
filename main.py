from core.scanner import run_nmap_scan
from core.logger import log_event
from core.threading_scan import scan_targets_concurrently
from report_generator import generate_report
from html_report import generate_reports
from core.threat_intel import check_ip_reputation
from database import save_scan

def build_scan_results(ip_range):
    print(f"[+] Scanning network: {ip_range}")
    log_event(f"Scan started for {ip_range}")
    
    # Run core Nmap discovery
    scan_data = run_nmap_scan(ip_range)

    # Threat Intelligence Execution
    unique_hosts = set(entry['host'] for entry in scan_data)
    for host in unique_hosts:
        intel = check_ip_reputation(host)
        print(f"\n[+] Threat Intelligence for {host}:")
        print(f"    Reputation: {intel['reputation']}")
        print(f"    Botnet Activity: {intel['botnet_activity']}")
        print(f"    Details: {intel['details']}\n")
        log_event(f"Threat Intel ({host}) -> Reputation: {intel['reputation']}")

    # Multi-threaded vulnerability lookup and banner grabbing
    structured_results = scan_targets_concurrently(scan_data)
    
    return structured_results

if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python3 main.py <target-ip-or-range-or-domain>")
        print("Example: python3 main.py example.com")
        exit(1)

    target = sys.argv[1]

    print("=" * 50)
    print("VulnHawk - Intelligent Vulnerability Detection Platform")
    print("=" * 50)

    try:
        results = build_scan_results(target)
        
        # Original TXT Report
        generate_report(results, style="detailed")
        
        # Auto-generate JSON + HTML Reports
        generate_reports(results)
        
        # DB Tracking
        save_scan(target, "Completed", results)
        
        log_event(f"Scan finished for {target}")
        print("\n[+] Scan process completed successfully.")
        print("[+] Check your 'dashboard/app.py' to view the historical results in the Web UI!")

    except Exception as e:
        save_scan(target, "Failed", str(e))
        log_event(f"Scan failed for {target}: {str(e)}", level="error")
        print(f"\n[!] Error during scan: {e}")
