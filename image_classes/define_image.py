from imports.imports import Image

class BannerImage:
    def __init__(self):
        self.image_path = "images/default_banner.png"
        self.width, self.height = self.get_image_dimensions()

    def get_image_dimensions(self):
        with Image.open(self.image_path) as img:
            return img.size
