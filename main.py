import os
from dotenv import load_dotenv

from app.teamsretrieval import get_teams
from database.teams_update import bulk_insert_teams


load_dotenv()


def main():
    """Main entry point when script is directly executed."""

    current_season = 2023  # This should be made more dynamic later

    retrieved_teams = get_teams(current_season)

    if retrieved_teams is None:
        print("Failed to get teams, aborting database update.")
        return

    bulk_insert_teams(retrieved_teams)


if __name__ == "__main__":
    main()
