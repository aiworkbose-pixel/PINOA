
# ==========================================================
# PINOA - NETWORK PATH ANALYSIS
# Uses the central network topology module
# ==========================================================

from network_topology import find_path


def analyze_paths(source, destinations):

    print("=" * 65)
    print("       PINOA - NETWORK PATH ANALYSIS")
    print("=" * 65)

    print("\nIncident Source:", source)
    print("Incident Type: Backbone Uplink Congestion")

    for destination in destinations:

        path = find_path(source, destination)

        if path:
            print("\nDestination:", destination)
            print("Network Path:")
            print("  " + " -> ".join(path))
            print("Number of Hops:", len(path) - 1)
        else:
            print("\nDestination:", destination)
            print("No path found.")

    print("\nPath analysis completed successfully!")


if __name__ == "__main__":

    source = "ISP-UPLINK-01"

    destinations = [
        "ISP-CORE-R1",
        "ISP-CORE-R2",
        "ISP-PE-R1",
        "ISP-PE-R2",
        "ISP-POP-DELHI",
        "ISP-POP-MUMBAI",
        "ISP-FW-01",
        "ISP-SW-01",
        "ISP-BNG-01"
    ]

    analyze_paths(source, destinations)
