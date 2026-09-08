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
            play_state.release_caught_balls()
            settings.SOUNDS["hurt"].stop()
            settings.SOUNDS["hurt"].play()
            if timer in play_state.timers:
                play_state.timers.remove(timer)

        timer = Timer.after(5, deactivate)
        play_state.timers.append(timer)
