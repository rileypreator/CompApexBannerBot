"""
Created by: Riley Preator
Created on: 10/29/2023
Last modified on: 10/29/2023
"""


"""
A class representing a team's placement in a competition.

Attributes:
-----------
team_name : str
    The name of the team.
team_abrev : str
    The abbreviation of the team's name.
rank : int
    The current rank of the team based on the most recent polling of the power rankings.
team_points : int
    The number of points earned by the team this week by the power rankings.
"""
class TeamPlace:

    def __init__(self, team_name, team_abrev, rank, team_points):
        self.team_name = team_name
        self.team_abrev = team_abrev
        self.rank = rank
        self.team_points = team_points
