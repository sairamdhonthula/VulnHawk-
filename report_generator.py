import os
from datetime import datetime

def generate_report(scan_results, style="detailed"):
    if style != "detailed":
        print("[!] Invalid style selected. Defaulting to 'detailed'.")

    os.makedirs("reports", exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    filename = f"reports/scan_report_{timestamp}.txt"

    lines = []
    lines.append("NETWORK VULNERABILITY SCAN REPORT")
    lines.append("=" * 50)
    lines.append("")

    for result in scan_results:
        lines.append(f"Host        : {result['host']}")
        lines.append(f"Open Port   : {result['port']}")
        lines.append(f"Service     : {result['service']}")
        lines.append(f"Version     : {result['version']}")
        lines.append("")

        if result["vulnerabilities"]:
            lines.append("Known Vulnerabilities:")
            for vuln in result["vulnerabilities"]:
                lines.append(f"  - Title         : {vuln['title']}")
                lines.append(f"    CVE ID        : {vuln['cve']}")
                lines.append(f"    Exploit-DB    : {vuln['exploitdb_link']}")
                lines.append(f"    EDB-ID        : {vuln['exploitdb_id']}")
                lines.append(f"    Metasploit    : {vuln['msf_module']}")
                lines.append(f"    Severity      : {vuln['severity']}")
                lines.append(f"    Rank          : {vuln['msf_rank']}")
                lines.append(f"    Disclosure    : {vuln['disclosure_date']}")
                lines.append(f"    Check Support : {'Yes' if vuln['check_supported'] else 'No'}")
                lines.append("    Recommendation:")
                lines.append(f"    → {vuln['recommendation']}")
                lines.append("")
        else:
            lines.append("No known critical vulnerabilities found for this service.")
            lines.append("")

        lines.append("-" * 50)
        lines.append("")

    lines.append(f"Scan completed: {datetime.now().strftime('%d %B %Y - %I:%M %p')}")
    lines.append("")

    with open(filename, "w") as f:
        f.write("\n".join(lines))

    print(f"[✓] Detailed report saved to: {filename}")
