import cv2

class ImageOperations:

    """
        Creates a box on the given image using cv2.rectangle().

        Args:
            image (numpy.ndarray): The image to draw the box on.
            pt1 (tuple): The (x, y) coordinates of the top-left corner of the box.
            pt2 (tuple): The (x, y) coordinates of the bottom-right corner of the box.
            color (tuple): The (B, G, R) color of the box.
            thickness (int): The thickness of the box lines.

        Returns:
            numpy.ndarray: The image with the box drawn on it.
    """
    @staticmethod
    def create_box(image, pt1, pt2, color, thickness):

        cv2.rectangle(image, pt1, pt2, color, thickness)
        return image


    """
        Adds an image to another image with coordinates using OpenCV.

        Args:
            background_image (numpy.ndarray): The image to add the other image to.
            foreground_image (numpy.ndarray): The image to be added to the background image.
            x (int): The x-coordinate of the top-left corner of the foreground image.
            y (int): The y-coordinate of the top-left corner of the foreground image.

        Returns:
            numpy.ndarray: The image with the foreground image added to it.
    """
    @staticmethod
    def add_image(background_image, foreground_image, x, y):

        height, width, _ = foreground_image.shape
        roi = background_image[y:y+height, x:x+width]
        result = cv2.addWeighted(roi, 0, foreground_image, 1, 0)
        background_image[y:y+height, x:x+width] = result
        return background_image

