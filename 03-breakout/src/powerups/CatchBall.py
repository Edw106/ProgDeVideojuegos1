from gale.timer import Timer

import settings
from src.powerups.PowerUp import PowerUp


class CatchBall(PowerUp):
    """
    Power-up to catch the ball with the paddle.
    """

    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 7)

    def take(self, *args, **kwargs) -> None:
        self.active = False
        self.using = True
        settings.SOUNDS["paddle_hit"].stop()
        settings.SOUNDS["paddle_hit"].play()
        self.notify(self)
        Timer.after(7, self.finish)

    def finish(self) -> None:
        settings.SOUNDS["hurt"].stop()
        settings.SOUNDS["hurt"].play()
        super().finish()

    def pause(self) -> None:
        Timer.pause()

    def resume(self) -> None:
        Timer.resume()

    def get_name(self) -> str:
        return "CatchBall"
