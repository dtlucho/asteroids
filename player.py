"""
Player module for the Asteroids game.

This module defines the Player class, which represents the player-controlled
spaceship. It handles player movement, rotation, and shooting.
"""

import pygame

from circleshape import CircleShape
from shot import Shot
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN, SCREEN_WIDTH, SCREEN_HEIGHT

class Player(CircleShape):
    """
    Player-controlled spaceship.
    
    The Player class represents the player's spaceship in the game, handling:
    - Movement based on keyboard input
    - Rotation to change direction
    - Shooting projectiles
    - Collision detection with asteroids
    
    The spaceship is drawn as a triangle pointing in the direction of travel.
    """
    
    def __init__(self: 'Player', x: float, y: float):
        """
        Initialize a new Player.
        
        Args:
            x: Initial x-coordinate
            y: Initial y-coordinate
        """
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0           # Rotation angle in degrees (0 = up)
        self.shoot_cooldown = 0      # Cooldown timer for shooting
    
    def triangle(self: 'Player') -> list[pygame.Vector2]:
        """
        Calculate the vertices of the player's triangle shape.
        
        Returns:
            list: Three points defining the triangle's vertices
        """
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius            # Front point
        b = self.position - forward * self.radius - right    # Back-left point
        c = self.position - forward * self.radius + right    # Back-right point
        return [a, b, c]
    
    def draw(self: 'Player', screen: pygame.Surface):
        """
        Draw the player's spaceship on the screen.
        
        Args:
            screen: Pygame surface to draw on
        """
        pygame.draw.polygon(screen, (255,255,255), self.triangle(), 2)
    
    def rotate(self: 'Player', dt: float):
        """
        Rotate the player's spaceship.
        
        Args:
            dt: Delta time in seconds since the last frame
        """
        self.rotation += PLAYER_TURN_SPEED * dt

    def update(self: 'Player', dt: float):
        """
        Update the player's state based on keyboard input.
        
        Handles rotation, movement, and shooting based on key presses.
        Also updates cooldown timers.
        
        Args:
            dt: Delta time in seconds since the last frame
        """
        # Update shooting cooldown
        self.shoot_cooldown -= dt
        
        # Get current keyboard state
        keys = pygame.key.get_pressed()

        # Handle rotation (left/right)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.rotate(-dt)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.rotate(dt)
            
        # Handle movement (forward/backward)
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.move(dt)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.move(-dt)
            
        # Handle shooting
        if keys[pygame.K_SPACE]:
            self.shoot()
        
        # Keep player on screen by wrapping around edges
        self.wrap_position(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    def move(self: 'Player', dt: float):
        """
        Move the player in the current facing direction.
        
        Args:
            dt: Delta time in seconds since the last frame
        """
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self: 'Player'):
        """
        Fire a projectile if cooldown has expired.
        
        Creates a new Shot object moving in the direction the player is facing.
        """
        if self.shoot_cooldown > 0:
            return
            
        # Reset cooldown timer
        self.shoot_cooldown = PLAYER_SHOOT_COOLDOWN
        
        # Create new shot at player's position
        shot = Shot(self.position.x, self.position.y)
        
        # Set shot velocity in direction player is facing
        direction = pygame.Vector2(0, 1).rotate(self.rotation)
        velocity = direction * PLAYER_SHOOT_SPEED
        shot.velocity = velocity