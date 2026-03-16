import nmap
import urllib.parse
import re

def clean_target(target):
    """
    Cleans the input target to support IPs, CIDR blocks, domains, and URLs.
    Example: http://example.com/path -> example.com
    """
    target = target.strip()
    
    # Check if it's an IP CIDR block (leave it alone)
    if re.match(r'^\d{1,3}(\.\d{1,3}){3}/\d{1,2}$', target):
        return target
        
    # If the user enters a website URL, extract just the domain
    if target.startswith("http://") or target.startswith("https://"):
        parsed = urllib.parse.urlparse(target)
        target = parsed.netloc
        
    # Remove any trailing paths if they just copy-pasted example.com/page
    if '/' in target:
        target = target.split('/')[0]
        
    return target

def run_nmap_scan(ip_range):
    target = clean_target(ip_range)
    nm = nmap.PortScanner()
    results = []

    print(f"[+] Running Nmap scan on: {target}")
    nm.scan(hosts=target, arguments='-Pn -sV -T4')

    for host in nm.all_hosts():
        for proto in nm[host].all_protocols():
            ports = nm[host][proto].keys()
            for port in ports:
                service = nm[host][proto][port].get('name', '')
                version = nm[host][proto][port].get('version', '')
                results.append({
                    'host': host,
                    'port': port,
                    'service': service,
                    'version': version
                })

    return results
