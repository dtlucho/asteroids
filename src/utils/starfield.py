"""
Starfield module for the Asteroids game.

This module defines the Starfield class, which creates a parallax
scrolling star background effect.
"""

import pygame
import random
import math


class Starfield:
    """
    Creates a parallax scrolling starfield background.
    
    The starfield creates multiple layers of stars that move at different
    speeds to create a sense of depth and movement through space.
    """
    
    def __init__(self, screen_width, screen_height, star_count=100):
        """
        Initialize the starfield.
        
        Args:
            screen_width: Width of the game screen
            screen_height: Height of the game screen
            star_count: Number of stars to generate
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.stars = []
        
        # Create stars with different depths (layers)
        for _ in range(star_count):
            # Assign a random layer (depth) to each star
            layer = random.randint(0, 2)
            
            # Create a star with random position and layer
            star = {
                'x': random.randint(0, screen_width),
                'y': random.randint(0, screen_height),
                'layer': layer,
                'size': 1 if layer == 0 else (2 if layer == 1 else 3),
                'brightness': random.randint(100, 255),
                'twinkle_speed': random.uniform(1.0, 3.0),
                'twinkle_offset': random.uniform(0, 2 * math.pi),
                'twinkle_time': 0  # Initialize twinkle_time
            }
            self.stars.append(star)
    
    def update(self, dt, player_velocity=None):
        """
        Update star positions based on player movement.
        
        Args:
            dt: Delta time in seconds since the last frame
            player_velocity: Optional player velocity vector for parallax effect
        """
        # Default movement if no player velocity is provided
        move_x = 0
        move_y = 0
        
        # If player velocity is provided, move stars in the opposite direction
        if player_velocity:
            # Scale down the movement for a subtle effect
            move_x = -player_velocity.x * dt * 0.1
            move_y = -player_velocity.y * dt * 0.1
        
        # Update each star's position
        for star in self.stars:
            # Stars in different layers move at different speeds
            layer_speed = 0.5 + star['layer'] * 0.5  # 0.5, 1.0, or 1.5 based on layer
            
            # Move the star
            star['x'] += move_x * layer_speed
            star['y'] += move_y * layer_speed
            
            # Update star twinkle effect
            star['twinkle_time'] += dt
            
            # Wrap stars around the screen edges
            if star['x'] < 0:
                star['x'] += self.screen_width
            elif star['x'] >= self.screen_width:
                star['x'] -= self.screen_width
                
            if star['y'] < 0:
                star['y'] += self.screen_height
            elif star['y'] >= self.screen_height:
                star['y'] -= self.screen_height
    
    def draw(self, screen):
        """
        Draw the starfield on the screen.
        
        Args:
            screen: Pygame surface to draw on
        """
        for star in self.stars:
            # Calculate twinkle effect (pulsing brightness)
            twinkle = math.sin(star['twinkle_time'] * star['twinkle_speed'] + star['twinkle_offset'])
            brightness_mod = int(twinkle * 30)  # Vary brightness by ±30
            brightness = max(50, min(255, star['brightness'] + brightness_mod))
            
            # Set star color based on brightness and a slight color tint
            color = (
                brightness,  # Red
                brightness,  # Green
                min(255, brightness + 20)  # Blue (slightly higher for a cool tint)
            )
            
            # Draw the star
            if star['size'] == 1:
                # Small stars are just single pixels
                screen.set_at((int(star['x']), int(star['y'])), color)
            else:
                # Larger stars are small circles
                pygame.draw.circle(
                    screen,
                    color,
                    (int(star['x']), int(star['y'])),
                    star['size'] // 2
                )
