import pygame
from typing import Any
from gale.stencil import Stencil

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
        
        # The key isn't active/collidable until it finishes emerging
        self.active = False 
        self.collidable = True
        self.collected = False

        # Create a stencil the size of our virtual screen
        self.stencil = Stencil((settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT))
        
    def on_collide(self, player: Any) -> None:
        pass

    def on_consume(self, player: Any) -> None:
        if self.active and not self.collected:
            self.collected = True
            self.game_level.on_key_collected()

    def render(self, surface: pygame.Surface, camera: Any) -> None:
        if self.collected:
            return
            
        # 1. Create a transparent surface the size of the screen
        key_surface = pygame.Surface((settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT), pygame.SRCALPHA)
        
        # 2. Draw the key onto this transparent surface (using DrawableMixin's logic)
        super().render(key_surface, camera)
        
        # 3. Create the stencil mask: we only want the key to be visible ABOVE the solid block
        # We calculate where the top of the block is on the screen right now
        block_screen_y = self.block_y - camera.y
        
        self.stencil.clear()
        # Draw a solid white rectangle covering the area ABOVE the block
        self.stencil.draw(lambda mask: pygame.draw.rect(
            mask, 
            (255, 255, 255, 255), 
            pygame.Rect(0, 0, settings.VIRTUAL_WIDTH, block_screen_y)
        ))
        
        # 4. Apply the stencil mask to the key_surface
        self.stencil.apply(key_surface)
        
        # 5. Finally, draw our masked key surface onto the main game surface
        surface.blit(key_surface, (0, 0))
