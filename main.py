import datetime

from request_nba_data.get_league_info import get_league_info
from request_nba_data.get_calendar import get_calendar_nb_games, get_calendar_game_ids, generate_tonight_games
from request_nba_data.get_players_info import get_players
from request_nba_data.get_teams_info import get_teams

from request_nba_data.get_pbp_scoreboard import update_play_by_play_and_scoreboards
from request_nba_data.get_pbp_nba_api_library import update_play_by_play_library


# Set constants
season_stage, year, display_year, current_date = get_league_info()

season_type = 'Regular Season'
if season_stage == 4:
    season_type = 'Playoffs'
elif season_stage == 1:
    season_type = 'Pre Season'
elif season_stage == 5:
    season_type = 'Play-in'

# Fetch data
print('Start Update:\nUpdating Constants at ' + datetime.datetime.now().__str__())

get_calendar_nb_games(year)
get_calendar_game_ids(year)
generate_tonight_games(year)

get_players(year)
get_teams(year)

print('\nUpdating Play by play and Scoreboards at ' + datetime.datetime.now().__str__())
update_play_by_play_and_scoreboards(year)

print('\nUpdating Play by play (Python nba_api) ' + datetime.datetime.now().__str__())
<<<<<<< HEAD
update_play_by_play_library(year=year, from_scratch=False, season_type=season_type)
=======
update_play_by_play_library(from_scratch=False, season_type=season_type)
>>>>>>> 9d2c5031ceba255021bf22dd97ea138d25f0c839

print('\nDone updating at ' + datetime.datetime.now().__str__())
