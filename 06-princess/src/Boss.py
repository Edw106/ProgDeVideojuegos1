import math
import pygame
from gale.timer import Timer

import settings
from src.Entity import Entity

class Fireball:
    def __init__(self, x: float, y: float, dx: float, dy: float) -> None:
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.width = 8
        self.height = 8
        self.dead = False
        self.speed = 60 # slow fireballs

    def get_collision_rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, dt: float) -> None:
        if self.dead: return
        self.x += self.dx * self.speed * dt
        self.y += self.dy * self.speed * dt
        
        # Out of bounds check
        if (self.x < settings.MAP_RENDER_OFFSET_X or 
            self.x > settings.VIRTUAL_WIDTH - settings.MAP_RENDER_OFFSET_X or
            self.y < settings.MAP_RENDER_OFFSET_Y or
            self.y > settings.VIRTUAL_HEIGHT - settings.MAP_RENDER_OFFSET_Y):
            self.dead = True

    def render(self, surface: pygame.Surface, offset_x: float = 0, offset_y: float = 0) -> None:
        rect = pygame.Rect(self.x + offset_x, self.y + offset_y, self.width, self.height)
        pygame.draw.circle(surface, (255, 50, 50), rect.center, self.width // 2)

    def collides(self, target) -> bool:
        return self.get_collision_rect().colliderect(target.get_collision_rect())

from src.states.entity.BaseEntityState import BaseEntityState

class BossVulnerableState(BaseEntityState):
    def enter(self) -> None:
        self.entity.change_animation("vulnerable")
        
    def process_ai(self, room, dt: float) -> None:
        # Boss does not move or do AI logic while vulnerable
        pass
        
    def render(self, surface: pygame.Surface) -> None:
        anim = self.entity.current_animation
        self.entity.render_sprite(surface, anim.texture_id, anim.get_current_frame())

class Boss(Entity):
    def __init__(self, player, room, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player = player
        self.room = room
        self.sword_immune = True
        self.immunity_timer = None
        
        # Start firing loop
        Timer.after(3.0, self.fire)
        
    def fire(self):
        if self.dead:
            return
            
        # Do not fire if vulnerable
        if not self.sword_immune:
            Timer.after(3.0, self.fire)
            return
            
        dx = self.player.x - self.x
        dy = self.player.y - self.y
        length = math.hypot(dx, dy)
        if length > 0:
            dx /= length
            dy /= length
            
        fb = Fireball(self.x + self.width/2, self.y + self.height/2, dx, dy)
        self.room.enemy_projectiles.append(fb)
        
        Timer.after(3.0, self.fire)
        
    def damage(self, amount: int, is_arrow: bool = False) -> None:
        if self.sword_immune and not is_arrow:
            # play block sound if desired
            return
            
        if is_arrow and self.sword_immune:
            self.sword_immune = False
            self.change_state("vulnerable")
            # Vulnerable for 3 seconds
            if self.immunity_timer:
                self.immunity_timer.remove()
            self.immunity_timer = Timer.after(3.0, self._restore_immunity)
            settings.SOUNDS["hit-enemy"].play()
            return
            
        # Normal damage
        super().damage(amount)
        
    def _restore_immunity(self):
        self.sword_immune = True
        self.immunity_timer = None
        if not self.dead:
            self.change_state("idle")
