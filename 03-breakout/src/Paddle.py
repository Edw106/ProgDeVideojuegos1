"""
ISPPV1 2023
Study Case: Breakout

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class Paddle.
"""

import pygame
from typing import Any

import settings

from .EventManager import EventManager


class Paddle(EventManager):
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.width = 64
        self.height = 16

        # By default, the blue paddle
        self.skin = 0

        # By default, the 64-pixels-width paddle.
        self.size = 1

        self.texture = settings.TEXTURES["spritesheet"]
        self.frames = settings.FRAMES["paddles"]

        # The paddle only move horizontally
        self.vx = 0
        self._can_catch = False
        self.active_catch_powerups = []

    def can_catch(self) -> bool:
        return self._can_catch

    def set_can_catch(self, can_catch: bool) -> None:
        self._can_catch = can_catch

    def on_event(self, event: Any) -> None:
        if hasattr(event, "get_name") and event.get_name() == "CatchBall":
            if getattr(event, "using", False):
                if event not in self.active_catch_powerups:
                    self.active_catch_powerups.append(event)
                self.set_can_catch(True)
            else:
                if event in self.active_catch_powerups:
                    self.active_catch_powerups.remove(event)
                self.active_catch_powerups = [
                    p for p in self.active_catch_powerups if getattr(p, "using", False)
                ]
                if not self.active_catch_powerups:
                    self.set_can_catch(False)
        elif event == "POWERUP: CatchBall":
            self.set_can_catch(True)
        elif event in ("POWERUP_DEACTIVATE: CatchBall", "POWERUP_EXPIRED: CatchBall", "POWERUP_FINISHED: CatchBall"):
            self.active_catch_powerups = [
                p for p in self.active_catch_powerups if getattr(p, "using", False)
            ]
            if not self.active_catch_powerups:
                self.set_can_catch(False)

    def resize(self, size: int) -> None:
        self.size = size
        self.width = (self.size + 1) * 32

    def dec_size(self):
        self.resize(max(0, self.size - 1))

    def inc_size(self):
        self.resize(min(3, self.size + 1))

    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, dt: float) -> None:
        next_x = self.x + self.vx * dt

        if self.vx < 0:
            self.x = max(0, next_x)
        else:
            self.x = min(settings.VIRTUAL_WIDTH - self.width, next_x)

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self.texture, (self.x, self.y), self.frames[self.skin][self.size])
