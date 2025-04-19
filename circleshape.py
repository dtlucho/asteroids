"""
Base Circle Shape module for the Asteroids game.

This module provides the fundamental CircleShape class that serves as the base
for most game objects, implementing shared functionality like:
- Basic physics (position, velocity)
- Collision detection
- Common interface for drawing and updating
"""

import pygame

class CircleShape(pygame.sprite.Sprite):
    """
    Base class for circular game objects.
    
    This class extends pygame.sprite.Sprite and implements common functionality
    for game objects including position, velocity, collision detection, and the
    interface for drawing and updating.
    
    All drawable game objects (Player, Asteroid, Shot) should inherit from this class.
    """
    
    def __init__(self, x, y, radius):
        """
        Initialize a new CircleShape.
        
        Args:
            x: Initial x-coordinate
            y: Initial y-coordinate
            radius: Radius of the circular shape for collision detection
        """
        # Add object to appropriate sprite groups if containers are defined
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        """
        Draw the object on the screen.
        
        This is an abstract method that should be implemented by subclasses.
        
        Args:
            screen: The pygame surface to draw on
        """
        # Sub-classes must override this method
        pass

    def update(self, dt):
        """
        Update the object's state for the current frame.
        
        This is an abstract method that should be implemented by subclasses.
        
        Args:
            dt: Delta time in seconds since the last frame
        """
        # Sub-classes must override this method
        pass

    def check_collision(self, other):
        """
        Check if this object collides with another CircleShape.
        
        Uses simple circle-circle collision detection based on the distance
        between centers compared to the sum of radii.
        
        Args:
            other: Another CircleShape object to check collision with
            
        Returns:
            bool: True if collision detected, False otherwise
        """
        distance = self.position.distance_to(other.position)
        if distance <= self.radius + other.radius:
            return True
        return False
    
    def wrap_position(self, screen_width, screen_height):
        """
        Wrap the object's position around screen edges.
        
        When object moves off one edge of the screen, it reappears
        from the opposite edge.
        
        Args:
            screen_width: Width of the game screen
            screen_height: Height of the game screen
        """
        # Wrap horizontally
        if self.position.x < -self.radius:
            self.position.x = screen_width + self.radius
        elif self.position.x > screen_width + self.radius:
            self.position.x = -self.radius
            
        # Wrap vertically
        if self.position.y < -self.radius:
            self.position.y = screen_height + self.radius
        elif self.position.y > screen_height + self.radius:
            self.position.y = -self.radius
