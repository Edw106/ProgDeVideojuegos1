import random
from typing import Optional, List
from abc import ABC, abstractmethod

import settings
from src.GhostPowerUp import GhostPowerUp
from gale.factory import Factory



class GhostSpawnStrategy(ABC):
    def __init__(self) -> None:
        self.ghost_power_up_factory: Factory = Factory(GhostPowerUp)
        self.time_to_spawn : float = 0.0
        self.spawn_timer: float = 0.0

    @abstractmethod
    def update(self, dt: float, ghosts: List[GhostPowerUp]) -> None:
        pass

    @abstractmethod
    def try_spawn(self):
        pass

    


class HardGhostSpawnStrategy(GhostSpawnStrategy):
    def __init__(self) -> None:
        super().__init__()
        self._new_time_to_spawn()
        self.time_to_spawn = 0
        self.probability = 0.1

    def _new_time_to_spawn(self) -> None:
        self.time_to_spawn = random.uniform(4, 7)
     
    def update(self, dt: float, ghosts: List[GhostPowerUp]) -> None:
        """self.spawn_timer += dt
        if self.spawn_timer >= self.time_to_spawn:
            self.spawn_timer = 0.0
            self._new_time_to_spawn()
            y = random.randint(0, settings.VIRTUAL_HEIGHT)

            retry = True
            while retry:
                ghosts.append(self.ghost_power_up_factory.create(settings.VIRTUAL_WIDTH, y))
                retry = False"""

    def try_spawn(self, y: float, ghosts: List[GhostPowerUp], x_offset: Optional[float] = 0) -> None:
        if(random.random() < self.probability):
            ghosts.append(self.ghost_power_up_factory.create(settings.VIRTUAL_WIDTH + x_offset, y))

 
            