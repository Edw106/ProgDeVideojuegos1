import pygame
import random
import settings
from src.world.Room import Room
from src.Boss import Boss
from src.definitions.entity import ENTITY_DEFS
from src.states.entity.EntityIdleState import EntityIdleState
from src.world.Doorway import Doorway
from src.Boss import Boss

class BossRoom(Room):
    def __init__(self, player, on_game_over, entry_direction="bottom"):
        # We don't spawn chest in boss room
        super().__init__(player, on_game_over, False)
        
        # Override doorways: only one door (the entry door)
        # We need to know which way the player came from. 
        # Wait, if player moved UP to enter, the entry door is BOTTOM.
        self.doorways = [Doorway(entry_direction, False, self)]
        self._doorways_by_direction = {
            doorway.direction: doorway for doorway in self.doorways
        }
        
        self.enemy_projectiles = []
        
    def _generate_entities(self) -> None:
        self.entities = []
        # Spawn Boss at the opposite side of the room
        bx = settings.MAP_RENDER_OFFSET_X + settings.MAP_WIDTH * settings.TILE_SIZE / 2
        by = settings.MAP_RENDER_OFFSET_Y + settings.MAP_HEIGHT * settings.TILE_SIZE / 2
        
        definition = ENTITY_DEFS["skeleton"]
        # Copy animation defs to avoid mutating the original definition
        import copy
        anim_defs = copy.deepcopy(definition["animations"])
        anim_defs["vulnerable"] = {
            "frames": [11, 35, 47, 23],
            "interval": 0.15,
            "texture": "entities"
        }
        
        boss = Boss(
            player=self.player,
            room=self,
            x=bx,
            y=by,
            width=16,
            height=16,
            walk_speed=20,
            health=300,
            animation_defs=anim_defs,
            states={}
        )
        from src.states.entity.EntityWalkState import EntityWalkState
        from src.Boss import BossVulnerableState
        boss.state_machine.states = {
            "idle": lambda sm, e=boss: EntityIdleState(e, sm),
            "walk": lambda sm, e=boss: EntityWalkState(e, sm),
            "vulnerable": lambda sm, e=boss: BossVulnerableState(e, sm),
        }
        boss.change_state("idle")
        self.entities.append(boss)
        
    def _generate_objects(self) -> None:
        # No objects (pots, switches) in the boss room
        self.objects = []
        
    def update(self, dt: float) -> None:
        super().update(dt)
        
        boss_alive = any(isinstance(e, Boss) for e in self.entities)
        if not boss_alive and not getattr(self, "boss_defeated_handled", False):
            self.boss_defeated_handled = True
            for doorway in self.doorways:
                doorway.open = True
            settings.SOUNDS["door"].play()
            
        
                        
        # Fireball collisions
        for proj in list(self.enemy_projectiles):
            proj.update(dt)
            if not proj.dead and proj.collides(self.player):
                if not self.player.invulnerable:
                    # Instant death
                    self.player.health = 0
                    self.on_game_over()
                proj.dead = True
                
            if proj.dead:
                self.enemy_projectiles.remove(proj)
                
    def render(self, surface: pygame.Surface, camera_offset_x: float = 0, camera_offset_y: float = 0) -> None:
        super().render(surface, camera_offset_x, camera_offset_y)
        for proj in self.enemy_projectiles:
            proj.render(surface, camera_offset_x, camera_offset_y)
