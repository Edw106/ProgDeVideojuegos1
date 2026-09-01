"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class LogPair: a top log
(rendered flipped upside down) and a bottom log, LOGS_GAP pixels
apart, that scroll left together and score once the bird passes them.
"""

import pygame
import random

import settings
import gale.timer
import gale.animation
from .GhostPowerUp import GhostPowerUp


class LogPair:
    def __init__(self, x: float, y: float, moving: bool = False) -> None:
        self.x: float = x
        self.y: float = y
        self.scored: bool = False
        self.moving: bool = moving
        self.move_interval: float = random.uniform(1.0, 2.0)
        self.move_timer: float = 0.0
        self.opened: bool = True

    def get_top_rect(self) -> pygame.Rect:
        if self.opened:
            return pygame.Rect(round(self.x), round(self.y), settings.LOG_WIDTH, settings.LOG_HEIGHT)
        else:
            return pygame.Rect(round(self.x), round(self.y + settings.LOGS_GAP/2), settings.LOG_WIDTH, settings.LOG_HEIGHT)

    def get_bottom_rect(self) -> pygame.Rect:
        if self.opened:
            return pygame.Rect(
                round(self.x),
                round(self.y + settings.LOGS_GAP + settings.LOG_HEIGHT),
                settings.LOG_WIDTH,
                settings.LOG_HEIGHT,
            )
        else:
            return pygame.Rect(
                round(self.x),
                round(self.y + settings.LOGS_GAP/2 + settings.LOG_HEIGHT),
                settings.LOG_WIDTH,
                settings.LOG_HEIGHT,
            )

    def get_center_y(self):
        return self.y + settings.LOG_HEIGHT + settings.LOGS_GAP/2

    def collides(self, rect: pygame.Rect) -> bool:
        return self.get_top_rect().colliderect(rect) or self.get_bottom_rect().colliderect(rect)

    def update(self, dt: float) -> None:

        self.x += -settings.MAIN_SCROLL_SPEED * dt

        self.move_timer += dt
        if(self.moving and self.move_timer >= self.move_interval):
            self.move_timer = 0.0
            if self.opened:
                settings.SOUNDS["explosion"].play()
                self.close()
            else:
                self.open()

    def open(self) -> None:
        self.opened = True
    
    def close(self) -> None:
        self.opened = False


    def is_out_of_game(self) -> bool:
        return self.x < -settings.LOG_WIDTH

    def update_scored(self, rect: pygame.Rect) -> bool:
        if self.scored:
            return False

        if rect.left > self.x + settings.LOG_WIDTH:
            self.scored = True
            return True

        return False

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(settings.TEXTURES["log_inverted"], self.get_top_rect())
        surface.blit(settings.TEXTURES["log"], self.get_bottom_rect())
