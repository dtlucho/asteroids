"""
Power-up Manager module for the Asteroids game.

This module defines the PowerUpManager class, which handles spawning
and managing power-ups in the game.
"""

import pygame
import random
from src.entities.power_up import PowerUp, PowerUpType


class PowerUpManager:
    """
    Manages power-ups in the game.
    
    The PowerUpManager is responsible for:
    - Spawning power-ups at random intervals
    - Managing power-up collection by the player
    - Applying power-up effects
    
    This centralizes power-up logic and makes it easier to balance
    and tune power-up spawning.
    """
    
    def __init__(self, spawn_interval_range=(1, 3)):
        """
        Initialize the power-up manager.
        
        Args:
            spawn_interval_range: Tuple of (min, max) seconds between power-up spawns
        """
        self.power_ups = pygame.sprite.Group()
        self.min_spawn_interval, self.max_spawn_interval = spawn_interval_range
        self.spawn_timer = random.uniform(self.min_spawn_interval, self.max_spawn_interval)
        
        # Set container group for power-ups
        PowerUp.containers = self.power_ups
        
        # Reference to sound manager (set by Game class)
        self.sound_manager = None
    
    def update(self, dt, player):
        """
        Update power-ups and check for collisions with the player.
        
        Args:
            dt: Delta time in seconds since the last frame
            player: The player object to check collisions with
            
        Returns:
            bool: True if a power-up was collected, False otherwise
        """
        # Update spawn timer
        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            self.spawn_power_up(player.position)
            self.spawn_timer = random.uniform(self.min_spawn_interval, self.max_spawn_interval)
        
        # Update all power-ups
        self.power_ups.update(dt)
        
        # Check for collisions with player
        collected = False
        for power_up in list(self.power_ups):  # Create a copy of the list to safely modify during iteration
            # Calculate distance between player and power-up centers
            distance = player.position.distance_to(power_up.position)
            
            # Use a slightly larger collision radius for better usability
            collection_radius = player.radius + power_up.radius * 1.2
            
            if distance <= collection_radius:
                # Apply power-up effect to player
                player.add_power_up(power_up.type, power_up.duration)
                
                # Play collection sound
                if self.sound_manager:
                    self.sound_manager.play("shoot")  # Reuse shoot sound for now
                
                # Remove the power-up
                power_up.kill()
                collected = True
        
        return collected
    
    def spawn_power_up(self, avoid_position=None):
        """
        Spawn a new power-up at a random position.
        
        Args:
            avoid_position: Optional position to avoid (e.g., player position)
        """
        # Create a new power-up and add it to the power_ups group
        power_up = PowerUp.spawn_random(avoid_position)
        self.power_ups.add(power_up)
        return power_up
    
    def draw(self, screen):
        """
        Draw all power-ups.
        
        Args:
            screen: Pygame surface to draw on
        """
        for power_up in self.power_ups:
            power_up.draw(screen)
    
    def reset(self):
        """
        Reset the power-up manager, removing all power-ups.
        """
        self.power_ups.empty()
        self.spawn_timer = random.uniform(self.min_spawn_interval, self.max_spawn_interval)
