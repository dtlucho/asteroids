"""
Player module for the Asteroids game.

This module defines the Player class, which represents the player-controlled
spaceship. It handles player movement, rotation, and shooting.
"""

import pygame
import math

from src.entities.base import CircleShape
from src.entities.shot import Shot
from src.utils.constants import (
    PLAYER_RADIUS,
    PLAYER_TURN_SPEED,
    PLAYER_SPEED,
    PLAYER_SHOOT_SPEED,
    PLAYER_SHOOT_COOLDOWN,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
)
from src.entities.power_up import PowerUpType


class Player(CircleShape):
    """
    Player-controlled spaceship.

    The Player class represents the player's spaceship in the game, handling:
    - Movement based on keyboard input
    - Rotation to change direction
    - Shooting projectiles
    - Collision detection with asteroids
    - Power-up collection and effects

    The spaceship is drawn as a triangle pointing in the direction of travel.
    """
    
    # Class-level reference to sound manager (set by Game class)
    sound_manager = None
    
    # Speed boost multiplier
    SPEED_BOOST_MULTIPLIER = 1.8

    def __init__(self: "Player", x: float, y: float):
        """
        Initialize a new Player.

        Args:
            x: Initial x-coordinate
            y: Initial y-coordinate
        """
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0  # Rotation angle in degrees (0 = up)
        self.angle = 0     # Rotation angle in radians (for consistency)
        self.direction = pygame.Vector2(0, -1)  # Direction vector
        self.shoot_cooldown = 0  # Cooldown timer for shooting
        self.thrusting = False  # Flag to indicate if thrusting
        
        # Power-up properties
        self.active_power_ups = {}
        self.has_shield = False
        self.has_triple_shot = False
        self.has_speed_boost = False
        self.shield_color = (0, 255, 255)  # Cyan

    def triangle(self: "Player") -> list[pygame.Vector2]:
        """
        Calculate the vertices of the player's triangle shape.

        Returns:
            list: Three points defining the triangle's vertices
        """
        # Use the direction vector for consistency
        forward = self.direction
        right = pygame.Vector2(forward.y, -forward.x) * self.radius / 1.5
        a = self.position + forward * self.radius  # Front point
        b = self.position - forward * self.radius - right  # Back-left point
        c = self.position - forward * self.radius + right  # Back-right point
        return [a, b, c]

    def draw(self: "Player", screen: pygame.Surface):
        """
        Draw the player's spaceship on the screen.

        Args:
            screen: Pygame surface to draw on
        """
        # Draw shield if active
        if self.has_shield:
            # Draw shield as a circle around the ship
            pygame.draw.circle(
                screen, 
                self.shield_color, 
                self.position, 
                self.radius * 1.3, 
                2
            )
        
        # Draw the ship
        pygame.draw.polygon(screen, (255, 255, 255), self.triangle(), 2)
        
        # Draw visual indicator for triple shot
        if self.has_triple_shot:
            # Draw small dots at the front of the ship
            forward = self.direction
            right = pygame.Vector2(forward.y, -forward.x)
            
            # Center dot (front of ship)
            front_pos = self.position + forward * (self.radius + 5)
            pygame.draw.circle(screen, (255, 0, 255), front_pos, 2)
            
            # Left and right dots
            left_pos = front_pos - right * 5
            right_pos = front_pos + right * 5
            pygame.draw.circle(screen, (255, 0, 255), left_pos, 2)
            pygame.draw.circle(screen, (255, 0, 255), right_pos, 2)
        
        # Draw visual indicator for speed boost
        if self.has_speed_boost:
            # Draw small trail behind the ship
            backward = -self.direction
            trail_pos = self.position + backward * (self.radius + 5)
            
            # Draw a small flame-like shape
            trail_points = [
                trail_pos,
                trail_pos + backward.rotate(20) * 10,
                trail_pos + backward * 15,
                trail_pos + backward.rotate(-20) * 10
            ]
            pygame.draw.polygon(screen, (255, 255, 0), trail_points, 1)

    def rotate(self: "Player", dt: float):
        """
        Rotate the player's spaceship.

        Args:
            dt: Delta time in seconds since the last frame
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rotation += PLAYER_TURN_SPEED * dt
            self.angle += PLAYER_TURN_SPEED * dt * (math.pi / 180)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotation -= PLAYER_TURN_SPEED * dt
            self.angle -= PLAYER_TURN_SPEED * dt * (math.pi / 180)
            
        # Normalize angle to [0, 2π)
        self.angle %= 2 * math.pi
        
        # Update direction vector
        self.direction = pygame.Vector2(
            math.sin(self.angle),
            -math.cos(self.angle)
        )

    def move(self: "Player", dt: float):
        """
        Move the player in the current facing direction.

        Args:
            dt: Delta time in seconds since the last frame
        """
        # Use the direction vector for movement
        forward = self.direction
        
        # Apply speed boost if active
        speed = PLAYER_SPEED
        if self.has_speed_boost:
            speed *= self.SPEED_BOOST_MULTIPLIER
            
        self.position += forward * speed * dt

    def update(self: "Player", dt: float):
        """
        Update the player's state based on keyboard input.

        Handles rotation, movement, and shooting based on key presses.
        Also updates cooldown timers and power-up durations.

        Args:
            dt: Delta time in seconds since the last frame
        """
        # Update power-up timers
        self.update_power_ups(dt)
        
        # Update cooldown timer
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= dt

        # Handle rotation
        self.rotate(dt)

        # Handle movement
        keys = pygame.key.get_pressed()
        self.thrusting = False  # Reset thrusting flag
        
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move(dt)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move(-dt)

        # Handle shooting
        if keys[pygame.K_SPACE] and self.shoot_cooldown <= 0:
            self.shoot()
            self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN
            
        # Keep player on screen by wrapping around edges
        self.wrap_position(SCREEN_WIDTH, SCREEN_HEIGHT)

    def shoot(self):
        """
        Fire a projectile if cooldown has expired.

        Creates a new Shot object moving in the direction the player is facing.
        If triple shot is active, fires three shots in a spread pattern.
        """
        # Use the player's direction vector
        direction = self.direction
        
        if self.has_triple_shot:
            # Create three shots in a spread pattern
            left_dir = pygame.Vector2(direction).rotate(-15)
            right_dir = pygame.Vector2(direction).rotate(15)
            self._create_shot(left_dir)   # Left shot
            self._create_shot(direction)  # Center shot
            self._create_shot(right_dir)  # Right shot
        else:
            # Create a single shot
            self._create_shot(direction)
        
        # Play shooting sound if sound manager is available
        if Player.sound_manager:
            Player.sound_manager.play("shoot")
    
    def _create_shot(self, direction):
        """
        Create a single shot moving in the specified direction.
        
        Args:
            direction: Direction vector for the shot
        """
        # Create new shot at player's position
        shot = Shot(self.position.x, self.position.y)
        
        # Set shot velocity
        velocity = direction * PLAYER_SHOOT_SPEED
        shot.velocity = velocity
    
    def update_power_ups(self, dt):
        """
        Update power-up timers and remove expired ones.
        
        Args:
            dt: Delta time in seconds since the last frame
        """
        # Update each active power-up timer
        expired_power_ups = []
        
        for power_type, time_left in self.active_power_ups.items():
            # Reduce time left
            self.active_power_ups[power_type] = time_left - dt
            
            # Check if expired
            if self.active_power_ups[power_type] <= 0:
                expired_power_ups.append(power_type)
        
        # Remove expired power-ups
        for power_type in expired_power_ups:
            self.remove_power_up(power_type)
    
    def add_power_up(self, power_type, duration):
        """
        Add a power-up effect to the player.
        
        Args:
            power_type: Type of power-up to add
            duration: Duration of the power-up in seconds
        """
        # Add or refresh the power-up timer
        self.active_power_ups[power_type] = duration
        
        # Apply power-up effect
        if power_type == PowerUpType.SHIELD:
            self.has_shield = True
        elif power_type == PowerUpType.TRIPLE_SHOT:
            self.has_triple_shot = True
        elif power_type == PowerUpType.SPEED_BOOST:
            self.has_speed_boost = True
        
        # Play sound effect if available
        if Player.sound_manager:
            Player.sound_manager.play("shoot")  # Reuse shoot sound for now
    
    def remove_power_up(self, power_type):
        """
        Remove a power-up effect from the player.
        
        Args:
            power_type: Type of power-up to remove
        """
        # Remove the power-up from active list
        if power_type in self.active_power_ups:
            del self.active_power_ups[power_type]
        
        # Remove power-up effect
        if power_type == PowerUpType.SHIELD:
            self.has_shield = False
        elif power_type == PowerUpType.TRIPLE_SHOT:
            self.has_triple_shot = False
        elif power_type == PowerUpType.SPEED_BOOST:
            self.has_speed_boost = False
    
    def has_active_shield(self):
        """
        Check if the player has an active shield.
        
        Returns:
            bool: True if shield is active, False otherwise
        """
        return self.has_shield
