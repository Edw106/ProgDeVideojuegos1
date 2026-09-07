"""
ISPPV1 2023
Study Case: Breakout

This file contains the specialization of PowerUp for the fire ball.
"""

from typing import TypeVar
import random

from src.powerups.PowerUp import PowerUp
from gale.timer import Timer

import settings


class FireBallPowerUp(PowerUp):
    """
    Power-up to turn balls into fire balls that don't bounce off bricks.
    """

    def __init__(self, x: int, y: int) -> None:
        # Usamos otro frame para este power-up, por ejemplo el 6
        super().__init__(x, y, 6)

    def take(self, play_state: TypeVar("PlayState")) -> None:
        if hasattr(play_state, 'fireball_timer_item') and play_state.fireball_timer_item:
            play_state.fireball_timer_item.remove()

        for ball in play_state.balls:
            ball.is_fire = True
            ball.frame = 1  # 1 o 5 podrían ser el frame rojo, usemos 1 como ejemplo rojo
        
        play_state.is_fire_mode = True

        def deactivate_fireball():
            play_state.is_fire_mode = False
            for ball in play_state.balls:
                ball.is_fire = False
                ball.frame = random.randint(0, 6)

        play_state.fireball_timer_item = Timer.after(10, deactivate_fireball)

        settings.SOUNDS["paddle_hit"].stop()
        settings.SOUNDS["paddle_hit"].play()

        self.active = False
