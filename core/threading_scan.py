from concurrent.futures import ThreadPoolExecutor, as_completed
from core.exploit_mapper import search_exploits
from core.banner_grabber import grab_banner
from core.logger import log_event

def process_target(entry):
    host = entry['host']
    port = entry['port']
    service = entry['service']
    version = entry['version']

    # Banner Grabbing if version is empty
    if not version or version.strip() == '':
        banner = grab_banner(host, port)
        if banner:
            version = banner
            entry['version'] = version
            log_event(f"Grabbed banner for {host}:{port} -> {version}")

    log_event(f"Scanning {host}:{port} - {service} {version}")
    
    # Exploit mapping takes the most time
    vulns = search_exploits(service, version)
    
    for v in vulns:
        if v.get('cve') != 'Unknown':
            log_event(f"Exploit matched {v['cve']} for {host}:{port}")

    return {
        "host": host,
        "port": port,
        "service": service,
        "version": version,
        "vulnerabilities": vulns
    }

def scan_targets_concurrently(scan_data, max_workers=20):
    structured_results = []
    log_event(f"Starting multi-threaded vulnerability scan for {len(scan_data)} services")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_entry = {executor.submit(process_target, entry): entry for entry in scan_data}
        
        for future in as_completed(future_to_entry):
            try:
                result = future.result()
                structured_results.append(result)
            except Exception as exc:
                entry = future_to_entry[future]
                log_event(f"{entry['host']}:{entry['port']} generated an exception: {exc}", level="error")
                
    return structured_results
