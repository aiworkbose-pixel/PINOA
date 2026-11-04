
# ==========================================================
# PINOA - NETWORK IMPACT ANALYSIS
# Uses the central network topology module
# ==========================================================

from network_topology import find_impacted_devices


def analyze_impact(source_device, incident_type):

    affected = find_impacted_devices(source_device)

    print("=" * 65)
    print("       PINOA - NETWORK IMPACT ANALYSIS")
    print("=" * 65)

    print("\nSimulated incident :", source_device)
    print("Incident type      :", incident_type)

    print("\nPOTENTIALLY AFFECTED NETWORK ELEMENTS")
    print("-" * 65)

    if affected:
        for device in affected:
            print("[IMPACTED]", device)
    else:
        print("No downstream devices found.")

    print("-" * 65)
    print("Total potentially affected elements:", len(affected))

    print("\nImpact analysis completed successfully!")

    return affected


if __name__ == "__main__":

    analyze_impact(
        "ISP-UPLINK-01",
        "Backbone uplink congestion"
    )
