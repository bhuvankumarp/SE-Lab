"""
Spawner: decides when and where new falling objects appear.

- Varied timing: the gap between spawns is random within a range.
- Varied, safe positions: x is always inside the playable area and is kept
  away from recent spawn points so objects don't stack in one spot.
- Capped: no new object spawns while the screen already holds the maximum.
"""

import random

from game.falling_object import FallingObject

MIN_SPAWN_INTERVAL = 30      # frames (0.5 s at 60 FPS)
MAX_SPAWN_INTERVAL = 75      # frames (1.25 s)
MAX_OBJECTS_ON_SCREEN = 6
MIN_SPAWN_GAP = 90           # px between a new spawn and recent spawns
RECENT_SPAWNS_REMEMBERED = 3
OBJECT_RADIUS = 14


class Spawner:
    def __init__(self, screen_width, rng=None):
        self.screen_width = screen_width
        self.rng = rng or random
        self.recent_x = []
        self.frames_until_spawn = 0

    def _pick_x(self):
        margin = OBJECT_RADIUS + 6
        lo, hi = margin, self.screen_width - margin
        positions = range(lo, hi + 1)

        def gap(x):
            return min((abs(x - r) for r in self.recent_x), default=self.screen_width)

        allowed = [x for x in positions if gap(x) >= MIN_SPAWN_GAP]
        if allowed:
            return self.rng.choice(allowed)
        return max(positions, key=gap)  # no free spot: use the one furthest from recent spawns

    def update(self, objects):
        """Call once per frame; returns a new FallingObject or None."""
        self.frames_until_spawn -= 1
        if self.frames_until_spawn > 0:
            return None
        if len(objects) >= MAX_OBJECTS_ON_SCREEN:
            self.frames_until_spawn = 10  # screen is full: check again shortly
            return None
        x = self._pick_x()
        self.recent_x = (self.recent_x + [x])[-RECENT_SPAWNS_REMEMBERED:]
        self.frames_until_spawn = self.rng.randint(MIN_SPAWN_INTERVAL, MAX_SPAWN_INTERVAL)
        return FallingObject(x=x, y=-OBJECT_RADIUS, radius=OBJECT_RADIUS, speed=3)
