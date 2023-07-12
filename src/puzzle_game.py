"""
    CS 5001
    Fall 2022
    Marian Padron
    Final Project

    Module that organizes SliderPuzzleGame class and runs it to have a
    functional game.
"""

from slider_puzzle_game_class import SliderPuzzleGame


def main():

    # Pass file containing the first puzzle that will be created and initialize
    # a slider puzzle game object
    game = SliderPuzzleGame("src/puz_files/mario.puz")

    # Begin game by showing splash screen
    game.show_splash_screen()

    # Get player name and max moves, game will only commence once valid inputs
    game.player_name = game.get_player_name()

    if game.player_name:  # asks for max moves input once it has a valid name
        game.max_moves = game.get_max_moves()

    # Set up board
    if game.max_moves:

        # Create board for game
        game.create_board()
        game.thumbnail_turtle = game.create_thumbnail()

        # Read leaderboard file
        game.leaders_list = game.read_leaderboard()

        # Create turtle that will show total player moves to user
        game.moves_turtle = game.create_moves_turtle()

        # Begin game by placing scrambled tiles of the passed puzzle file
        game.place_tiles(game.puzzle.scrambled_images)

        # Listen for user clicks that will control game object methods
        game.listen_for_clicks()

if __name__ == "__main__":
    main()
