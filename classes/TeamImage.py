"""
Created by: Riley Preator
Created on: 11/05/2023
Last modified on: 11/05/2023
"""

from imports.imports import Image

"""
A class representing an image for a team in a competition.

Attributes:
- width : int
    The width of the image.
- height : int
    The height of the image.
- teamAbrv : str
    The abbreviation of the team name.
- improvement : float
    The improvement percentage of the team.
- image_path : str
    The path to the image file.

Methods:
- get_image_dimensions(): Returns the dimensions of the image.
"""
class TeamImage:

    def __init__(self, teamAbrv, improvement, rank):
        self.width = 100
        self.height = 100

        self.teamAbrv = teamAbrv
        self.improvement = improvement
        self.rank = rank

        self.image_path = ""

        # Create the team image
        self.generate_image()

    def get_image_dimensions(self):
        with Image.open(self.image_path) as img:
            return img.size

    def generate_image():
        # TODO: Generate the image
        print("Generating image...")

