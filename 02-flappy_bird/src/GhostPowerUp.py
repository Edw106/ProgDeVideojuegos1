import pygame

from src.Bird import Bird
import settings

class GhostPowerUp:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.used = False

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(round(self.x), round(self.y), settings.POWER_UP_SIDE, settings.POWER_UP_SIDE)

    def collides(self, rect: pygame.Rect) -> bool:
        return self.get_rect().colliderect(rect)

    def update(self, dt: float) -> None:
        self.x += -settings.MAIN_SCROLL_SPEED * dt

    def use(self, bird: Bird) -> None:
        bird.power_up("ghost")
        self.used = True

    def render(self, surface: pygame.surface) -> None:
        texture = settings.TEXTURES["ghost"]
        surface.blit(texture, self.get_rect())