"""
    CS 5001
    Fall 2022
    Marian Padron
    Final Project (additional files)

    Module that holds PuzzleFileReader class and LeaderboardFileReader class.
"""

import random


class PuzzleFileReader:
    """
        Class that creates a puzzle instance containing all attributes
        outlined in the puzzle.puz file passed.
    """


    def __init__(self, puzzle_file: str):
        """
            Constructs all necessary attributes for puzzle instance.
            Parameters: puzzle_file (str, name of puzzle '.puz' file)
            Return: None
        """

        self.puzzle_file = puzzle_file

        # Create attributes for later assignment of values
        self.malformed_puzzle = False  # a check for incorrect metadata in file
        self.characteristics = {}
        self.unscrambled_images = []
        self.scrambled_images = []

        # Call method to obtain puzzle characteristics and unscrambled images
        self.read_puzzle_file()

        # Create more specific attributes for easy access from object/instance
        self.tile_number = int(self.characteristics["number"])
        self.thumbnail = self.characteristics["thumbnail"]
        self.image_size = int(self.characteristics["size"])

        # Assign value to malformed_puzzle check and add scrambled images
        self.check_if_malformed()
        self.scramble_images()


    def read_puzzle_file(self):
        """
            Method: read_puzzle_file; reads '.puz' file, adds keys/values to
            characteristics dictionary and adds file names to
            unscrambled_images list
            Parameters: self (class instance)
            Return: None
        """
        with open(self.puzzle_file, "r") as file:
            file = file.readlines()
            file_list = [line.replace("\n", "") for line in file]

            for line in file_list[:4]:  # first 4 lines hold puzzle info
                key, value = line.split(":")
                self.characteristics[key] = value.replace(" ", "")

            for line in file_list[4:]:  # hold ordered images file names
                value = line.split(":")[1].replace(" ", "")
                self.unscrambled_images.append(value)


    def scramble_images(self):
        """
            Method: scramble_images, takes list of unscrambled images and
            shuffles them randomly to create new list of scrambled images
            Parameters: self (class instance)
            Return: None
        """
        self.scrambled_images = [file_name for file_name in
                                 self.unscrambled_images]
        random.shuffle(self.scrambled_images)


    def check_if_malformed(self):
        """
            Method: check_if_malformed, checks if puzzle size is something
            other than a 4(2x2), 9(3x3) or 16(4x4) puzzle, assigns
            True to malformed_puzzle attribute if metadata incorrect
            Parameters: self (class instance)
            Returns: None, prints to terminal if malformed file was passed
        """
        possible_sizes = [4, 9, 16]
        if self.tile_number not in possible_sizes:
            self.malformed_puzzle = True
            print("WARNING from PuzzleFileReader: user has passed a malformed "
                  "file")


    def __str__(self):
        """
            Method: __str__
            Parameters: self (class instance)
            Returns: str representation of object
        """
        return (f"PuzzleFileReader object.\n"
                f"puzzle file: {self.puzzle_file}\n"
                f"puzzle characteristics: {self.characteristics}\n")


class LeaderboardFileReader:
    """
        Class that reads leaderboard file and assigns attributes about the file
        to the class instance.
    """


    def __init__(self, leaderboard_file: str):
        """
            Constructs attributes for leaderboard file instance.
            Parameters: leader_board_file (str, name of file containing
            leaderboard players and scores)
            Returns: None
        """
        self.leaderboard_file = leaderboard_file

        # Placeholder attributes for later assignment
        self.file_list = None
        self.found_file = True

        # Call method to read passed file
        self.read_leaderboard_file()


    def read_leaderboard_file(self):
        """
            Method: read_leaderboard_file, reads leaderboard file and assigns
            to file_list attribute a list containing nested lists with
            player names and player moves, if file is not found it assigns
            False to found_file attribute
            Parameters: self (class instance)
            Returns: None, prints to terminal if file passed was not found
        """
        try:
            with open(self.leaderboard_file, "r") as file:
                self.file_list = [[line.split()[0], line.split()[1]] for line
                                  in file.readlines()]

        except FileNotFoundError:
            self.found_file = False
            print(f"Error from LeaderboardFileReader: There is no \
{self.leaderboard_file} file found.")


    def __str__(self):
        """
            Method: __str__
            Parameters: self (class instance)
            Returns: str representation of object
        """
        return (f"LeaderboardFileReader object\n"
                f"found file: {self.found_file} "
                f"\nleaderboard file: {self.leaderboard_file}\n"
                f"file list: {self.file_list}\n")
