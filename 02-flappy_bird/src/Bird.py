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
    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        self.x: float = x
        self.y: float = y
        self.width: float = width
        self.height: float = height
        self.vy: float = 0.0
        self.jumping: bool = False

    def get_rect(self) -> pygame.Rect:
        #tolerance
        tol_x = self.width * 0.15
        tol_y = self.height * 0.15
        return pygame.Rect(round(self.x + tol_x), round(self.y + tol_y), self.width - 2 * tol_x, self.height - 2 * tol_y)

    def jump(self) -> None:
        self.jumping = True

    def update(self, dt: float) -> None:
        self.vy += settings.GRAVITY * dt

        if self.jumping:
            settings.SOUNDS["jump"].play()
            self.vy = -settings.JUMP_TAKEOFF_SPEED
            self.jumping = False

        self.y += self.vy * dt

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(settings.TEXTURES["bird"], self.get_rect())
