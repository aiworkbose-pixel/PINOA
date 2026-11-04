
# ==========================================================
# PINOA - AUTOMATIC ALARM DETECTOR
# Uses shared monitoring data from network_monitor.py
# ==========================================================

from network_monitor import collect_metrics


def detect_alarms(results):

    critical_alarms = []
    high_alarms = []
    medium_alarms = []
    normal_devices = []

    print("=" * 70)
    print("       PINOA - AUTOMATIC ALARM DETECTOR")
    print("=" * 70)

    print("\nDEVICE ALARM ANALYSIS\n")

    for result in results:

        device = result["device"]
        severity = result["severity"]

        print(
            f"{device:20} | "
            f"CPU: {result['cpu']:2}% | "
            f"Loss: {result['packet_loss']:5}% | "
            f"Latency: {result['latency']:3} ms | "
            f"{severity}"
        )

        if severity == "CRITICAL":
            critical_alarms.append(device)

        elif severity == "HIGH":
            high_alarms.append(device)

        elif severity == "MEDIUM":
            medium_alarms.append(device)

        else:
            normal_devices.append(device)

    print("\n" + "=" * 70)
    print("                ALARM SUMMARY")
    print("=" * 70)

    print("Critical alarms :", len(critical_alarms))
    print("High alarms     :", len(high_alarms))
    print("Medium alarms   :", len(medium_alarms))
    print("Normal devices  :", len(normal_devices))

    print("\nCritical devices:")
    for device in critical_alarms:
        print("  [CRITICAL]", device)

    print("\nHigh severity devices:")
    for device in high_alarms:
        print("  [HIGH]", device)

    print("\nMedium severity devices:")
    for device in medium_alarms:
        print("  [MEDIUM]", device)

    print("\nAlarm detection completed.")

    return {
        "critical": critical_alarms,
        "high": high_alarms,
        "medium": medium_alarms,
        "normal": normal_devices
    }


if __name__ == "__main__":

    print("\nCollecting monitoring data from PINOA...")

    monitoring_results = collect_metrics()

    detect_alarms(monitoring_results)
