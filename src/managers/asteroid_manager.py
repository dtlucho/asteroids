"""
Asteroid Manager module for the Asteroids game.

This module defines the AsteroidField class, which manages the creation
and spawning of asteroids throughout the game.
"""

import pygame
import random
from src.entities.asteroid import Asteroid
from src.utils.constants import (
    ASTEROID_MIN_RADIUS,
    ASTEROID_MAX_RADIUS,
    ASTEROID_KINDS,
    ASTEROID_SPAWN_RATE,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)


class AsteroidField(pygame.sprite.Sprite):
    """
    Manages the spawning and creation of asteroids.game_state_callback

    The AsteroidField class is responsible for:
    - Spawning new asteroids at random edges of the screen
    - Controlling the rate and difficulty of asteroid spawning
    - Managing asteroid velocity and size distribution
    """

    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self: "AsteroidField"):
        """
        Initialize the asteroid field manager.

        Sets up initial spawn timer and difficulty parameters.
        """
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0
        self.spawn_rate = ASTEROID_SPAWN_RATE
        self.speed_multiplier = 1.0

    def spawn(
        self: "AsteroidField",
        radius: float,
        position: pygame.Vector2,
        velocity: pygame.Vector2,
    ):
        """
        Spawn a new asteroid with the given parameters.

        Args:
            radius: Size of the asteroid to spawn
            position: Initial position of the asteroid
            velocity: Initial velocity vector of the asteroid
        """
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self: "AsteroidField", dt: float):
        """
        Update the asteroid field, potentially spawning new asteroids.

        Args:
            dt: Delta time in seconds since the last frame
        """
        self.spawn_timer += dt
        if self.spawn_timer > self.spawn_rate:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            base_speed = random.randint(40, 100)
            speed = base_speed * self.speed_multiplier
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)
