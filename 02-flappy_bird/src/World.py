"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class World: the scrolling
background/ground, and the log pairs the bird must fly through.
"""

from typing import List, Optional

import pygame

import settings
from src.LogPair import LogPair
from src.LogSpawnStrategy import *



class World:
    def __init__(self, mode: Optional[str] = None) -> None:
        self.background_x: float = 0.0
        self.ground_x: float = 0.0

        self.mode: Optional[str] = mode
        self.logs_spawn_strategy: Optional[LogsSpawnStrategy] = None
        self.set_mode(mode)

        self.logs: List[LogPair] = []

    def set_mode(self, mode: Optional[str] = None) -> None:
        #Si existe no la vuelvo a instanciar
        print(f"World mode: {mode}")
        if self.mode == mode:
            return

        self.mode = mode
        
        if mode == "normal":
            self.logs_spawn_strategy = NormalLogsSpawnStrategy() #Instanciado
        else:
            self.logs_spawn_strategy = None


    def collides(self, rect: pygame.Rect) -> bool:
        """Recibe un rectangulo y lo compara con los de los troncos"""
        if rect.bottom >= settings.VIRTUAL_HEIGHT:
            return True

        return any(log_pair.collides(rect) for log_pair in self.logs)

    def update_scored(self, rect: pygame.Rect) -> bool:
        return any(log_pair.update_scored(rect) for log_pair in self.logs)

    def update(self, dt: float) -> None:
        """Este tiene dos comportamientos"""
        if self.logs_spawn_strategy is not None:
            self.logs_spawn_strategy.update(dt, self.logs)

        self.background_x += -settings.BACK_SCROLL_SPEED * dt

        if self.background_x <= -settings.BACKGROUND_LOOPING_POINT:
            self.background_x = 0

        self.ground_x += -settings.MAIN_SCROLL_SPEED * dt

        if self.ground_x <= -settings.VIRTUAL_WIDTH:
            self.ground_x = 0

        for log_pair in self.logs:
            log_pair.update(dt)

        self.logs = [log_pair for log_pair in self.logs if not log_pair.is_out_of_game()]

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(settings.TEXTURES["background"], (round(self.background_x), 0))

        for log_pair in self.logs:
            log_pair.render(surface)

        surface.blit(
            settings.TEXTURES["ground"],
            (round(self.ground_x), settings.VIRTUAL_HEIGHT - settings.GROUND_HEIGHT),
        )
