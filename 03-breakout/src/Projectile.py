"""
ISPPV1 2023
Study Case: Breakout

This file contains the Projectile class for the cannons power-up.
"""

import pygame
import settings


class Projectile:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.width = 4
        self.height = 10
        self.vy = -300
        self.active = True

    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, dt: float) -> None:
        self.y += self.vy * dt
        if self.y < 0:
            self.active = False

    def render(self, surface: pygame.Surface) -> None:
        # Draw a bright cyan/yellow rectangle for the projectile
        pygame.draw.rect(surface, (0, 255, 255), self.get_collision_rect())
