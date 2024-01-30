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
from controllers.api_operations import api_startup, update_banner, grab_flair_list, grab_user_activity

def run_main_operation():
    startup()

    # Check for system arguments to get the stats of the subreddit and verify the Reddit API is working
    if len(sys.argv) >= 2:
        if sys.argv[1] == "stats":
            api_result = api_startup(True)
        elif sys.argv[1] == "flair_list":
            api_result = grab_flair_list()
        elif sys.argv[1] == "update_banner":
            # Get the previous rankings from the previous_scores.json file
            previous_rankings = get_previous_rankings()

            # Create a new rankings banner
            create_new_rankings(previous_rankings)

            # Upload the banner
            update_banner()
        elif sys.argv[1] == "user_activity":
            grab_user_activity(sys.argv[2])

        else:
            api_result = api_startup(False)
    else:
        api_result = api_startup(False)

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


