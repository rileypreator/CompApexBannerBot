from imports.imports import Image

class TeamImage:
    def __init__(self, teamName):
        self.width = 100
        self.height = 100
        self.image_name

    def get_image_dimensions(self):
        with Image.open(self.image_path) as img:
            return img.size

