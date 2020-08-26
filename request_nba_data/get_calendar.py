import json
import requests
import os
import sys
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from request_nba_data.constants import HEADERS, SCOREBOARD_URL
from request_nba_data.get_league_info import get_league_info


season_stage, year, display_year, current_date = get_league_info()


def get_calendar_nb_games():
    try:
        with open(f'data/calendar/calendar_nb_games_{year}.json') as f:
            calendar_nb_games = json.load(f)

            if calendar_nb_games['updateTime'][:10] == datetime.date.today().__str__():
                return calendar_nb_games
    except FileNotFoundError:
        pass

    calendar_requests = requests.get('http://data.nba.net/10s/prod/v1/calendar.json',
                                     headers=HEADERS,
                                     proxies=None)

    if not os.path.exists('data/calendar'):
        os.makedirs('data/calendar')

    calendar_nb_games = calendar_requests.json()
    calendar_nb_games['updateTime'] = datetime.datetime.now().__str__()

    with open(f'data/calendar/calendar_nb_games_{year}.json', 'w', encoding='utf-8') as f:
        json.dump(calendar_nb_games, f, ensure_ascii=False, indent=4)

    print('Calendar nb games updated')
    return calendar_requests.json()


def load_season_dates(path_to_calendar_file=None):  # 'data/calendar/calendar_nb_games.json'
    if path_to_calendar_file is not None:
        with open(path_to_calendar_file) as f:
            calendar = json.load(f)
    else:
        calendar = get_calendar_nb_games()

    start = datetime.datetime.strptime(calendar['startDateCurrentSeason'], '%Y%m%d').date()
    end = datetime.datetime.strptime(calendar['endDate'], '%Y%m%d').date()

    return start, end, calendar


def get_calendar_game_ids():
    try:
        with open(f'data/calendar/calendar_game_ids_{year}.json') as f:
            calendar_game_ids = json.load(f)

            if calendar_game_ids['updateTime'][:10] == datetime.date.today().__str__():
                return calendar_game_ids
    except FileNotFoundError:
        pass

    season_start, season_end, data_calendar = load_season_dates()

    current_date = season_start

    calendar_game_ids = dict()

    while current_date <= season_end:
        current_date_nba_format = ''.join(str(current_date).split('-'))

        if current_date_nba_format in data_calendar.keys() and data_calendar[current_date_nba_format] > 0:
            # Contains games' info (id, season stage id)
            daily_score_board = requests.get(SCOREBOARD_URL.format(date=current_date_nba_format),
                                             headers=HEADERS,
                                             proxies=None).json()

            calendar_game_ids[current_date_nba_format] = [{'gameId': game['gameId'],
                                                           'seasonStageId': game['seasonStageId'],
                                                           'gameUrlCode': game['gameUrlCode'],
                                                           'statusNum': game['statusNum'],
                                                           'startTimeUTC': game['startTimeUTC']}
                                                          for game in daily_score_board['games']]

        current_date += datetime.timedelta(days=1)

    calendar_game_ids['updateTime'] = datetime.datetime.now().__str__()

    with open(f'data/calendar/calendar_game_ids_{year}.json', 'w', encoding='utf-8') as f:
        json.dump(calendar_game_ids, f, ensure_ascii=False, indent=4)

    print('Calendar game ids updated')
    return calendar_game_ids


def generate_tonight_games(path_to_calendar_file='data/calendar/calendar_game_ids.json',
                           today_date=datetime.datetime.utcnow().date()):
    if path_to_calendar_file is not None:
        try:
            with open('data/calendar/calendar_game_ids.json') as f:
                data_calendar_game_ids = json.load(f)
        except FileNotFoundError:
            data_calendar_game_ids = get_calendar_game_ids()  # Much longer
    else:
        data_calendar_game_ids = get_calendar_game_ids()  # Much longer

    for game_date in data_calendar_game_ids.keys():
        if datetime.datetime.strptime(game_date, '%Y%m%d').date() >= today_date:
            tonight_games = {game_date: data_calendar_game_ids[game_date],
                             'updateTime': datetime.datetime.now().__str__()}
            with open('data/calendar/tonight_games.json', 'w', encoding='utf-8') as f:
                json.dump(tonight_games, f, ensure_ascii=False, indent=4)

            return tonight_games


if __name__ == '__main__':
    get_calendar_nb_games()

    get_calendar_game_ids()
    generate_tonight_games()
