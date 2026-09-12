"""
ISPPV1 2023
Study Case: Match-3

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class Tile.
"""

import pygame

import settings

from gale.timer import Timer


class Tile:
    def __init__(self, i: int, j: int, color: int, variety: int, powerup_type: int = 0) -> None:
        self.i = i
        self.j = j
        self.x = self.j * settings.TILE_SIZE
        self.y = self.i * settings.TILE_SIZE
        self.color = color
        self.variety = variety
        self.powerup_type = powerup_type
        self.blink_visible = True
        
        if self.powerup_type > 0:
            def toggle_blink():
                self.blink_visible = not self.blink_visible
            Timer.every(0.5, toggle_blink)
            
        self.alpha_surface = pygame.Surface(
            (settings.TILE_SIZE, settings.TILE_SIZE), pygame.SRCALPHA
        )


        

    def render(self, surface: pygame.Surface, offset_x: int, offset_y: int) -> None:
        self.alpha_surface.blit(
            settings.TEXTURES["tiles"],
            (0, 0),
            settings.FRAMES["tiles"][self.color][self.variety],
        )
        pygame.draw.rect(
            self.alpha_surface,
            (34, 32, 52, 200),
            pygame.Rect(0, 0, settings.TILE_SIZE, settings.TILE_SIZE),
            border_radius=7,
        )
        surface.blit(self.alpha_surface, (self.x + 2 + offset_x, self.y + 2 + offset_y))
        surface.blit(
            settings.TEXTURES["tiles"],
            (self.x + offset_x, self.y + offset_y),
            settings.FRAMES["tiles"][self.color][self.variety],
        )

        # Blinking overlay for power-ups
        if self.powerup_type == 1 and self.blink_visible:
            overlay = pygame.Surface((settings.TILE_SIZE, settings.TILE_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(overlay, (255, 0, 0, 100), pygame.Rect(0, 0, settings.TILE_SIZE, settings.TILE_SIZE), border_radius=4)
            surface.blit(overlay, (self.x + offset_x, self.y + offset_y))
        elif self.powerup_type == 2 and self.blink_visible:
            overlay = pygame.Surface((settings.TILE_SIZE, settings.TILE_SIZE), pygame.SRCALPHA)
            pygame.draw.rect(overlay, (0, 191, 255, 100), pygame.Rect(0, 0, settings.TILE_SIZE, settings.TILE_SIZE), border_radius=4)
            surface.blit(overlay, (self.x + offset_x, self.y + offset_y))
