"""
    CS 5001
    Fall 2022
    Marian Padron
    Final Project (additional files)

    Module containing main SliderPuzzleGame class for running game.
"""

from turtle import *
from src.file_reading_classes import PuzzleFileReader, LeaderboardFileReader
from datetime import datetime
from src import gameboard
import math
import time
import os


class SliderPuzzleGame(Turtle):
    """
        Class that creates a slider puzzle game instance and all its attributes
        and methods to run game.
    """


    def __init__(self, puzzle_file: str):
        """
            Constructs attributes for running the slider puzzle game.
            Parameters: None
            Returns: None
        """

        self.puzzle_file = puzzle_file

        # Create puzzle object with contents from puzzle file
        self.puzzle = PuzzleFileReader(self.puzzle_file)

        # Initialize main screen that class methods will use to operate game
        self.screen = gameboard.screen_setup()

        # Create main game attributes
        self.turtles = []  # holds all turtles used to create puzzle tiles
        self.placed_images_list = []  # lists image file names as placed on board
        self.turtle_locations = []  # lists tuple coordinates of placed turtles
        self.player_moves = 0  # used to sum any time player swaps a tile

        # Placeholder attributes that will have values once game methods called
        self.player_name = None  # name of user/player
        self.max_moves = None  # max moves inputted by user
        self.moves_turtle = None  # turtle object that updates score on screen
        self.thumbnail_turtle = None  # turtle object used for puzzle thumbnail
        self.leaders_list = None  # list with names and scores from leaderboard

        # Get instance to pass swap_tiles method everytime screen is clicked
        onscreenclick(self.swap_tiles)


    def show_splash_screen(self):
        """
            Method: show_splash_screen, shows splash screen to user when called
            Parameters: self (class instance)
            Returns: None
        """
        # Create turtle object with splash image using gameboard
        splash_turtle = gameboard.create_button(self.screen,
                                                "Resources/splash_screen.gif",
                                                (0, 0))
        time.sleep(2)
        splash_turtle.hideturtle()  # removes splash screen after 2 secs


    def create_thumbnail(self) -> object:
        """
            Method: create_thumbnail, creates and shows puzzle image thumbnail
            when called
            Parameters: self (class instance)
            Returns: turtle object containing thumbnail so that image may
            be altered if puzzle is changed
        """
        return gameboard.create_button(self.screen, self.puzzle.thumbnail,
                                       (320, 265))


    def create_moves_turtle(self) -> object:
        """
            Method: create_moves_turtle, creates and shows total sum of player
            moves in status bar
            Parameters: self (class instance)
            Returns: turtle object so that text may be altered as game
            progresses
        """
        return gameboard.update_moves_text(self.player_moves)


    def listen_for_clicks(self):
        """
            Method: listen_for_clicks, when called will make instance's screen
            attribute appear to user unless closed out
            Parameters: self (class instance)
            Return: None
        """
        mainloop()


    def get_player_name(self) -> str:
        """
            Method: get_player_name, receives player name input from user,
            loops until it receives a valid input
            Parameters: self (class instance)
            Returns: player_name (str)
        """
        player_name = self.screen.textinput("CS 5001 Puzzle Slide",
                                            "Enter your name (no spaces "
                                            "please!): ")

        while True:
            # If user clicks on cancel return None, which will exit main game
            if player_name is None:
                print("Player has exited game.")
                return None

            # Loop until receive valid input from user
            elif player_name == "" or " " in player_name:
                player_name = self.screen.textinput("CS 5001 Puzzle Slide",
                                                    "Enter your name (no "
                                                    "spaces please!): ")
            else:
                return player_name  # return name once valid input


    def get_max_moves(self) -> int:
        """
            Method: get_max_moves, receives maximum tries input from user,
            keeps looping until receives valid input (number 5 - 200)
            Parameters: self (class instance)
            Returns: max_moves (int)
        """
        max_moves = self.screen.numinput("CS 5001 Puzzle Slide",
                                         "Enter the number of moves ("
                                         "chances) you want (5 - 200):",
                                         50)

        while True:
            # Return None if user clicks on 'cancel', exits game
            if max_moves is None:
                print("Player has exited game.")
                return None

            # Keep looping if user has input an invalid number
            elif not 5 <= int(max_moves) <= 200:
                max_moves = self.screen.numinput("CS 5001 Puzzle Slide",
                                                 "The number must be "
                                                 "between 5 and 200.\nEnter "
                                                 "the number of moves ("
                                                 "chances) you want:", 50)
            else:
                return int(max_moves)  # return number once valid input


    def create_board(self):
        """
            Method: create_board, uses gameboard module to create turtle
            objects that will fill board for game
            Parameters: self (class instance)
            Returns: None
        """
        gameboard.create_puzzle_board()  # creates area for puzzle
        gameboard.create_status_area()  # creates status area
        gameboard.create_leader_board()  # creates leaderboard area
        gameboard.create_button(self.screen, "Resources/quitbutton.gif",
                                (270, -230))  # quit button
        gameboard.create_button(self.screen, "Resources/resetbutton.gif",
                                (167, -230))  # reset button
        gameboard.create_button(self.screen, "Resources/loadbutton.gif",
                                (62, -230))  # load button


    def update_player_moves(self):
        """
            Method: update_player_moves, clears turtle object displaying
            current player moves and updates with new moves everytime a tile is
            swapped
            Parameters: self (class instance)
            Returns: None
        """
        self.moves_turtle.clear()
        style = ("Arial", 18, "bold")
        self.moves_turtle.write(f"PLAYER MOVES: {self.player_moves}",
                                font=style, align="left")


    def draw_tile_outline(self, turtle: object, x_coordinate: int,
                          y_coordinate: int):
        """
            Method: draw_tile, uses same turtle object used to create a tile
            to draw square outline around location of puzzle image
            Parameters: turtle (turtle object that will create a tile),
            x_coordinate (int, x_coordinate of center of tile),
            y_coordinate (int, y_coordinate of center of tile)
            Returns: None
        """
        image_size = self.puzzle.image_size  # size of puzzle tile
        turtle.hideturtle()
        turtle.penup()

        # Make turtle draw a square with x and y coordinates at middle,
        # this will outline the tiles that make up the puzzle
        turtle.goto(x_coordinate - image_size / 2,
                    y_coordinate + image_size / 2)
        turtle.pendown()
        turtle.width(2)
        turtle.color("black")
        for turn in range(4):
            turtle.forward(image_size)
            turtle.right(90)
        turtle.penup()


    def create_tile(self, image_file: str, x_coordinate: int,
                    y_coordinate: int) -> int and int:
        """
            Method: create_tile_turtle, creates a turtle object at given
            coordinates that shows the puzzle tile image
            Parameters: image_file (str, name of file with puzzle image),
            x_coordinate (int, x_coordinate of center of tile),
            y_coordinate (int, y_coordinate of center of tile)
            Returns: x_coordinate (int) and y_coordinate (int) of turtle
        """
        # Create turtle and use draw_tile_outline method to draw square
        turtle = Turtle()
        turtle.speed(0)
        self.draw_tile_outline(turtle, x_coordinate, y_coordinate)

        # Make turtle go to center (x, y coordinates) and show puzzle image
        turtle.goto(x_coordinate, y_coordinate)
        self.screen.addshape(image_file)  # adds image to screen for turtle use
        turtle.shape(image_file)
        turtle.showturtle()

        # Append turtles to turtles list attribute as they are created
        self.turtles.append(turtle)

        # Append created turtle's center coordinates to turtle_locations list
        turtle_position = (math.trunc(turtle.xcor()), math.trunc(
            turtle.ycor()))  # math.trunc used to avoid rounding errors
        self.turtle_locations.append(turtle_position)

        # Return coordinates of turtle to calculate position of next turtle
        return math.trunc(turtle.xcor()), math.trunc(turtle.ycor())


    def place_tiles(self, puzzle_images: list):
        """
            Method: place_tiles, creates and places puzzle tiles on gameboard
            based on a list of scrambled or unscrambled image file names
            Parameters: puzzle_images (list, contains file names of images to
            be passed onto turtle to create tiles)
            Returns: None
        """
        image_size = self.puzzle.image_size  # size of puzzle tile

        # Keep record of tile images currently being placed on board
        for file_name in puzzle_images:
            self.placed_images_list.append(file_name)

        # Make copy of images list for popping values as board gets created
        to_be_placed = [image for image in puzzle_images]

        # Get upper left tile's center coordinates to start puzzle
        puzzle_upper_x = gameboard.UPPER_LEFT_X + image_size / 2 + 10
        puzzle_upper_y = gameboard.UPPER_LEFT_Y - image_size / 2 - 10

        # Create variables that will hold the previous tile center coordinates
        previous_x, previous_y = puzzle_upper_x, puzzle_upper_y

        # Create board dimension (2x2, 3x3, 4x4)
        board_dimension = int(self.puzzle.tile_number ** (1 / 2))

        # Use board dimension to iterate and create tiles at given coordinates
        for i in range(board_dimension):

            # Go through the to_be_placed list and create tiles left to right
            for image in to_be_placed[:board_dimension]:

                # Pass image to create_tile, method returns coordinates of
                # previous tile to make calculation of next tile position
                previous_x, previous_y = self.create_tile(image, previous_x,
                                                          previous_y)
                to_be_placed.pop(0)  # pop first placed tile from list
                previous_x += image_size  # update location of next tile

            # Once done iterating through the first line of tiles loop back
            # and create next row
            previous_x = puzzle_upper_x
            previous_y -= image_size


    def find_blank_index(self) -> int:
        """
            Method: update_blank_index, uses placed_images_list attribute to
            find the index location of the blank tile, which will be used for
            swapping
            Parameters: self (class instance)
            Returns: index (int, the index value of the blank tile)
        """
        # Iterate through placed_images_list until it finds blank tile file
        for index, file_name in enumerate(self.placed_images_list):
            if "blank" in file_name:
                return index


    def clear_board(self):
        """
            Method: clear_board, deletes all placed puzzle tiles and clears all
            list attributes that contain placed puzzle images, created turtles
            for tiles, and coordinates of placed tiles
            Parameters: self (class instance)
            Returns: None
        """
        for turtle in self.turtles:
            turtle.clear()
            turtle.hideturtle()
        self.turtles.clear()
        self.placed_images_list.clear()
        self.turtle_locations.clear()


    def log_error(self, error_message:str, location: str):
        """
            Method: log_error, writes to '5001_puzzle.err' everytime game has
            encountered a file or leaderboard error
            Parameters: self (class instance), error_message,
            Returns: None
        """
        # Get date and time of error
        today = datetime.now()
        date = today.date()
        time = today.strftime('%H:%M:%S')

        # Open error file and append record
        with open("src/5001_puzzle.err", "a") as outfile:
            outfile.write(
                f"DATE:{date}  TIME:{time}  {error_message}  "
                f"LOCATION: {location}\n")


    def read_leaderboard(self) -> list:
        """
            Method: read_leaderboard, reads leaderboard.txt file and writes
            players and scores to screen, returns the list of found players
            and scores to be updated if current user wins the game, if file
            not found pops up error to user
            Parameters: self (class instance)
            Returns: leaders_list (list, containing the names and scores of
            players on the leaderboard.txt file)
        """
        # Check if found leaderboard file
        leader_board = LeaderboardFileReader("src/leaderboard.txt")
        if leader_board.found_file:

            # Add players and scores to screen leaderboard
            leaders_list = leader_board.file_list
            gameboard.add_players_to_leaderboard(leaders_list)

            # If didn't find file log error to '5001_puzzle.error'
        else:
            self.log_error("ERROR: Could not find/open leader_board.txt",
                           "ReadLeaderBoard.read_leaderboard_file()")

            # Create empty list that will be passed to create new leaderboard
            leaders_list = []
            error_turtle = gameboard.create_button(self.screen,
                                                   "Resources/leaderboard_error.gif",
                                                   (0, 0))  # error pop up
            time.sleep(2)
            error_turtle.hideturtle()
        return leaders_list


    def reset_button(self):
        """
            Method: reset_button, clears all placed tiles and corresponding
            lists, and re-places puzzle tiles with sorted images
            Parameters: self (class instance)
            Returns: None
        """
        self.clear_board()
        self.place_tiles(self.puzzle.unscrambled_images)


    def quit_button(self):
        """
            Method: quit_button, used for quitting the game, displays quit
            message to user and then game credits before user clicks off the
            game
            Parameters: self (class instance)
            Returns: None
        """
        # Show quit message, sleep 2 seconds and then show credits
        quit_turtle = gameboard.create_button(self.screen,
                                              'Resources/quitmsg.gif', (0, 0))
        time.sleep(2)
        quit_turtle.hideturtle()
        gameboard.create_button(self.screen, 'Resources/credits.gif', (0, 0))

        # Quit game once user clicks on screen
        self.screen.exitonclick()


    def load_button_prompt(self) -> str:
        """
            Method: load_button_prompt, reads all puzzle files located in
            directory and returns a prompt text with included file names to use
            once user clicks on 'load' button
            Parameters: self (class instance)
            Returns: str (str containing prompt text for user input)
        """
        prompt_text = [
            "Enter the name of the file you wish to load. Files in directory "
            "inlcude:",
            "\n"]

        # Read file names in directory
        file_names = os.listdir("src/puz_files")

        # Create list of only puzzle files (end in '.puz')
        puzzle_files = [file for file in file_names if file[-4:] == ".puz"]

        # Append up to 10 files names to prompt
        if len(puzzle_files) <= 10:
            for file_name in puzzle_files:
                prompt_text.append(file_name)
                prompt_text.append("\n")
        else:

            # If more than 10 file names found then display 10 and show pop up
            for i in range(10):
                prompt_text.append(puzzle_files[i])
                prompt_text.append("\n")
            pop_up_turtle = gameboard.create_button(self.screen,
                                                    "Resources/file_warning.gif", (0, 0))

            # Log more than 10 files error to '5001_puzzle.err' file
            self.log_error("WARNING: There are more than 10 puzzle files "
                           "available in file directory.",
                           "SliderPuzzleGame.read_file_directory()")
            time.sleep(2)
            pop_up_turtle.hideturtle()

        return "".join(prompt_text)


    def load_button(self):
        """
            Method: load_button, get new puzzle file name from user and loads
            new puzzle game with said file, if file does not exist or if it is
            malformed if will pop up a message to user and terminal
            Parameters: self (class instance)
            Returns: None
        """
        # Get prompt text with available puzzle files in directory
        prompt_text = self.load_button_prompt()
        print(prompt_text)

        # Get user input
        new_file = str(
            self.screen.textinput("CS 5001 Slider Puzzle", prompt_text))

        print(new_file)
        # Add root to file
        new_file = "src/puz_files/" + new_file

        # Stop method if user clicks on cancel, resume game
        if new_file == "None":
            return

        # Check is provided file exists
        elif os.path.exists(new_file):

            # Check if provided file is malformed and log error if yes
            puzzle_check = PuzzleFileReader(new_file)
            if puzzle_check.malformed_puzzle:
                self.log_error(
                    f"ERROR: The provided file, {new_file}, contains a "
                    f"malformed puzzle", "SliderPuzzleGame.load_button()")

                # Show error pop up
                turtle = gameboard.create_button(self.screen,
                                                 "Resources/file_error.gif",
                                                 (0, 0))
                time.sleep(2)
                turtle.hideturtle()

                # Raise error to terminal
                raise Exception("The file passed contains a malformed puzzle.")

            # Run new puzzle if not malformed
            else:
                self.puzzle_file = new_file

                # Clear previous variables and turtles from screen
                self.clear_board()
                self.player_moves = 0
                self.update_player_moves()  # display player moves back at 0

                # Load new game
                self.puzzle = PuzzleFileReader(self.puzzle_file)

                # Update thumbnail image
                self.screen.addshape(self.puzzle.thumbnail)
                self.thumbnail_turtle.shape(self.puzzle.thumbnail)

                # Place new puzzle tiles
                self.place_tiles(self.puzzle.scrambled_images)
        else:

            # Log error if provided file does not exist and create error pop up
            self.log_error(f"ERROR: Could not find file {new_file}",
                           "SliderPuzzleGame.load_button()")
            error_turtle = gameboard.create_button(self.screen,
                                                   "Resources/file_error.gif",
                                                   (0, 0))
            time.sleep(2)
            error_turtle.hideturtle()

            # Raise FileNotFoundError to terminal
            raise FileNotFoundError


    def add_player_score(self) -> list:
        """
            Method: add_player_score, adds player name and score to leaderboard
             players list if they've won the game, if leaderboard file was not
             found, it passes new player and score to write to new leaderboard
             Parameters: self (class instance)
             Returns: previous_leaders (list, contains list of previous leaders
             including new player) OR player_input (list, containing new player
             name and score to write to new leaderboard)
        """
        # Make list containing player name and winning score
        player_input = [self.player_name, self.player_moves]

        # Check if leaders list file was found and is not empty
        if self.leaders_list:

            # Make a list containing name and score of previous leaders
            previous_leaders = [leader for leader in self.leaders_list]

            # Insert new player's name and score at correct location in list
            # Inserts score first in line if score better than first leader's
            if player_input[1] <= int(previous_leaders[0][1]):
                previous_leaders.insert(0, player_input[:])
                player_input.pop(0)

            # Inserts player score last if worse than last leader's
            elif player_input[1] > int(previous_leaders[-1][1]):
                previous_leaders.append(player_input[:])
                player_input.pop(0)
            else:

                # If neither top nor bottom score, loop through scores and
                # insert at correct location
                for i in range(len(previous_leaders) - 1):
                    if int(previous_leaders[i][1]) <= player_input[1] <= \
                            int(previous_leaders[i + 1][1]):
                        previous_leaders.insert(i + 1, player_input[:])
                        player_input.clear()

            return previous_leaders
        else:
            # Return new player score to write to leaderboard
            return [player_input]


    def write_leaderboard_file(self, new_leaders: list):
        """
            Method: write_leaderboard_file, takes list of players to write to
            leaderboard.txt and write their name and score to file
            Parameters: self (class instance), new_leaders (list, containing
            nested lists of player names and scores)
            Returns: None
        """
        with open("src/leaderboard.txt", "w") as outfile:
            for leader in new_leaders:
                outfile.write(f"{leader[0]} {leader[1]}\n")


    def check_puzzle_status(self):
        """
            Method: check_puzzle_status, checks current status of the board
            after each swap, pops up winning message if player won and passes
            new player's name and score to write to leaderboard file it then
            end the game, if player has hit max moves it pops up loosing
            message and ends game
            Parameters: self (class instance)
            Return: None
        """
        # Check if player is still within the max moves and if puzzle
        # images are in correct order
        if self.player_moves <= self.max_moves and self.placed_images_list == self.puzzle.unscrambled_images:
            print("Player has won.")  # print to terminal game status
            win_turtle = gameboard.create_button(self.screen,
                                                 "Resources/winner.gif",
                                                 (0, 0))  # show win pop up
            time.sleep(2)
            win_turtle.hideturtle()
            gameboard.create_button(self.screen, 'Resources/credits.gif',
                                    (0, 0))  # show credits
            self.screen.exitonclick()  # close game on screen click

            # Add player name and moves to leaders list to write to leaderboard
            new_leaders = self.add_player_score()  # sorts list with new player
            self.write_leaderboard_file(new_leaders)  # writes to file

        # If player has hit max moves
        elif self.player_moves == self.max_moves:
            print("Player has lost.")  # print to terminal game status
            loose_turtle = gameboard.create_button(self.screen,
                                                   "Resources/Lose.gif",
                                                   (0, 0))  # looses pop up
            time.sleep(2)
            loose_turtle.hideturtle()
            gameboard.create_button(self.screen, 'Resources/credits.gif',
                                    (0, 0))  # show credits
            self.screen.exitonclick()  # close game on screen click


    def check_click(self, click_coordinates: tuple):
        """
            Method: check_click, checks user's click coordinates against the
            coordinates of the blank tile, if user clicked on a tile adjacent
            to the blank tile check_click will return coordinates of clicked
            tile, if user clicks on any button the check_click will call
            the corresponding method
            Parameters: self (class instance), click_coordinates (tuple,
            contains x-coordinate and y-coordinate of click)
            Returns: tuple (if within scope of blank tile,
            returns x and y coordinate of tile surrounding the click)
        """
        image_size = self.puzzle.image_size  # size of tile image

        # Check if user has clicked on load, reset, or quit buttons
        if 131 <= click_coordinates[0] <= 201 and -263 <= click_coordinates[
            1] <= -192:
            self.reset_button()
        elif 24 <= click_coordinates[0] <= 98 and -265 <= click_coordinates[
            1] <= -193:
            self.load_button()
        elif 231 <= click_coordinates[0] <= 307 and -253 <= click_coordinates[
            1] <= -206:
            self.quit_button()
        else:

            # Get index and tile/turtle coordinates of blank tile
            blank_index = self.find_blank_index()
            blank_coordinates = self.turtle_locations[blank_index]

            # Calculate center coordinates of tile above, below, left,
            # and right of blank tile (adjacent tiles)
            top_tile = (
                blank_coordinates[0], blank_coordinates[1] + image_size)
            bottom_tile = (
                blank_coordinates[0], blank_coordinates[1] - image_size)
            left_tile = (
                blank_coordinates[0] - image_size, blank_coordinates[1])
            right_tile = (
                blank_coordinates[0] + image_size, blank_coordinates[1])

            # Check if click is within x range of blank (top and bottom tile)
            if blank_coordinates[0] - image_size / 2 <= click_coordinates[0] \
                    <= blank_coordinates[0] + image_size / 2:
                # Check if within y range of top tile
                if top_tile[1] - image_size / 2 <= click_coordinates[1] <= \
                        top_tile[1] + image_size / 2:
                    return top_tile  # user clicked on top tile
                else:
                    return bottom_tile  # user clicked on the bottom tile

            # Check if within y range of blank (left and right tile)
            elif blank_coordinates[1] - image_size / 2 <= click_coordinates[
                1] <= blank_coordinates[1] + image_size / 2:
                # Check if within x range of left tile
                if left_tile[0] - image_size / 2 <= click_coordinates[0] <= \
                        left_tile[0] + image_size / 2:
                    return left_tile  # user clicked on left tile
                else:
                    return right_tile  # user clicked on right tile

            # Return None if user didn't click within the adjacent tiles
            else:
                return None


    def swap_tiles(self, x_coordinate, y_coordinate):
        """
            Method: swap_tiles, checks user's click location and if clicked
            tile is adjacent, it swaps tiles with blank, updates corresponding
            turtles, turtle_locations, and placed_images_list
            Parameters: x_coordinate (int, x-coordinate of click),
            y_coordinate (int, y-coordinate of click)
            Return: None
        """
        # Check click, receives coordinates if user clicked on adjacent tile
        tile_coordinates = self.check_click(
            (int(x_coordinate), int(y_coordinate)))  # passes tuple to method

        if tile_coordinates:

            # Get index and coordinates of blank tile
            blank_index = self.find_blank_index()
            blank_coordinates = self.turtle_locations[blank_index]

            # Check if there is a turtle/puzzle image at tile coordinates,
            # used to make sure nothing happens if user clicks outside puzzle
            if tile_coordinates in self.turtle_locations:

                # Find index and turtle for that tile
                tile_index = int(self.turtle_locations.index(tile_coordinates))

                # Swap tile and blank on board
                self.turtles[tile_index].goto(blank_coordinates)
                self.turtles[blank_index].goto(tile_coordinates)

                # Swap tile and blank coordinates in lists
                self.turtle_locations[tile_index] = blank_coordinates
                self.turtle_locations[blank_index] = tile_coordinates

                # Swap corresponding tile turtles in turtles list
                self.turtles[tile_index], self.turtles[blank_index] = \
                    self.turtles[blank_index], self.turtles[tile_index]

                # Swap locations of turtle coordinates in list
                self.turtle_locations[tile_index], self.turtle_locations[
                    blank_index] = self.turtle_locations[blank_index], \
                                   self.turtle_locations[tile_index]

                # Swap locations of tile image file and blank image file
                self.placed_images_list[tile_index], self.placed_images_list[
                    blank_index] = self.placed_images_list[blank_index], \
                                   self.placed_images_list[tile_index]

                # Update player moves if managed to swap
                self.player_moves += 1
                self.update_player_moves()

                # Check if player has finished puzzle
                self.check_puzzle_status()


    def __str__(self):
        """
            Method: __str__
            Parameters: self (class instance)
            Returns: str representation of object
        """
        return f"--- SliderPuzzleGame object. ---\n"\
               f"puzzle object: {self.puzzle.__str__()}" \
               f"passed tile images: {self.placed_images_list}\n" \
               f"tile turtles: {self.turtles}\n" \
               f"turtle/tile locations: {self.turtle_locations}\n" \
               f"player name: {self.player_name}\n" \
               f"current moves: {self.player_moves}\n" \
               f"leaderboard list: {self.leaders_list.__str__()}\n"
