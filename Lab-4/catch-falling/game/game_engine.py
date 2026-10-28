"""
GameEngine: owns the basket and all falling objects.

Catches require the object to reach basket height (Task 1), the basket
stays fully on screen with smooth movement (Task 2), spawning is handled
by game.spawner.Spawner (Task 3), and SPACE triggers a temporary basket
speed boost (Task 4).
"""

import pygame

from game.basket import Basket
from game.collision import is_caught
from game.renderer import WIDTH, HEIGHT
from game.spawner import Spawner

MAX_MISSES = 5


class GameEngine:
    def __init__(self):
        self.basket = Basket(x=WIDTH / 2, y=HEIGHT - 30)
        self.objects = []
        self.spawner = Spawner(WIDTH)
        self.score = 0
        self.misses = 0
        self.game_over = False

    def handle_input(self, keys_pressed):
        if self.game_over:
            return
        # Held keys are read every frame, so movement is continuous; holding
        # both arrows cancels out instead of favouring one direction.
        direction = int(bool(keys_pressed[pygame.K_RIGHT])) - int(bool(keys_pressed[pygame.K_LEFT]))
        self.basket.move(direction, WIDTH)

    def handle_keydown(self, key):
        if self.game_over and key == pygame.K_r:
            self.__init__()
        elif not self.game_over and key == pygame.K_SPACE:
            self.basket.activate_boost()

    def update(self):
        if self.game_over:
            return

        self.basket.update_boost()

        new_obj = self.spawner.update(self.objects)
        if new_obj is not None:
            self.objects.append(new_obj)

        for obj in self.objects:
            obj.update()

        # Collect every catch first, then rebuild the list, so removing one
        # object can never make the loop skip the object after it.
        basket_rect = self.basket.get_rect()
        caught = [obj for obj in self.objects if is_caught(basket_rect, obj)]
        if caught:
            self.score += len(caught)
            self.objects = [obj for obj in self.objects if obj not in caught]

        missed = [o for o in self.objects if o.is_past_bottom(HEIGHT)]
        if missed:
            self.objects = [o for o in self.objects if not o.is_past_bottom(HEIGHT)]
            self.misses += len(missed)
            if self.misses >= MAX_MISSES:
                self.game_over = True

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.basket, self.objects)
        renderer.draw_text(surface, font, f"Score: {self.score}", (10, 10))
        renderer.draw_text(surface, font, f"Misses: {self.misses}/{MAX_MISSES}", (10, 36))
        renderer.draw_boost_status(surface, font, self.basket)

        if self.game_over:
            renderer.draw_banner(surface, font, f"Game Over! Final score: {self.score}. Press R to restart.")
