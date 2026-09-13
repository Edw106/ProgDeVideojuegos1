"""
This file contains the class PlayerChestRewardState.
"""

from typing import Any, TypeVar

import pygame

from gale.state import StateMachine
from gale.timer import Timer

from src.states.entity.BaseEntityState import BaseEntityState
from settings import TEXTURES

class PlayerChestRewardState(BaseEntityState):
    def __init__(
        self,
        player: TypeVar("Player"),
        state_machine: StateMachine,
        dungeon: TypeVar("Dungeon"),
    ) -> None:
        super().__init__(player, state_machine)
        self.dungeon = dungeon
        self.bow_image = TEXTURES["bow"]
        self.chest = None
        self.show_bow = False

    def enter(self, chest: Any) -> None:
        self.chest = chest
        # Chest state is already "open", so we just update the dungeon state
        self.dungeon.chest_opened = True
        self.entity.change_animation("chest-reward")
        self.show_bow = False
        
        # Schedule the state transition
        # First wait for the animation (agacharse y levantarse)
        # Then show the bow
        # Then go back to idle
        def show_item():
            self.show_bow = True
            
        def finish_reward():
            self.entity.has_bow = True
            self.entity.change_state("idle")
            
        # The chest-reward animation has 3 frames at 0.25 interval = 0.75 seconds. 
        # First two frames (agacharse/levantarse) take 0.5 seconds.
        Timer.after(0.5, show_item)
        Timer.after(2.5, finish_reward)

    def update(self, dt: float) -> None:
        self.entity.sword_requested = False
        self.entity.interact_requested = False
        # Do not allow movement
        pass

    def render(self, surface: pygame.Surface) -> None:
        anim = self.entity.current_animation
        self.entity.render_sprite(surface, anim.texture_id, anim.get_current_frame())
        
        if self.show_bow:
            # Render the bow above the player's head
            surface.blit(
                self.bow_image,
                (self.entity.x, self.entity.y - self.bow_image.get_height())
            )
