"""
Asteroids game main module.

This is the main entry point for the game, handling:
- Game initialization
- Main game loop
- State management
- Event handling
"""

import pygame
import time

from constants import *
from game_state import GameState
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
import ui


def main():
    """
    Main game function that initializes the game and runs the main loop.
    """
    print("Starting asteroids!")
    print("Screen width:", SCREEN_WIDTH)
    print("Screen height:", SCREEN_HEIGHT)

    # Initialize pygame and create window
    pygame.init()
    title_font = pygame.font.Font(None, 64)  # Larger font for titles
    normal_font = pygame.font.Font(None, 36)  # Medium font for instructions
    small_font = pygame.font.Font(None, 24)  # Small font for scores/misc

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Asteroids")  # Set window title
    clock = pygame.time.Clock()

    # Create sprite groups for game objects
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # Set container groups for each game object type
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = updatable
    Shot.containers = (shots, updatable, drawable)

    # Initialize score
    score = 0

    # Create initial game objects
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    # Delta time for frame rate independence
    dt = 0

    # Start in menu state
    current_game_state = GameState.MENU

    # In the main function after initializing game objects
    difficulty_level = 1
    difficulty_timer = 0
    DIFFICULTY_INCREASE_INTERVAL = 30  # seconds

    prev_time = time.time()
    fps_update_timer = 0
    fps = 0

    # Main game loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and current_game_state == GameState.PLAYING:
                    current_game_state = GameState.PAUSED
                elif (
                    event.key == pygame.K_SPACE
                    and current_game_state == GameState.PAUSED
                ):
                    current_game_state = GameState.PLAYING
                elif (
                    event.key == pygame.K_SPACE and current_game_state == GameState.MENU
                ):
                    # Reset game when starting from menu
                    player, asteroid_field = reset_game(
                        updatable, drawable, asteroids, shots
                    )
                    score = 0
                    current_game_state = GameState.PLAYING
                elif (
                    event.key == pygame.K_RETURN
                    and current_game_state == GameState.GAME_OVER
                ):
                    current_game_state = GameState.MENU

        # Update based on game state
        if current_game_state == GameState.MENU:
            pass  # No updates needed in menu
        elif current_game_state == GameState.PLAYING:
            # Update all game objects
            updatable.update(dt)

            # Check for collisions
            for asteroid in asteroids:
                if player.check_collision(asteroid):
                    current_game_state = GameState.GAME_OVER

                for bullet in shots:
                    if bullet.check_collision(asteroid):
                        # Add score based on asteroid size
                        asteroid_score = ASTEROID_BASE_SCORE * (
                            asteroid.radius // ASTEROID_MIN_RADIUS
                        )
                        score += asteroid_score

                        # Display floating score text for feedback
                        ui.add_floating_score(asteroid.position, asteroid_score)

                        asteroid.split()
                        bullet.kill()
                        break

            # Update difficulty level
            difficulty_timer += dt
            if difficulty_timer >= DIFFICULTY_INCREASE_INTERVAL:
                difficulty_timer = 0
                difficulty_level += 1
                print(f"Difficulty increased to level {difficulty_level}")

            # Adjust asteroid field parameters based on difficulty
            asteroid_field.spawn_rate = max(
                0.2, ASTEROID_SPAWN_RATE - (difficulty_level * 0.05)
            )
            asteroid_field.speed_multiplier = 1.0 + (difficulty_level * 0.1)
        elif current_game_state == GameState.PAUSED:
            pass  # No updates when paused
        elif current_game_state == GameState.GAME_OVER:
            pass  # No updates when game over

        # Draw based on game state
        screen.fill((0, 0, 0))  # Clear screen with black

        # Current time for animations
        current_time = time.time()
        frame_time = current_time - prev_time
        prev_time = current_time

        fps_update_timer += dt
        if fps_update_timer >= 0.5:  # Update FPS display twice per second
            fps = 1.0 / max(frame_time, 0.001)  # Avoid division by zero
            fps_update_timer = 0

        if current_game_state == GameState.MENU:
            ui.draw_menu_screen(screen, title_font, normal_font, current_time)
        elif current_game_state == GameState.PLAYING:
            ui.draw_game_screen(drawable, screen, small_font, score, dt)
        elif current_game_state == GameState.PAUSED:
            ui.draw_paused_screen(drawable, screen, title_font, normal_font)
        elif current_game_state == GameState.GAME_OVER:
            ui.draw_game_over_screen(drawable, screen, title_font, normal_font, score)

        # Draw debug information if in debug mode
        if DEBUG_MODE:
            ui.draw_debug_info(screen, small_font, fps)

        # Update display
        pygame.display.flip()

        # limit the framerate to 60 FPS and calculate delta time
        dt = clock.tick(60) / 1000


def reset_game(updatable, drawable, asteroids, shots):
    """
    Reset game objects and state for a new game

    Args:
        updatable: Group containing updatable game objects
        drawable: Group containing drawable game objects
        asteroids: Group containing asteroid objects
        shots: Group containing player shots

    Returns:
        tuple: (player, asteroid_field) - newly created game objects
    """
    # Clear existing sprite groups
    updatable.empty()
    drawable.empty()
    asteroids.empty()
    shots.empty()

    # Recreate player and asteroid field
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    asteroid_field = AsteroidField()

    return player, asteroid_field


if __name__ == "__main__":
    main()
