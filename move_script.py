import os
import shutil

os.makedirs('core', exist_ok=True)
files = ['scanner.py', 'exploit_mapper.py', 'cve_lookup.py', 'risk_scoring.py', 'banner_grabber.py', 'threat_intel.py', 'logger.py', 'threading_scan.py']
for f in files:
    if os.path.exists(f):
        try:
            shutil.move(f, 'core/')
        except Exception as e:
            print(f"Error moving {f}: {e}")
