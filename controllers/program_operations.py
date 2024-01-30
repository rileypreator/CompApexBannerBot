"""
Created by: Riley Preator
Created on: 11/05/2023
Last modified on: 1/29/2024
"""

from classes.BannerImage import BannerImage
from imports.imports import cv2
from imports.imports import json
from imports.imports import sys
from controllers.ranking_operations import create_new_rankings
from controllers.api_operations import api_startup

def run_main_operation():
    startup()

    if len(sys.argv) >= 2:
        if sys.argv[1] == "stats":
            api_result = api_startup(True)
        else:
            api_result = api_startup(False)
    else:
        api_result = api_startup(False)
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


