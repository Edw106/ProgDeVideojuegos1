"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class TitleScreenState.
"""

import pygame
from typing import Optional

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text

import settings
from src.Bird import Bird
from src.World import World


class PauseState(BaseState):
    def enter(self, 
              mode: Optional[str],
              world: World, 
              bird: Bird, 
              score: int) -> None:
        self.mode = mode
        self.world = world
        self.bird = bird
        self.score = score

    def update(self, dt: float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)
        self.bird.render(surface)
        render_text(
            surface,
            f"Score: {self.score}",
            settings.FONTS["flappy"],
            20,
            10,
            settings.COLOR_WHITE,
            shadowed=True,
        )
        render_text(
            surface,
            "Paused",
            settings.FONTS["flappy"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 2,
            settings.COLOR_WHITE,
            center=True,
            shadowed=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "pause" and input_data.pressed:
            self.state_machine.change(
                "count_down", 
                mode=self.mode,
                world=self.world, 
                update_world=False, 
                bird=self.bird,
                score=self.score)
