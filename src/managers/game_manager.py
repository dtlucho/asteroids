"""
Game Manager module for the Asteroids game.

This module defines the Game class, which handles:
- Game initialization
- Main game loop
- State management
- Event handling
"""

import pygame
import time

from src.utils.constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    DEBUG_MODE,
)
from src.utils.resource_manager import ResourceManager
from src.utils.game_state import GameState
from src.entities.player import Player
from src.entities.asteroid import Asteroid
from src.managers.asteroid_manager import AsteroidField
from src.managers.collision_manager import CollisionManager
from src.managers.sound_manager import SoundManager
from src.managers.power_up_manager import PowerUpManager
from src.entities.shot import Shot
from src.ui import screens
from src.entities.power_up import PowerUp
from src.utils.starfield import Starfield
from src.effects.explosion import ExplosionManager
from src.effects.screen_shake import ScreenShake


class Game:
    """
    Main game class that manages the game loop and state.
    
    This class is responsible for:
    - Initializing pygame and game objects
    - Running the main game loop
    - Handling state transitions
    - Processing input events
    - Managing collisions and scoring
    """
    
    def __init__(self):
        """
        Initialize the game, pygame, and create the game window.
        """
        print("Starting asteroids!")
        print("Screen width:", SCREEN_WIDTH)
        print("Screen height:", SCREEN_HEIGHT)

        # Initialize pygame and create window
        pygame.init()
        
        # Initialize resource manager
        self.resource_manager = ResourceManager()
        
        # Load fonts through the resource manager
        self.title_font = self.resource_manager.get_font(64)  # Larger font for titles
        self.normal_font = self.resource_manager.get_font(36)  # Medium font for instructions
        self.small_font = self.resource_manager.get_font(24)  # Small font for scores/misc
        
        # Create sprite groups for game objects
        self.updatable = pygame.sprite.Group()
        self.drawable = pygame.sprite.Group()
        self.asteroids = pygame.sprite.Group()
        self.shots = pygame.sprite.Group()
        self.power_ups = pygame.sprite.Group()
        
        # Create managers
        self.collision_manager = CollisionManager(self.handle_collision_event)
        self.power_up_manager = PowerUpManager()
        
        # Make sure the power-up manager uses our sprite group
        self.power_up_manager.power_ups = self.power_ups
        
        # Create sound manager and load sounds
        self.sound_manager = SoundManager(self.resource_manager)
        self.sound_manager.load_sounds()
        
        # Set sound manager references in game entities and managers
        Player.sound_manager = self.sound_manager
        Asteroid.sound_manager = self.sound_manager
        PowerUp.sound_manager = self.sound_manager
        self.collision_manager.sound_manager = self.sound_manager
        self.power_up_manager.sound_manager = self.sound_manager

        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Asteroids")  # Set window title
        self.clock = pygame.time.Clock()

        # Set container groups for each game object type
        Player.containers = (self.updatable, self.drawable)
        Asteroid.containers = (self.asteroids, self.updatable, self.drawable)
        AsteroidField.containers = self.updatable
        Shot.containers = (self.shots, self.updatable, self.drawable)
        
        # Set power-up containers - this is important for proper sprite group management
        PowerUp.containers = (self.power_ups, self.updatable, self.drawable)

        # Create visual effects
        self.starfield = Starfield(SCREEN_WIDTH, SCREEN_HEIGHT, star_count=150)
        self.explosion_manager = ExplosionManager()
        self.screen_shake = ScreenShake()
        
        # Create initial game objects
        self.player = None
        self.asteroid_field = None
        
        # Reset game to initial state
        self.reset_game()

        # Delta time for frame rate independence
        self.dt = 0

        # Start in menu state
        self.current_game_state = GameState.MENU

        # Difficulty settings
        self.difficulty_level = 1
        self.difficulty_timer = 0
        self.DIFFICULTY_INCREASE_INTERVAL = 30  # seconds

        # FPS tracking
        self.prev_time = time.time()
        self.fps_update_timer = 0
        self.fps = 0
        
    def handle_collision_event(self, event_type, **kwargs):
        """
        Handle collision events from the collision manager.
        
        Args:
            event_type: Type of collision event
            **kwargs: Additional event data
        """
        if event_type == "player_death":
            # Create a large explosion at player position
            if hasattr(self, 'player') and self.player:
                self.explosion_manager.create_explosion(
                    self.player.position.x,
                    self.player.position.y,
                    size=40  # Large explosion for player death
                )
                # Strong screen shake for player death
                self.screen_shake.start(intensity=15, duration=0.6)
            self.current_game_state = GameState.GAME_OVER
            
        elif event_type == "asteroid_destroyed":
            # Create explosion at asteroid position
            if 'position' in kwargs and 'size' in kwargs:
                self.explosion_manager.create_explosion(
                    kwargs['position'].x,
                    kwargs['position'].y,
                    size=kwargs['size']
                )
                # Screen shake intensity based on asteroid size
                shake_intensity = min(10, kwargs['size'] / 4)
                self.screen_shake.start(intensity=shake_intensity, duration=0.3)
                
    def reset_game(self):
        """
        Reset game objects and state for a new game.
        
        Clears all sprite groups and recreates the player and asteroid field.
        """
        # Clear existing sprite groups
        self.updatable.empty()
        self.drawable.empty()
        self.asteroids.empty()
        self.shots.empty()
        self.power_ups.empty()

        # Recreate player and asteroid field
        self.player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.asteroid_field = AsteroidField()
        
        # Reset managers
        self.collision_manager.reset()
        self.power_up_manager.reset()
        
        # Reset difficulty
        self.difficulty_level = 1
        self.difficulty_timer = 0
        
    def handle_events(self):
        """
        Process input events and handle state transitions.
        
        Returns:
            bool: False if the game should exit, True otherwise
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and self.current_game_state == GameState.PLAYING:
                    self.current_game_state = GameState.PAUSED
                elif (
                    event.key == pygame.K_SPACE
                    and self.current_game_state == GameState.PAUSED
                ):
                    self.current_game_state = GameState.PLAYING
                elif (
                    event.key == pygame.K_SPACE and self.current_game_state == GameState.MENU
                ):
                    # Reset game when starting from menu
                    self.reset_game()
                    self.collision_manager.reset()
                    self.current_game_state = GameState.PLAYING
                    # Play a sound effect when starting the game
                    self.sound_manager.play("shoot")
                elif (
                    event.key == pygame.K_RETURN
                    and self.current_game_state == GameState.GAME_OVER
                ):
                    self.current_game_state = GameState.MENU
                    
        return True
        
    def update(self):
        """
        Update game state based on current game state.
        
        Handles different update logic for different game states.
        """
        if self.current_game_state == GameState.MENU:
            pass  # No updates needed in menu
            
        elif self.current_game_state == GameState.PLAYING:
            # Update starfield with player velocity for parallax effect
            self.starfield.update(self.dt, self.player.velocity if self.player else None)
            
            # Update visual effects
            self.explosion_manager.update(self.dt)
            self.screen_shake.update(self.dt)
            
            # Update all game objects
            self.updatable.update(self.dt)

            # Check for collisions using the collision manager
            self.collision_manager.check_player_asteroid_collisions(self.player, self.asteroids)
            self.collision_manager.check_shot_asteroid_collisions(self.shots, self.asteroids)
            
            # Update power-ups
            self.power_up_manager.update(self.dt, self.player)
            
            # Update floating score texts
            screens.update_floating_scores(self.dt)

            # Update difficulty level
            self.difficulty_timer += self.dt
            if self.difficulty_timer >= self.DIFFICULTY_INCREASE_INTERVAL:
                self.difficulty_timer = 0
                self.difficulty_level += 1
                print(f"Difficulty increased to level {self.difficulty_level}")

            # Adjust asteroid field parameters based on difficulty
            self.asteroid_field.spawn_rate = max(
                0.2, self.asteroid_field.spawn_rate - (self.difficulty_level * 0.05)
            )
            self.asteroid_field.speed_multiplier = 1.0 + (self.difficulty_level * 0.1)
            
        elif self.current_game_state == GameState.PAUSED:
            pass  # No updates when paused
            
        elif self.current_game_state == GameState.GAME_OVER:
            pass  # No updates when game over
            
    def render(self):
        """
        Render the current game state to the screen.
        
        Draws different UI elements based on the current game state.
        """
        # Create a temporary surface for rendering with screen shake
        temp_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Clear screen with very dark blue (almost black, but with a hint of color)
        temp_surface.fill((2, 3, 10))
        
        # Draw starfield background
        self.starfield.draw(temp_surface)
        
        # Draw explosion effects
        self.explosion_manager.draw(temp_surface)

        # Current time for animations
        current_time = time.time()
        frame_time = current_time - self.prev_time
        self.prev_time = current_time

        # Update FPS counter
        self.fps_update_timer += self.dt
        if self.fps_update_timer >= 0.5:  # Update FPS display twice per second
            self.fps = 1.0 / max(frame_time, 0.001)  # Avoid division by zero
            self.fps_update_timer = 0

        # Draw based on game state
        if self.current_game_state == GameState.MENU:
            screens.draw_menu_screen(temp_surface, self.title_font, self.normal_font, current_time)
        elif self.current_game_state == GameState.PLAYING:
            # Draw game objects
            screens.draw_game_screen(self.drawable, temp_surface, self.small_font, self.collision_manager.get_score(), self.dt)
            
            # Draw power-ups
            self.power_up_manager.draw(temp_surface)
            
            # Draw floating score texts
            screens.draw_floating_scores(temp_surface, self.small_font)
        elif self.current_game_state == GameState.PAUSED:
            screens.draw_paused_screen(self.drawable, temp_surface, self.title_font, self.normal_font)
        elif self.current_game_state == GameState.GAME_OVER:
            screens.draw_game_over_screen(self.drawable, temp_surface, self.title_font, self.normal_font, self.collision_manager.get_score())

        # Draw debug information if in debug mode
        if DEBUG_MODE:
            screens.draw_debug_info(temp_surface, self.small_font, self.fps)
            
        # Apply screen shake and blit the temp surface to the main screen
        self.screen.blit(temp_surface, (self.screen_shake.offset_x, self.screen_shake.offset_y))

        # Update display
        pygame.display.flip()
        
    def run(self):
        """
        Run the main game loop.
        
        This is the main entry point for the game.
        """
        running = True
        while running:
            # Handle events
            running = self.handle_events()
            
            # Update game state
            self.update()
            
            # Render
            self.render()
            
            # Limit the framerate to 60 FPS and calculate delta time
            self.dt = self.clock.tick(60) / 1000
