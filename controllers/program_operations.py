"""
Created by: Riley Preator
Created on: 11/05/2023
Last modified on: 12/14/2023
"""

from classes.BannerImage import BannerImage
from imports.imports import cv2
from imports.imports import json


def run_main_operation():
    startup()

    previous_rankings = get_previous_rankings()

    create_new_rankings(previous_rankings)


def startup():
    # create a BannerImage object and verify the file size
    banner_image = BannerImage()
    print("Banner sizes:", banner_image.width, " x ", banner_image.height)


def get_previous_rankings():
    # read the previous rankings so that improvements can be calculated
    previous_rankings = []
    with open("data/previous_scores.json") as file:
        previous_rankings = json.load(file)
    
    return previous_rankings

def create_new_rankings(previous_rankings):
    # create a new rankings list. For testing purposes. The teams will be generated just through the sample json right now
    # However, once the API to receive the new rankings is created, this will be changed to use that API

    
    new_rankings = []
