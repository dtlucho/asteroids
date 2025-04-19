"""
Explosion effects module for the Asteroids game.

This module defines the Explosion and ExplosionManager classes, which create
particle-based explosion effects when asteroids are destroyed or the player is hit.
"""

import pygame
import random
import math


class Particle:
    """
    A single particle in an explosion effect.

    Particles have position, velocity, size, color, and lifetime properties.
    """

    def __init__(
        self: "Particle",
        x: float,
        y: float,
        size: float,
        color: tuple,
        velocity: tuple,
        lifetime: float,
    ):
        """
        Initialize a new particle.

        Args:
            x: Initial x-coordinate
            y: Initial y-coordinate
            size: Size of the particle
            color: Color of the particle (r, g, b)
            velocity: Velocity vector (dx, dy)
            lifetime: How long the particle lives in seconds
        """
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(velocity)
        self.initial_size = size
        self.size = size
        self.color = color
        self.initial_lifetime = lifetime
        self.lifetime = lifetime
        self.alive = True

    def update(self: "Particle", dt: float):
        """
        Update the particle state.

        Args:
            dt: Delta time in seconds since the last frame
        """
        # Update position based on velocity
        self.position += self.velocity * dt

        # Slow down the particle over time
        self.velocity *= 0.95

        # Reduce lifetime
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.alive = False
            return

        # Calculate size and opacity based on remaining lifetime
        life_ratio = self.lifetime / self.initial_lifetime
        self.size = self.initial_size * life_ratio

        # Update color to fade out
        if len(self.color) == 3:
            r, g, b = self.color
            alpha = int(255 * life_ratio)
            self.color = (r, g, b, alpha)
        elif len(self.color) == 4:
            r, g, b, _ = self.color
            alpha = int(255 * life_ratio)
            self.color = (r, g, b, alpha)

    def draw(self: "Particle", screen: pygame.Surface):
        """
        Draw the particle on the screen.

        Args:
            screen: Pygame surface to draw on
        """
        # Draw the particle as a circle
        if self.size >= 1:
            pygame.draw.circle(
                screen,
                self.color,
                (int(self.position.x), int(self.position.y)),
                int(self.size),
            )


class Explosion:
    """
    A collection of particles that form an explosion effect.
    """

    def __init__(
        self: "Explosion", x: float, y: float, size: float, particle_count: int = 20
    ):
        """
        Initialize a new explosion.

        Args:
            x: Center x-coordinate of the explosion
            y: Center y-coordinate of the explosion
            size: Size of the explosion (affects particle count and size)
            particle_count: Base number of particles to create
        """
        self.position = pygame.Vector2(x, y)
        self.particles = []
        self.alive = True

        # Adjust particle count based on explosion size
        actual_particle_count = int(particle_count * (size / 20))

        # Create particles
        for _ in range(actual_particle_count):
            # Random angle and speed for the particle
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(20, 100) * (size / 30)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)

            # Random size for the particle
            particle_size = random.uniform(1, 3) * (size / 20)

            # Random lifetime
            lifetime = random.uniform(0.5, 1.5)

            # Random color (yellowish to reddish)
            r = random.randint(200, 255)
            g = random.randint(100, 200)
            b = random.randint(0, 50)
            # Include alpha channel
            color = (r, g, b, 255)

            # Create the particle
            particle = Particle(x, y, particle_size, color, velocity, lifetime)
            self.particles.append(particle)

    def update(self: "Explosion", dt: float):
        """
        Update all particles in the explosion.

        Args:
            dt: Delta time in seconds since the last frame
        """
        alive_particles = []

        for particle in self.particles:
            particle.update(dt)
            if particle.alive:
                alive_particles.append(particle)

        self.particles = alive_particles

        # If all particles are dead, the explosion is done
        if not self.particles:
            self.alive = False

    def draw(self: "Explosion", screen: pygame.Surface):
        """
        Draw all particles in the explosion.

        Args:
            screen: Pygame surface to draw on
        """
        for particle in self.particles:
            particle.draw(screen)


class ExplosionManager:
    """
    Manages multiple explosions in the game.
    """

    def __init__(self):
        """
        Initialize the explosion manager.
        """
        self.explosions = []

    def create_explosion(self: "ExplosionManager", x: float, y: float, size: float):
        """
        Create a new explosion.

        Args:
            x: Center x-coordinate of the explosion
            y: Center y-coordinate of the explosion
            size: Size of the explosion
        """
        explosion = Explosion(x, y, size)
        self.explosions.append(explosion)

    def update(self: "ExplosionManager", dt: float):
        """
        Update all explosions.

        Args:
            dt: Delta time in seconds since the last frame
        """
        alive_explosions = []

        for explosion in self.explosions:
            explosion.update(dt)
            if explosion.alive:
                alive_explosions.append(explosion)

        self.explosions = alive_explosions

    def draw(self: "ExplosionManager", screen: pygame.Surface):
        """
        Draw all explosions.

        Args:
            screen: Pygame surface to draw on
        """
        for explosion in self.explosions:
            explosion.draw(screen)
