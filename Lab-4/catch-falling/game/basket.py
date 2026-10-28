"""
Basket: the player-controlled catcher at the bottom of the screen.
"""

import pygame

# How quickly the basket's velocity eases toward the target speed each frame
# (0..1). High enough to feel responsive, low enough to avoid jerky starts/stops.
ACCELERATION = 0.35

BOOST_MULTIPLIER = 2.0
BOOST_DURATION_FRAMES = 180   # 3 s at 60 FPS
BOOST_COOLDOWN_FRAMES = 300   # 5 s before it can be used again


class Basket:
    def __init__(self, x, y, width=90, height=24, speed=5):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.velocity = 0.0
        self.boosted_frames = 0
        self.boost_cooldown = 0
        self.normal_speed = speed
        self.boost_speed = speed * BOOST_MULTIPLIER

    @property
    def is_boosted(self):
        return self.boosted_frames > 0

    def activate_boost(self):
        """Start a speed boost if one isn't running and the cooldown is over."""
        if self.is_boosted or self.boost_cooldown > 0:
            return False
        self.boosted_frames = BOOST_DURATION_FRAMES
        self.speed = self.boost_speed
        return True

    def update_boost(self):
        """Count the boost down once per frame; restore normal speed when it ends."""
        if self.boosted_frames > 0:
            self.boosted_frames -= 1
            if self.boosted_frames == 0:
                self.speed = self.normal_speed
                self.boost_cooldown = BOOST_COOLDOWN_FRAMES
        elif self.boost_cooldown > 0:
            self.boost_cooldown -= 1

    def move(self, direction, screen_width):
        """Move one frame. direction is -1 (left), 0 (none) or +1 (right)."""
        target = direction * self.speed
        self.velocity += (target - self.velocity) * ACCELERATION
        if direction == 0 and abs(self.velocity) < 0.1:
            self.velocity = 0.0
        self.x += self.velocity
        self.clamp(screen_width)

    def clamp(self, screen_width):
        """Keep the whole basket on screen, accounting for its own width."""
        half = self.width / 2
        if self.x < half or self.x > screen_width - half:
            self.x = max(half, min(screen_width - half, self.x))
            self.velocity = 0.0

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2), int(self.y - self.height / 2),
            self.width, self.height,
        )
