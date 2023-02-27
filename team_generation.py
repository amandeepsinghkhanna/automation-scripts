"""
    @Script-Name:team_generation.py
    @Script-Author: Amandeep Singh Khanna
    @Python-Version: Python 3.9+
    @Script-Description: A Python module to generate groups of teams for projects.
"""

# Importing required modules:
import random
import pandas as pd


class GenerateTeams(object):
    """
        Class: GenerateTeams
        Description: Genrates a random group of roll numbers for teams for a
        project.

        Instance-variables:
        1. team_size -> int -> No. of members per team, the value fo team_size
        must be > 1 <= n_stds.
        2. n_studs -> int -> No. of students in the class/course, the value of
        n_studs must be >= team_size.
        3. roll_prefix -> str -> Prefix for the roll number value, example
        '16BDA'.
        4. whitelist -> list -> A list of roll numbers in str that have dropped
        out of the course, these roll numbers will be excluded from the team
        generation process. These must include the prefixed str as well, exmple
        - ['16BDA001', '16BDA002']
        5. seed_val -> int -> A seed value for the random number generator.
        This is essential to make the results reproduceable. The default value
        is 42.
    """

    def __init__(self, team_size, n_stds, roll_prefix, whitelist, seed_val=42):
        assert (team_size > 1) or (
            team_size <= n_stds
        ), "team_size must be > 1 or <= n_stds"
        assert n_stds >= team_size, "n_stds must be >= team_size"

        self.team_size = team_size
        self.n_stds = n_stds
        self.roll_prefix = roll_prefix
        self.whitelist = whitelist
        random.seed(seed_val)

    def gen_roll_num_lst(self):
        """
            Method: gen_roll_num_lst
            Description: Generates a list of roll numbers for each student in
            the class.

            Returns:
            1. roll_num_lst -> lst -> List of roll numbers for each of the
            students in class.
        """
        roll_num_lst = []
        for n in range(1, self.n_stds + 1):
            if n < 10:
                roll = f"{self.roll_prefix}0{n}"
            else:
                roll = f"{self.roll_prefix}{n}"
            if roll not in self.whitelist:
                roll_num_lst.append(roll)
        random.shuffle(roll_num_lst)
        return roll_num_lst

    @staticmethod
    def gen_team(n, std_lst):
        """
            Method: gen_team
            Description: Generates a team by selecting n random members from the
            std_lst.

            Parameters:
            1. n -> int -> No. of members to be randomly picked as members of a
            team.
            2. std_list -> list -> A list of str values representing roll
            numbers for each of the students to be grouped into teams.

            Returns:
            1. team -> list -> A list of str values representing roll numbers
            selected as a part of a team.
        """
        std_lst = set(std_lst)
        team = set()
        for tm_idx in range(n):
            roll = random.choice(list(std_lst))
            team.add(roll)
            std_lst.remove(roll)
        return team

    def gen_n_teams(self):
        """
            Method: gen_n_teams
            Description: Genrates a random group of roll numbers for teams for a
            project.

            Returns: 
            1. teams -> pandas.core.DataFrame -> A DataFrame with each row 
            representing a team & each column representing a member of the team. 
        """
        roll_num_lst = set(self.gen_roll_num_lst())
        teams = []
        while len(roll_num_lst) > self.team_size:
            team = self.gen_team(n=self.team_size, std_lst=roll_num_lst)
            teams.append(team)
            roll_num_lst = roll_num_lst - set(team)
        if len(roll_num_lst) > 0:
            teams.append(roll_num_lst)
        teams = pd.DataFrame(teams)
        teams.index = [f"TEAM_{idx}" for idx in teams.index]
        teams.columns = [f"MEMBER_{idx}" for idx in range(1, self.team_size + 1)]
        return teams