
# ==========================================================
# PINOA - INTELLIGENT INCIDENT CORRELATION ENGINE
# Uses shared monitoring data and central network topology
# ==========================================================

from network_monitor import collect_metrics
from network_topology import find_impacted_devices


def correlate_incidents(results):

    print("\n" + "=" * 70)
    print("       PINOA - INTELLIGENT INCIDENT CORRELATION")
    print("=" * 70)

    alert_devices = {
        result["device"]
        for result in results
        if result["severity"] in ["CRITICAL", "HIGH", "MEDIUM"]
    }

    print("\nDETECTED ABNORMAL DEVICES")
    print("-" * 70)

    for result in results:
        if result["device"] in alert_devices:
            print(
                f"{result['device']:20} | "
                f"{result['severity']:8} | "
                f"{', '.join(result['issues'])}"
            )

    print("\n" + "=" * 70)
    print("             ROOT CAUSE INVESTIGATION")
    print("=" * 70)

    candidates = []

    for result in results:

        root = result["device"]

        if root not in alert_devices:
            continue

        impacted = set(find_impacted_devices(root))
        matching = impacted.intersection(alert_devices)

        if len(matching) >= 2:

            candidates.append({
                "root": root,
                "severity": result["severity"],
                "issues": result["issues"],
                "impacted": sorted(matching),
                "correlated_count": len(matching)
            })

    best = None

    if candidates:

        candidates.sort(
            key=lambda item: (
                item["correlated_count"],
                item["severity"] == "CRITICAL"
            ),
            reverse=True
        )

        best = candidates[0]

        print("\nPOTENTIAL COMMON SOURCE")
        print("Source Device :", best["root"])
        print("Source Severity :", best["severity"])
        print("Detected Issues :", ", ".join(best["issues"]))

        print("\nCORRELATED DOWNSTREAM DEVICES")

        for device in best["impacted"]:
            print("  [POTENTIALLY IMPACTED]", device)

        print("\nRECOMMENDED INVESTIGATION")

        print("  1. Check source device health and performance.")
        print("  2. Inspect connected interfaces and packet drops.")
        print("  3. Verify routing and link connectivity.")
        print("  4. Compare downstream device metrics.")
        print("  5. Review timestamps and historical alarm patterns.")
        print("  6. Confirm the cause before taking action.")

    else:

        print("\nNo common source identified from current alerts.")
        print("Investigate individual device alerts separately.")

    print("\n" + "=" * 70)
    print("IMPORTANT:")
    print("Correlation is based on topology and simulated metrics.")
    print("It does not prove that the source caused downstream alerts.")
    print("No network configuration changes have been performed.")
    print("=" * 70)

    return best


if __name__ == "__main__":

    print("\nCollecting monitoring data from PINOA...")

    monitoring_results = collect_metrics()

    correlate_incidents(monitoring_results)
