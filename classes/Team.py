"""
Created by: Riley Preator
Created on: 11/05/2023
Last modified on: 11/05/2023
"""

from TeamPlace import TeamPlace
from TeamImage import TeamImage

"""
A class representing a team in a competition.

Attributes:
team_place : TeamPlace
    The place the team finished in the competition.
rank : int
    The teams given rank for the ranking
"""
class Team:
    def __init__(self, team_place: TeamPlace, rank):
        self.team_place = team_place
        self.rank = rank

        # Generate the team image
        self.team_image = TeamImage(team_place.team_abrv, team_place.improvement, rank)
