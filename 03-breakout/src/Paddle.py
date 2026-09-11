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
        super().__init__()
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
        self._vx = 0
        self._can_catch = False
        self.active_catch_powerups = 0

    @property
    def vx(self) -> float:
        return self._vx

    @vx.setter
    def vx(self, value: float) -> None:
        if self._vx != value:
            self._vx = value
            self.notify("PADDLE_VELOCITY_CHANGE", vx=self._vx, x=self.x, y=self.y, width=self.width)

    def can_catch(self) -> bool:
        return self._can_catch

    def set_can_catch(self, can_catch: bool) -> None:
        self._can_catch = can_catch

    def on_event(self, event: Any, *args, **kwargs) -> None:
        if event in ("POWERUP: CatchBall", "POWERUP_ACTIVATE: CatchBall"):
            self.active_catch_powerups += 1
            self.set_can_catch(True)
        elif event in ("POWERUP_DEACTIVATE: CatchBall", "POWERUP_FINISHED: CatchBall", "POWERUP_EXPIRED: CatchBall"):
            self.active_catch_powerups = max(0, self.active_catch_powerups - 1)
            if self.active_catch_powerups == 0:
                self.set_can_catch(False)
        elif event == "POWERUP: Cannons":
            self.notify("PADDLE_VELOCITY_CHANGE", vx=self._vx, x=self.x, y=self.y, width=self.width)

    def resize(self, size: int) -> None:
        self.size = size
        self.width = (self.size + 1) * 32
        self.notify("PADDLE_RESIZE", width=self.width, x=self.x)

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
        paddle_img = self.texture.subsurface(self.frames[self.skin][self.size]).copy()
        if self._can_catch:
            paddle_img.fill((60, 60, 0), special_flags=pygame.BLEND_RGB_ADD)
        surface.blit(paddle_img, (self.x, self.y))
