
from datetime import datetime
import uuid

from congestion_monitor import analyze_congestion


def generate_incident_report(congestion_analysis, save_to_file=True):
    """
    Generate an incident report using shared congestion analysis.
    """

    link_name = congestion_analysis["link"]
    capacity = congestion_analysis["capacity"]
    peak_traffic = congestion_analysis["peak_traffic"]
    peak_utilization = congestion_analysis["peak_utilization"]

    if peak_utilization >= 95:
        severity = "CRITICAL"
        probable_cause = "Possible backbone uplink congestion"

        recommendations = [
            "Check interface utilization and traffic trends.",
            "Identify top bandwidth-consuming sources.",
            "Check interface errors and packet discards.",
            "Review routing and traffic engineering.",
            "Evaluate capacity augmentation if congestion persists."
        ]

    elif peak_utilization >= 85:
        severity = "WARNING"
        probable_cause = "Elevated backbone utilization"

        recommendations = [
            "Monitor utilization during peak hours.",
            "Review bandwidth consumption patterns.",
            "Check interface errors and discards."
        ]

    else:
        severity = "NORMAL"
        probable_cause = "No significant congestion detected"

        recommendations = [
            "Continue routine network monitoring."
        ]

    incident_id = "PINOA-" + uuid.uuid4().hex[:8].upper()

    report = f"""
============================================================
        PINOA - NETWORK INCIDENT REPORT
============================================================

Incident ID       : {incident_id}
Generated On      : {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}

NETWORK DETAILS
------------------------------------------------------------
Affected Link     : {link_name}
Link Capacity     : {capacity} Mbps
Peak Traffic      : {peak_traffic} Mbps
Peak Utilization  : {peak_utilization:.1f}%
Severity          : {severity}

OBSERVATION
------------------------------------------------------------
Peak utilization reached {peak_utilization:.1f}% of link capacity.

PROBABLE CAUSE
------------------------------------------------------------
{probable_cause}

RECOMMENDED NOC ACTIONS
------------------------------------------------------------
"""

    for number, action in enumerate(recommendations, start=1):
        report += f"{number}. {action}\n"

    report += """
------------------------------------------------------------
IMPORTANT:
This is an automated simulation-based assessment.
Verify actual network measurements before taking action.
No network configuration changes have been performed.
============================================================
"""

    filename = "incident_" + incident_id + ".txt"

    if save_to_file:
        with open(filename, "w", encoding="utf-8") as file:
            file.write(report)

        print(f"Incident report saved successfully: {filename}")

    print(report)

    return {
        "incident_id": incident_id,
        "severity": severity,
        "report": report,
        "filename": filename if save_to_file else None
    }


if __name__ == "__main__":
    congestion_results = analyze_congestion()
    generate_incident_report(congestion_results)
