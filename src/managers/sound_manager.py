"""
Sound Manager module for the Asteroids game.

This module defines the SoundManager class, which handles loading
and playing sound effects in the game.
"""

import pygame
from src.utils.resource_manager import ResourceManager


class SoundManager:
    """
    Manages sound effects for the game.

    The SoundManager is responsible for:
    - Loading sound assets
    - Playing sound effects at appropriate times
    - Controlling sound volume

    This provides a simple interface for playing sounds throughout the game.
    """

    def __init__(
        self: "SoundManager", resource_manager: "ResourceManager"
    ):
        """
        Initialize the sound manager.

        Args:
            resource_manager: ResourceManager instance to use for loading sounds
        """
        # Initialize pygame mixer if not already initialized
        if not pygame.mixer.get_init():
            pygame.mixer.init()

        # Use provided resource manager or create a new one
        self.resource_manager = resource_manager or ResourceManager()

        # Set default volume
        self.volume = 0.7  # 70% volume

        # Define available sound effects
        self.available_sounds = [
            "shoot",
            "explosion_large",
            "explosion_small",
            "game_over",
        ]

        # Dictionary to store loaded sounds
        self.sounds = {}

        # Flag to enable/disable sounds
        self.enabled = True

    def load_sounds(self: "SoundManager"):
        """
        Load all game sound effects.

        Creates placeholder sound effects directly in memory.
        """
        # Create placeholder sounds directly in memory
        for name in self.available_sounds:
            try:
                # Generate a placeholder sound directly
                sound_data = self._generate_placeholder_sound(name)
                self.sounds[name] = pygame.mixer.Sound(buffer=sound_data)
                self.sounds[name].set_volume(self.volume)
            except Exception as e:
                print(f"Warning: Could not create sound {name}: {e}")

    def _generate_placeholder_sound(self: "SoundManager", sound_type: str) -> bytes:
        """
        Generate a simple placeholder sound.

        Args:
            sound_type: Type of sound to generate

        Returns:
            bytes: Sound data as bytes
        """
        # Sample rate and bit depth
        sample_rate = 22050
        bits = 16

        # Generate different sounds based on type
        if sound_type == "shoot":
            # Short high-pitched sound
            duration = 0.1  # seconds
            frequency = 880  # Hz (A5)
        elif sound_type == "explosion_small":
            # Medium noise burst
            duration = 0.3
            frequency = 220  # Hz (A3)
        elif sound_type == "explosion_large":
            # Longer, lower noise burst
            duration = 0.5
            frequency = 110  # Hz (A2)
        elif sound_type == "game_over":
            # Descending tone
            duration = 1.0
            frequency = 440  # Hz (A4)
        else:
            # Default sound
            duration = 0.2
            frequency = 440  # Hz (A4)

        # Calculate buffer size
        buffer_size = int(sample_rate * duration)

        # Create a simple sine wave
        import array
        import math

        max_amplitude = 2 ** (bits - 1) - 1

        # Create the buffer
        buffer = array.array("h", [0] * buffer_size)

        # Fill the buffer with a sine wave
        for i in range(buffer_size):
            t = i / sample_rate  # Time in seconds

            # Different sound generation based on type
            if sound_type == "game_over":
                # Descending tone
                freq = frequency * (1 - t / duration)
                value = int(max_amplitude * math.sin(2 * math.pi * freq * t))
            elif "explosion" in sound_type:
                # Noise with decay
                import random

                decay = 1 - t / duration
                value = int(max_amplitude * decay * (random.random() * 2 - 1))
            else:
                # Simple sine wave
                value = int(max_amplitude * math.sin(2 * math.pi * frequency * t))

            buffer[i] = value

        return buffer

    def play(self: "SoundManager", sound_name: str):
        """
        Play a sound effect by name.

        Args:
            sound_name: Name of the sound to play
        """
        if not self.enabled:
            return

        if sound_name in self.sounds:
            self.sounds[sound_name].play()
        else:
            print(f"Warning: Sound '{sound_name}' not loaded")

    def set_volume(self: "SoundManager", volume: float):
        """
        Set the volume for all sounds.

        Args:
            volume: Volume level (0.0 to 1.0)
        """
        self.volume = max(0.0, min(1.0, volume))

        # Update volume for all loaded sounds
        for sound in self.sounds.values():
            sound.set_volume(self.volume)

    def enable(self: "SoundManager", enabled: bool = True):
        """
        Enable or disable sound effects.

        Args:
            enabled: True to enable sounds, False to disable
        """
        self.enabled = enabled
