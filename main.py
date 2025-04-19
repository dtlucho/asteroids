"""
Asteroids game main module.

This is the main entry point for the game, which creates and runs
the Game instance.
"""

from src.managers.game_manager import Game


def main():
    """
    Main entry point for the Asteroids game.
    
    Creates a Game instance and runs the main game loop.
    """
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
