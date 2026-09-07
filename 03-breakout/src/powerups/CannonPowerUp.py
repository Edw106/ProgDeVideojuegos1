"""
ISPPV1 2023
Study Case: Breakout

This file contains the specialization of PowerUp for the cannons.
"""

from typing import TypeVar

from src.powerups.PowerUp import PowerUp
from gale.timer import Timer

import settings


class CannonPowerUp(PowerUp):
    """
    Power-up to add cannons to the paddle.
    """

    def __init__(self, x: int, y: int) -> None:
        # Usamos otro frame para este power-up, por ejemplo el 5
        super().__init__(x, y, 5)

    def take(self, play_state: TypeVar("PlayState")) -> None:
        paddle = play_state.paddle
        paddle.has_cannons = True

        if hasattr(paddle, 'cannon_timer_item') and paddle.cannon_timer_item:
            paddle.cannon_timer_item.remove()

        def deactivate_cannons():
            paddle.has_cannons = False

        paddle.cannon_timer_item = Timer.after(10, deactivate_cannons)

        settings.SOUNDS["paddle_hit"].stop()
        settings.SOUNDS["paddle_hit"].play()

        self.active = False
