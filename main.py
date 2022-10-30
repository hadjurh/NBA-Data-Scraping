import datetime
from request_nba_data.get_league_info import get_league_info
from request_nba_data.get_calendar import get_calendar_nb_games, get_calendar_game_ids, generate_tonight_games
from request_nba_data.get_players_info import get_players
from request_nba_data.get_teams_info import get_teams

from request_nba_data.get_pbp_scoreboard import update_play_by_play_and_scoreboards


# Set constants, synchronized with data.nba.net
season_stage, year, display_year, current_date = get_league_info()  # To be monitored: nba.net
season_stage, year, display_year, current_date = 2, 2020, "2022-23", None

season_type = 'Regular Season'
if season_stage == 4:
    season_type = 'Playoffs'
elif season_stage == 1:
    season_type = 'Pre Season'
elif season_stage == 5:
    season_type = 'Play-in'

# Fetch data
print(f'\n---------- Start Update ----------\n'
      f'Season type: {season_type}; Year: {year}; Display year: {display_year}; NBA API Date {current_date}\n'
      f'Updating Constants at {datetime.datetime.now()}\n')

get_calendar_nb_games(year)
get_calendar_game_ids(year)
generate_tonight_games(year)

get_players(year)
get_teams(year)

print('\nUpdating Play by play and Scoreboards at ' + datetime.datetime.now().__str__())
# update_play_by_play_and_scoreboards(year, datetime.datetime.today().date() - datetime.timedelta(days=4))
update_play_by_play_and_scoreboards(year, None)

print('\nDone updating at ' + datetime.datetime.now().__str__())
