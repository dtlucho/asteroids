"""
Shot module for the Asteroids game.

This module defines the Shot class, which represents projectiles fired
by the player. Shots travel in a straight line and can destroy asteroids.
"""

import pygame

from src.entities.base import CircleShape
from src.utils.constants import SHOT_RADIUS, SCREEN_WIDTH, SCREEN_HEIGHT, SHOT_LIFETIME


class Shot(CircleShape):
    """
    Projectile fired by the player.

    Shots move in a straight line with constant velocity and can destroy
    asteroids on collision. They have a limited lifetime and are removed
    after traveling a certain distance or when they hit an asteroid.
    """

    def __init__(self: "Shot", x: float, y: float):
        """
        Initialize a new Shot.

        Args:
            x: Initial x-coordinate (usually player's position)
            y: Initial y-coordinate (usually player's position)
        """
        super().__init__(x, y, SHOT_RADIUS)
        self.lifetime = SHOT_LIFETIME  # Time before shot disappears

    def draw(self: "Shot", screen: pygame.Surface):
        """
        Draw the shot on the screen as a small circle.

        Args:
            screen: Pygame surface to draw on
        """
        pygame.draw.circle(screen, (255, 255, 255), self.position, self.radius, 2)

    def update(self: "Shot", dt: float):
        """
        Update the shot's position and lifetime.

        Args:
            dt: Delta time in seconds since the last frame
        """
        # Move the shot based on velocity
        self.position += self.velocity * dt

        # Reduce lifetime and remove if expired
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()

        # Keep shot on screen
        self.wrap_position(SCREEN_WIDTH, SCREEN_HEIGHT)
