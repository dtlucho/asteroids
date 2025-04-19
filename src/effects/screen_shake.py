"""
Screen shake module for the Asteroids game.

This module defines the ScreenShake class, which creates a camera shake effect
when explosions or collisions occur.
"""

import random
import math

import pygame


class ScreenShake:
    """
    Creates a screen shake effect for impacts and explosions.

    The screen shake effect works by offsetting the rendering position
    of game elements, creating the illusion of camera shake.
    """

    def __init__(self: "ScreenShake"):
        """
        Initialize the screen shake effect.
        """
        self.duration = 0  # How long the shake lasts
        self.intensity = 0  # How strong the shake is
        self.offset_x = 0  # Current x offset
        self.offset_y = 0  # Current y offset
        self.decay = 5.0  # How quickly the shake effect decays

    def start(self: "ScreenShake", intensity: float = 5.0, duration: float = 0.3):
        """
        Start a screen shake effect.

        Args:
            intensity: Maximum pixel offset for the shake
            duration: How long the shake lasts in seconds
        """
        # Only start a new shake if it's stronger than the current one
        if intensity > self.intensity:
            self.intensity = intensity
            self.duration = duration

    def update(self: "ScreenShake", dt: float):
        """
        Update the screen shake effect.

        Args:
            dt: Delta time in seconds since the last frame
        """
        if self.duration > 0:
            # Reduce the remaining duration
            self.duration -= dt

            # Calculate shake intensity based on remaining duration
            current_intensity = self.intensity * (self.duration / self.decay)

            # Generate random offset within the current intensity
            self.offset_x = random.uniform(-1, 1) * current_intensity
            self.offset_y = random.uniform(-1, 1) * current_intensity

            # Ensure duration doesn't go negative
            if self.duration <= 0:
                self.duration = 0
                self.offset_x = 0
                self.offset_y = 0
        else:
            # No shake effect active
            self.offset_x = 0
            self.offset_y = 0

    def apply(self: "ScreenShake", position: tuple) -> tuple:
        """
        Apply the screen shake effect to a position.

        Args:
            position: The original position (x, y)

        Returns:
            tuple: The modified position with shake applied
        """
        return (position[0] + self.offset_x, position[1] + self.offset_y)

    def apply_surface(
        self: "ScreenShake", surface: pygame.Surface, screen: pygame.Surface
    ) -> tuple:
        """
        Apply the screen shake effect when blitting a surface.

        Args:
            surface: The pygame surface to blit
            screen: The target screen to blit onto

        Returns:
            tuple: The position to blit at with shake applied
        """
        return screen.blit(surface, (self.offset_x, self.offset_y))
