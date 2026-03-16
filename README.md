# VulnHawk – Intelligent Vulnerability Detection Platform

"Securing the next generation of global connectivity."

© 2026 Sairam. All Rights Reserved.

VulnHawk – Intelligent Vulnerability Detection Platform is a Python-based network vulnerability scanner that:

- Discovers hosts/services via Nmap
- Maps discovered services to known exploits (optionally via Exploit-DB `searchsploit`)
- Enriches findings with CVE details using the public CIRCL CVE API (no API key required)
- Generates local reports in TXT/JSON/HTML/PDF
- Provides a simple local web dashboard to run scans by entering an IP/CIDR/domain/URL

Important: This project is intended for educational use and authorized security testing only.

## What it does

1. Runs an Nmap service scan (`-Pn -sV -T4`) against a target.
2. For each discovered service/version, performs exploit lookups and CVE enrichment.
3. Produces structured results and writes reports to the `reports/` folder.
4. Optionally runs through a local Flask dashboard to start scans from a browser.

## Features

- Nmap-based discovery + service detection
- Exploit mapping via Exploit-DB (`searchsploit`) when available
- CVE enrichment via CIRCL CVE API
- Multi-threaded processing for per-service analysis
- Reports: `.txt`, `.json`, `.html`, `.pdf`
- Local web dashboard (Flask)

## Project structure (key files)

- `main.py` — CLI entrypoint (scan from terminal)
- `web_dashboard.py` — simple Flask dashboard (scan from browser)
- `dashboard/app.py` — dashboard UI with scan history (SQLite)
- `core/` — scanning + enrichment modules
- `reports/` — generated outputs

## Prerequisites

### Required

- Python 3.x
- Nmap installed on your machine and available on PATH

To verify Nmap:

```bash
nmap --version
```

### Optional (recommended)

- `searchsploit` (Exploit-DB) for richer exploit mapping
	- If `searchsploit` is not installed, the scanner still runs, but exploit results may be limited.

## Installation

This repository is often opened with a nested folder layout. Make sure you are in the folder that contains `requirements.txt` and `web_dashboard.py`.

### Windows (cmd)

```bat
cd C:\Users\Sairam\Downloads\NetVulnScanner-main\NetVulnScanner-main

py -3 -m venv .venv
.\.venv\Scripts\activate

python -m pip install -r requirements.txt
```

### Linux / macOS

```bash
cd NetVulnScanner-main/NetVulnScanner-main

python3 -m venv .venv
source .venv/bin/activate

python -m pip install -r requirements.txt
```

## Usage

You can run VulnHawk – Intelligent Vulnerability Detection Platform either from a browser dashboard or directly from the terminal.

### Option A — Web dashboard (recommended for interactive use)

Start the server:

```bash
python web_dashboard.py
```

Open:

- http://127.0.0.1:5000

Enter one of the following target formats in the UI:

- Domain: `example.com`
- URL: `https://example.com` (the scanner extracts the host)
- Single IP: `192.168.1.10`
- CIDR range: `192.168.1.0/24`

### Option B — CLI (scan from terminal)

```bash
python main.py example.com
```

More examples:

```bash
python main.py 127.0.0.1
python main.py 192.168.1.10
python main.py 192.168.1.0/24
python main.py https://example.com
```

## Outputs

All reports are saved under the `reports/` directory.

- TXT report: `reports/scan_report_YYYY-MM-DD_HH-MM.txt`
- JSON report: `reports/scan_YYYY_MM_DD_HH_MM_SS.json`
- HTML report: `reports/scan_YYYY_MM_DD_HH_MM_SS.html`
- PDF report: `reports/scan_YYYY_MM_DD_HH_MM_SS.pdf`

## Notes on accuracy

- Nmap service version detection is best-effort and depends on network visibility and service fingerprinting.
- CVE enrichment uses the public CIRCL CVE API; if the API is rate-limited or unreachable, CVE fields may show as Unknown.
- The current “Threat Intelligence” check is a simulated/mock implementation (no external API keys required).

## Troubleshooting

### “Could not open requirements file: requirements.txt”

You’re in the wrong folder. `cd` into the directory that contains `requirements.txt`.

### “python: can’t open file … web_dashboard.py”

Same root cause as above — wrong working directory.

### “python run server.py” fails

That command is not used by this project. Use:

- `python web_dashboard.py` (web UI)
- `python main.py <target>` (CLI)

### Nmap errors / empty results

Ensure Nmap is installed and accessible:

```bash
nmap --version
```

### “searchsploit is not recognized …” (Windows)

This is expected if Exploit-DB isn’t installed. The scanner will still run, but exploit mapping may be limited.

## Secrets (.env) and credentials

Do not hardcode or commit secrets (API keys, passwords, tokens, certificates).

- Use a local `.env` file for development secrets if needed.
- `.env` and common key/cert file types are excluded via `.gitignore`.
- Rotate any credentials immediately if they were ever committed to Git.

## Security + legal disclaimer

Use this tool only on systems you own or where you have explicit written permission to test.
Unauthorized scanning can be illegal and may disrupt services.

## Contributing

Contributions are welcome:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request with a clear description and test notes

## License

This repository is released under a proprietary, all-rights-reserved license.
See `LICENSE` and `NOTICE`.
