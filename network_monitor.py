
# ==========================================================
# PINOA - INTELLIGENT NETWORK MONITORING ENGINE
# Reusable monitoring module for incident correlation
# ==========================================================

import random

DEVICES = [
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


def analyze_device(device):

    cpu = random.randint(10, 95)
    memory = random.randint(30, 95)
    bandwidth = random.randint(100, 950)
    packet_loss = round(random.uniform(0, 5), 2)
    latency = random.randint(5, 150)

    issues = []
    actions = []

    if cpu > 90:
        issues.append("Critical CPU utilization")
        actions.append("Investigate CPU-intensive processes")
    elif cpu > 80:
        issues.append("High CPU utilization")
        actions.append("Check device processing load")

    if memory > 85:
        issues.append("High memory utilization")
        actions.append("Check memory consumption")

    if packet_loss > 3:
        issues.append("High packet loss")
        actions.append("Investigate interface errors and congestion")

    if latency > 100:
        issues.append("High network latency")
        actions.append("Check routing and link performance")

    if cpu > 90:
        severity = "CRITICAL"
    elif cpu > 80 or memory > 85 or packet_loss > 3:
        severity = "HIGH"
    elif latency > 100:
        severity = "MEDIUM"
    else:
        severity = "NORMAL"

    return {
        "device": device,
        "cpu": cpu,
        "memory": memory,
        "bandwidth": bandwidth,
        "packet_loss": packet_loss,
        "latency": latency,
        "severity": severity,
        "issues": issues,
        "actions": actions
    }


def collect_metrics():

    results = []

    for device in DEVICES:
        results.append(analyze_device(device))

    return results


def display_results(results):

    print("=" * 70)
    print("       PINOA - INTELLIGENT NETWORK MONITORING ENGINE")
    print("=" * 70)

    print("\nAnalyzing network devices...\n")

    for result in results:

        print(f"DEVICE       : {result['device']}")
        print(f"CPU          : {result['cpu']}%")
        print(f"MEMORY       : {result['memory']}%")
        print(f"BANDWIDTH    : {result['bandwidth']} Mbps")
        print(f"PACKET LOSS  : {result['packet_loss']}%")
        print(f"LATENCY      : {result['latency']} ms")
        print(f"SEVERITY     : {result['severity']}")

        if result["issues"]:
            print("ISSUES       :")
            for issue in result["issues"]:
                print(f"  - {issue}")

            print("RECOMMENDED ACTIONS:")
            for action in result["actions"]:
                print(f"  - {action}")
        else:
            print("ISSUES       : No abnormal conditions detected")

        print("-" * 70)

    critical = sum(1 for r in results if r["severity"] == "CRITICAL")
    high = sum(1 for r in results if r["severity"] == "HIGH")
    medium = sum(1 for r in results if r["severity"] == "MEDIUM")
    normal = sum(1 for r in results if r["severity"] == "NORMAL")

    print("\n" + "=" * 70)
    print("             PINOA - NETWORK HEALTH SUMMARY")
    print("=" * 70)

    print(f"Total Devices : {len(results)}")
    print(f"CRITICAL      : {critical}")
    print(f"HIGH          : {high}")
    print(f"MEDIUM        : {medium}")
    print(f"NORMAL        : {normal}")

    print("\nNetwork analysis completed.")


if __name__ == "__main__":

    monitoring_results = collect_metrics()
    display_results(monitoring_results)
