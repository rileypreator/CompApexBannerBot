"""
Created by: Riley Preator
Created on: 11/05/2023
Last modified on: 6/13/2024
"""

import cv2

# This stackoverflow post was used to help create this class: https://stackoverflow.com/questions/44650888/resize-an-image-without-distortion-opencv
def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)

    # return the resized image
    return resized

def team_image_resize(image):
    (height, width) = image.shape[:2]
    ratio = 0
    
    if (height == 100 and width == 100):
        resized_image = cv2.resize(image, (99,99), interpolation=cv2.INTER_AREA)
    elif (height >= width):
        ratio = width / height
        dimensions = (int(100 * ratio), 100)
        resized_image = cv2.resize(image, dimensions, interpolation=cv2.INTER_AREA)
    else:
        ratio = height / width
        dimensions = (100, int(100 * ratio))
        resized_image = cv2.resize(image, dimensions, interpolation=cv2.INTER_AREA)
        
    return resized_image

# Resize any image with a defined width as passed through the parameters
def resize_image_width(image, desired_width):
    height, width = image.shape[:2]
    
    ratio = desired_width / width
    new_height = int(height * ratio)

    resized_image = cv2.resize(image, (desired_width, new_height))
    return resized_image
    