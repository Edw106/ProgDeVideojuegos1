"""
Crea un temporizador es 3, y lo baja hasta 1, luego cambia a playing state
"""

import pygame

from typing import Optional

from gale.state import BaseState
from gale.text import render_text

import settings
from src.World import World
from src.Bird import Bird


class CountDownState(BaseState):
    def enter(
            self, 
            world: Optional[World] = None,  
            update_world: bool = True,
            bird: Optional[Bird] = None,
            score: Optional[int] = None) -> None:
        self.world = world if world is not None else World(mode=None)
        self.update_world = update_world
        self.bird = bird
        self.score = score

        self.counter = 3
        self.timer = 0.0

    def update(self, dt: float) -> None:
        self.timer += dt

        if self.timer >= 1.0:
            self.timer = 0.0
            self.counter -= 1

            if self.counter == 0:
                self.state_machine.change(
                    "playing", 
                    world=self.world, 
                    bird=self.bird, 
                    score=self.score)
                return
        if self.update_world:
            self.world.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)

        if(self.bird != None):
            self.bird.render(surface)

        if(self.score != None):
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
            str(self.counter),
            settings.FONTS["huge"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 2,
            settings.COLOR_WHITE,
            center=True,
            shadowed=True,
        )
