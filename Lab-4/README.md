# Lab 4: VibeCoding (Catch the Falling Objects)

**Student:** BHUVAN KUMAR P (PES1UG24AM069)

Assigned repo: [SETAPESU26/07_catch_falling](https://github.com/SETAPESU26/07_catch_falling) · AI tool: Claude (Claude Code)

## Objective

Use a VibeCoding tool to fix the broken starter game and add the features listed in its README. Record a 10-second video before and after the changes, and submit the code and chat history.

## Deliverables

| Deliverable | Location |
|---|---|
| a. Videos (before / after, 10 s each) | [Before_Video_Lab4_PES1UG24AM069.mp4](videos/Before_Video_Lab4_PES1UG24AM069.mp4), [After_Video_Lab4_PES1UG24AM069.mp4](videos/After_Video_Lab4_PES1UG24AM069.mp4) |
| b. Updated code | [catch-falling/](catch-falling) (the original assignment README is in [catch-falling/README.md](catch-falling/README.md)) |
| c. Chat history | [Chat_History_Lab4_PES1UG24AM069.pdf](Chat_History_Lab4_PES1UG24AM069.pdf) |

## What was fixed and added

1. **Task 1, collision bug:** `is_caught` (in `game/collision.py`) now also requires the object to have reached basket height. The catch loop in `game/game_engine.py` no longer removes items from the list it is iterating, so adjacent objects are both credited.
2. **Task 2, basket control:** `Basket.move()`/`clamp()` keep the whole basket on screen (the clamp accounts for its width), and eased velocity gives smooth, continuous movement while a key is held.
3. **Task 3, spawning:** new `game/spawner.py`. Objects spawn at random 30–75 frame intervals, x stays inside the playable area and at least 90 px from the last 3 spawns, and at most 6 objects are on screen.
4. **Task 4, speed boost:** SPACE doubles basket speed for 3 s, then it returns to normal automatically, followed by a 5 s cooldown. While active, the basket glows cyan and a BOOST timer bar shows in the top-right corner.

## Run

Requires Python 3.10+.

```bash
cd catch-falling
pip install -r requirements.txt
python main.py
```

**Controls:** Left/Right arrows move the basket, SPACE gives a speed boost, R restarts after game over.

## Expected behaviour (verified)

These were checked with scripted tests on this code (Pygame 2.6.1, Python 3.11, headless):
- An object directly above the basket at the top of the screen is **not** caught; one at basket height **is**; two adjacent catchable objects both score.
- Holding Left or Right for 400 frames keeps the basket fully inside the 700 px window.
- Over 2 minutes of play: 134 spawns, all x positions between 20 and 676, intervals of 30–75 frames, no two consecutive spawns within 90 px, and no spawn while 6 objects are on screen.
- SPACE raises basket speed from 5 to 10 for 3 s, then it returns to 5; SPACE during the cooldown is ignored.
- The game is over after 5 misses; press R to restart.
