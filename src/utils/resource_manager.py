"""
Resource Manager module for the Asteroids game.

This module defines the ResourceManager class, which centralizes the loading
and caching of game assets such as fonts, images, and sounds.
"""

import pygame
import os


class ResourceManager:
    """
    Manages game resources like fonts, images, and sounds.
    
    The ResourceManager is responsible for:
    - Loading resources from files
    - Caching resources to avoid redundant loading
    - Providing a clean interface for accessing resources
    
    This improves performance and maintainability by centralizing
    resource management.
    """
    
    def __init__(self):
        """
        Initialize the resource manager.
        
        Sets up empty caches for different types of resources.
        """
        self.fonts = {}  # Cache for loaded fonts
        self.images = {}  # Cache for loaded images (for future use)
        self.sounds = {}  # Cache for loaded sounds (for future use)
        
        # Path to assets directory
        self.assets_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'assets')
        
        # Path to retro font
        self.retro_font_path = os.path.join(self.assets_dir, 'fonts', 'arcade_classic.ttf')
        
        # Check if retro font exists
        if not os.path.exists(self.retro_font_path):
            print(f"Warning: Retro font not found at {self.retro_font_path}")
            self.retro_font_path = None
    
    def get_font(self, size, name=None, use_retro=True):
        """
        Get a font of the specified size.
        
        Loads the font if it's not already cached, otherwise returns
        the cached version.
        
        Args:
            size: Font size in points
            name: Font name or path (None for default font)
            use_retro: Whether to use the retro font (if available)
            
        Returns:
            pygame.font.Font: The requested font
        """
        # If retro font is requested and available, use it
        if use_retro and self.retro_font_path and os.path.exists(self.retro_font_path):
            name = self.retro_font_path
        
        # Create a unique key for this font
        key = f"{name}_{size}"
        
        # Check if the font is already cached
        if key not in self.fonts:
            # Load and cache the font
            self.fonts[key] = pygame.font.Font(name, size)
        
        return self.fonts[key]
    
    def load_image(self, path, convert_alpha=True):
        """
        Load an image from the specified path.
        
        Args:
            path: Path to the image file
            convert_alpha: Whether to convert the image for alpha blending
            
        Returns:
            pygame.Surface: The loaded image
        """
        # Check if the image is already cached
        if path not in self.images:
            # Load the image
            image = pygame.image.load(path)
            
            # Convert the image for faster blitting
            if convert_alpha:
                image = image.convert_alpha()
            else:
                image = image.convert()
            
            # Cache the image
            self.images[path] = image
        
        return self.images[path]
    
    def load_sound(self, path):
        """
        Load a sound from the specified path.
        
        Args:
            path: Path to the sound file
            
        Returns:
            pygame.mixer.Sound: The loaded sound
        """
        # Check if the sound is already cached
        if path not in self.sounds:
            # Load and cache the sound
            self.sounds[path] = pygame.mixer.Sound(path)
        
        return self.sounds[path]
    
    def clear_cache(self, resource_type=None):
        """
        Clear the resource cache.
        
        Args:
            resource_type: Type of resource to clear ('fonts', 'images', 'sounds'),
                          or None to clear all caches
        """
        if resource_type == 'fonts' or resource_type is None:
            self.fonts.clear()
        
        if resource_type == 'images' or resource_type is None:
            self.images.clear()
        
        if resource_type == 'sounds' or resource_type is None:
            self.sounds.clear()
