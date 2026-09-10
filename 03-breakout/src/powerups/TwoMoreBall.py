"""
ISPPV1 2023
Study Case: Breakout

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the specialization of PowerUp to add two more ball to the game.
"""

import settings
from src.powerups.PowerUp import PowerUp


class TwoMoreBall(PowerUp):
    """
    Power-up to add two more ball to the game.
    """

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 8)

    def take(self, *args, **kwargs) -> None:
        super().take(*args, **kwargs)
        settings.SOUNDS["paddle_hit"].stop()
        settings.SOUNDS["paddle_hit"].play()
        self.finish()

    def get_name(self) -> str:
        return "TwoMoreBall"
