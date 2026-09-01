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
        bird = self.bird

        if input_id == "jump" and input_data.pressed:
            bird.jump()
        
        if input_id in ("left", "right"):
            if input_data.pressed:
                if input_id == "left":
                    bird.move_left()
                if input_id == "right":
                    bird.move_right()
            elif input_data.released:

                l = input_id == "left" and bird.is_moving_left()
                r = input_id == "right" and bird.is_moving_right()
                    
                if l or r:
                    bird.stop_x_movement()
