"""
Asteroid module for the Asteroids game.

This module defines the Asteroid class, which represents the obstacles
that the player must avoid or destroy.
"""

import pygame
import random

from circleshape import CircleShape
from constants import ASTEROID_MIN_RADIUS


class Asteroid(CircleShape):
    """
    Asteroid obstacle that players must avoid or destroy.

    Asteroids move in straight lines and can be split into smaller
    asteroids when hit by player shots.
    """

    def __init__(self: "Asteroid", x: float, y: float, radius: float):
        """
        Initialize a new Asteroid.

        Args:
            x: Initial x-coordinate
            y: Initial y-coordinate
            radius: Size of the asteroid
        """
        super().__init__(x, y, radius)

    def draw(self: "Asteroid", screen: pygame.Surface):
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius, 2)

    def update(self: "Asteroid", dt: float):
        self.position += self.velocity * dt

    def split(self: "Asteroid") -> bool:
        """
        Split the asteroid into two smaller ones when hit.

        If the asteroid is already at minimum size, it's simply removed.
        Otherwise, it creates two smaller asteroids moving in different directions.

        Returns:
            bool: True if the asteroid was split, False if it was just destroyed
        """
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return False

        # Create explosion effect here

        angle = random.uniform(20, 50)
        velocity_1 = self.velocity.rotate(angle)
        velocity_2 = self.velocity.rotate(-angle)
        old_radius = self.radius

        # Add momentum to child asteroids
        asteroid_1 = Asteroid(
            self.position.x, self.position.y, old_radius - ASTEROID_MIN_RADIUS
        )
        asteroid_2 = Asteroid(
            self.position.x, self.position.y, old_radius - ASTEROID_MIN_RADIUS
        )
        asteroid_1.velocity = velocity_1 * 1.2
        asteroid_2.velocity = velocity_2 * 1.2

        return True
