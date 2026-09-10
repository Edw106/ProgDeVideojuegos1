from typing import TypeVar, Any
import pygame

import settings
from src.powerups.PowerUp import PowerUp


class Cannons(PowerUp):
    """
    Power-up to equip the paddle with cannons.
    """
    _active_cannon = None # class-level variable, it belongs to the class itself, not to any instance

    def __init__(self, x: int, y: int) -> None:
        # Power-up frame from the spritesheet
        super().__init__(x, y, 6)
        self.paddle_x = 0
        self.paddle_y = 0
        self.paddle_width = 0
        self.paddle_vx = 0
        self.shots_fired = 0

    def take(self, *args: Any, **kwargs: Any) -> None:
        if Cannons._active_cannon is not None and Cannons._active_cannon is not self:
            Cannons._active_cannon.finish()
        Cannons._active_cannon = self

        super().take(*args, **kwargs)
        self.shots_fired = 0
        settings.SOUNDS["hurt"].stop()
        settings.SOUNDS["hurt"].play()

    def on_event(self, event: Any, *args, **kwargs) -> None:
        super().on_event(event, *args, **kwargs)
        if event == "PADDLE_VELOCITY_CHANGE":
            self.paddle_vx = kwargs.get("vx", self.paddle_vx)
            self.paddle_x = kwargs.get("x", self.paddle_x)
            self.paddle_y = kwargs.get("y", self.paddle_y)
            self.paddle_width = kwargs.get("width", self.paddle_width)
        elif event == "FIRE_CANNONS":
            if self.using and self.shots_fired < 3:
                self.shots_fired += 1
                c_width = settings.TEXTURES["cannon"].get_width()
                c_height = settings.TEXTURES["cannon"].get_height()
                left_x = self.paddle_x + c_width / 2 - 2
                left_y = self.paddle_y - c_height
                right_x = self.paddle_x + self.paddle_width - c_width / 2 - 2
                right_y = self.paddle_y - c_height
                self.notify("SPAWN_PROJECTILES", left_x=left_x, left_y=left_y, right_x=right_x, right_y=right_y)
                
                if self.shots_fired >= 3:
                    self.finish()

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
            surface.blit(cannon_texture, (self.paddle_x - c_width/2, self.paddle_y - c_height/2))
            # Render right cannon
            surface.blit(cannon_texture, (self.paddle_x + self.paddle_width - c_width/2, self.paddle_y - c_height/2))

    def pause(self) -> None:
        pass

    def resume(self) -> None:
        pass

    def finish(self) -> None:
        super().finish()
        if Cannons._active_cannon is self:
            Cannons._active_cannon = None
        settings.SOUNDS["hurt"].stop()
        settings.SOUNDS["hurt"].play()
