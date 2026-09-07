"""
ISPPV1 2023
Study Case: Breakout

This file contains the specialization of PowerUp for the sticky paddle (catch).
"""

from typing import TypeVar

from src.powerups.PowerUp import PowerUp
from gale.timer import Timer

import settings


class StickyPowerUp(PowerUp):
    """
    Power-up to make the paddle sticky so it catches the ball.
    """

    def __init__(self, x: int, y: int) -> None:
        # Usamos el frame 4 para representarlo (puedes cambiarlo).
        super().__init__(x, y, 4)

    def take(self, play_state: TypeVar("PlayState")) -> None:
        paddle = play_state.paddle
        paddle.is_sticky = True

        # Desactivar después de 10 segundos usando gale.timer
        if hasattr(paddle, 'sticky_timer_item') and paddle.sticky_timer_item:
            paddle.sticky_timer_item.remove()

        def deactivate_sticky():
            paddle.is_sticky = False
            # Si hay pelotas pegadas al acabar el tiempo, se sueltan automáticamente.
            for ball in play_state.balls:
                if getattr(ball, 'is_attached', False):
                    ball.is_attached = False
                    ball.vy = -150

        paddle.sticky_timer_item = Timer.after(10, deactivate_sticky)

        settings.SOUNDS["paddle_hit"].stop()
        settings.SOUNDS["paddle_hit"].play()

        self.active = False
