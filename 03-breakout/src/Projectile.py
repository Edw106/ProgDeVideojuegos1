from typing import Any
import pygame
import settings


class Projectile:
    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y
        self.width = 4
        self.height = 4
        self.vx = 0
        self.vy = -200
        self.active = True

    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def collides(self, obj: Any) -> bool:
        return self.get_collision_rect().colliderect(obj.get_collision_rect())

    def update(self, dt: float) -> None:
        if self.y + self.height < 0:
            self.active = False
        else:
            self.y += self.vy * dt

    def render(self, surface: pygame.Surface) -> None:
        if self.active:
            pygame.draw.rect(
                surface, (255, 255, 255), (self.x, self.y, self.width, self.height)
            )
