import os
from dotenv import load_dotenv

from app.teamsretrieval import get_teams
from app.standings_retrieval import get_standings
from database.teams_update import update_teams
from database.standings_update import 


load_dotenv()


def main():
    """Main entry point when script is directly executed."""

    current_season = 2023  # This should be made more dynamic later

    # retrieved_teams = get_teams(current_season)

    # if retrieved_teams is None:
    #     print("Failed to get teams, aborting database update.")
    #     return

    # update_teams(retrieved_teams)

    retrieved_standings = get_standings(current_season)



if __name__ == "__main__":
    main()
