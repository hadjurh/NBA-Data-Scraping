# Basic packages
from time import sleep
import pandas as pd
import datetime
import os

# NBA api
from nba_api.stats.endpoints.playbyplayv2 import PlayByPlayV2
from nba_api.stats.endpoints.scoreboardv2 import ScoreboardV2

# This project's utils
from request_nba_data.get_calendar import load_season_dates
from request_nba_data.constants import SEASONS_DATES


def update_play_by_play_library(from_scratch=False, season_type='Regular Season'):
    if not os.path.exists('data/play_by_play_library'):
        os.makedirs('data/play_by_play_library')

    # Current Season
    end_date = datetime.date.today()
    seasons = ['2019-20']

    # Past
    # from_scratch = True
    # seasons = ['2018-19', '2017-18',
    #            '2016-17', '2015-16',
    #            '2014-15', '2013-14',
    #            '2012-13', '2011-12',
    #            '2010-11', '2009-10']

    for season in seasons:
        season_start, season_end = SEASONS_DATES[season]['start_date'], SEASONS_DATES[season]['end_date']

        play_by_play_df = pd.DataFrame()

        current_date = season_start

        if season_type == 'Regular Season':
            path_to_play_by_play = 'data/play_by_play_library/play_by_play_{}.csv'.format(
                '_' + season if season != '2019-20' else '')
            end_date = datetime.date(2020, 8, 15)
        elif season_type == 'Playoffs':
            path_to_play_by_play = 'data/play_by_play_library/play_by_play_playoffs{}.csv'.format(
                '_' + season if season != '2019-20' else '')
            current_date = datetime.date(2020, 8, 17)
        elif season_type == 'Play-in':
            path_to_play_by_play = 'data/play_by_play_library/play_by_play_play_in{}.csv'.format(
                '_' + season if season != '2019-20' else '')
            current_date = datetime.date(2020, 8, 15)
            end_date = datetime.date(2020, 8, 16)

        if not from_scratch:
            play_by_play_df = pd.read_csv(path_to_play_by_play)

            current_date = datetime.datetime.strptime(play_by_play_df.iloc[-1]['DATE'], '%Y-%m-%d').date() + \
                           datetime.timedelta(days=1)

        if current_date == end_date:
            print('Already up-to-date')
            return

        while current_date < end_date:
            print(current_date)
            daily_games = ScoreboardV2(game_date=str(current_date)).game_header.get_data_frame()
            sleep(0.4)

            for game_id, home_team_id, visitor_team_id \
                    in zip(daily_games['GAME_ID'], daily_games['HOME_TEAM_ID'], daily_games['VISITOR_TEAM_ID']):

                # Exclude All-Star
                if game_id[:3] not in ['002', '004', '005']:  # '005' : Play-in; '004' : Playoffs
                    print(f'Ignoring {game_id} on {current_date}')
                    continue

                play_by_play = PlayByPlayV2(game_id=game_id).play_by_play.get_data_frame()
                play_by_play = play_by_play.join(
                    pd.DataFrame([current_date] * len(play_by_play.index), columns=['DATE']))

                play_by_play_df = play_by_play_df.append(play_by_play)

                sleep(0.4)

            current_date += datetime.timedelta(days=1)

        play_by_play_df.to_csv(path_to_play_by_play, index=False)
