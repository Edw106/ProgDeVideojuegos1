import settings
from src.powerups.PowerUp import PowerUp
from gale.timer import Timer

class FireBall(PowerUp):
    """
    Power-up to turn the balls into fireballs.
    """
    def __init__(self, x: int, y: int) -> None:
        super().__init__(x, y, 6)

    def take(self, *args, **kwargs) -> None:
        super().take(*args, **kwargs)
        settings.SOUNDS["hurt"].stop()
        settings.SOUNDS["hurt"].play()
        Timer.after(5, self.request_finish)

    def request_finish(self) -> None:
        self.notify("POWERUP_FINISHED_REQUEST: FireBall")
        self.finish()

    def get_name(self) -> str:
        return "FireBall"

    def pause(self) -> None:
        Timer.pause()

    def resume(self) -> None:
        Timer.resume()
