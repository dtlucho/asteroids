"""
Asteroid module for the Asteroids game.

This module defines the Asteroid class, which represents the obstacles
that the player must avoid or destroy.
"""

import pygame
import random
import math

from src.entities.base import CircleShape
from src.utils.constants import ASTEROID_MIN_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT


class Asteroid(CircleShape):
    """
    Asteroid obstacle that players must avoid or destroy.

    Asteroids move in straight lines and can be split into smaller
    asteroids when hit by player shots.
    """

    # Class-level reference to sound manager (set by Game class)
    sound_manager = None

    def __init__(self: "Asteroid", x: float, y: float, radius: float):
        """
        Initialize a new Asteroid.

        Args:
            x: Initial x-coordinate
            y: Initial y-coordinate
            radius: Size of the asteroid
        """
        super().__init__(x, y, radius)

        # Generate a random irregular shape for the asteroid
        self.vertices = self._generate_asteroid_shape()

        # Rotation properties for the asteroid
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-20, 20)  # Degrees per second

    def draw(self: "Asteroid", screen: pygame.Surface):
        # Transform vertices based on current position and rotation
        transformed_vertices = self._get_transformed_vertices()

        # Draw the asteroid as an irregular polygon
        pygame.draw.polygon(screen, (255, 255, 255), transformed_vertices, 2)

        # Optionally add some details to make it look more like a rock
        if self.radius > ASTEROID_MIN_RADIUS * 2:
            # Add some craters for larger asteroids
            for _ in range(min(int(self.radius / 10), 3)):
                # Random position within the asteroid
                angle = random.uniform(0, 2 * math.pi)
                distance = random.uniform(0.2, 0.7) * self.radius
                crater_pos = (
                    self.position.x + math.cos(angle) * distance,
                    self.position.y + math.sin(angle) * distance,
                )
                # Draw a small crater
                pygame.draw.circle(screen, (0, 0, 0), crater_pos, self.radius * 0.1, 1)

    def update(self: "Asteroid", dt: float):
        # Update position based on velocity
        self.position += self.velocity * dt

        # Update rotation
        self.rotation += self.rotation_speed * dt
        self.rotation %= 360  # Keep rotation in [0, 360) range

        # Wrap around screen edges
        self.wrap_position(SCREEN_WIDTH, SCREEN_HEIGHT)

    def _generate_asteroid_shape(self: "Asteroid") -> list:
        """
        Generate vertices for an irregular asteroid shape.

        Returns:
            list: List of points (relative to center) defining the asteroid shape
        """
        num_vertices = random.randint(6, 10)  # Number of vertices for the asteroid
        vertices = []

        for i in range(num_vertices):
            # Calculate angle for this vertex
            angle = 2 * math.pi * i / num_vertices

            # Randomize the radius a bit to create an irregular shape
            # The radius variation gets smaller for smaller asteroids to maintain collision accuracy
            radius_variation = max(0.1, min(0.3, self.radius / 30))
            vertex_radius = self.radius * random.uniform(
                1 - radius_variation, 1 + radius_variation
            )

            # Calculate vertex position (relative to center)
            x = math.cos(angle) * vertex_radius
            y = math.sin(angle) * vertex_radius

            vertices.append(pygame.Vector2(x, y))

        return vertices

    def _get_transformed_vertices(self: "Asteroid") -> list:
        """
        Get the asteroid vertices transformed by current position and rotation.

        Returns:
            list: List of transformed vertex positions
        """
        transformed = []

        for vertex in self.vertices:
            # Rotate the vertex
            angle_rad = math.radians(self.rotation)
            rotated_x = vertex.x * math.cos(angle_rad) - vertex.y * math.sin(angle_rad)
            rotated_y = vertex.x * math.sin(angle_rad) + vertex.y * math.cos(angle_rad)

            # Translate to current position
            transformed.append(
                (self.position.x + rotated_x, self.position.y + rotated_y)
            )

        return transformed

    def split(self: "Asteroid") -> bool:
        """
        Split the asteroid into two smaller ones when hit.

        If the asteroid is already at minimum size, it's simply removed.
        Otherwise, it creates two smaller asteroids moving in different directions.

        Returns:
            bool: True if the asteroid was split, False if it was just destroyed
        """
        self.kill()

        # Play appropriate sound effect based on asteroid size
        if Asteroid.sound_manager:
            if self.radius <= ASTEROID_MIN_RADIUS:
                Asteroid.sound_manager.play("explosion_small")
            else:
                Asteroid.sound_manager.play("explosion_large")

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
