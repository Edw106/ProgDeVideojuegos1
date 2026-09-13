"""
Arrow class for the bow.
"""

import pygame
import settings

class Arrow:
    def __init__(self, x: float, y: float, direction: str) -> None:
        self.x = x
        self.y = y
        # The arrow might be a bit smaller than the tile size
        self.width = settings.TEXTURES["arrow"].get_width()
        self.height = settings.TEXTURES["arrow"].get_height()
        self.direction = direction

    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def render(self, surface: pygame.Surface, offset_x: float = 0, offset_y: float = 0) -> None:
        img = settings.TEXTURES["arrow"]
        # Assuming the base image faces right
        if self.direction == "left":
            img = pygame.transform.flip(img, True, False)
        elif self.direction == "up":
            img = pygame.transform.rotate(img, 90)
        elif self.direction == "down":
            img = pygame.transform.rotate(img, -90)
            
        surface.blit(img, (self.x + offset_x, self.y + offset_y))
