"""
ISPPV1 2023
Study Case: Super Martian (Platformer)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class GameLevel.
"""

import random
from typing import Any, Dict, Optional

import pygame

from gale.tilemap import CollisionType, collision_type_at, load_tiled_map
from gale.timer import Timer

import settings
from src.Creature import Creature
from src.FlyingCreature import FlyingCreature
from src.GameEntity import GameEntity
from src.GameItem import GameItem
from src.definitions import creatures, items


class GameLevel:
    def __init__(self, num_level: int) -> None:
        self.tilemap = load_tiled_map(settings.TILEMAPS[num_level])
        self.creatures = []
        self.items = []

        self.key_block_row = None
        self.key_block_col = None
        self.key_block_gid = None
        self.key_block_active = False
        self.key_spawned = False

        ground_layer = self.tilemap.get_layer("ground")
        for row in range(len(ground_layer)):
            for col in range(len(ground_layer[row])):
                gid = ground_layer[row][col]
                if gid > 0:
                    props = self.tilemap.properties_of_gid(gid)
                    if props and "key" in props:
                        self.key_block_row = row
                        self.key_block_col = col
                        self.key_block_gid = gid
                        self.tilemap.set_gid("ground", row, col, 0)
                        break
            if self.key_block_gid is not None:
                break

        for obj in self.tilemap.object_layers.get("creatures", []):
            self.add_creature(
                {
                    "tile_index": obj.properties["tile_index"],
                    "x": obj.x,
                    "y": obj.y,
                    "width": obj.width,
                    "height": obj.height,
                }
            )

        for obj in self.tilemap.object_layers.get("coins", []):
            self.add_item(
                {
                    "item_name": "coins",
                    "frame_index": obj.properties.get("frame_index", 62),
                    "x": obj.x,
                    "y": obj.y,
                    "width": obj.width,
                    "height": obj.height,
                }
            )

        self._schedule_flying_creature_spawn()

    def reveal_key_block(self) -> None:
        if not self.key_block_active and self.key_block_gid is not None:
            self.key_block_active = True
            self.tilemap.set_gid("ground", self.key_block_row, self.key_block_col, self.key_block_gid)

    def add_item(self, item_data: Dict[str, Any]) -> None:
        item_name = item_data.pop("item_name")
        definition = items.ITEMS[item_name][item_data["frame_index"]]
        definition.update(item_data)
        self.items.append(GameItem(**definition))

    def add_creature(self, creature_data: Dict[str, Any]) -> None:
        definition = creatures.CREATURES[creature_data["tile_index"]]
        self.creatures.append(
            Creature(
                creature_data["x"],
                creature_data["y"],
                creature_data["width"],
                creature_data["height"],
                self,
                **definition,
            )
        )

    def _schedule_flying_creature_spawn(self) -> None:
        delay = random.uniform(
            settings.FLYING_CREATURE_MIN_SPAWN_DELAY,
            settings.FLYING_CREATURE_MAX_SPAWN_DELAY,
        )
        Timer.after(delay, self._spawn_flying_creature)

    def _pick_open_row(self, col: int) -> Optional[int]:
        """
        Scans column col from the top down and returns a random row
        strictly above the first solid/platform tile found there (with one
        extra row of buffer so the creature is unambiguously flying in open
        air, not skimming the surface), or None if the column has no clear
        row at all to spawn in.
        """
        first_solid_row = self.tilemap.rows

        for row in range(self.tilemap.rows):
            if (
                collision_type_at(self.tilemap, GameEntity.COLLISION_LAYER, row, col)
                != CollisionType.NONE
            ):
                first_solid_row = row
                break

        max_row = first_solid_row - 2

        if max_row < 0:
            return None

        return random.randint(0, max_row)

    def _spawn_flying_creature(self) -> None:
        from_left = random.choice([True, False])
        col = 0 if from_left else self.tilemap.cols - 1
        row = self._pick_open_row(col)

        if row is not None:
            definition = random.choice(creatures.FLYING_CREATURES)
            x = 0 if from_left else self.tilemap.pixel_width - 16
            y = row * self.tilemap.tile_height
            direction = "right" if from_left else "left"
            self.creatures.append(
                FlyingCreature(x, y, 16, 16, self, direction, **definition)
            )

        self._schedule_flying_creature_spawn()

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(0, 0, self.tilemap.pixel_width, self.tilemap.pixel_height)

    def update(self, dt: float) -> None:
        for creature in self.creatures:
            creature.update(dt)

        # Remove dead creatures
        self.creatures = [
            creature for creature in self.creatures if not creature.is_dead
        ]

    def spawn_key(self) -> None:
        from src.KeyItem import KeyItem
        from gale.timer import Timer

        self.key_spawned = True
        settings.SOUNDS["count"].play()  # Feedback sound
        
        # Calculate start position based on the block's tile coordinates
        block_x, block_y = self.tilemap.position_of(self.key_block_row, self.key_block_col)
        
        # Create the Key object exactly at the block's coordinates
        self.special_key = KeyItem(block_x, block_y, self)
        self.items.append(self.special_key)
        
        # Tween it upwards by 16 pixels over 0.5 seconds, then make it active
        Timer.tween(
            0.5,
            [(self.special_key, {"y": block_y - 16})],
            on_finish=lambda: setattr(self.special_key, "active", True)
        )

    def on_key_collected(self) -> None:
        self.level_completed = True

    def render(self, surface: pygame.Surface, camera: Any) -> None:
        self.tilemap.render(surface, camera)
        for creature in self.creatures:
            creature.render(surface, camera)
        for item in self.items:
            if item.active:
                item.render(surface, camera)
