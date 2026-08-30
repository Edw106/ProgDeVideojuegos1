import random
from typing import Optional, List
from abc import ABC, abstractmethod

import settings
from src.GhostPowerUp import GhostPowerUp
from gale.factory import Factory



class GhostSpawnStrategy(ABC):
    def __init__(self) -> None:
        self.ghost_power_up_factory: Factory = Factory(GhostPowerUp)

    @abstractmethod
    def update(self, dt: float, logs: List[GhostPowerUp]) -> None:
        pass
    

class NormalGhostSpawnStrategy(GhostSpawnStrategy):
    def __init__(self) -> None:
        super().__init__()
        
     
    def update(self, dt: float, logs: List[GhostPowerUp]) -> None:
        self.logs_spawn_timer += dt

        if self.logs_spawn_timer >= settings.TIME_TO_SPAWN_LOGS:
            self.logs_spawn_timer = 0.0

            y: float = self.last_log_y + random.randint(-self.y_difference, self.y_difference)
            miny: float = -settings.LOG_HEIGHT + 10 #limite arriba
            maxy: float = -110 #limite abajo
            if(y < miny):
                y = miny
            if(y > maxy):
                y = maxy
 
            self.last_log_y = y
            logs.append(self.ghost_power_up_factory.create(settings.VIRTUAL_WIDTH, y))


class HardGhostSpawnStrategy(GhostSpawnStrategy):
    def __init__(self, ghost_spawn_strategy: Optional[GhostSpawnStrategy] = None) -> None:
        super().__init__(ghost_spawn_strategy)
        self.y_difference = 80
        self.last_log_y = -settings.LOG_HEIGHT + random.randint(0, 80) + 20
        self.variation = 0
        
     
    def update(self, dt: float, logs: List[GhostPowerUp]) -> None:
        self.logs_spawn_timer += dt
        self.current_time_to_spawn_logs = settings.TIME_TO_SPAWN_LOGS + self.variation
        if self.logs_spawn_timer >= self.current_time_to_spawn_logs:
            self.logs_spawn_timer = 0.0

            retry = True
            while retry:
                #variacion de tiempo en spawnear
                self.variation = random.uniform(-1, 1) #Recalculo

                #variacion de altura respecto a la cercanía
                """
                si el tiempo es el de dos troncos pegados, la variacion debe ser muy cercana a 0
                si los troncos estan separados como el tiempo normal, la variacion va a ser la declarada (60)
                si los troncos están al doble de distancia, la variacion es el doble, pero avanza linealmente
                """
                x_distance = settings.MAIN_SCROLL_SPEED * self.current_time_to_spawn_logs
                log_distance = settings.MAIN_SCROLL_SPEED * settings.TIME_TO_SPAWN_LOGS

                min_x = settings.LOG_WIDTH * 0.5
                normal_x = log_distance

                if x_distance <= min_x:
                    normalized_y_distance = 0.0
                elif x_distance <= normal_x*0.66:
                    normalized_y_distance = (x_distance - min_x) / (normal_x - min_x)# Interpolacion lineal
                    normalized_y_distance = normalized_y_distance**1.5 #vuelve la curva más suave
                else:
                    normalized_y_distance = ((x_distance - min_x) / (normal_x - min_x))
                    normalized_y_distance = normalized_y_distance**2.5 #vuelve la curva más agresiva

                

                
                #sacando el offset de y
                current_y_difference = int(normalized_y_distance * self.y_difference)

                
                y_offset = random.randint(
                    int(2*current_y_difference/3), 
                    current_y_difference) * random.choice([-1, 1])
                y: float = self.last_log_y + y_offset
                miny: float = -settings.LOG_HEIGHT + 10 #limite arriba
                maxy: float = -110 #limite abajo

                if(self.last_log_y - current_y_difference < miny and self.last_log_y + current_y_difference > maxy):
                    retry = False
                    if(y < miny):
                        y = miny
                    elif(y > maxy):
                        y = maxy
                elif(y < miny):
                    retry = True
                elif(y > maxy):
                    retry = True
                else:
                    retry = False
 
            self.last_log_y = y
            moving_log = random.random() < 0.3
            logs.append(self.ghost_power_up_factory.create(settings.VIRTUAL_WIDTH, y, {"moving": moving_log}))