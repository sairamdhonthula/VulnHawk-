from flask import Flask, render_template, request, jsonify
import sys
import os
import json

# Ensure parent directory modules are accessible
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from database import save_scan, get_scan_history, get_scan_results

# Explicitly tell Flask where the templates are
app = Flask(__name__, template_folder='templates', static_folder='static')

@app.route('/')
def dashboard():
    return render_template("dashboard.html")

@app.route('/api/history', methods=['GET'])
def api_history():
    try:
        history = get_scan_history()
        return jsonify(history)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/history/<int:scan_id>', methods=['GET'])
def api_get_history_scan(scan_id):
    try:
        results = get_scan_results(scan_id)
        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/scan', methods=['POST'])
def api_scan():
    data = request.json
    target = data.get("target")
    if not target:
        return jsonify({"error": "No target specified"}), 400
    
    # Save an initial "in progress" state
    scan_id = save_scan(target, "Running", None)

    # Dynamic imports to load main module logic
    from main import build_scan_results
    from report_generator import generate_report
    from html_report import generate_reports
    
    try:
        results = build_scan_results(target)
        
        # Reports
        generate_report(results, style="detailed")
        generate_reports(results)
        
        # Save real data back
        # In SQLite, we can just insert a new one as "Completed" for simplicity.
        save_scan(target, "Completed", results)

        return jsonify({"status": "success", "results": results})
    except Exception as e:
        save_scan(target, "Failed", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("=" * 50)
    print("🛡️ VulnHawk Dashboard Active")
    print("=" * 50)
    print("[+] Dashboard Link: http://127.0.0.1:5000")
    print("[+] Press CTRL+C to stop.")
    app.run(host='127.0.0.1', port=5000, debug=True)
