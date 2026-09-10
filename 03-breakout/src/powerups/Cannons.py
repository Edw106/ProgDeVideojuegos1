from typing import TypeVar, Any
import pygame
from gale.timer import Timer

import settings
from src.powerups.PowerUp import PowerUp


class Cannons(PowerUp):
    """
    Power-up to equip the paddle with cannons.
    """

    def __init__(self, x: int, y: int) -> None:
        # Power-up frame from the spritesheet
        super().__init__(x, y, 6)
        self.paddle_x = 0
        self.paddle_y = 0
        self.paddle_width = 0
        self.paddle_vx = 0

    def take(self, *args: Any, **kwargs: Any) -> None:
        super().take(*args, **kwargs)
        self.active = False
        self.using = True
        settings.SOUNDS["hurt"].stop()
        settings.SOUNDS["hurt"].play()
        Timer.after(7, self.finish)

    def on_event(self, event: Any, *args, **kwargs) -> None:
        super().on_event(event, *args, **kwargs)
        if event == "PADDLE_VELOCITY_CHANGE":
            self.paddle_vx = kwargs.get("vx", self.paddle_vx)
            self.paddle_x = kwargs.get("x", self.paddle_x)
            self.paddle_y = kwargs.get("y", self.paddle_y)
            self.paddle_width = kwargs.get("width", self.paddle_width)

    def get_name(self) -> str:
        return "Cannons"

    def update(self, dt: float) -> None:
        super().update(dt)
        if self.using:
            next_x = self.paddle_x + self.paddle_vx * dt
            if self.paddle_vx < 0:
                self.paddle_x = max(0, next_x)
            else:
                self.paddle_x = min(settings.VIRTUAL_WIDTH - self.paddle_width, next_x)

    def render(self, surface: pygame.Surface) -> None:
        if self.active:
            super().render(surface)
        elif self.using:
            cannon_texture = settings.TEXTURES["cannon"]
            c_width = cannon_texture.get_width()
            c_height = cannon_texture.get_height()
            # Render left cannon
            surface.blit(cannon_texture, (self.paddle_x, self.paddle_y - c_height))
            # Render right cannon
            surface.blit(cannon_texture, (self.paddle_x + self.paddle_width - c_width, self.paddle_y - c_height))

    def pause(self) -> None:
        Timer.pause()

    def resume(self) -> None:
        Timer.resume()

    def finish(self) -> None:
        super().finish()
        settings.SOUNDS["hurt"].stop()
        settings.SOUNDS["hurt"].play()
