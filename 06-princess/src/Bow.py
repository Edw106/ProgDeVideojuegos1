"""
Bow class that fires arrows.
"""

from src.Projectile import Projectile
from src.Arrow import Arrow

from gale.timer import Timer

class ArrowFactory:
    @staticmethod
    def create(x: float, y: float, direction: str) -> Arrow:
        return Arrow(x, y, direction)

class Bow:
    def __init__(self, dungeon) -> None:
        self.dungeon = dungeon
        self.can_fire = True
        
    def fire(self, x: float, y: float, direction: str) -> None:
        if not self.can_fire:
            return
            
        arrow_obj = ArrowFactory.create(x, y, direction)
        proj = Projectile(arrow_obj, direction)
        self.dungeon.current_room.projectiles.append(proj)
        
        self.can_fire = False
        Timer.after(2.0, self._reset_cooldown)
        
    def _reset_cooldown(self) -> None:
        self.can_fire = True
