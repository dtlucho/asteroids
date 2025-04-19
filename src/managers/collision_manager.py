"""
Collision Manager module for the Asteroids game.

This module defines the CollisionManager class, which centralizes all
collision detection and response logic in the game.
"""

import pygame
from src.utils.constants import ASTEROID_BASE_SCORE, ASTEROID_MIN_RADIUS
from src.ui import screens


class CollisionManager:
    """
    Manages collision detection and response between game objects.
    
    The CollisionManager is responsible for:
    - Detecting collisions between different types of game objects
    - Handling the appropriate responses to collisions
    - Managing scoring when asteroids are destroyed
    
    This centralizes collision logic that would otherwise be spread across
    different game objects or the main game loop.
    """
    
    def __init__(self, game_state_callback=None):
        """
        Initialize the collision manager.
        
        Args:
            game_state_callback: Optional callback function to notify about game state
                                changes (e.g., player death)
        """
        self.game_state_callback = game_state_callback
        self.score = 0
    
    def check_player_asteroid_collisions(self, player, asteroids):
        """
        Check for collisions between the player and asteroids.
        
        Args:
            player: The player object
            asteroids: Group of asteroid objects
            
        Returns:
            bool: True if a collision was detected, False otherwise
        """
        for asteroid in asteroids:
            if player.check_collision(asteroid):
                if self.game_state_callback:
                    self.game_state_callback("player_death")
                return True
        return False
    
    def check_shot_asteroid_collisions(self, shots, asteroids):
        """
        Check for collisions between shots and asteroids.
        
        Args:
            shots: Group of shot objects
            asteroids: Group of asteroid objects
            
        Returns:
            int: Number of collisions detected and processed
        """
        collision_count = 0
        
        for asteroid in asteroids:
            for shot in shots:
                if shot.check_collision(asteroid):
                    # Calculate score based on asteroid size
                    asteroid_score = ASTEROID_BASE_SCORE * (
                        asteroid.radius // ASTEROID_MIN_RADIUS
                    )
                    self.score += asteroid_score
                    
                    # Display floating score text for feedback
                    screens.add_floating_score(asteroid.position, asteroid_score)
                    
                    # Split asteroid and remove shot
                    asteroid.split()
                    shot.kill()
                    
                    collision_count += 1
                    break  # Move to next asteroid after collision
        
        return collision_count
    
    def get_score(self):
        """
        Get the current score.
        
        Returns:
            int: The current score
        """
        return self.score
    
    def reset(self):
        """
        Reset the collision manager state.
        
        This resets the score to zero and any other state that needs to be
        reset when starting a new game.
        """
        self.score = 0
