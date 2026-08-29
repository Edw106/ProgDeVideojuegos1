"""
Esta clase es la única que hereda de Game
Reproduce la música

Ésta tiene a statemachine, donde debes guardar los estados correspondientes 
(previamente definidos en states)

update, render y on_input son los de la state machine (casi completamente)

"""

import pygame

from gale.game import Game
from gale.input_handler import InputData
from gale.state import StateMachine

import settings
from src import states


class FlappyBird(Game):
    def init(self) -> None:
        pygame.mixer.music.play(loops=-1)
        self.state_machine = StateMachine(
            {
                "title": states.TitleScreenState,
                "count_down": states.CountDownState,
                "playing": states.PlayingState,
                "pause": states.PauseState
            }
        )
        self.state_machine.change("title")

    def update(self, dt: float) -> None:
        self.state_machine.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        surface.fill(settings.COLOR_BACKGROUND)
        self.state_machine.render(surface)

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "quit" and input_data.pressed:
            self.quit()
        else:
            self.state_machine.on_input(input_id, input_data)
