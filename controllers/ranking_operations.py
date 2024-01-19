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

def create_new_rankings(previous_rankings):
    # create a new rankings list. For testing purposes. The teams will be generated just through the sample json right now
    # However, once the API to receive the new rankings is created, this will be changed to use that API
    new_rankings = []
    with open("data/current_scores.json") as file:
        new_rankings = json.load(file)

    team_objects = create_team_objects(previous_rankings, new_rankings)

    apply_team_objects(team_objects)

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

    background_photo = cv2.imread("images/scaled_background.png", cv2.IMREAD_UNCHANGED)
    background_photo = cv2.cvtColor(background_photo, cv2.COLOR_BGRA2RGBA)
    team_locations = [
        (1400, 10),
        (1150, 10),
        (1650, 10)
    ]

    team_iterator = 0
    while team_iterator < 25:

        # Set the first three images with static locations
        if (team_iterator < 3):
            x_offset = team_locations[team_iterator][0]
            y_offset = team_locations[team_iterator][1]

        # Set the next 11 images with a formula
        elif (team_iterator >= 3 and team_iterator < 14):
            x_offset = 231 + (team_iterator - 3) * 236
            y_offset = 140

        # Set the last 11 images with a formula
        else:
            x_offset = 231 + (team_iterator - 14) * 236
            y_offset = 260

        team_photo = team_objects[team_iterator].team_image.team_placement_image

        background_photo[y_offset:y_offset+team_photo.shape[0], x_offset:x_offset+team_photo.shape[1]] = team_photo
        print(team_iterator)
        team_iterator += 1

    cv2.imwrite("images/final_background.png", background_photo)