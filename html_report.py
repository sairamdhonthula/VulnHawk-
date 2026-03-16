import json
import os
from datetime import datetime

def generate_json_report(scan_results, timestamp):
    os.makedirs("reports", exist_ok=True)
    filename = f"reports/scan_{timestamp}.json"
    with open(filename, "w") as f:
        json.dump(scan_results, f, indent=4)
    print(f"[✓] JSON report saved to: {filename}")

def generate_html_report(scan_results, timestamp):
    os.makedirs("reports", exist_ok=True)
    filename = f"reports/scan_{timestamp}.html"
    
    html_content = f"""
    <html>
    <head>
        <title>Vulnerability Scan Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            h2 {{ color: #333; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; text-align: left; padding: 10px; }}
            th {{ background-color: #f4f4f4; }}
            .critical {{ background-color: #e74c3c; color: white; }}
            .high {{ background-color: #f39c12; color: white; }}
            .medium {{ background-color: #f1c40f; color: black; }}
            .low {{ background-color: #2ecc71; color: white; }}
            .none, .unknown {{ background-color: #bdc3c7; color: black; }}
        </style>
    </head>
    <body>
        <h2>Network Vulnerability Scan Report</h2>
        <p><b>Scan completed:</b> {datetime.now().strftime('%d %B %Y - %I:%M %p')}</p>
        <table>
            <tr>
                <th>Host</th>
                <th>Port</th>
                <th>Service</th>
                <th>CVE</th>
                <th>Risk</th>
            </tr>
    """

    for result in scan_results:
        host = result.get('host', 'Unknown')
        port = result.get('port', 'Unknown')
        service = result.get('service', 'Unknown')
        vulns = result.get('vulnerabilities', [])
        
        if not vulns:
            html_content += f"""
            <tr>
                <td>{host}</td>
                <td>{port}</td>
                <td>{service}</td>
                <td>None</td>
                <td class="none">None</td>
            </tr>
            """
        else:
            for vuln in vulns:
                cve = vuln.get('cve', 'Unknown')
                severity = vuln.get('severity', 'Unknown').lower()
                
                html_content += f"""
            <tr>
                <td>{host}</td>
                <td>{port}</td>
                <td>{service}</td>
                <td>{cve}</td>
                <td class="{severity}">{severity.upper()}</td>
            </tr>
                """

    html_content += """
        </table>
    </body>
    </html>
    """
    
    with open(filename, "w") as f:
        f.write(html_content)
    print(f"[✓] HTML report saved to: {filename}")

def generate_pdf_report(scan_results, timestamp):
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib.styles import getSampleStyleSheet
        
        os.makedirs("reports", exist_ok=True)
        filename = f"reports/scan_{timestamp}.pdf"
        
        doc = SimpleDocTemplate(filename, pagesize=letter)
        elements = []
        
        styles = getSampleStyleSheet()
        title = Paragraph(f"VulnHawk Vulnerability Report ({timestamp})", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        data = [["Host", "Port", "Service", "CVE", "Risk"]]
        
        for result in scan_results:
            host = result.get('host', 'Unknown')
            port = result.get('port', 'Unknown')
            service = result.get('service', 'Unknown')
            vulns = result.get('vulnerabilities', [])
            
            if not vulns:
                data.append([host, str(port), service, "None", "None"])
            else:
                for vuln in vulns:
                    cve = vuln.get('cve', 'Unknown')
                    severity = vuln.get('severity', 'Unknown').upper()
                    data.append([host, str(port), service, cve, severity])
                    
        table = Table(data)
        style = TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ])
        
        for i in range(1, len(data)):
            risk = data[i][4]
            bg_color = colors.beige
            if risk == 'CRITICAL':
                bg_color = colors.pink
            elif risk == 'HIGH':
                bg_color = colors.orange
            elif risk == 'MEDIUM':
                bg_color = colors.yellow
            elif risk == 'LOW':
                bg_color = colors.lightgreen
            style.add('BACKGROUND', (0,i), (-1,i), bg_color)
            
        table.setStyle(style)
        elements.append(table)
        
        doc.build(elements)
        print(f"[✓] PDF report saved to: {filename}")
    except ImportError:
        print("[!] reportlab is not installed. PDF generation skipped.")

def generate_reports(scan_results):
    timestamp = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    generate_json_report(scan_results, timestamp)
    generate_html_report(scan_results, timestamp)
    generate_pdf_report(scan_results, timestamp)
    return timestamp
