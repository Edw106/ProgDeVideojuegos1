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
from typing import Optional
from collections.abc import Callable


class Bird:
    def __init__(self, x: float, y: float, width: float, height: float, horizontal_movement: bool = False) -> None:
        self.x: float = x
        self.y: float = y
        self.width: float = width
        self.height: float = height
        self._vy: float = 0.0
        self.jumping: bool = False
        self._vx: float = 0.0

        #Hitboz tolerance
        self.tol_x = self.width * 0.15
        self.tol_y = self.height * 0.15

        self._is_ghost =  False
        self._ghost_timer = 0
        self._ghost_on_finish = None

    def is_ghost(self) -> None:
        return self._is_ghost

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def get_hurtbox(self) -> pygame.Rect:
        #si el pajaro es fantasma, no tenga hitbox
        if self._is_ghost:
            return pygame.Rect(0,0,0,0)

        return pygame.Rect(
            round(self.x + self.tol_x), 
            round(self.y + self.tol_y), 
            self.width - 2 * self.tol_x, 
            self.height - 2 * self.tol_y)
        

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

    def ghost_power_up(self, time: float, on_finish: Optional[Callable] = None) -> None:
        self._is_ghost = True
        self._ghost_timer = 0
        self._ghost_time = time
        self._ghost_on_finish = on_finish

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

        #actualiza el fantasma, el temporizador
        if self._is_ghost:
            self._ghost_timer += dt
            if self._ghost_timer >= self._ghost_time:
                self._is_ghost = False
                self._ghost_timer = 0
                if self._ghost_on_finish is not None:
                    self._ghost_on_finish()


    def render(self, surface: pygame.Surface) -> None:

        if(self._is_ghost):
            surface.blit(settings.TEXTURES["bird_ghost"], self.get_rect())
        else:
            surface.blit(settings.TEXTURES["bird"], self.get_rect())
