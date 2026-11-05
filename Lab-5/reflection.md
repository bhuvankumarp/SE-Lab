# Lab 5: Reflection

**Student:** BHUVAN KUMAR P (PES1UG24AM069)

## 1. Which issues were the easiest to fix, and which were the hardest? Why?

**Easiest:** the Flake8 style issues (E302/E305 blank lines, E501 long lines) and the Pylint conventions (docstrings, `assignDriver` → `assign_driver`, f-strings). They are mechanical, the message names the exact line, and fixing them can't change behaviour.

**Hardest:** the bare `except: pass` (Bandit B110 / Pylint W0702). Deleting it was easy, but it was hiding a real bug: R3's trip `"full"` made `average_load` raise a `TypeError` that was silently swallowed. Fixing it properly meant deciding what valid data looks like (non-negative integers), validating at the point of entry, and making `average_load` handle a route with no trips. The tool showed where the smell was, not what the right design was.

The R3 `KeyError` crash and the unknown-route crash were also hard in a different way: **no tool reported them**. I only found them by running the program, which the assignment README hints at.

## 2. Did the static analysis tools report any false positives? Describe one.

Partly. **Bandit B311** flags `random.choice` because the standard pseudo-random generator isn't safe for security purposes. Picking a shuttle driver isn't a security decision, so as a *security* finding it's a false positive here. But it still pointed at a real design problem: the function ignored its `route_id` argument and returned a different driver each run. I replaced it with a deterministic rota, which fixes both the Bandit finding and the Pylint unused-argument warning. Switching to `secrets.choice` would have silenced Bandit while keeping the bug.

Pylint **W0603 (global-statement)** isn't wrong, but code can need shared module state. Here the cleaner answer was to update the dictionary in place rather than suppress the warning.

## 3. How would you integrate static analysis into your development workflow?

- **In the editor:** run Flake8 and Pylint as I type, so style and simple bugs are fixed immediately.
- **Pre-commit hook:** run Flake8, Pylint (with a minimum score such as 9.5) and Bandit on changed files, so problems never reach the repository.
- **CI pipeline (e.g. GitHub Actions):** run all three tools on every push and pull request, and fail the build on any Bandit Medium/High finding, any Flake8 error or a Pylint score below the threshold. Save the reports as build artefacts.
- **Shared configuration:** keep the rules in a project config file (`setup.cfg` / `pyproject.toml`) so the whole team uses the same rules. Allow `# nosec` / `# pylint: disable` only with a written reason.
- **Alongside tests:** static analysis doesn't replace running the code. Unit tests for edge cases (negative counts, removed routes, unknown input) would have caught the crashes the tools missed.

## 4. What tangible improvements did you observe after applying the fixes?

- **Correctness:**
  - Bad data (`-6`, `"full"`) is now rejected with a clear `Rejected: …` message instead of corrupting averages or being silently skipped.
  - R2's average is no longer distorted by the negative trip.
- **Robustness:** the program no longer crashes. Before, it always ended with `KeyError: 'R3'`, and any unknown route lookup also crashed. Now it finishes and lists the available routes.
- **Predictability:**
  - Each route always gets the same driver.
  - Each call to `add_trip_log` gets its own log list instead of one shared list that keeps growing.
- **Resource safety:** files are closed reliably and use an explicit UTF-8 encoding.
- **Readability and maintainability:** docstrings on every function, PEP 8 layout, consistent naming, no hidden `global`, and the module can be imported without running.
- **Measured quality:** Pylint 6.25 → **10.00/10**, Bandit 2 → **0**, Flake8 10 → **0**.
