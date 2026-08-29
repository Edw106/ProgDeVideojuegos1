"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class World: the scrolling
background/ground, and the log pairs the bird must fly through.
"""

import random
from typing import List, Optional

import pygame

from gale.factory import Factory

import settings
from src.LogPair import LogPair

from abc import ABC, abstractmethod

class LogsSpawnStrategy(ABC):
    def __init__(self, logs_spawn_strategy: Optional['LogsSpawnStrategy'] = None) -> None: #Las autoreferencias entre comillas simples
        if logs_spawn_strategy == None:
            self.logs_spawn_timer: float = 0.0
            self.log_pair_factory: Factory = Factory(LogPair)
            self.last_log_y: float = -settings.LOG_HEIGHT + random.randint(0, 80) + 20
            #Guardo el ultimo Y para saber donde spawnear el siguiente LogPair
        else:
            self.logs_spawn_timer: float = logs_spawn_strategy.logs_spawn_timer
            self.log_pair_factory: Factory = logs_spawn_strategy.log_pair_factory
            self.last_log_y: float = logs_spawn_strategy.last_log_y

    @abstractmethod
    def update(self, dt: float) -> None:
        pass

class NormalLogsSpawnStrategy(LogsSpawnStrategy):
    def __init__(self, logs_spawn_strategy: Optional[LogsSpawnStrategy] = None) -> None:
        super().__init__(logs_spawn_strategy)
        self.y_offset = 60
        
     
    def update(self, dt: float, logs: List[LogPair]) -> None:
        self.logs_spawn_timer += dt

        if self.logs_spawn_timer >= settings.TIME_TO_SPAWN_LOGS:
            self.logs_spawn_timer = 0.0

            y: float = self.last_log_y + random.randint(-self.y_offset, self.y_offset)
            miny: float = -settings.LOG_HEIGHT + 10 #limite arriba
            maxy: float = settings.VIRTUAL_HEIGHT + 90 - settings.LOG_HEIGHT #limite abajo
            if(y < miny):
                y = miny
            if(y > maxy):
                y = maxy
 
            self.last_log_y = y
            logs.append(self.log_pair_factory.create(settings.VIRTUAL_WIDTH, y))


class World:
    def __init__(self, mode: Optional[str] = None) -> None:
        self.background_x: float = 0.0
        self.ground_x: float = 0.0

        self.mode: Optional[str] = mode
        self.logs_spawn_strategy: Optional[LogsSpawnStrategy] = None
        self.set_mode(mode)

        self.logs: List[LogPair] = []


    def set_mode(self, mode: Optional[str] = None) -> None:
        #Si existe no la vuelvo a instanciars
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
