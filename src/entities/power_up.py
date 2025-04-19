"""
Power-up module for the Asteroids game.

This module defines the PowerUp class, which represents collectible
items that provide temporary abilities to the player.
"""

import pygame
import random
import math
from enum import Enum, auto

from src.entities.base import CircleShape
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT


class PowerUpType(Enum):
    """Types of power-ups available in the game."""
    SHIELD = auto()
    TRIPLE_SHOT = auto()
    SPEED_BOOST = auto()


class PowerUp(CircleShape):
    """
    Collectible power-up that provides temporary abilities to the player.
    
    Power-ups move slowly across the screen and can be collected by the player
    to gain temporary abilities like shields, triple shots, or speed boosts.
    """
    
    # Class-level reference to sound manager (set by Game class)
    sound_manager = None
    
    # Power-up properties
    RADIUS = 15
    DURATION = {
        PowerUpType.SHIELD: 10.0,      # 10 seconds of shield
        PowerUpType.TRIPLE_SHOT: 5.0,  # 5 seconds of triple shot
        PowerUpType.SPEED_BOOST: 7.0,  # 7 seconds of speed boost
    }
    COLORS = {
        PowerUpType.SHIELD: (0, 255, 255),      # Cyan for shield
        PowerUpType.TRIPLE_SHOT: (255, 0, 255), # Magenta for triple shot
        PowerUpType.SPEED_BOOST: (255, 255, 0), # Yellow for speed boost
    }
    
    def __init__(self, x, y, power_type=None):
        """
        Initialize a new PowerUp.
        
        Args:
            x: Initial x-coordinate
            y: Initial y-coordinate
            power_type: Type of power-up (if None, a random type is chosen)
        """
        super().__init__(x, y, self.RADIUS)
        
        # Set power-up type (random if not specified)
        self.type = power_type or random.choice(list(PowerUpType))
        
        # Set color based on type
        self.color = self.COLORS[self.type]
        
        # Set duration based on type
        self.duration = self.DURATION[self.type]
        
        # Set initial velocity (slow drifting motion)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(20, 40)
        self.velocity = pygame.Vector2(math.cos(angle), math.sin(angle)) * speed
        
        # Set lifetime (power-ups disappear after a while if not collected)
        self.lifetime = random.uniform(5.0, 10.0)  # 5-10 seconds
        
        # Animation variables
        self.pulse_time = 0
        self.pulse_speed = 2.0
        self.min_scale = 0.8
        self.max_scale = 1.2
    
    def update(self, dt):
        """
        Update the power-up's position, animation, and lifetime.
        
        Args:
            dt: Delta time in seconds since the last frame
        """
        # Move the power-up
        self.position += self.velocity * dt
        
        # Update animation
        self.pulse_time += dt * self.pulse_speed
        
        # Update lifetime and remove if expired
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()
        
        # Keep power-up on screen
        self.wrap_position(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    def draw(self, screen):
        """
        Draw the power-up on the screen.
        
        Args:
            screen: Pygame surface to draw on
        """
        # Calculate pulse scale
        scale = self.min_scale + (self.max_scale - self.min_scale) * (
            0.5 + 0.5 * math.sin(self.pulse_time)
        )
        
        # Draw outer circle (pulsing)
        radius = int(self.radius * scale)
        pygame.draw.circle(screen, self.color, self.position, radius, 2)
        
        # Draw inner symbol based on power-up type
        if self.type == PowerUpType.SHIELD:
            # Shield symbol (circle)
            inner_radius = int(self.radius * 0.5 * scale)
            pygame.draw.circle(screen, self.color, self.position, inner_radius, 1)
        
        elif self.type == PowerUpType.TRIPLE_SHOT:
            # Triple shot symbol (three small dots in a triangle)
            inner_radius = int(self.radius * 0.2 * scale)
            offset = int(self.radius * 0.4 * scale)
            
            # Top dot
            pygame.draw.circle(
                screen, 
                self.color, 
                (self.position.x, self.position.y - offset),
                inner_radius
            )
            
            # Bottom left dot
            pygame.draw.circle(
                screen, 
                self.color, 
                (self.position.x - offset, self.position.y + offset),
                inner_radius
            )
            
            # Bottom right dot
            pygame.draw.circle(
                screen, 
                self.color, 
                (self.position.x + offset, self.position.y + offset),
                inner_radius
            )
        
        elif self.type == PowerUpType.SPEED_BOOST:
            # Speed boost symbol (arrow)
            arrow_size = int(self.radius * 0.7 * scale)
            
            # Draw arrow pointing up
            points = [
                (self.position.x, self.position.y - arrow_size),  # Top
                (self.position.x - arrow_size/2, self.position.y + arrow_size/2),  # Bottom left
                (self.position.x + arrow_size/2, self.position.y + arrow_size/2),  # Bottom right
            ]
            pygame.draw.polygon(screen, self.color, points, 1)
    
    @classmethod
    def spawn_random(cls, avoid_position=None, min_distance=100):
        """
        Spawn a power-up at a random position on the screen.
        
        Args:
            avoid_position: Optional position to avoid (e.g., player position)
            min_distance: Minimum distance from the position to avoid
            
        Returns:
            PowerUp: A new power-up instance
        """
        # Keep trying positions until we find one far enough from avoid_position
        for _ in range(10):  # Try up to 10 times
            x = random.uniform(50, SCREEN_WIDTH - 50)
            y = random.uniform(50, SCREEN_HEIGHT - 50)
            
            # If we need to avoid a position, check the distance
            if avoid_position:
                distance = pygame.Vector2(x, y).distance_to(avoid_position)
                if distance < min_distance:
                    continue  # Too close, try again
            
            # Create and return the power-up
            power_up = cls(x, y)
            return power_up
        
        # If we couldn't find a good position after 10 tries, just use a random one
        power_up = cls(
            random.uniform(50, SCREEN_WIDTH - 50),
            random.uniform(50, SCREEN_HEIGHT - 50)
        )
        return power_up
