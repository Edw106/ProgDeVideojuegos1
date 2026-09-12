"""
ISPPV1 2023
Study Case: Match-3

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class Board.
"""

from typing import List, Optional, Tuple, Any, Dict, Set

import pygame

import random

import settings
from src.Tile import Tile


class Board:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
        self.matches: List[List[Tile]] = []
        self.explosions: List[List[Tile]] = []
        self.spawn_powerups: List[Tuple[int, int, int, int]] = []
        self.tiles: List[List[Tile]] = []
        valid_board = False
        while(not valid_board):
            self._initialize_tiles()
            valid_board = self.any_valid_move()

    def render(self, surface: pygame.Surface) -> None:
        for row in self.tiles:
            for tile in row:
                tile.render(surface, self.x, self.y)

    def _is_match_generated(self, i: int, j: int, color: int) -> bool:
        if (
            i >= 2
            and self.tiles[i - 1][j].color == color
            and self.tiles[i - 2][j].color == color
        ):
            return True

        return (
            j >= 2
            and self.tiles[i][j - 1].color == color
            and self.tiles[i][j - 2].color == color
        )

    def random_color_number(self) -> int:
        return random.choice([0, 5, 8, 10, 11, 16])


    def _initialize_tiles(self) -> None:
        self.tiles = [
            [None for _ in range(settings.BOARD_WIDTH)]
            for _ in range(settings.BOARD_HEIGHT)
        ]
        for i in range(settings.BOARD_HEIGHT):
            for j in range(settings.BOARD_WIDTH):
                color = self.random_color_number()
                while self._is_match_generated(i, j, color):
                    color = self.random_color_number()

                self.tiles[i][j] = Tile(
                    i, j, color, random.randint(0, settings.NUM_VARIETIES - 1)
                )

    def _calculate_match_rec(self, tile: Tile) -> Set[Tile]:
        if tile in self.in_stack:
            return []

        self.in_stack.add(tile)

        color_to_match = tile.color

        ## Check horizontal match
        h_match: List[Tile] = []

        # Check left
        if tile.j > 0:
            left = max(0, tile.j - 2)
            for j in range(tile.j - 1, left - 1, -1):
                if self.tiles[tile.i][j].color != color_to_match:
                    break
                h_match.append(self.tiles[tile.i][j])

        # Check right
        if tile.j < settings.BOARD_WIDTH - 1:
            right = min(settings.BOARD_WIDTH - 1, tile.j + 2)
            for j in range(tile.j + 1, right + 1):
                if self.tiles[tile.i][j].color != color_to_match:
                    break
                h_match.append(self.tiles[tile.i][j])

        ## Check vertical match
        v_match: List[Tile] = []

        # Check top
        if tile.i > 0:
            top = max(0, tile.i - 2)
            for i in range(tile.i - 1, top - 1, -1):
                if self.tiles[i][tile.j].color != color_to_match:
                    break
                v_match.append(self.tiles[i][tile.j])

        # Check bottom
        if tile.i < settings.BOARD_HEIGHT - 1:
            bottom = min(settings.BOARD_HEIGHT - 1, tile.i + 2)
            for i in range(tile.i + 1, bottom + 1):
                if self.tiles[i][tile.j].color != color_to_match:
                    break
                v_match.append(self.tiles[i][tile.j])

        match: List[Tile] = []

        if len(h_match) >= 2:
            for t in h_match:
                if t not in self.in_match:
                    self.in_match.add(t)
                    match.append(t)

        if len(v_match) >= 2:
            for t in v_match:
                if t not in self.in_match:
                    self.in_match.add(t)
                    match.append(t)

        if len(match) > 0:
            if tile not in self.in_match:
                self.in_match.add(tile)
                match.append(tile)

        for t in match:
            match += self._calculate_match_rec(t)

        self.in_stack.remove(tile)
        return match

    def any_valid_move(self) -> bool:
        original_matches = self.matches.copy()
        original_explosions = self.explosions.copy() if hasattr(self, 'explosions') else []
        original_spawns = self.spawn_powerups.copy() if hasattr(self, 'spawn_powerups') else []
        
        for i in range(settings.BOARD_HEIGHT):
            for j in range(settings.BOARD_WIDTH):
                tile1 = self.tiles[i][j]
                
                # Check right neighbor
                if j < settings.BOARD_WIDTH - 1:
                    tile2 = self.tiles[i][j + 1]
                    # Swap
                    self.tiles[i][j], self.tiles[i][j + 1] = tile2, tile1
                    tile1.j, tile2.j = tile2.j, tile1.j
                    
                    self.matches = []
                    self.explosions = []
                    self.spawn_powerups = []
                    matches = self.calculate_matches_for([tile1, tile2])
                    
                    # Swap back
                    self.tiles[i][j], self.tiles[i][j + 1] = tile1, tile2
                    tile1.j, tile2.j = tile2.j, tile1.j
                    
                    if matches is not None:
                        self.matches = original_matches
                        self.explosions = original_explosions
                        self.spawn_powerups = original_spawns
                        return True
                        
                # Check bottom neighbor
                if i < settings.BOARD_HEIGHT - 1:
                    tile2 = self.tiles[i + 1][j]
                    # Swap
                    self.tiles[i][j], self.tiles[i + 1][j] = tile2, tile1
                    tile1.i, tile2.i = tile2.i, tile1.i
                    
                    self.matches = []
                    self.explosions = []
                    self.spawn_powerups = []
                    matches = self.calculate_matches_for([tile1, tile2])
                    
                    # Swap back
                    self.tiles[i][j], self.tiles[i + 1][j] = tile1, tile2
                    tile1.i, tile2.i = tile2.i, tile1.i
                    
                    if matches is not None:
                        self.matches = original_matches
                        self.explosions = original_explosions
                        self.spawn_powerups = original_spawns
                        return True
                        
        self.matches = original_matches
        self.explosions = original_explosions
        self.spawn_powerups = original_spawns
        return False

    def _calculate_explosions(self, match: List[Tile]) -> List[Tile]:
        expanded = set(match)
        explosions = set()
        queue = list(match)
        
        while queue:
            t = queue.pop(0)
            if t.powerup_type == 1:
                # Add horizontal and vertical neighbors
                for i in range(settings.BOARD_HEIGHT):
                    t2 = self.tiles[i][t.j]
                    if t2 is not None and t2 not in expanded:
                        expanded.add(t2)
                        explosions.add(t2)
                        queue.append(t2)
                for j in range(settings.BOARD_WIDTH):
                    t2 = self.tiles[t.i][j]
                    if t2 is not None and t2 not in expanded:
                        expanded.add(t2)
                        explosions.add(t2)
                        queue.append(t2)
            elif t.powerup_type == 2:
                # Add all tiles of the same color
                for i in range(settings.BOARD_HEIGHT):
                    for j in range(settings.BOARD_WIDTH):
                        t2 = self.tiles[i][j]
                        if t2 is not None and t2.color == t.color and t2 not in expanded:
                            expanded.add(t2)
                            explosions.add(t2)
                            queue.append(t2)
        return list(explosions)

    def calculate_matches_for(
        self, new_tiles: List[Tile], force_explode: bool = False
    ) -> Optional[Tuple[List[List[Tile]], List[List[Tile]]]]:
        self.in_match: Set[Tile] = set()
        self.in_stack: Set[Tile] = set()
        self.explosions: List[List[Tile]] = []

        for tile in new_tiles:
            if tile in self.in_match:
                continue
                
            if force_explode and tile.powerup_type > 0:
                match = [tile]
            else:
                match = self._calculate_match_rec(tile)
                
            if len(match) >= 4 and not force_explode:
                ptype = 2 if len(match) >= 5 else 1
                spawn_tile = next((t for t in match if t in new_tiles), match[0])
                self.spawn_powerups.append((spawn_tile.i, spawn_tile.j, spawn_tile.color, ptype))

            if len(match) > 0:
                self.matches.append(match)
                explosion = self._calculate_explosions(match)
                if explosion:
                    self.explosions.append(explosion)

        # Clear tracking sets
        self.in_match = set()
        self.in_stack = set()

        return (self.matches, self.explosions) if len(self.matches) > 0 else None

    def remove_matches(self) -> None:
        for match in self.matches:
            for tile in match:
                self.tiles[tile.i][tile.j] = None
        for explosion in self.explosions:
            for tile in explosion:
                self.tiles[tile.i][tile.j] = None

        self.matches = []
        self.explosions = []
        
        for (i, j, color, ptype) in self.spawn_powerups:
            if self.tiles[i][j] is None:
                variety = 4 if ptype == 1 else 0
                self.tiles[i][j] = Tile(i, j, color, variety, powerup_type=ptype)
                
        self.spawn_powerups = []

    def get_falling_tiles(self) -> Tuple[Any, Dict[str, Any]]:
        # List of tweens to create
        tweens: Tuple[Tile, Dict[str, Any]] = []

        # for each column, go up tile by tile until we hit a space
        for j in range(settings.BOARD_WIDTH):
            space = False
            space_i = -1
            i = settings.BOARD_HEIGHT - 1

            while i >= 0:
                tile = self.tiles[i][j]

                # if our previous tile was a space
                if space:
                    # if the current tile is not a space
                    if tile is not None:
                        self.tiles[space_i][j] = tile
                        tile.i = space_i

                        # set its prior position to None
                        self.tiles[i][j] = None

                        tweens.append((tile, {"y": tile.i * settings.TILE_SIZE}))
                        space = False
                        i = space_i
                        space_i = -1
                elif tile is None:
                    space = True

                    if space_i == -1:
                        space_i = i

                i -= 1

        # create a replacement tiles at the top of the screen
        for j in range(settings.BOARD_WIDTH):
            for i in range(settings.BOARD_HEIGHT):
                tile = self.tiles[i][j]

                if tile is None:
                    tile = Tile(
                        i,
                        j,
                        self.random_color_number(),
                        random.randint(0, settings.NUM_VARIETIES - 1),
                    )
                    tile.y -= settings.TILE_SIZE
                    self.tiles[i][j] = tile
                    tweens.append((tile, {"y": tile.i * settings.TILE_SIZE}))

        return tweens
