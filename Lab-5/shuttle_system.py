"""Campus Shuttle Timetable & Fleet Tracker.

Logs passenger counts per trip, works out average loads, flags
under-used routes and syncs the fleet data to fleet.json.
"""

import json
from datetime import datetime

routes = {"R1": {"name": "Main Gate - Library", "trips": []},
          "R2": {"name": "Hostel - Sports Complex", "trips": []},
          "R3": {"name": "Admin Block - Metro", "trips": []}}
MIN_CAPACITY = 10
DRIVERS = ["Prakash", "Leela", "Imran", "Tom"]


def is_valid_count(passenger_count):
    """Return True if passenger_count is a non-negative int (not a bool)."""
    return (isinstance(passenger_count, int)
            and not isinstance(passenger_count, bool)
            and passenger_count >= 0)


def add_trip_log(route_id, passenger_count, logs=None):
    """Record a trip's passenger count and return the trip log.

    Raises ValueError for counts that are negative or not integers.
    A new log list is created per call unless one is passed in.
    """
    if not is_valid_count(passenger_count):
        raise ValueError(
            f"invalid passenger count {passenger_count!r} for {route_id}")
    if logs is None:
        logs = []
    routes[route_id]["trips"].append(passenger_count)
    logs.append(f"{datetime.now()}: {route_id} carried {passenger_count}")
    return logs


def remove_route(route_id):
    """Remove a route from the fleet."""
    del routes[route_id]


def average_load(route_id):
    """Return the average passengers per trip, or None if no trips."""
    trips = routes[route_id]["trips"]
    if not trips:
        return None
    return sum(trips) / len(trips)


def underused_routes():
    """Return the routes whose average load is below MIN_CAPACITY."""
    flagged = []
    for route_id in routes:
        avg = average_load(route_id)
        if avg is not None and avg < MIN_CAPACITY:
            flagged.append(route_id)
    return flagged


def assign_driver(route_id):
    """Return the route's driver from a fixed rota (same route each time)."""
    return DRIVERS[sorted(routes).index(route_id) % len(DRIVERS)]


def sync_fleet_data(file="fleet.json"):
    """Save the fleet to a JSON file and reload it into routes in place."""
    with open(file, "w", encoding="utf-8") as out:
        json.dump(routes, out)
    with open(file, encoding="utf-8") as src:
        loaded = json.load(src)
    routes.clear()
    routes.update(loaded)


def main():
    """Run the shuttle tracker demo."""
    sample_trips = [("R1", 32), ("R1", 28), ("R2", 4), ("R2", -6),
                    ("R3", "full")]
    for route_id, count in sample_trips:
        try:
            add_trip_log(route_id, count)
        except ValueError as err:
            print("Rejected:", err)
    print("Driver for R1:", assign_driver("R1"))
    print("Underused:", underused_routes())
    print("R1 average:", average_load("R1"))
    r3_avg = average_load("R3")
    print("R3 average:", "no valid trips" if r3_avg is None else r3_avg)
    sync_fleet_data()
    remove_route("R3")
    choice = input("Route to look up (Enter for R2): ").strip().upper() or "R2"
    if choice in routes:
        print("Trips on", choice, ":", routes[choice]["trips"])
    else:
        print("Unknown route:", choice,
              "- available:", ", ".join(sorted(routes)))


if __name__ == "__main__":
    main()
