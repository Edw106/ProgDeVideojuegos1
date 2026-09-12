"""
ISPPV1 2023
Study Case: Match-3

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class PlayState.
"""

from typing import Dict, Any, List

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text
from gale.timer import Timer

import settings


class PlayState(BaseState):
    def enter(self, **enter_params: Dict[str, Any]) -> None:
        self.level = enter_params["level"]
        self.board = enter_params["board"]
        self.score = enter_params["score"]

        # Position in the grid which we are highlighting
        self.board_highlight_i1 = -1
        self.board_highlight_j1 = -1
        self.board_highlight_i2 = -1
        self.board_highlight_j2 = -1

        self.highlighted_tile = False
        self.dragging_tile = None

        self.active = True

        self.timer = settings.LEVEL_TIME

        self.goal_score = self.score + self.level * 1.25 * 1000

        # A surface that supports alpha to highlight a selected tile
        self.tile_alpha_surface = pygame.Surface(
            (settings.TILE_SIZE, settings.TILE_SIZE), pygame.SRCALPHA
        )
        pygame.draw.rect(
            self.tile_alpha_surface,
            (255, 255, 255, 96),
            pygame.Rect(0, 0, settings.TILE_SIZE, settings.TILE_SIZE),
            border_radius=7,
        )

        # A surface that supports alpha to draw behind the text.
        self.text_alpha_surface = pygame.Surface((212, 136), pygame.SRCALPHA)
        pygame.draw.rect(
            self.text_alpha_surface, (56, 56, 56, 234), pygame.Rect(0, 0, 212, 136)
        )

        def decrement_timer():
            if not self.no_moves_text:
                self.timer -= 1

                # Play warning sound on timer if we get low
                if self.timer <= 5:
                    settings.SOUNDS["clock"].play()

        Timer.every(1, decrement_timer)

        self.no_moves_text = False

        self._check_any_valid_move()

    def _check_any_valid_move(self): # And reset if not
        if not self.board.any_valid_move():
            self.active = False
            self.no_moves_text = True
            
            def reset_board():
                self.board._initialize_tiles()
                self.no_moves_text = False
                self.active = True
                
            Timer.after(3.0, reset_board)

    def update(self, _: float) -> None:
        if self.timer <= 0:
            Timer.clear()
            settings.SOUNDS["game-over"].play()
            self.state_machine.change("game-over", score=self.score)

        if self.score >= self.goal_score:
            Timer.clear()
            settings.SOUNDS["next-level"].play()
            self.state_machine.change("begin", level=self.level + 1, score=self.score)

        if self.dragging_tile is not None:
            pos_x, pos_y = pygame.mouse.get_pos()
            pos_x = pos_x * settings.VIRTUAL_WIDTH // settings.WINDOW_WIDTH
            pos_y = pos_y * settings.VIRTUAL_HEIGHT // settings.WINDOW_HEIGHT
            self.dragging_tile.x = pos_x - self.board.x - settings.TILE_SIZE // 2
            self.dragging_tile.y = pos_y - self.board.y - settings.TILE_SIZE // 2

    def render(self, surface: pygame.Surface) -> None:
        self.board.render(surface)

        if self.highlighted_tile:
            if self.dragging_tile is not None:
                x = self.dragging_tile.x + self.board.x
                y = self.dragging_tile.y + self.board.y
            else:
                x = self.highlighted_j1 * settings.TILE_SIZE + self.board.x
                y = self.highlighted_i1 * settings.TILE_SIZE + self.board.y
            surface.blit(self.tile_alpha_surface, (x, y))

        surface.blit(self.text_alpha_surface, (16, 16))
        render_text(
            surface,
            f"Level: {self.level}",
            settings.FONTS["medium"],
            30,
            24,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Score: {self.score}",
            settings.FONTS["medium"],
            30,
            52,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Goal: {self.goal_score}",
            settings.FONTS["medium"],
            30,
            80,
            (99, 155, 255),
            shadowed=True,
        )
        render_text(
            surface,
            f"Timer: {self.timer}",
            settings.FONTS["medium"],
            30,
            108,
            (99, 155, 255),
            shadowed=True,
        )

        if self.no_moves_text:
            # Render background for text
            rect_surface = pygame.Surface((settings.VIRTUAL_WIDTH, 40), pygame.SRCALPHA)
            pygame.draw.rect(rect_surface, (56, 56, 56, 234), pygame.Rect(0, 0, settings.VIRTUAL_WIDTH, 40))
            surface.blit(rect_surface, (0, settings.VIRTUAL_HEIGHT // 2 - 20))

            render_text(
                surface,
                "No Valid Moves! Recreating Board...",
                settings.FONTS["medium"],
                settings.VIRTUAL_WIDTH // 2,
                settings.VIRTUAL_HEIGHT // 2,
                (255, 255, 255),
                center=True,
                shadowed=True,
            )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if not self.active:
            return

        if input_id == "click":
            if input_data.pressed:
                pos_x, pos_y = input_data.position
                pos_x = pos_x * settings.VIRTUAL_WIDTH // settings.WINDOW_WIDTH
                pos_y = pos_y * settings.VIRTUAL_HEIGHT // settings.WINDOW_HEIGHT
                i = (pos_y - self.board.y) // settings.TILE_SIZE
                j = (pos_x - self.board.x) // settings.TILE_SIZE
                
                if 0 <= i < settings.BOARD_HEIGHT and 0 <= j < settings.BOARD_WIDTH:
                    self.highlighted_tile = True
                    self.highlighted_i1 = i
                    self.highlighted_j1 = j
                    self.dragging_tile = self.board.tiles[i][j]
            else:
                pos_x, pos_y = pygame.mouse.get_pos()
                pos_x = pos_x * settings.VIRTUAL_WIDTH // settings.WINDOW_WIDTH
                pos_y = pos_y * settings.VIRTUAL_HEIGHT // settings.WINDOW_HEIGHT
                i = (pos_y - self.board.y) // settings.TILE_SIZE
                j = (pos_x - self.board.x) // settings.TILE_SIZE

                if self.highlighted_tile:
                    self.dragging_tile = None
                    if 0 <= i < settings.BOARD_HEIGHT and 0 <= j < settings.BOARD_WIDTH:
                        self.highlighted_i2 = i
                        self.highlighted_j2 = j
                        di = abs(self.highlighted_i2 - self.highlighted_i1)
                        dj = abs(self.highlighted_j2 - self.highlighted_j1)

                        if di == 0 and dj == 0:
                            clicked_tile = self.board.tiles[self.highlighted_i1][self.highlighted_j1]
                            if clicked_tile.powerup_type > 0:
                                self.active = False
                                clicked_tile.x = self.highlighted_j1 * settings.TILE_SIZE
                                clicked_tile.y = self.highlighted_i1 * settings.TILE_SIZE
                                self._calculate_matches([clicked_tile], force_explode=True)
                            else:
                                clicked_tile.x = self.highlighted_j1 * settings.TILE_SIZE
                                clicked_tile.y = self.highlighted_i1 * settings.TILE_SIZE
                        elif di <= 1 and dj <= 1 and di != dj:
                            self.active = False
                            tile1 = self.board.tiles[self.highlighted_i1][
                                self.highlighted_j1
                            ]
                            tile2 = self.board.tiles[self.highlighted_i2][
                                self.highlighted_j2
                            ]

                            def arrive():
                                tile1 = self.board.tiles[self.highlighted_i1][
                                    self.highlighted_j1
                                ]
                                tile2 = self.board.tiles[self.highlighted_i2][
                                    self.highlighted_j2
                                ]
                                (
                                    self.board.tiles[tile1.i][tile1.j],
                                    self.board.tiles[tile2.i][tile2.j],
                                ) = (
                                    self.board.tiles[tile2.i][tile2.j],
                                    self.board.tiles[tile1.i][tile1.j],
                                )
                                tile1.i, tile1.j, tile2.i, tile2.j = (
                                    tile2.i,
                                    tile2.j,
                                    tile1.i,
                                    tile1.j,
                                )
                                self._calculate_matches([tile1, tile2], revert_on_failure=True)

                            # Swap tiles
                            Timer.tween(
                                0.25,
                                [
                                    (tile1, {"x": tile2.x, "y": tile2.y}),
                                    (tile2, {"x": self.highlighted_j1 * settings.TILE_SIZE, "y": self.highlighted_i1 * settings.TILE_SIZE}),
                                ],
                                on_finish=arrive,
                            )
                        else:
                            tile = self.board.tiles[self.highlighted_i1][self.highlighted_j1]
                            tile.x = self.highlighted_j1 * settings.TILE_SIZE
                            tile.y = self.highlighted_i1 * settings.TILE_SIZE
                    else:
                        tile = self.board.tiles[self.highlighted_i1][self.highlighted_j1]
                        tile.x = self.highlighted_j1 * settings.TILE_SIZE
                        tile.y = self.highlighted_i1 * settings.TILE_SIZE
                    
                    self.highlighted_tile = False

    def _calculate_matches(self, tiles: List, revert_on_failure: bool = False, force_explode: bool = False) -> None:
        matches = self.board.calculate_matches_for(tiles, force_explode=force_explode)

        if matches is None:
            if revert_on_failure and len(tiles) == 2:
                tile1, tile2 = tiles[0], tiles[1]

                settings.SOUNDS["error"].play()

                def revert():
                    (
                        self.board.tiles[tile1.i][tile1.j],
                        self.board.tiles[tile2.i][tile2.j],
                    ) = (
                        self.board.tiles[tile2.i][tile2.j],
                        self.board.tiles[tile1.i][tile1.j],
                    )
                    tile1.i, tile1.j, tile2.i, tile2.j = (
                        tile2.i,
                        tile2.j,
                        tile1.i,
                        tile1.j,
                    )
                    self.active = True

                Timer.tween(
                    0.25,
                    [
                        (tile1, {"x": tile2.x, "y": tile2.y}),
                        (tile2, {"x": tile1.x, "y": tile1.y}),
                    ],
                    on_finish=revert,
                )
            else:
                self.active = True
                self._check_any_valid_move()
            return

        settings.SOUNDS["match"].stop()
        settings.SOUNDS["match"].play()

        for match in matches:
            self.score += len(match) * 50

        self.board.remove_matches()

        falling_tiles = self.board.get_falling_tiles()

        Timer.tween(
            0.25,
            falling_tiles,
            on_finish=lambda: self._calculate_matches(
                [item[0] for item in falling_tiles]
            ),
        )
