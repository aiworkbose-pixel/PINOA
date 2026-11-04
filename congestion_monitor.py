
import random

LINK_CAPACITY_MBPS = 1000

TRAFFIC_SAMPLES = [
    420, 510, 650, 720, 810,
    870, 920, 950, 980, 960
]


def analyze_congestion(samples=None):
    """
    Analyze simulated backbone traffic samples.
    Returns structured congestion results.
    """

    if samples is None:
        samples = TRAFFIC_SAMPLES

    results = []

    for sample_number, traffic in enumerate(samples, start=1):

        utilization = (traffic / LINK_CAPACITY_MBPS) * 100

        if utilization >= 95:
            status = "CRITICAL"
            packet_loss = round(random.uniform(3, 6), 2)
            latency = random.randint(100, 160)

        elif utilization >= 85:
            status = "WARNING"
            packet_loss = round(random.uniform(1, 3), 2)
            latency = random.randint(60, 100)

        else:
            status = "NORMAL"
            packet_loss = round(random.uniform(0, 0.5), 2)
            latency = random.randint(10, 50)

        results.append({
            "sample": sample_number,
            "link": "ISP-UPLINK-01",
            "traffic": traffic,
            "capacity": LINK_CAPACITY_MBPS,
            "utilization": round(utilization, 1),
            "packet_loss": packet_loss,
            "latency": latency,
            "status": status
        })

    critical_count = sum(
        1 for item in results
        if item["status"] == "CRITICAL"
    )

    warning_count = sum(
        1 for item in results
        if item["status"] == "WARNING"
    )

    normal_count = sum(
        1 for item in results
        if item["status"] == "NORMAL"
    )

    return {
        "link": "ISP-UPLINK-01",
        "capacity": LINK_CAPACITY_MBPS,
        "samples": results,
        "critical_count": critical_count,
        "warning_count": warning_count,
        "normal_count": normal_count,
        "peak_traffic": max(samples) if samples else 0,
        "peak_utilization": round(
            max(samples) / LINK_CAPACITY_MBPS * 100, 1
        ) if samples else 0
    }


def display_congestion(analysis):
    """Display congestion analysis in the terminal."""

    print("=" * 65)
    print("       PINOA - BACKBONE CONGESTION MONITOR")
    print("=" * 65)

    print("\nMonitoring link:", analysis["link"])
    print("Link Capacity  :", analysis["capacity"], "Mbps")
    print("-" * 65)

    for item in analysis["samples"]:
        print(
            f"Sample {item['sample']:02}: "
            f"Traffic: {item['traffic']:4} Mbps | "
            f"Utilization: {item['utilization']:5.1f}% | "
            f"Loss: {item['packet_loss']:4}% | "
            f"Latency: {item['latency']:3} ms | "
            f"{item['status']}"
        )

    print("\n" + "=" * 65)
    print("CONGESTION ANALYSIS")
    print("=" * 65)

    print("Critical samples :", analysis["critical_count"])
    print("Warning samples  :", analysis["warning_count"])
    print("Normal samples   :", analysis["normal_count"])
    print("Peak traffic     :", analysis["peak_traffic"], "Mbps")
    print("Peak utilization :", analysis["peak_utilization"], "%")

    print("\nSimulation only - no live PRTG data.")
    print("Backbone monitoring completed.")


if __name__ == "__main__":
    congestion_analysis = analyze_congestion()
    display_congestion(congestion_analysis)
