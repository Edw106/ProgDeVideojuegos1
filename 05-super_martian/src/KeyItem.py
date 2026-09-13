import pygame
from typing import Any

import settings
from src import mixins


class KeyItem(mixins.DrawableMixin, mixins.CollidableMixin):
    def __init__(self, x: float, y: float, game_level: Any) -> None:
        self.x = x
        self.y = y
        self.width = 16
        self.height = 16
        self.texture_id = "key"
        self.frame_index = 0
        self.flipped = False
        
        self.game_level = game_level
        self.block_y = y  # original y (bottom of the spawn area), used for stencil
        
        # The key is active (rendered) immediately, but not collidable until it finishes emerging
        self.active = True 
        self.collidable = False
        self.collected = False
        
    def on_collide(self, player: Any) -> None:
        pass

    def on_consume(self, player: Any) -> None:
        if self.active and not self.collected:
            self.collected = True
            self.game_level.on_key_collected()

    def render(self, surface: pygame.Surface, camera: Any) -> None:
        if self.collected:
            return
            
        # Draw the key normally (it will render over the block because items are drawn after the tilemap)
        super().render(surface, camera)
