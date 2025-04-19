"""
UI-related functionality for the Asteroids game.

This module contains functions for rendering game UI elements including:
- Text rendering with different positioning options
- Animated text effects
- Game state-specific screens (menu, game, pause, game over)
"""

import math
import pygame
import time
from src.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, UI_COLORS, UI_POSITIONS, SHOW_FPS

# List to store floating score texts
floating_scores = []


def draw_text(
    surface: pygame.Surface,
    text: str,
    font: pygame.font.Font,
    color: tuple[int, int, int],
    position: tuple[int, int],
    centered: bool = False,
):
    """
    Render text on a surface

    Args:
        surface: The pygame surface to draw on
        text: The text string to render
        font: The pygame font object to use
        color: RGB tuple for text color
        position: (x, y) tuple for position
        centered: If True, text will be centered at position
    """
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()

    if centered:
        text_rect.center = position
    else:
        text_rect.topleft = position

    surface.blit(text_surface, text_rect)


def draw_pulsing_text(
    surface: pygame.Surface,
    text: str,
    font: pygame.font.Font,
    color: tuple[int, int, int],
    position: tuple[int, int],
    time_passed: float,
    speed: float = 2.0,
    min_scale: float = 0.9,
    max_scale: float = 1.1,
):
    """
    Render text with a pulsing animation

    Args:
        surface: The pygame surface to draw on
        text: The text string to render
        font: The pygame font object to use
        color: RGB tuple for text color
        position: (x, y) tuple for center position
        time_passed: Current game time in seconds for animation
        speed: Speed of pulsation
        min_scale: Minimum scale factor
        max_scale: Maximum scale factor
    """
    # Calculate scale factor based on sine wave
    scale = min_scale + (max_scale - min_scale) * (
        0.5 + 0.5 * math.sin(time_passed * speed)
    )

    # Render text
    text_surface = font.render(text, True, color)

    # Scale text (simple scaling - more advanced scaling would use pygame.transform.smoothscale)
    scaled_width = int(text_surface.get_width() * scale)
    scaled_height = int(text_surface.get_height() * scale)
    scaled_surface = pygame.transform.scale(text_surface, (scaled_width, scaled_height))

    # Position text
    text_rect = scaled_surface.get_rect(center=position)

    # Draw text
    surface.blit(scaled_surface, text_rect)


def draw_menu_screen(
    screen: pygame.Surface,
    title_font: pygame.font.Font,
    normal_font: pygame.font.Font,
    current_time: float,
):
    """
    Draw the menu screen with title and instructions

    Args:
        screen: The pygame surface to draw on
        title_font: Font for the title
        normal_font: Font for instructions
        current_time: Current time for animations
    """
    draw_text(
        screen,
        "ASTEROIDS",
        title_font,
        UI_COLORS["title"],
        UI_POSITIONS["title"],
        centered=True,
    )

    draw_text(
        screen,
        "Arrow keys to move, SPACE to shoot",
        normal_font,
        UI_COLORS["instructions"],
        UI_POSITIONS["instructions"],
        centered=True,
    )

    # Animated "Press SPACE to start" text
    draw_pulsing_text(
        screen,
        "Press SPACE to start",
        normal_font,
        UI_COLORS["instructions"],
        UI_POSITIONS["start_prompt"],
        current_time,
    )


def draw_game_screen(
    drawable: pygame.sprite.Group,
    screen: pygame.Surface,
    small_font: pygame.font.Font = None,
    score: int = 0,
    dt: float = 0,
):
    """
    Draw the main gameplay screen

    Args:
        drawable: Group of drawable game objects
        screen: The pygame surface to draw on
        small_font: Font for score display (optional)
        score: Current score to display (optional)
        dt: Delta time for updating animations (optional)
    """
    # Draw all game objects
    for obj in drawable:
        obj.draw(screen)

    # Draw score if font is provided
    if small_font:
        draw_text(
            screen,
            f"SCORE: {score}",
            small_font,
            UI_COLORS["score"],
            UI_POSITIONS["score"],
            centered=False,
        )
        
        # Update and draw floating score texts
        update_floating_scores(dt)
        draw_floating_scores(screen, small_font)


def draw_game_over_screen(
    drawable: pygame.sprite.Group,
    screen: pygame.Surface,
    title_font: pygame.font.Font,
    normal_font: pygame.font.Font,
    score: int = 0,
):
    """
    Draw the game over screen with final score

    Args:
        drawable: Group of drawable game objects (shown in background)
        screen: The pygame surface to draw on
        title_font: Font for game over text
        normal_font: Font for instructions
        score: Final score to display (optional)
    """
    # Draw the final game state in background
    for obj in drawable:
        obj.draw(screen)

    # Semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # Semi-transparent black
    screen.blit(overlay, (0, 0))

    # Game Over text
    draw_text(
        screen,
        "GAME OVER",
        title_font,
        UI_COLORS["game_over"],
        UI_POSITIONS["game_over"],
        centered=True,
    )

    # Show score if available
    if score > 0:
        draw_text(
            screen,
            f"FINAL SCORE: {score}",
            normal_font,
            UI_COLORS["score"],
            UI_POSITIONS["final_score"],
            centered=True,
        )

    draw_text(
        screen,
        "Press ENTER to restart",
        normal_font,
        UI_COLORS["instructions"],
        UI_POSITIONS["restart_prompt"],
        centered=True,
    )


def draw_paused_screen(
    drawable: pygame.sprite.Group,
    screen: pygame.Surface,
    title_font: pygame.font.Font,
    normal_font: pygame.font.Font,
):
    """
    Draw the pause screen overlay

    Args:
        drawable: Group of drawable game objects (shown in background)
        screen: The pygame surface to draw on
        title_font: Font for 'PAUSED' text
        normal_font: Font for instructions
    """
    # Draw the current game state in background
    for obj in drawable:
        obj.draw(screen)

    # Semi-transparent overlay
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # Semi-transparent black
    screen.blit(overlay, (0, 0))

    # Paused title
    draw_text(
        screen,
        "PAUSED",
        title_font,
        UI_COLORS["instructions"],
        UI_POSITIONS["paused_title"],
        centered=True,
    )

    # Paused instructions
    draw_text(
        screen,
        "Press SPACE to continue",
        normal_font,
        UI_COLORS["instructions"],
        UI_POSITIONS["paused_instructions"],
        centered=True,
    )


def add_floating_score(position, value):
    """
    Add a floating score text at the specified position

    Args:
        position: (x, y) tuple for the position where the score was earned
        value: Score value to display
    """
    floating_scores.append({
        "position": pygame.Vector2(position),
        "value": value,
        "color": (255, 255, 100),  # Yellow color for visibility
        "created_time": time.time(),
        "lifetime": 1.5,  # How long the text stays on screen
        "velocity": pygame.Vector2(0, -50)  # Move upward
    })


def update_floating_scores(dt):
    """
    Update floating score positions and lifetimes

    Args:
        dt: Delta time in seconds since the last frame
    """
    current_time = time.time()
    # Update each floating score and remove expired ones
    for i in range(len(floating_scores) - 1, -1, -1):
        score = floating_scores[i]
        # Update position
        score["position"] += score["velocity"] * dt
        # Check if expired
        if current_time - score["created_time"] > score["lifetime"]:
            floating_scores.pop(i)


def draw_floating_scores(screen, font):
    """
    Draw all active floating score texts

    Args:
        screen: The pygame surface to draw on
        font: Font to use for score text
    """
    for score in floating_scores:
        # Calculate alpha based on remaining lifetime
        elapsed = time.time() - score["created_time"]
        alpha = max(0, min(255, int(255 * (1 - elapsed / score["lifetime"]))))
        
        # Create color with alpha
        color = list(score["color"])
        
        # Draw the score text
        text = f"+{score['value']}"
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=score["position"])
        screen.blit(text_surface, text_rect)


def draw_debug_info(screen: pygame.Surface, small_font: pygame.font.Font, fps: float):
    """
    Draw debug information like FPS counter

    Args:
        screen: The pygame surface to draw on
        small_font: Font for debug info text
        fps: Current frames per second
    """
    if SHOW_FPS:
        fps_text = f"FPS: {int(fps)}"
        draw_text(
            screen,
            fps_text,
            small_font,
            (150, 150, 150),
            (SCREEN_WIDTH - 100, 20),
            centered=False,
        )
