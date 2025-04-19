"""
Collision Manager module for the Asteroids game.

This module defines the CollisionManager class, which centralizes all
collision detection and response logic in the game.
"""

from collections.abc import Callable
import pygame
from src.entities.player import Player
from src.utils.constants import ASTEROID_BASE_SCORE, ASTEROID_MIN_RADIUS
from src.ui import screens
from src.entities.power_up import PowerUpType


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

    def __init__(self: "CollisionManager", game_state_callback: Callable | None = None):
        """
        Initialize the collision manager.

        Args:
            game_state_callback: Optional callback function to notify about game state
                                changes (e.g., player death)
        """
        self.game_state_callback = game_state_callback
        self.score = 0

        # Reference to sound manager (set by Game class)
        self.sound_manager = None

    def check_player_asteroid_collisions(
        self: "CollisionManager", player: "Player", asteroids: pygame.sprite.Group
    ) -> bool:
        """
        Check for collisions between the player and asteroids.

        If the player has a shield, it will absorb one collision.

        Args:
            player: The player object
            asteroids: Group of asteroid objects

        Returns:
            bool: True if a collision was detected, False otherwise
        """
        for asteroid in asteroids:
            if player.check_collision(asteroid):
                # Check if player has a shield
                if player.has_active_shield():
                    # Shield absorbs the collision
                    player.remove_power_up(PowerUpType.SHIELD)

                    # Create a new smaller asteroid (like a deflection)
                    asteroid.split()

                    # Play shield hit sound if available
                    if self.sound_manager:
                        self.sound_manager.play("explosion_small")

                    return False
                else:
                    # No shield, player is hit
                    if self.game_state_callback:
                        self.game_state_callback("player_death")
                    return True
        return False

    def check_shot_asteroid_collisions(
        self: "CollisionManager",
        shots: pygame.sprite.Group,
        asteroids: pygame.sprite.Group,
    ) -> int:
        """
        Check for collisions between shots and asteroids.

        Args:
            shots: Group of shot objects
            asteroids: Group of asteroid objects

        Returns:
            int: Number of asteroids destroyed
        """
        destroyed_count = 0

        for shot in shots:
            for asteroid in asteroids:
                if shot.check_collision(asteroid):
                    # Calculate score based on asteroid size
                    score_value = int(
                        ASTEROID_BASE_SCORE / (asteroid.radius / ASTEROID_MIN_RADIUS)
                    )
                    self.score += score_value

                    # Create floating score text
                    screens.add_floating_score(asteroid.position, score_value)

                    # Store asteroid position and size for explosion effect
                    asteroid_position = pygame.Vector2(asteroid.position)
                    asteroid_size = asteroid.radius

                    # Try to split the asteroid
                    asteroid.split()

                    # Remove the shot
                    shot.kill()

                    # Notify about asteroid destruction with position and size
                    if self.game_state_callback:
                        self.game_state_callback(
                            "asteroid_destroyed",
                            position=asteroid_position,
                            size=asteroid_size,
                        )

                    destroyed_count += 1
                    break  # Shot can only hit one asteroid

        return destroyed_count

    def get_score(self: "CollisionManager") -> int:
        """
        Get the current score.

        Returns:
            int: The current score
        """
        return self.score

    def reset(self: "CollisionManager"):
        """
        Reset the collision manager state.

        This resets the score to zero and any other state that needs to be
        reset when starting a new game.
        """
        self.score = 0
