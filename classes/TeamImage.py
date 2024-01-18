"""
Created by: Riley Preator
Created on: 11/05/2023
Last modified on: 1/18/2024
"""

from imports.imports import Image
from imports.imports import cv2
from imports.imports import np
import os

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
- team_placement_image : Image
    The final image for the team.

Methods:
- get_image_dimensions(): Returns the dimensions of the image.
"""
class TeamImage:

    def __init__(self, teamAbrv, improvement, rank):
        self.width = 200
        self.height = 120

        self.teamAbrv = teamAbrv
        self.improvement = improvement
        self.rank = rank


        self.image_path = "images/team_images/" + self.teamAbrv + "_logo.png"

        if not os.path.exists(self.image_path):
            self.image_path = "images/team_images/default_team_logo.png"

        # Create the team image
        self.team_placement_image = self.generate_image()

    def get_image_dimensions(self):
        if os.path.exists(self.image_path):
            with Image.open(self.image_path) as img:
                return img.size

    def generate_image(self):
        # TODO: Generate the image
        image_size = self.get_image_dimensions()

        if image_size == -1:
            raise FileNotFoundError(f"Image not found: {self.image_path}")

        # Create brand new image with grey background
        color = (215, 224, 218)
        blank_image = np.full((self.height, self.width, 3), color, np.uint8)

        alpha_image = self.add_alpha_channel(blank_image)

        rounded_image =  self.add_rounded_border(alpha_image, 3, (255, 255, 255))

        cv2.imshow("Rounded Image", rounded_image)
        cv2.waitKey()
        return Image.open(self.image_path)


    # add a border around the initial image to make it so that the border is added with the color provided
    def add_rounded_border(self, image_array, border_size, border_color):
        if image_array.shape[2] != 4:
            raise ValueError("Image array must have four channels (RGBA).")

        # Separate the alpha channel
        alpha_channel = image_array[:, :, 3]
        color_channels = image_array[:, :, :3]

        h, w = alpha_channel.shape

        # Create a mask with rounded corners
        mask = np.zeros((h, w), dtype=np.uint8)
        radius = border_size
        cv2.circle(mask, (radius, radius), radius, (255), -1)
        cv2.circle(mask, (w - radius, radius), radius, (255), -1)
        cv2.circle(mask, (radius, h - radius), radius, (255), -1)
        cv2.circle(mask, (w - radius, h - radius), radius, (255), -1)
        mask = cv2.rectangle(mask, (radius, 0), (w - radius, h), (255), -1)
        mask = cv2.rectangle(mask, (0, radius), (w, h - radius), (255), -1)

        # Apply the mask to the alpha channel
        rounded_alpha = cv2.bitwise_and(alpha_channel, alpha_channel, mask=mask)

        # Create a background for the border
        bordered_image = np.full((h + 2 * border_size, w + 2 * border_size, 4), (*border_color, 255), dtype=np.uint8)

        # Place the original image on the background
        bordered_image[border_size:border_size + h, border_size:border_size + w, :3] = color_channels
        bordered_image[border_size:border_size + h, border_size:border_size + w, 3] = rounded_alpha

        return bordered_image

    # add an alpha channel to the image
    def add_alpha_channel(self, image):
        b_channel, g_channel, r_channel = cv2.split(image)
        alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 50 #creating a dummy alpha channel image.
        alpha_image = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))

        return alpha_image
