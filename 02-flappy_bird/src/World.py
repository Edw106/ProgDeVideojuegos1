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
from src.GhostSpawnStrategy import *
from src.Bird import Bird


class World:
    def __init__(self, mode: Optional[str] = None) -> None:
        self.background_x: float = 0.0
        self.ground_x: float = 0.0

        self.mode: Optional[str] = mode
        self.logs_spawn_strategy: Optional[LogsSpawnStrategy] = None
        self.ghosts_spawn_strategy: Optional[GhostSpawnStrategy] = None
        self.set_mode(mode)

        self.logs: List[LogPair] = []
        self.ghost_power_ups: List[GhostPowerUp] = []
        self.last_log_y = 0
        self.ghosts_probability = 0.1

    def set_mode(self, mode: Optional[str] = None) -> None:
        #Si existe no la vuelvo a instanciar
        if self.mode == mode:
            return

        self.mode = mode
        
        if mode == "normal":
            self.logs_spawn_strategy = NormalLogsSpawnStrategy() #Instanciado
            self.ghosts_spawn_strategy = None
        elif mode == "hard":
            self.logs_spawn_strategy = HardLogsSpawnStrategy()
            self.ghosts_spawn_strategy = HardGhostSpawnStrategy()
        else:
            self.logs_spawn_strategy = None
            self.ghosts_spawn_strategy = None


    def collides(self, rect: pygame.Rect) -> bool:
        """Recibe un rectangulo y lo compara con los de los troncos"""
        if rect.bottom >= settings.VIRTUAL_HEIGHT:
            return True

        return any(log_pair.collides(rect) for log_pair in self.logs)

    def update_scored(self, rect: pygame.Rect) -> bool:
        return any(log_pair.update_scored(rect) for log_pair in self.logs)

    def get_colliding_ghost_power_up(self, rect: pygame.Rect) -> Optional[GhostPowerUp]:
        for g in self.ghost_power_ups:
            if g.collides(rect):
                return g

        return None

                
    def update(self, dt: float) -> None:
        """Este tiene dos comportamientos"""
        if self.logs_spawn_strategy is not None:
            self.logs_spawn_strategy.update(dt, self.logs)


        if self.ghosts_spawn_strategy is not None:
            self.ghosts_spawn_strategy.update(dt, self.ghost_power_ups)

            if self.logs.__len__() != 0:
                if self.last_log_y != self.logs[-1]:
                    self.last_log_y = self.logs[-1]
                    if random.random() < self.ghosts_probability:
                        self.ghosts_spawn_strategy.spawn(
                            y = self.logs[-1].get_center_y() -settings.POWER_UP_SIDE/2, 
                            ghosts = self.ghost_power_ups,
                            x_offset = settings.LOG_WIDTH/2 - settings.POWER_UP_SIDE/2
                        )

        self.background_x += -settings.BACK_SCROLL_SPEED * dt

        if self.background_x <= -settings.BACKGROUND_LOOPING_POINT:
            self.background_x = 0

        self.ground_x += -settings.MAIN_SCROLL_SPEED * dt

        if self.ground_x <= -settings.VIRTUAL_WIDTH:
            self.ground_x = 0

        for log_pair in self.logs:
            log_pair.update(dt)
        self.logs = [log_pair for log_pair in self.logs if not log_pair.is_out_of_game()]

        for ghost in self.ghost_power_ups:
            ghost.update(dt)
        self.ghost_power_ups = [g for g in self.ghost_power_ups if not g.is_out_of_game() and not g.is_used()]

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(settings.TEXTURES["background"], (round(self.background_x), 0))

        for g in self.ghost_power_ups:
            g.render(surface)

        for log_pair in self.logs:
            log_pair.render(surface)

        surface.blit(
            settings.TEXTURES["ground"],
            (round(self.ground_x), settings.VIRTUAL_HEIGHT - settings.GROUND_HEIGHT),
        )
