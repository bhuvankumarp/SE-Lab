"""
renderer: all pygame drawing lives here, kept separate from game logic.
"""

import pygame

WIDTH, HEIGHT = 700, 500
WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (25, 30, 45)
COLOR_BASKET = (150, 110, 70)
COLOR_BASKET_BOOST = (80, 220, 255)
COLOR_BOOST = (80, 220, 255)
COLOR_MUTED = (150, 160, 180)
COLOR_TEXT = (255, 255, 255)


def draw_scene(surface, basket, objects):
    surface.fill(COLOR_BG)
    for obj in objects:
        pygame.draw.circle(surface, obj.color, (int(obj.x), int(obj.y)), obj.radius)
    rect = basket.get_rect()
    if basket.is_boosted:
        # Glow behind the basket while the boost is active.
        pygame.draw.rect(surface, (40, 110, 140), rect.inflate(14, 10), border_radius=10)
    pygame.draw.rect(surface, COLOR_BASKET_BOOST if basket.is_boosted else COLOR_BASKET,
                     rect, border_radius=6)


def draw_text(surface, font, text, pos, color=COLOR_TEXT):
    surface.blit(font.render(text, True, color), pos)


def draw_boost_status(surface, font, basket):
    """Top-right boost indicator: active timer bar, cooldown, or ready."""
    from game.basket import BOOST_DURATION_FRAMES
    if basket.is_boosted:
        text, color = f"BOOST x2  {basket.boosted_frames / 60:.1f}s", COLOR_BOOST
    elif basket.boost_cooldown > 0:
        text, color = f"Boost in {basket.boost_cooldown / 60:.1f}s", COLOR_MUTED
    else:
        text, color = "Boost ready: SPACE", COLOR_TEXT
    label = font.render(text, True, color)
    # Right-align against the window edge so the text never gets clipped,
    # whatever font pygame falls back to.
    x = surface.get_width() - label.get_width() - 10
    surface.blit(label, (x, 10))
    if basket.is_boosted:
        w = label.get_width()
        frac = basket.boosted_frames / BOOST_DURATION_FRAMES
        pygame.draw.rect(surface, (60, 70, 90), (x, 38, w, 8), border_radius=4)
        pygame.draw.rect(surface, COLOR_BOOST, (x, 38, int(w * frac), 8), border_radius=4)


def draw_banner(surface, font, text):
    surf = font.render(text, True, (255, 220, 80))
    rect = surf.get_rect(center=(surface.get_width() // 2, surface.get_height() // 2))
    surface.blit(surf, rect)
