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
from request_nba_data.constants import HEADERS, SCOREBOARD_URL, BOXSCORE_URL, PLAY_BY_PLAY_URL
from request_nba_data.get_calendar import load_season_dates


def request_data(game, url, write_only, folder):
    if not os.path.isfile(f'data/{folder}/{game.game_id}.json') and write_only:
        request = requests.get(url, headers=HEADERS)
        data_dict = request.json()

        if not os.path.exists(f'data/{folder}'):
            os.makedirs(f'data/{folder}')

        with open(f'data/{folder}/{game.game_id}.json', 'w', encoding='utf-8') as f:
            json.dump(data_dict, f, ensure_ascii=False, indent=4)

        return 'Updated'

    elif not write_only:
        request = requests.get(url, headers=HEADERS, proxies=None)
        return request.json()

    return None


class Game(object):
    """
    Describe an NBA game and its basic information
    """

    def __init__(self, game_id, date):
        self.game_id = game_id
        self.date = date
        self._get_uptodate_game_info()

    def __str__(self):
        return f'Id: {self.game_id}, Date: {self.date}, UrlCode: {self.game_url_code}, ' \
               f'StatusNum: {self.status_num}, Period: {self.game_info["period"]["current"]}, ' \
               f'Clock: {self.game_info["clock"]}'

    def _get_uptodate_game_info(self):
        request = requests.get(SCOREBOARD_URL.format(date=self.date), headers=HEADERS, proxies=None)
        data_dict = request.json()

        self.game_info = [game_info for game_info in data_dict['games'] if game_info['gameId'] == self.game_id][0]

        if self.game_info['clock'] == '':
            self.game_info['clock'] = '0:00'

        elif self.game_info['clock'].__contains__('.') and not self.game_info['clock'].__contains__(':'):
            time_info = [int(i) for i in self.game_info['clock'].split('.')]
            time_info[0] = time_info[0] + 1 if time_info[1] >= 5 else time_info[0]
            self.game_info['clock'] = f'0:{time_info[0]}' if time_info[0] > 9 else f'0:0{time_info[0]}'

        self.game_url_code = self.game_info['gameUrlCode']
        self.status_num = self.game_info['statusNum']
        self.start_time_utc = self.game_info['startTimeUTC']
        self.is_game_activated = self.game_info['isGameActivated']

        return data_dict

    def get_scoreboard(self, print_update_done=True, write_only=False):
        """
        :param print_update_done: Print in the command line if the file containing the scoreboard is updated
        :param write_only: Try updating the file and return 'Updated' if so, 'None' otherwise
        :return:
        """
        scoreboards_dict = request_data(self, BOXSCORE_URL.format(date=self.date, game_id=self.game_id),
                                        write_only, folder='scoreboards')

        if print_update_done and scoreboards_dict == 'Updated':
            print(f'Scoreboard {self.game_id} updated')

        return scoreboards_dict

    def get_active_players(self):
        return ['{} {}'.format(p['firstName'], p['lastName']) for p in self.get_scoreboard()['stats']['activePlayers']]

    def get_play_by_play(self, print_update_done=True):
        rows = []

        for period in range(1, self.game_info['period']['current'] + 1):
            period_play_by_play = request_data(self,
                                               PLAY_BY_PLAY_URL.format(date=self.date,
                                                                       game_id=self.game_id,
                                                                       period_num=period),
                                               False,
                                               'play_by_play')

            for play_dict in period_play_by_play['plays']:
                if play_dict['clock'].__contains__('.'):
                    time_info = [int(i) for i in play_dict['clock'].replace('.', ':').split(':')]
                    time_info[1] = time_info[1] + 1 if time_info[2] >= 5 else time_info[1]

                    assert time_info[0] == 0

                    play_dict['clock'] = f'0:{time_info[1]}' if time_info[1] > 9 else f'0:0{time_info[1]}'

                if play_dict['clock'][0] == '0' and len(play_dict['clock']) == 5:
                    play_dict['clock'] = play_dict['clock'][1:]

                rows.append([play_dict['clock'], int(play_dict['eventMsgType']), play_dict['description'],
                             play_dict['personId'], play_dict['teamId'],
                             play_dict['vTeamScore'] + ' - ' + play_dict['hTeamScore'], period,
                             nan, nan, nan, nan])

        indices = ['PCTIMESTRING', 'EVENTMSGTYPE', 'HOMEDESCRIPTION',
                   'PLAYER1_ID', 'PLAYER1_TEAM_ID', 'SCORE', 'PERIOD',
                   'VISITORDESCRIPTION', 'PLAYER1_NAME', 'PLAYER2_NAME', 'PLAYER3_NAME']
        play_by_play_dict = {"resultSets": [{"name": "PlayByPlay", "headers": indices, "rowSet": rows}]}

        if not os.path.exists('data/play_by_play'):
            os.makedirs('data/play_by_play')

        with open(f'data/play_by_play/{self.game_id}.json', 'w', encoding='utf-8') as f:
            json.dump(play_by_play_dict, f, ensure_ascii=False, indent=4)

        if print_update_done:
            print(f'Play by play {self.game_id} updated')

        play_by_play_df = pd.DataFrame.from_dict(play_by_play_dict['resultSets'][0]['rowSet'])
        play_by_play_df.columns = play_by_play_dict['resultSets'][0]['headers']

        return play_by_play_df


def update_play_by_play_and_scoreboards(year):
    season_start, season_end, data_calendar = load_season_dates()
    current_date = season_start

    if not os.path.exists('data/play_by_play'):
        os.makedirs('data/play_by_play')
    if not os.path.exists('data/scoreboards'):
        os.makedirs('data/scoreboards')

    play_by_play_ids = [re.findall(r'\d+', pbp_file)[0] for pbp_file in glob('data/play_by_play/*.json')]
    scoreboards_ids = [re.findall(r'\d+', sb_file)[0] for sb_file in glob('data/scoreboards/*.json')]

    with open(f'data/calendar/calendar_game_ids_{year}.json') as f:
        data_calendar_game_ids = json.load(f)

    while current_date < datetime.today().date():
        current_date_nba_format = ''.join(str(current_date).split('-'))

        if current_date_nba_format in data_calendar_game_ids.keys():
            for game_info in data_calendar_game_ids[current_date_nba_format]:

                if game_info['gameId'] in play_by_play_ids and game_info['gameId'] in scoreboards_ids or \
                        game_info['gameId'][:3] not in ['002', '004', '005']:  # '005' : Play-in; '004' : Playoffs
                    # Ignore games that have already been stored
                    continue

                print(current_date, game_info['gameUrlCode'])
                current_game = Game(game_info['gameId'], current_date_nba_format)

                if game_info['gameId'] not in play_by_play_ids:
                    current_game.get_play_by_play()
                if game_info['gameId'] not in scoreboards_ids:
                    current_game.get_scoreboard(write_only=True)

                print('\n----------------\n')

        current_date += timedelta(days=1)
