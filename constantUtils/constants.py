###list of constant values for passing as query arguments

from collections import namedtuple

League = namedtuple("League", ["name", "id"])

LEAGUES = [
    League(name="Premier League", id=39),
    League(name="Bundesliga", id=78),
    League(name="Serie A", id=135),
    League(name="Ligue 1", id=61),
    League(name="La Liga", id=140),
]
