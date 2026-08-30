"""
Tiene:
Posición en pantalla
Tamaño en pantalla
Velocidad vertical
Bool a ver si salta

Puede
Dar un rectangulo de pygame
Saltar

update:
cae si no salta
salta y luego cae si salta

render:
dibuja con surface.blit(...)
"""

import pygame

import settings


class Bird:
    def __init__(self, x: float, y: float, width: float, height: float, horizontal_movement: bool = False) -> None:
        self.x: float = x
        self.y: float = y
        self.width: float = width
        self.height: float = height
        self._vy: float = 0.0
        self.jumping: bool = False
        self._vx: float = 0.0

    def get_rect(self) -> pygame.Rect:
        #tolerance
        tol_x = self.width * 0.15
        tol_y = self.height * 0.15
        return pygame.Rect(round(self.x + tol_x), round(self.y + tol_y), self.width - 2 * tol_x, self.height - 2 * tol_y)

    def jump(self) -> None:
        self.jumping = True

    def move_left(self) -> None:
        self._vx = -settings.MAIN_SCROLL_SPEED

    def move_right(self) -> None:
        self._vx = settings.MAIN_SCROLL_SPEED

    def stop_x_movement(self) -> None:
        self._vx = 0

    def is_moving_left(self) -> None:
        return self._vx < 0
    
    def is_moving_right(self) -> None:
        return self._vx > 0
    

    def update(self, dt: float) -> None:
        self._vy += settings.GRAVITY * dt

        if self.jumping:
            settings.SOUNDS["jump"].play()
            self._vy = -settings.JUMP_TAKEOFF_SPEED
            self.jumping = False

        self.y += self._vy * dt
        if self.x >= 0 and self.x <= settings.VIRTUAL_WIDTH - self.width:
            self.x += self._vx * dt
        else:
            self._vx = 0.0
            self.x = max(0, min(self.x, settings.VIRTUAL_WIDTH - self.width))


    def render(self, surface: pygame.Surface) -> None:
        surface.blit(settings.TEXTURES["bird"], self.get_rect())
