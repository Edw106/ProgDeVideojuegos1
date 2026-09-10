"""
ISPPV1 2023
Study Case: Breakout

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the base class PowerUp as an abstract class.
"""

from typing import TypeVar, Any

import pygame
from ..EventManager import EventManager

import settings


class PowerUp(EventManager):
    """
    The base power-up.
    """

    def __init__(self, x: int, y: int, frame: int) -> None:
        super().__init__()
        self.x = x
        self.y = y
        self.active = True
        self.using = False
        self.vy = 100
        self.frame = frame
        
    def take(self, *args: Any, **kwargs: Any) -> None:
        self.active = False
        self.using = True
        self.notify(f"POWERUP: {self.get_name()}")

    def finish(self) -> None:
        self.using = False
        self.notify(f"POWERUP_FINISHED: {self.get_name()}")

    def pause(self) -> None:
        pass

    def resume(self) -> None:
        pass

    def on_event(self, event: Any, *args, **kwargs) -> None:
        match event:
            case "PAUSE":
                self.pause()
            case "RESUME":
                self.resume()

    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, 16, 16)

    def collides(self, obj: Any) -> bool:
        return self.get_collision_rect().colliderect(obj.get_collision_rect())

    def update(self, dt: float) -> None:
        if self.y > settings.VIRTUAL_HEIGHT:
            self.active = False

        self.y += self.vy * dt

    def render(self, surface: pygame.Surface) -> None:
        if self.active:
            surface.blit(
                settings.TEXTURES["spritesheet"],
                (self.x, self.y),
                settings.FRAMES["powerups"][self.frame],
            )


    def get_name(self) -> str:
        raise NotImplementedError
