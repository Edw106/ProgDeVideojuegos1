from abc import ABC, abstractmethod
from gale.input_handler import InputData
import settings
from src.Bird import Bird

class BirdMovingStrategy(ABC):
    def __init__(self, bird: Bird) -> None:
        self.bird = bird

    @abstractmethod
    def on_input(self, input_id: str, input_data: InputData) -> None:
        pass

class StaticBirdMovingStrategy(BirdMovingStrategy):
    def __init__(self, bird: Bird) -> None:
        super().__init__(bird)

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "jump" and input_data.pressed:
            self.bird.jump()

class HorizontalBirdMovingStrategy(BirdMovingStrategy):
    def __init__(self, bird: Bird) -> None:
        super().__init__(bird)

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "jump" and input_data.pressed:
            self.bird.jump()

        bird = self.bird
        
        if input_id in ("left", "right"):
            if input_data.pressed:
                bird.vx = (
                    -settings.MAIN_SCROLL_SPEED if input_id == "left" else settings.MAIN_SCROLL_SPEED*1.3
                )
            elif input_data.released:
                sign = -1 if input_id == "left" else 1
                if bird.vx == sign * settings.MAIN_SCROLL_SPEED:
                    bird.vx = 0
                elif bird.vx == sign * settings.MAIN_SCROLL_SPEED*1.3:
                    bird.vx = 0
