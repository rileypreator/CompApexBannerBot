"""
Created by: Riley Preator
Created on: 11/05/2023
Last modified on: 1/18/2024
"""

from imports.imports import Image, ImageFont, ImageDraw
from imports.imports import cv2
from imports.imports import np
from imports.imports import os


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
- team_logo_image : Numpy Array
    The team's logo image.
- team_placement_image : Numpy Array
    The final image for the team.

Methods:
- get_image_dimensions(): Returns the dimensions of the image.
"""
class TeamImage:

    def __init__(self, teamAbrv, improvement, rank):
        self.width = 200
        self.height = 110

        self.team_Abrv = teamAbrv
        self.improvement = improvement
        self.rank = rank
        self.has_team_logo = True

        # Find the team logo path or default to the normal Apex logo
        self.team_logo_image_path = "images/team_images/" + self.team_Abrv + "_logo.png"
        if not os.path.exists(self.team_logo_image_path):
            self.team_logo_image_path = "images/team_images/default_team_logo.png"
            self.has_team_logo = False

        self.team_logo_image = cv2.imread(self.team_logo_image_path, cv2.IMREAD_UNCHANGED)

        # Create the team image
        self.team_placement_image = self.generate_image()

    def get_image_dimensions(self):
        if os.path.exists(self.team_logo_image_path):
            with Image.open(self.team_logo_image_path) as img:
                return img.size

    def generate_image(self):
        image_size = self.get_image_dimensions()

        if image_size == -1:
            raise FileNotFoundError(f"Image not found: {self.team_logo_image_path}")

        # Create brand new image with grey background
        color = [89, 88, 87, 180]
        blank_image = np.full((self.height, self.width, 4), color, np.uint8)

        # Add border to overall image
        rounded_image =  self.add_rounded_border(blank_image, 2, (150, 149, 149))

        # Add placement to image
        placement_image = self.add_placement_text(rounded_image)

        # Add team logo to image
        team_image = self.add_team_image(placement_image)

        # Add team name to image if the team doesn't have a logo
        if not self.has_team_logo:
            team_image = self.add_team_name(team_image)

        # Resize the image if the team is in the top 3
        if (self.rank > 3):
            team_image = self.resize_image(team_image, 0.89)

        cv2.imwrite("images/team_placement_images/" + self.team_Abrv + "_placement.png", team_image)
        return team_image


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

        alpha_channel = alpha_channel.astype(np.uint8)
        alpha_image = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))

        return alpha_image

    # add team logo to the image
    def add_team_image(self, image):

        overlay_image = self.team_logo_image
        background = image

        x_offset = 90
        y_offset = 6
        # Calculate the overlay image region dimensions
        y1, y2 = y_offset, y_offset + overlay_image.shape[0]
        x1, x2 = x_offset, x_offset + overlay_image.shape[1]

        # Check if the dimensions of the overlay exceed the background dimensions
        if y2 > background.shape[0] or x2 > background.shape[1]:
            raise ValueError("Overlay image exceeds background dimensions.")

        # Extract the alpha channel from the overlay and create an alpha mask
        alpha_s = overlay_image[:, :, 3] / 255.0
        alpha_l = 1.0 - alpha_s

        # Loop over the color channels
        for c in range(0, 3):
            background[y1:y2, x1:x2, c] = (alpha_s * overlay_image[:, :, c] + alpha_l * background[y1:y2, x1:x2, c])

        return background

    # add placement text to image
    def add_placement_text(self, image):
        # Use pillow to import a custom font for the text

        if image.shape[2] < 4:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        pil_image = Image.fromarray(image)

        txt_image = Image.new("RGBA", pil_image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_image)
        font = ImageFont.truetype("data/Apex_Regular.otf", size=60)

        text = str(self.rank)
        text_width = font.getmask(text).getbbox()[2]

        draw.text((50 - int((text_width / 2)), 25), str(self.rank), font=font, fill=(255, 255, 255, 255))

        combined = Image.alpha_composite(pil_image, txt_image)
        final_image = np.array(combined)

        if final_image.shape[2] == 4:
            final_image = cv2.cvtColor(final_image, cv2.COLOR_RGBA2BGRA)

        return final_image

    def resize_image(self, image, percent):
        new_width = int(image.shape[1] * percent)
        new_height = int(image.shape[0] * percent)
        new_size = (new_width, new_height)

        # Resize the image
        resized_image = cv2.resize(image, new_size)

        return resized_image

    def add_team_name(self, image):
        # Use pillow to import a custom font for the text

        if image.shape[2] < 4:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
        pil_image = Image.fromarray(image)

        txt_image = Image.new("RGBA", pil_image.size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(txt_image)
        font = ImageFont.truetype("data/Apex_Regular.otf", size=30)

        text = self.team_Abrv
        text_width = font.getmask(text).getbbox()[2]

        draw.text((140 - int((text_width / 2)), 55), text, font=font, fill=(255, 255, 255, 255))

        combined = Image.alpha_composite(pil_image, txt_image)
        final_image = np.array(combined)

        if final_image.shape[2] == 4:
            final_image = cv2.cvtColor(final_image, cv2.COLOR_RGBA2BGRA)

        return final_image