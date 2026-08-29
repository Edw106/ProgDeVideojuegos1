import random
from typing import Optional, List
from abc import ABC, abstractmethod

import settings
from src.LogPair import LogPair
from gale.factory import Factory



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
    def update(self, dt: float, logs: List[LogPair]) -> None:
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
