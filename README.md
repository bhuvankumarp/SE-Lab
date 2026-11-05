# SE-Lab

**Course:** Software Engineering Lab

**Student Name:** BHUVAN KUMAR P | **SRN:** PES1UG24AM069

Software Engineering lab work covering Labs 1–5, including completed experiments, source files and relevant documentation.

## Contents

| Folder | Lab | Contents |
|---|---|---|
| [Lab-1](Lab-1) | Requirements Engineering & UML Use-Case Modelling (Problem Statement #14) | Lab 1 report |
| [Lab-2](Lab-2) | Agile Planning in Jira (Problem Statement #14) | Individual report for Epic KAN-4 *Wellness Dashboard & Reports*, plus backlog, story point, sprint board and burndown images |
| [Lab-3](Lab-3) | Component Modelling & Architectural Pattern Selection (Problem Statement #14) | UML component diagram and one-page architecture justification |
| [Lab-4](Lab-4) | VibeCoding: Catch the Falling Objects (assigned repo `SETAPESU26/07_catch_falling`) | Updated code, before/after videos, chat history |
| [Lab-5](Lab-5) | Static Code Analysis: Campus Shuttle Tracker (assigned repo `SETAPESU26/L5_07_campus_shuttle`) | Cleaned code, before/after Pylint/Bandit/Flake8 reports, issue table, reflection |

Labs 1 to 3 cover **Problem Statement #14, Corporate Mental Wellness & Counseling Platform**: an anonymous counselling portal where employees check their stress levels, book confidential sessions with a licensed therapist and follow their own wellness indicators, without the employer learning who used it.

## Labs at a glance

- **Lab 1:** 5 functional and 2 non-functional requirements with measurable acceptance criteria, 6 actors, 13 use cases with «include»/«extend» relationships, a use-case diagram, and the use-case flow for UC-04 *View Wellness Trend Dashboard*.
- **Lab 2:** my unique Epic, KAN-4 *Wellness Dashboard & Reports* (FR-004, NFR-002), broken into 7 user stories (29 story points), with a 21-point Sprint 1, a sprint board, a burndown chart and reflection answers.
- **Lab 3:** Microservices architecture chosen for the platform, shown as a UML component diagram (ball-and-socket interfaces) with a written justification covering two reasons, a security advantage and a performance benefit.
- **Lab 4:** fixed the collision bug in a Pygame game and added basket boundary handling, controlled spawning and a temporary speed boost.
- **Lab 5:** analysed `shuttle_system.py` with Pylint, Bandit and Flake8 and fixed 14 documented issues (plus runtime crashes no tool flagged): Pylint 6.25 → 10.00/10, Bandit 2 → 0, Flake8 10 → 0.

## Tools and technologies

| Lab | Tools |
|---|---|
| Lab 1 | UML use-case modelling, Microsoft Word |
| Lab 2 | Jira Software, Atlassian connector in Claude Code, Microsoft Word |
| Lab 3 | UML component diagram (SVG exported to PNG/PDF), Microsoft Word |
| Lab 4 | Python 3, Pygame 2, Claude Code (AI pair-programming) |
| Lab 5 | Python 3, Pylint, Bandit, Flake8 |

## Navigating and running

Each lab folder has its own `README.md`. Documents are Word (`.docx`), PDF, PNG or SVG files. Lab 4 is the only lab with runnable code:

```bash
cd Lab-4/catch-falling
pip install -r requirements.txt
python main.py
```

## Acknowledgements

- Lab handouts and the Lab 4 starter game (`SETAPESU26/07_catch_falling`) are provided by the course.
- The Lab 1 report builds on the Team 14 (Helping Hands Software) shared report template; see [Lab-1/README.md](Lab-1/README.md).
- Claude Code (Anthropic) was used as the AI assistant where noted in each lab.
