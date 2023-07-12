"""
    CS 5001
    Fall 2022
    Marian Padron
    Final Project (additional files)

    Module that holds functions used to build the non-interactive parts of the
    slider puzzle game board.
"""

from turtle import *


UPPER_LEFT_X = -370  # upper left x-coordinate of screen used within functions
UPPER_LEFT_Y = 310  # upper left y-coordinate of screen used within functions


def screen_setup() -> object:
    """
        Function: screen_setup, sets up turtle screen object with given height
        and width
        Parameters: None
        Returns: screen object from turtle Screen class
    """
    screen = Screen()
    screen.title("CS 5001 Sliding Puzzle Game")
    screen.setup(790, 675)
    screen.screensize(790, 675)
    return screen


def draw_square(go_to_location: tuple, length: int, width: int,
                color: str) -> object:
    """
        Function: draw_square, draws a square on turtle screen object at given
        location, with given length, width, and color
        Parameters: go_to_location (tuple, x and y coordinates of upper left of
        square), length (int), width (int), color (str, color of desired square
        outline)
        Returns: created turtle object
    """
    turtle = Turtle()
    turtle.hideturtle()
    turtle.speed(0)
    turtle.penup()
    turtle.color(color)
    turtle.goto(go_to_location)
    turtle.width(3)
    turtle.pendown()

    # Draw area
    for turn in range(4):
        turtle.forward(width)
        turtle.right(90)
        turtle.forward(length)
        turtle.right(90)
    turtle.penup()
    return turtle


def create_puzzle_board() -> object:
    """
        Function: create_puzzle_board, draws area for puzzle using turtle
        Parameters: None
        Returns: turtle object created
    """

    turtle = draw_square((UPPER_LEFT_X, UPPER_LEFT_Y), 450, 450, "black")
    return turtle


def create_leader_board() -> object:
    """
        Function: create_leader_board, creates the area where the names of
        players in the leaderboard will be displayed, using turtle
        Parameters: None
        Returns: turtle object created
    """

    turtle = draw_square((-UPPER_LEFT_X - 280, UPPER_LEFT_Y), 450, 275, "navy")

    # Write leaderboard title
    turtle.goto(100, 270)
    style = ("Arial", 15, "bold")
    turtle.write("LEADERS:", font=style, align="left")
    return turtle


def create_status_area() -> object:
    """
        Function: create_status_area, creates area where the player moves
         and buttons for game will be placed
        Parameters: None
        Returns: turtle object created
    """

    turtle = draw_square((UPPER_LEFT_X, - 150), 160, 734, "black")
    return turtle


def create_button(screen: object, file_name: str, coordinates: tuple) \
        -> object:
    """
        Function: create_button, creates a turtle image or 'button' with
        specified file image at specified coordinates
        Parameters: screen (turtle screen object), file_name (str, name of file
        containing 'button' image), coordinates (tuple, x and y coordinates of
        desired image position)
        Returns: turtle object created
    """
    screen.addshape(file_name)  # adds file image to screen object for use
    turtle = Turtle()
    turtle.speed(0)
    turtle.penup()
    turtle.goto(coordinates)
    turtle.shape(file_name)
    return turtle


def update_moves_text(player_moves: int or str) -> object:
    """
        Function: update_moves_text, creates and updates text that will display
        player moves to user, using turtle
        Parameters: player_moves (int or str, contains total player moves)
        Returns: turtle object created
    """
    turtle = Turtle()
    turtle.hideturtle()
    turtle.penup()
    turtle.goto(-340, -238)
    style = ("Arial", 18, "bold")
    turtle.color("navy")

    # Write on screen
    turtle.write(f"PLAYER MOVES: {player_moves}", font=style, align="left")
    return turtle


def add_players_to_leaderboard(leaders_list: list) -> object:
    """
        Function: add_players_to_leaderboard, gets a list containing nested
        lists that hold player name at index 0 and player score at index 1,
        uses turtle to write those players names and scores to the leaderboard
        Parameters: leaders_list (list, containing nested lists)
        Returns: created turtle object
    """
    turtle = Turtle()
    turtle.penup()
    turtle.hideturtle()
    turtle.goto(- UPPER_LEFT_X - 270, UPPER_LEFT_Y - 100)
    style = ("Arial", 14, "bold")
    turtle.color("skyblue")

    # Write up to 13 names on leaderboard
    try:
        for i in range(13):
            turtle.write(f"{leaders_list[i][1]}:  {leaders_list[i][0]}\n",
                         font=style, align="left")

            # Move down for next name
            turtle.goto(turtle.xcor(), turtle.ycor() - 28)

    # Return turtle object if have reached leaderboard index limit
    except IndexError:
        return turtle
    return turtle
