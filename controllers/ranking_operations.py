"""
Created by: Riley Preator
Created on: 12/14/2023
Last modified on: 12/14/2023
"""
from classes.TeamPlace import TeamPlace
from classes.Team import Team
from classes.TeamImage import TeamImage
from imports.imports import json

def create_new_rankings(previous_rankings):
    # create a new rankings list. For testing purposes. The teams will be generated just through the sample json right now
    # However, once the API to receive the new rankings is created, this will be changed to use that API
    new_rankings = []
    with open("data/current_scores.json") as file:
        new_rankings = json.load(file)

    team_objects = create_team_objects(previous_rankings, new_rankings)

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