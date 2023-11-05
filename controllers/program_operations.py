"""
Created by: Riley Preator
Created on: 11/05/2023
Last modified on: 11/05/2023
"""

from classes.BannerImage import BannerImage

def startup():
    # create a BannerImage object
    banner_image = BannerImage()

    # do any other startup tasks here

    print("Banner sizes:", banner_image.width, " x ", banner_image.height)
