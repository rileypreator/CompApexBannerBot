"""
Created by: Riley Preator
Created on: 12/14/2023
Last modified on: 1/18/2024
"""
from classes.TeamPlace import TeamPlace
from classes.Team import Team
from classes.TeamImage import TeamImage
from imports.imports import json
from imports.imports import cv2
from imports.imports import Image, ImageFont, ImageDraw
from imports.imports import np

def create_new_rankings(previous_rankings):
    # create a new rankings list. For testing purposes. The teams will be generated just through the sample json right now
    # However, once the API to receive the new rankings is created, this will be changed to use that API
    new_rankings = []
    with open("data/current_scores.json") as file:
        new_rankings = json.load(file)

    team_objects = create_team_objects(previous_rankings, new_rankings)

    subreddit_banner = apply_team_objects(team_objects)
    apply_subreddit_logo(subreddit_banner)

def create_team_objects(previous_rankings, new_rankings):
    # create a list of team objects from the previous rankings
    team_objects = []

    team_iterator = 0
    new_rankings_list = new_rankings["teams"]
    while team_iterator < 25:
        # calculate the improvement between last weeks ranking, and this weeks ranking and store it as the improvement variable
        improvement = calculate_improvement(previous_rankings, new_rankings_list[team_iterator]["placement"], new_rankings_list[team_iterator]["team_name"])

        # Make a team place object that can be used to track the team's placement and then create a Team object with that team place object
        team_place = TeamPlace(new_rankings_list[team_iterator]["team_name"], new_rankings_list[team_iterator]["team_name"], new_rankings_list[team_iterator]["placement"], new_rankings_list[team_iterator]["score"], improvement)
        team_objects.append(Team(team_place))

        # iterate through the loop with the team_iterator object
        team_iterator += 1

    return team_objects

def calculate_improvement(previous_rankings, new_rankings_placement, team_name):
    previous_rankings_list = previous_rankings["teams"]

    for i in previous_rankings_list:
        if i["team_name"] == team_name:
            improvement = i["placement"] - new_rankings_placement
            return improvement

    # if previous ranking isn't found as they are not on the previous ranking, return new string

    return "NEW"

def apply_team_objects(team_objects):

    background_photo = cv2.imread("images/actual_banner_background.png", 1)
    background_photo = cv2.cvtColor(background_photo, cv2.COLOR_RGB2RGBA)

    team_locations = [
        (1939, 10),
        (1820, 28),
        (2079, 28)
    ]

    team_iterator = 0
    while team_iterator < 25:

        # Set the first three images with static locations
        if (team_iterator < 3):
            x_offset = team_locations[team_iterator][0]
            y_offset = team_locations[team_iterator][1]

        # Set the next 11 images with a formula
        elif (team_iterator >= 3 and team_iterator < 14):
            x_offset = 1433 + (team_iterator - 3) * 105
            y_offset = 90

        # Set the last 11 images with a formula
        else:
            x_offset = 1433 + (team_iterator - 14) * 105
            y_offset = 140

        team_photo = team_objects[team_iterator].team_image.team_placement_image

        #  Make sure that the background image doesn't have an alpha channel
        if background_photo.shape[2] == 4:
            background_photo = cv2.cvtColor(background_photo, cv2.COLOR_BGRA2BGR)
        if team_photo.shape[2] != 4:
            raise Exception("The overlay image must have an alpha channel")

        # Split the overlay into RGB and Alpha channels
        overlay_rgb = team_photo[..., :3]
        alpha_mask = team_photo[..., 3]

        y1, y2 = y_offset, y_offset + overlay_rgb.shape[0]
        x1, x2 = x_offset, x_offset + overlay_rgb.shape[1]

        # Adjust alpha_mask and background for broadcasting
        alpha_mask = alpha_mask / 255.0
        alpha_mask = np.expand_dims(alpha_mask, axis=2)
        background_region = background_photo[y1:y2, x1:x2]

        # Blend the overlay with the background
        blended_region = (alpha_mask * overlay_rgb) + (1 - alpha_mask) * background_region
        background_photo[y1:y2, x1:x2] = blended_region

        # Save or display the result
        team_iterator += 1

    background_photo = cv2.cvtColor(background_photo, cv2.COLOR_RGB2RGBA)
    return background_photo


def apply_subreddit_logo(banner):
    # Use pillow to import a custom font for the text
    pil_image = Image.fromarray(banner)

    txt_image = Image.new("RGBA", pil_image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(txt_image)
    font = ImageFont.truetype("data/Apex_Regular.otf", size=40)
    position1 = (1527, 25)
    position2 = (2238, 25)
    draw.text(position1, "Apex Legends" , font=font, fill=(255, 255, 255, 255))
    draw.text(position2, "World Rankings" , font=font, fill=(255, 255, 255, 255))

    combined = Image.alpha_composite(pil_image, txt_image)
    final_image = np.array(combined)

    cv2.imwrite("images/final_background.png", final_image)
    return final_image