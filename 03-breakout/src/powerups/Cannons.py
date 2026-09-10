"""
ISPPV1 2023
Study Case: Breakout

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the specialization of PowerUp for Cannons.
"""

from typing import TypeVar

import settings
from src.powerups.PowerUp import PowerUp


class Cannons(PowerUp):
    """
    Power-up to equip the paddle with cannons.
    """

    def __init__(self, x: int, y: int) -> None:
        # Power-up frame from the spritesheet
        super().__init__(x, y, 6)

    def take(self, *args, **kwargs) -> None:
        self.active = False
        settings.SOUNDS["paddle_hit"].stop()
        settings.SOUNDS["paddle_hit"].play()

    def get_name(self) -> str:
        return "Cannons"
