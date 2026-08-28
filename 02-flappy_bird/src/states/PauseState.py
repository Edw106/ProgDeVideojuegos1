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
from src.World import World


class PauseState(BaseState):
    def enter(self, world: Optional[World] = None) -> None:
        self.world = World()

    def update(self, dt: float) -> None:
        self.world.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)
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
        if input_id == "confirm" and input_data.pressed:
            self.state_machine.change("PlayingState")
