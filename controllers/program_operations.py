"""
Created by: Riley Preator
Created on: 11/05/2023
Last modified on: 6/13/2024
"""

from classes.BannerImage import BannerImage
from imports.imports import cv2
from imports.imports import json
from imports.imports import sys
from controllers.ranking_operations import create_new_rankings
from controllers.api_operations import *

def run_main_operation():
    startup()

    # Check for system arguments to get the stats of the subreddit and verify the Reddit API is working
    if len(sys.argv) >= 3:
        if sys.argv[1] == "stats":
            api_result = reddit_api_startup(sys.argv[2], True)
        elif sys.argv[1] == "flair_list":
            api_result = grab_flair_list()
        elif sys.argv[1] == "update_banner":
            if len(sys.argv) == 3:
                # Get the previous rankings from the previous_scores.json file
                previous_rankings = get_previous_rankings()

                # Create a new rankings banner
                create_new_rankings(previous_rankings)

                # Upload the banner
                update_banner(sys.argv[2])
            else:
                print("Error: Please provide a subreddit name parameter for the banner")
        elif sys.argv[1] == "user_activity":
            grab_user_activity(sys.argv[2])
        elif sys.argv[1] == "pin_comments":
            api_result = get_approved_users(sys.argv[2])
        else:
            api_result = reddit_api_startup(False)
    else:
        api_result = reddit_api_startup(False)

def startup():
    # create a BannerImage object and verify the file size
    banner_image = BannerImage()


def get_previous_rankings():
    # read the previous rankings so that improvements can be calculated
    previous_rankings = []
    with open("data/previous_scores.json") as file:
        previous_rankings = json.load(file)

    return previous_rankings


