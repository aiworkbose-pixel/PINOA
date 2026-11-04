
# ==========================================================
# PINOA - CENTRAL NETWORK TOPOLOGY MODULE
# Shared topology for impact, path and incident analysis
# ==========================================================

from collections import deque

# Common network connections
CONNECTIONS = [
    ("INTERNET", "ISP-UPLINK-01", "Upstream"),
    ("ISP-UPLINK-01", "ISP-CORE-R1", "Backbone"),
    ("ISP-UPLINK-01", "ISP-CORE-R2", "Backbone"),
    ("ISP-CORE-R1", "ISP-PE-R1", "Core"),
    ("ISP-CORE-R2", "ISP-PE-R2", "Core"),
    ("ISP-PE-R1", "ISP-POP-DELHI", "POP"),
    ("ISP-PE-R2", "ISP-POP-MUMBAI", "POP"),
    ("ISP-CORE-R1", "ISP-FW-01", "Security"),
    ("ISP-FW-01", "ISP-SW-01", "Access"),
    ("ISP-SW-01", "ISP-BNG-01", "Subscriber")
]

# Backward-compatible connection list
connections = CONNECTIONS

# Build the common network adjacency map
ADJACENCY = {}

for source, destination, connection_type in CONNECTIONS:
    ADJACENCY.setdefault(source, []).append(destination)


def find_impacted_devices(source):
    """Find all downstream devices from a source device."""

    visited = set()
    queue = deque([source])

    while queue:
        current = queue.popleft()

        for neighbour in ADJACENCY.get(current, []):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(neighbour)

    visited.discard(source)
    return sorted(visited)


def find_path(source, destination):
    """Find the shortest path using breadth-first search."""

    queue = deque([[source]])
    visited = {source}

    while queue:
        path = queue.popleft()
        current = path[-1]

        if current == destination:
            return path

        for neighbour in ADJACENCY.get(current, []):
            if neighbour not in visited:
                visited.add(neighbour)
                queue.append(path + [neighbour])

    return None


if __name__ == "__main__":

    print("=" * 65)
    print("       PINOA - CENTRAL NETWORK TOPOLOGY")
    print("=" * 65)

    print("\nNETWORK CONNECTIONS\n")

    for source, destination, connection_type in CONNECTIONS:
        print(
            f"{source:20} --> "
            f"{destination:20} | {connection_type}"
        )

    nodes = set()

    for source, destination, _ in CONNECTIONS:
        nodes.add(source)
        nodes.add(destination)

    print("\n" + "=" * 65)
    print("TOPOLOGY SUMMARY")
    print("=" * 65)

    print("Total connections :", len(CONNECTIONS))
    print("Total network nodes :", len(nodes))

    print("\nTopology loaded successfully!")
