
from network_monitor import collect_metrics, display_results
from alarm_detector import detect_alarms
from incident_correlation import correlate_incidents
from congestion_monitor import analyze_congestion, display_congestion
from incident_report import generate_incident_report


def run_pinoa():

    print("=" * 65)
    print("  PINOA - PRTG INTELLIGENT NETWORK OPERATIONS ASSISTANT")
    print("=" * 65)

    print("\nWelcome to your AI Network Operations lab!")

    print("\nPROJECT ENVIRONMENT")
    print("-" * 65)
    print("Operating System : Windows 11")
    print("Monitoring Mode  : Simulated ISP Network")
    print("Network Access   : Read-only / No live changes")

    print("\nSIMULATED NETWORK DEVICES")
    print("-" * 65)

    devices = [
        "ISP-CORE-R1",
        "ISP-CORE-R2",
        "ISP-PE-R1",
        "ISP-PE-R2",
        "ISP-POP-DELHI",
        "ISP-POP-MUMBAI",
        "ISP-UPLINK-01",
        "ISP-FW-01",
        "ISP-SW-01",
        "ISP-BNG-01"
    ]

    for device in devices:
        print("[SIMULATED ONLINE]", device)

    # 1. Collect one shared monitoring snapshot
    print("\n\n1. NETWORK MONITORING")
    print("=" * 65)

    monitoring_results = collect_metrics()
    display_results(monitoring_results)

    # 2. Detect alarms using the same snapshot
    print("\n\n2. ALARM DETECTION")
    print("=" * 65)

    alarm_results = detect_alarms(monitoring_results)

    # 3. Correlate incidents using the same snapshot
    print("\n\n3. INCIDENT CORRELATION")
    print("=" * 65)

    correlation_result = correlate_incidents(monitoring_results)

    # 4. Analyze backbone congestion
    print("\n\n4. BACKBONE CONGESTION ANALYSIS")
    print("=" * 65)

    congestion_results = analyze_congestion()
    display_congestion(congestion_results)

    # 5. Generate incident report from shared congestion results
    print("\n\n5. INCIDENT REPORT GENERATION")
    print("=" * 65)

    incident_result = generate_incident_report(congestion_results)

    print("\n\nPINOA EXECUTION SUMMARY")
    print("=" * 65)

    print("Devices monitored       :", len(monitoring_results))
    print("Critical alarms         :", len(alarm_results["critical"]))
    print("High alarms             :", len(alarm_results["high"]))
    print("Medium alarms           :", len(alarm_results["medium"]))
    print("Normal devices          :", len(alarm_results["normal"]))

    print("Potential correlation   :",
          "Identified" if correlation_result else "Not identified")

    print("Backbone peak utilization:",
          congestion_results["peak_utilization"], "%")

    print("Incident severity       :", incident_result["severity"])
    print("Incident ID             :", incident_result["incident_id"])

    print("\nPINOA lab execution completed.")
    print("Simulation only - no live PRTG connection.")
    print("No network configuration changes have been performed.")

    print("=" * 65)


if __name__ == "__main__":
    run_pinoa()
