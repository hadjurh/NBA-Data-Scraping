import datetime
from request_nba_data.get_league_info import get_league_info
from request_nba_data.get_pbp_scoreboard import update_play_by_play_and_scoreboards


# Set constants and get calendar
print(f'\n---------- Start Update ----------\n')
season_stage, year, display_year, current_date, schedule = get_league_info()

season_type = 'Regular Season'
if season_stage == 4:
    season_type = 'Playoffs'
elif season_stage == 1:
    season_type = 'Pre Season'
elif season_stage == 5:
    season_type = 'Play-in'

# Fetch data
print(f'Season type: {season_type}; Year: {year}; Display year: {display_year}; NBA API Date {current_date}\n'
      f'Updating Constants at {datetime.datetime.now()}\n')

print('\nUpdating Play by play and Scoreboards at ' + datetime.datetime.now().__str__())
update_play_by_play_and_scoreboards(year, datetime.datetime.today().date() - datetime.timedelta(days=8))
# update_play_by_play_and_scoreboards(year, None)

print('\nDone updating at ' + datetime.datetime.now().__str__())
