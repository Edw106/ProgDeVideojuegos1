"""
Renderiza world y letras
En el input pasa a countdown state
"""

import pygame
from typing import Optional

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text

import settings
from src.World import World


class SelectScreenState(BaseState):
    def enter(self, world: Optional[World] = None) -> None:
        self.current_menu_item = 1
        self.world = world if world is not None else World(mode=None)

    def update(self, dt: float) -> None:
        self.world.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)

        color_normal = settings.COLOR_WHITE if self.current_menu_item == 1 else settings.COLOR_GRAY
        color_hard = settings.COLOR_WHITE if self.current_menu_item == 2 else settings.COLOR_GRAY

        render_text(
            surface,
            "Select Mode",
            settings.FONTS["flappy"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 4,
            settings.COLOR_WHITE,
            center=True,
            shadowed=True,
        )
        render_text(
            surface,
            "Normal",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 2,
            color_normal,
            center=True,
            shadowed=True,
        )
        render_text(
            surface,
            "Hard",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH / 2,
            3 * settings.VIRTUAL_HEIGHT / 4 - settings.VIRTUAL_HEIGHT / 6,
            color_hard,
            center=True,
            shadowed=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "confirm" and input_data.pressed:
            if self.current_menu_item == 1:
                self.state_machine.change("count_down", mode = "normal")
            elif self.current_menu_item == 2:
                self.state_machine.change("count_down", mode = "hard")

        if (input_id == "up" or input_id == "down") and input_data.pressed:
            if self.current_menu_item == 1:
                self.current_menu_item = 2
                settings.SOUNDS["hurt"].play()
            elif self.current_menu_item == 2:
                self.current_menu_item = 1
                settings.SOUNDS["jump"].play()

