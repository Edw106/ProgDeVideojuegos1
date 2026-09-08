from typing import TypeVar

from gale.timer import Timer

import settings
from src.powerups.PowerUp import PowerUp


class CatchBall(PowerUp):
    """
    Power-up to catch the ball with the paddle.
    """

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 7)

    def take(self, play_state: TypeVar("PlayState")) -> None:
        self.active = False
        settings.SOUNDS["paddle_hit"].stop()
        settings.SOUNDS["paddle_hit"].play()
        play_state.paddle.set_can_catch(True)

        def deactivate():
            play_state.paddle.set_can_catch(False)
            settings.SOUNDS["hurt"].stop()
            settings.SOUNDS["hurt"].play()

        Timer.after(5, deactivate)
