# Lab 5: Identified Issues and Fixes

**Student:** BHUVAN KUMAR P (PES1UG24AM069)  
**Program:** `shuttle_system.py` (assigned repo [SETAPESU26/L5_07_campus_shuttle](https://github.com/SETAPESU26/L5_07_campus_shuttle))

Line numbers refer to the **original** starter file ([reports/before](reports/before)). Rows are ordered high and medium severity first. Issue codes come from Pylint (`Wxxxx`/`Cxxxx`/`Rxxxx`), Bandit (`Bxxx`) and Flake8 (`Exxx`); rows marked *runtime* were found by running the program, and no tool flagged them.

| # | Issue | Type | Line(s) | Description | Fix Approach |
|---|-------|------|---------|-------------|--------------|
| 1 | Bare `except: pass` hides errors (Bandit B110, Pylint W0702, Flake8 E722) | Bug / Security | 26–30 | `underused_routes()` swallowed every exception. The non-numeric trip `"full"` on R3 raised a `TypeError` in `average_load`, which was silently ignored, so R3 was never checked. | Removed the `try` block. Passenger counts are validated when logged, and `average_load` returns `None` for a route with no trips, which `underused_routes` skips explicitly. |
| 2 | Invalid passenger counts accepted (*runtime*) | Bug | 12, 49–50 | `add_trip_log` stored `-6` and `"full"` without checks, so R2's average was −1.0 and R3 broke averaging. | New `is_valid_count()`; `add_trip_log` raises `ValueError` for anything that isn't a non-negative `int` (bools rejected too). `main()` catches it and prints `Rejected: …`. |
| 3 | Crash after removing a route (*runtime*) | Bug | 55, 58 | `main()` called `average_load("R3")` after `remove_route("R3")`, so the program always ended with `KeyError: 'R3'`. | R3's average is reported before the route is removed (as "no valid trips" when it has none). |
| 4 | Crash on unknown route lookup (*runtime*) | Bug | 56–57 | Any input other than an existing route (e.g. `R3`, `xyz`) raised `KeyError`; `r1` also failed because input wasn't normalised. | Input is stripped and upper-cased, and checked against `routes`; unknown routes print `Unknown route: … - available: R1, R2`. |
| 5 | Mutable default argument (Pylint W0102) | Bug | 11 | `logs=[]` is created once and shared, so every call kept appending to the same list. | Default changed to `None`, with a new list created inside the function. |
| 6 | Pseudo-random driver choice (Bandit B311) | Security / Design | 33–35 | `random.choice` isn't suitable where security matters, and here it also ignored `route_id`, giving a route a different driver on every run. | Deterministic rota: `DRIVERS[sorted(routes).index(route_id) % len(DRIVERS)]`. This also fixes Pylint W0613 (unused `route_id`). |
| 7 | Files opened without `with` or encoding (Pylint R1732, W1514) | Bug / Resource leak | 39–43 | The second `open()` was never closed, and a write error would leak the first handle. No encoding was given, so behaviour depended on the platform. | `with open(file, ..., encoding="utf-8")` for both the write and the read, using `json.dump` / `json.load`. |
| 8 | `global` statement (Pylint W0603) | Design | 38, 43 | `sync_fleet_data` rebound the module-level `routes`, so other references could point to the stale object. | Removed `global`; the reloaded data is applied in place with `routes.clear()` and `routes.update(loaded)`. |
| 9 | Program runs on import | Design | 60 | `main()` ran unconditionally, so importing the module (e.g. for tests) executed it and waited for input. | Wrapped in `if __name__ == "__main__":`. |
| 10 | Naming (Pylint C0103) | Convention | 33 | `assignDriver` isn't snake_case. | Renamed to `assign_driver` (and updated the call). |
| 11 | `%` string formatting (Pylint C0209) | Convention | 13 | Old-style formatting. | f-string. |
| 12 | Missing docstrings (Pylint C0114, C0116) | Convention | 1, 11, 16, 19, 23, 33, 37, 45 | No module or function docstrings. | Added a module docstring and a docstring for every function. |
| 13 | Blank lines (Flake8 E302, E305) | Style | 11, 16, 19, 23, 33, 37, 45, 60 | One blank line between top-level definitions instead of two. | Two blank lines before every top-level `def` and before the `__main__` guard. |
| 14 | Line too long (Flake8 E501) | Style | 13 | Line over 79 characters (and more appeared after the fixes). | Shortened or wrapped every long line. |

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 6.25/10 (18 messages) | **10.00/10** (0 messages) |
| Bandit | 2 issues (Low: B110, B311) | **0 issues** |
| Flake8 | 10 issues | **0 issues** |

Reports: [reports/before](reports/before) and [reports/after](reports/after).
