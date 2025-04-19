"""
Constants module for the Asteroids game.

This module defines all game constants in one place for easy tuning,
including screen dimensions, object sizes, speeds, and gameplay parameters.
"""

# Screen dimensions
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Asteroid parameters
ASTEROID_MIN_RADIUS = 20              # Radius of smallest asteroid
ASTEROID_KINDS = 3                    # Number of asteroid size tiers
ASTEROID_SPAWN_RATE = 0.8             # Seconds between spawns
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS
ASTEROID_BASE_SCORE = 100             # Score for destroying smallest asteroid

# Player parameters
PLAYER_RADIUS = 20                    # Size of player ship for collisions
PLAYER_TURN_SPEED = 300               # Rotation speed in degrees per second
PLAYER_SPEED = 200                    # Movement speed in pixels per second
PLAYER_SHOOT_SPEED = 500              # Shot velocity in pixels per second
PLAYER_SHOOT_COOLDOWN = 0.3           # Seconds between shots

# Shot parameters
SHOT_RADIUS = 5                       # Size of player shots
SHOT_LIFETIME = 2.0                   # Seconds before shot disappears