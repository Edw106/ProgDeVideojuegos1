"""
ISPPV1 2023
Study Case: Breakout

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class to define the Play state.
"""

import random
from typing import Any

import pygame

from gale.factory import AbstractFactory, Factory
from gale.state import BaseState
from gale.input_handler import InputData
from gale.text import render_text

import settings
import src.powerups
from src.Ball import Ball
from src.EventManager import EventManager


class PlayState(BaseState):
    def enter(self, **params: dict):
        self.level = params["level"]
        self.score = params["score"]
        self.lives = params["lives"]
        self.paddle = params["paddle"]
        self.balls = params["balls"]
        self.brickset = params["brickset"]
        self.live_factor = params["live_factor"]
        self.points_to_next_live = params["points_to_next_live"]
        self.points_to_next_grow_up = (
            self.score
            + settings.PADDLE_GROW_UP_POINTS * (self.paddle.size + 1) * self.level
        )
        self.powerups = params.get("powerups", [])

        self.powerups_abstract_factory = AbstractFactory("src.powerups")
        self.event_manager = EventManager()
        self.event_manager.register(self) # It registers itself
        self.event_manager.register(self.paddle)
        for ball in self.balls:
            self.event_manager.register(ball)
        self.event_manager.register(self.brickset)
        for powerup in self.powerups:
            self.event_manager.register(powerup)

        if not params.get("resume", False):
            self.launch_ball(self.balls[0])
        else:
            self.event_manager.notify("RESUME")

    def on_event(self, event: Any) -> None:
        if event == "POWERUP: TwoMoreBall":
            if not hasattr(self, "ball_factory"):
                self.ball_factory = Factory(Ball)
            for _ in range(2):
                b = self.ball_factory.create(
                    self.paddle.x + self.paddle.width // 2 - 4,
                    self.paddle.y - 8,
                )
                b.vx = random.randint(-80, 80)
                b.vy = random.randint(-170, -100)
                self.balls.append(b)
                self.event_manager.register(b)
        elif event == "POWERUP_FINISHED: CatchBall":
            if not self.paddle.can_catch():
                self.release_caught_balls()

    def launch_ball(self, ball: Any) -> None:
        ball.catch(False)
        ball.vx = random.randint(-80, 80)
        ball.vy = random.randint(-170, -100)
        settings.SOUNDS["paddle_hit"].stop()
        settings.SOUNDS["paddle_hit"].play()

    def release_caught_balls(self) -> None:
        for ball in self.balls:
            if ball.catch():
                self.launch_ball(ball)

    def update(self, dt: float) -> None:
        self.paddle.update(dt)

        # This moves the balls, checks whether they collides and handles what that entails
        for ball in self.balls:
            if ball.catch():
                if not self.paddle.can_catch():
                    self.launch_ball(ball)
                    continue
                ball.set_position(
                    ball.x + self.paddle.vx * dt,
                    self.paddle.y - ball.height,
                )
                continue

            ball.update(dt)
            ball.solve_world_boundaries()

            # Check collision with the paddle
            if ball.collides(self.paddle):
                settings.SOUNDS["paddle_hit"].stop()
                settings.SOUNDS["paddle_hit"].play()
                if self.paddle.can_catch():
                    ball.catch(True)
                    ball.set_position(ball.x, self.paddle.y - ball.height)
                    ball.set_velocity(0, 0)
                else:
                    ball.rebound(self.paddle)
                    ball.push(self.paddle)

            # Check collision with brickset
            if not ball.collides(self.brickset):
                continue

            brick = self.brickset.get_colliding_brick(ball.get_collision_rect())

            if brick is None:
                continue

            brick.hit()
            self.score += brick.score()
            ball.rebound(brick)

            # Check earn life
            if self.score >= self.points_to_next_live:
                settings.SOUNDS["life"].play()
                self.lives = min(3, self.lives + 1)
                self.live_factor += 0.5
                self.points_to_next_live += settings.LIVE_POINTS_BASE * self.live_factor

            # Check growing up of the paddle
            if self.score >= self.points_to_next_grow_up:
                settings.SOUNDS["grow_up"].play()
                self.points_to_next_grow_up += (
                    settings.PADDLE_GROW_UP_POINTS * (self.paddle.size + 1) * self.level
                )
                self.paddle.inc_size()

            # Chance to generate a power-up
            if random.random() < 0.1:
                r = brick.get_collision_rect()
                powerup_type = random.choice(["TwoMoreBall", "CatchBall"])
                powerup = self.powerups_abstract_factory.get_factory(powerup_type).create(
                    r.centerx - 8, r.centery - 8
                )
                self.powerups.append(powerup)
                self.event_manager.register(powerup)

        # Removing all balls that are not in play
        self.balls = [ball for ball in self.balls if ball.active]

        # Updating the brickset
        self.brickset.update(dt)

        # If there are not balls, you loose, change state
        if not self.balls:
            self.lives -= 1
            if self.lives == 0:
                self.state_machine.change("game_over", score=self.score)
            else:
                self.paddle.dec_size()
                self.state_machine.change(
                    "serve",
                    level=self.level,
                    score=self.score,
                    lives=self.lives,
                    paddle=self.paddle,
                    brickset=self.brickset,
                    points_to_next_live=self.points_to_next_live,
                    live_factor=self.live_factor,
                )

        # Update powerups
        for powerup in self.powerups:
            if powerup.active:
                powerup.update(dt)

                if powerup.collides(self.paddle):
                    powerup.register(self.paddle)
                    powerup.register(self)
                    self.event_manager.notify("POWERUP: " + powerup.get_name())
                    powerup.take()

        # Remove powerups that are not in play and not in use
        new_powerups = []
        for p in self.powerups:
            if p.active or p.using:
                new_powerups.append(p)
            else:
                self.event_manager.unregister(p)
        self.powerups = new_powerups

        # Check victory (if all blocks are broken), and changes state
        if self.brickset.size == 1 and next(
            (True for _, b in self.brickset.bricks.items() if b.broken), False
        ):
            self.state_machine.change(
                "victory",
                lives=self.lives,
                level=self.level,
                score=self.score,
                paddle=self.paddle,
                balls=self.balls,
                points_to_next_live=self.points_to_next_live,
                live_factor=self.live_factor,
            )

    def render(self, surface: pygame.Surface) -> None:
        heart_x = settings.VIRTUAL_WIDTH - 120

        i = 0
        # Draw filled hearts
        while i < self.lives:
            surface.blit(
                settings.TEXTURES["hearts"], (heart_x, 5), settings.FRAMES["hearts"][0]
            )
            heart_x += 11
            i += 1

        # Draw empty hearts
        while i < 3:
            surface.blit(
                settings.TEXTURES["hearts"], (heart_x, 5), settings.FRAMES["hearts"][1]
            )
            heart_x += 11
            i += 1

        render_text(
            surface,
            f"Score: {self.score}",
            settings.FONTS["tiny"],
            settings.VIRTUAL_WIDTH - 80,
            5,
            (255, 255, 255),
        )

        # The bricks
        self.brickset.render(surface)

        # The paddle
        self.paddle.render(surface)

        # All the balls
        for ball in self.balls:
            ball.render(surface)

        # All the power ups
        for powerup in self.powerups:
            if powerup.active:
                powerup.render(surface)

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "move_left":
            if input_data.pressed:
                self.paddle.vx = -settings.PADDLE_SPEED
            elif input_data.released and self.paddle.vx < 0:
                self.paddle.vx = 0
        elif input_id == "move_right":
            if input_data.pressed:
                self.paddle.vx = settings.PADDLE_SPEED
            elif input_data.released and self.paddle.vx > 0:
                self.paddle.vx = 0
        elif input_id == "enter" and input_data.pressed:
            self.release_caught_balls()
        elif input_id == "pause" and input_data.pressed:
            self.event_manager.notify("PAUSE")
            self.state_machine.change(
                "pause",
                level=self.level,
                score=self.score,
                lives=self.lives,
                paddle=self.paddle,
                balls=self.balls,
                brickset=self.brickset,
                points_to_next_live=self.points_to_next_live,
                live_factor=self.live_factor,
                powerups=self.powerups,
            )
