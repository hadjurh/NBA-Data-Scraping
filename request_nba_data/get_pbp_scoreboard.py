import os
import sys
import re
import json
from glob import glob
from datetime import datetime, timedelta
import requests
from numpy import nan
import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from request_nba_data.constants import HEADERS, BOXSCORE_URL, PLAY_BY_PLAY_URL
from request_nba_data.get_calendar import load_season_dates


def request_data(game, url, folder, headers=None):
    if not os.path.isfile(f'{folder}/{game.game_id}.json'):
        request = requests.get(url, headers=headers, timeout=3)
        data_dict = request.json()

        if not os.path.exists(f'{folder}'):
            os.makedirs(f'{folder}')

        with open(f'{folder}/{game.game_id}.json', 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, ensure_ascii=False, indent=4)

        return data_dict

    return None


class Game(object):
    """
    Describe an NBA game and its basic information
    """

    def __init__(self, game_id, date, year):
        self.game_id = game_id
        self.date = date
        self.year = year
        self._get_uptodate_game_info()

    def __str__(self):
        return f'Id: {self.game_id}, Date: {self.date}, UrlCode: {self.game_url_code}, ' \
               f'StatusNum: {self.status_num}, Period: {self.game_info["period"]["current"]}, ' \
               f'Clock: {self.game_info["clock"]}'

    def _get_uptodate_game_info(self):
        request = requests.get(BOXSCORE_URL.format(game_id=self.game_id), headers=HEADERS, timeout=3).json()

        self.game_info = request['game']
        self.game_url_code = self.game_info['gameCode']
        self.status_num = self.game_info['gameStatus']
        self.start_time_utc = self.game_info['gameTimeUTC']

        return self.game_info

    def get_scoreboard(self, print_update_done=True, write_only=False):
        """
        :param print_update_done: Print in the command line if the file containing the scoreboard is updated
        :param write_only: Try updating the file and return 'Updated' if so, 'None' otherwise
        :return:
        """
        scoreboards_dict = request_data(self, BOXSCORE_URL.format(game_id=self.game_id),
                                        folder=f'data/{self.year}/scoreboards',
                                        headers=HEADERS)

        if print_update_done and scoreboards_dict is not None:
            print(f'Scoreboard {self.game_id} updated')
            return scoreboards_dict

    def get_play_by_play(self, print_update_done=True):
        play_by_play_dict = request_data(self,
                                         PLAY_BY_PLAY_URL.format(game_id=self.game_id),
                                         folder=f'data/{self.year}/play_by_play',
                                         headers=HEADERS)

        if print_update_done and play_by_play_dict is not None:
            print(f'Play by play {self.game_id} updated')
            play_by_play_df = pd.DataFrame(play_by_play_dict['game']['actions'])
            return play_by_play_df


def update_play_by_play_and_scoreboards(year, date):
    season_start, season_end = load_season_dates(year)
    current_date = date if date is not None else season_start

    path_to_pbp = f'data/{year}/play_by_play'
    path_to_scoreboards = f'data/{year}/scoreboards'
    path_to_calendar_game_ids = f'data/{year}/calendar/calendar_{year}.json'

    if not os.path.exists(path_to_pbp):
        os.makedirs(path_to_pbp)
    if not os.path.exists(path_to_scoreboards):
        os.makedirs(path_to_scoreboards)

    play_by_play_ids = [re.findall(r'\d+', pbp_file)[1] for pbp_file in glob(f'{path_to_scoreboards}/*.json')]
    scoreboards_ids = [re.findall(r'\d+', sb_file)[1] for sb_file in glob(f'{path_to_scoreboards}/*.json')]

    with open(path_to_calendar_game_ids) as f:
        data_calendar_game_ids = json.load(f)

    while current_date < datetime.today().date():
        current_date_nba_format = ''.join(str(current_date).split('-'))

        if current_date_nba_format in data_calendar_game_ids.keys():
            for game_info in data_calendar_game_ids[current_date_nba_format]:

                if game_info['gameId'] in play_by_play_ids and game_info['gameId'] in scoreboards_ids or \
                        game_info['gameId'][:3] not in ['002', '004', '005']:  # '005' : Play-in; '004' : Playoffs
                    # Ignore games that have already been stored
                    continue

                print(current_date, game_info['gameCode'])
                try:
                    current_game = Game(game_info['gameId'], current_date_nba_format, year)
                except requests.exceptions.JSONDecodeError:
                    print(f"{game_info['gameCode']} ignored (JSONDecodeError)")
                    continue

                if current_game.status_num == 1:
                    print(f'{current_game.game_id} not played yet')
                elif current_game.status_num == 2:
                    print(f'{current_game.game_id} is being played')
                else:
                    if game_info['gameId'] not in play_by_play_ids:
                        current_game.get_play_by_play()
                    if game_info['gameId'] not in scoreboards_ids:
                        current_game.get_scoreboard(write_only=True)

                print('\n----------------\n')

        current_date += timedelta(days=1)
