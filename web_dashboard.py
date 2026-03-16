from flask import Flask, render_template_string, request, jsonify
from threading import Thread
import json
import os

# Note: We import the logic from main dynamically within the routes so we don't block the startup
# if imports try to do initializations.

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>VulnHawk – Intelligent Vulnerability Detection Platform</title>
    <!-- Bootstrap CSS for Professional Look -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        body { background-color: #f8f9fa; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        .hero { background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .card { box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: none; }
        .critical { background-color: #e74c3c !important; color: white !important; }
        .high { background-color: #f39c12 !important; color: white !important; }
        .medium { background-color: #f1c40f !important; color: black !important; }
        .low { background-color: #2ecc71 !important; color: white !important; }
    </style>
</head>
<body>
    <div class="container mt-4">
        <div class="hero text-center">
            <h1>🛡️ VulnHawk</h1>
            <p>Professional Enterprise Vulnerability Management</p>
        </div>
        
        <div class="row">
            <div class="col-md-4">
                <div class="card mb-4">
                    <div class="card-header bg-dark text-white font-weight-bold">Start New Scan</div>
                    <div class="card-body">
                        <form id="scan-form">
                            <div class="mb-3">
                                <label for="target" class="form-label">Target Website / Domain / IP</label>
                                <input type="text" id="target" class="form-control" placeholder="example.com or 192.168.1.10" required>
                            </div>
                            <button class="btn btn-primary w-100" type="submit" id="btn-scan">Launch Vulnerability Scan</button>
                        </form>
                        <div id="scan-status" class="mt-3 text-center fw-bold"></div>
                    </div>
                </div>
            </div>
            
            <div class="col-md-8">
                <div class="card mb-4">
                    <div class="card-header bg-dark text-white">Vulnerability Severity Overview</div>
                    <div class="card-body">
                        <canvas id="vulnChart" height="100"></canvas>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card mb-5">
            <div class="card-header bg-dark text-white d-flex justify-content-between align-items-center">
                <span>Scan Results</span>
                <span id="export-links" style="display:none;">
                    <button class="btn btn-sm btn-outline-light" onclick="alert('Reports are saved in the reports/ folder.')">Download Reports</button>
                </span>
            </div>
            <div class="card-body table-responsive">
                <table class="table table-hover table-bordered" id="results-table">
                    <thead class="table-light">
                        <tr>
                            <th>Host</th>
                            <th>Port/Protocol</th>
                            <th>Running Service</th>
                            <th>Version</th>
                            <th>CVE Findings</th>
                            <th>Risk Score</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr><td colspan="6" class="text-center text-muted">No scan data. Run a scan targeting a host or range.</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

    <script>
        let chartInstance = null;

        function updateChart(stats) {
            const ctx = document.getElementById('vulnChart').getContext('2d');
            if (chartInstance) chartInstance.destroy();
            
            chartInstance = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: ['Critical', 'High', 'Medium', 'Low', 'Unknown'],
                    datasets: [{
                        label: '# of Vulnerabilities',
                        data: [stats.critical, stats.high, stats.medium, stats.low, stats.unknown],
                        backgroundColor: ['#e74c3c', '#f39c12', '#f1c40f', '#2ecc71', '#bdc3c7']
                    }]
                },
                options: {
                    responsive: true,
                    scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } }
                }
            });
        }

        document.getElementById('scan-form').addEventListener('submit', async function(e) {
            e.preventDefault();
            const target = document.getElementById('target').value;
            if(!target) return;
            
            const statusDiv = document.getElementById('scan-status');
            const btn = document.getElementById('btn-scan');
            
            statusDiv.innerHTML = `<span class="spinner-border spinner-border-sm text-primary" role="status" aria-hidden="true"></span> Scanning ${target}...`;
            statusDiv.className = "mt-3 text-center text-primary fw-bold";
            btn.disabled = true;
            
            try {
                const response = await fetch('/api/scan', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({target: target})
                });
                const data = await response.json();
                
                statusDiv.innerText = "Scan Completed Successfully!";
                statusDiv.className = "mt-3 text-center text-success fw-bold";
                document.getElementById('export-links').style.display = 'inline';
                
                const tbody = document.querySelector('#results-table tbody');
                tbody.innerHTML = '';
                
                let stats = { critical: 0, high: 0, medium: 0, low: 0, unknown: 0 };
                
                if (data.results && data.results.length > 0) {
                    data.results.forEach(res => {
                        let cveCount = res.vulnerabilities ? res.vulnerabilities.length : 0;
                        let highestRisk = "none";
                        let riskColorClass = "";
                        
                        if (cveCount > 0) {
                            res.vulnerabilities.forEach(v => {
                                let sev = (v.severity || "unknown").toLowerCase();
                                if (sev === "critical") stats.critical++;
                                else if (sev === "high") stats.high++;
                                else if (sev === "medium") stats.medium++;
                                else if (sev === "low") stats.low++;
                                else stats.unknown++;
                                
                                if (sev === "critical") { highestRisk = "CRITICAL"; riskColorClass = "critical"; }
                                else if (sev === "high" && highestRisk !== "CRITICAL") { highestRisk = "HIGH"; riskColorClass = "high"; }
                                else if (sev === "medium" && !["CRITICAL", "HIGH"].includes(highestRisk)) { highestRisk = "MEDIUM"; riskColorClass = "medium"; }
                                else if (sev === "low" && highestRisk === "none") { highestRisk = "LOW"; riskColorClass = "low"; }
                            });
                        }
                        
                        const tr = document.createElement('tr');
                        tr.innerHTML = `
                            <td class="fw-bold">${res.host}</td>
                            <td>${res.port}</td>
                            <td>${res.service}</td>
                            <td>${res.version || 'Unknown'}</td>
                            <td>${cveCount} CVE(s)</td>
                            <td class="${riskColorClass} fw-bold text-center">${highestRisk.toUpperCase()}</td>
                        `;
                        tbody.appendChild(tr);
                    });
                } else {
                    tbody.innerHTML = '<tr><td colspan="6" class="text-center">No open ports or services found.</td></tr>';
                }
                updateChart(stats);
            } catch (err) {
                statusDiv.innerText = "Error: " + err.message;
                statusDiv.className = "mt-3 text-center text-danger fw-bold";
            } finally {
                btn.disabled = false;
            }
        });
        
        // Init empty chart
        updateChart({ critical: 0, high: 0, medium: 0, low: 0, unknown: 0 });
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/scan', methods=['POST'])
def api_scan():
    data = request.json
    target = data.get("target")
    if not target:
        return jsonify({"error": "No target specified"}), 400
    
    # Importing dynamically so web dashboard loads fast initially
    from main import build_scan_results
    from report_generator import generate_report
    from html_report import generate_reports
    
    try:
        results = build_scan_results(target)
        generate_report(results, style="detailed")
        generate_reports(results)
        
        return jsonify({"status": "success", "results": results})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("[*] Starting VulnHawk Web Dashboard on http://127.0.0.1:5000")
    print("[*] Press CTRL+C to stop.")
    app.run(host='127.0.0.1', port=5000, debug=True)
