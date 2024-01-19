"""
Created by: Riley Preator
Created on: 11/05/2023
Last modified on: 11/05/2023
"""

from imports.imports import cv2, Image

class BannerImage:
    def __init__(self):
        self.image_path = "images/actual_banner_background.png"
        self.width, self.height = self.get_image_dimensions()
        self.image = cv2.imread(self.image_path)

    def get_image_dimensions(self):
        with Image.open(self.image_path) as img:
            return img.size



