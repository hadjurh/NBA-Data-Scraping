import json
import requests
import os
import sys
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from request_nba_data.constants import HEADERS, SCOREBOARD_URL, SEASONS_DATES, SCHEDULE_URL


def get_calendar_nb_games(year):
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


def load_season_dates(year, path_to_calendar_file=None):  # 'data/calendar/calendar_nb_games.json'
    if path_to_calendar_file is not None:
        with open(path_to_calendar_file) as f:
            calendar = json.load(f)
    else:
        calendar = get_calendar_nb_games(year)

    start = SEASONS_DATES[f'{year}-{str(int(year) + 1)[2:]}']['start_date']
    end = SEASONS_DATES[f'{year}-{str(int(year) + 1)[2:]}']['end_date']

    return start, end, calendar


def get_calendar_game_ids(year):
    # Using http://data.nba.net/prod/v1/{year}/schedule.json,
    # which only requires 1 request.

    try:
        with open(f'data/calendar/calendar_game_ids_{year}.json') as f:
            calendar_game_ids = json.load(f)

            if calendar_game_ids['updateTime'][:10] == datetime.date.today().__str__():
                return calendar_game_ids
    except FileNotFoundError:
        pass

    schedule_requests = requests.get(SCHEDULE_URL.format(year=year),
                                     headers=HEADERS,
                                     proxies=None).json()['league']['standard']
    schedule_dates_nba_format_list = sorted(list(set([g['startDateEastern'] for g in schedule_requests])))

    calendar_game_ids = {
        date_nba_format: [{'gameId': game['gameId'],
                           'seasonStageId': game['seasonStageId'],
                           'gameUrlCode': game['gameUrlCode'],
                           'statusNum': game['statusNum'],
                           'startTimeUTC': game['startTimeUTC']} for game in schedule_requests if
                          game['startDateEastern'] == date_nba_format]
        for date_nba_format in schedule_dates_nba_format_list
    }

    calendar_game_ids['updateTime'] = datetime.datetime.now().__str__()

    with open(f'data/calendar/calendar_game_ids_{year}.json', 'w', encoding='utf-8') as f:
        json.dump(calendar_game_ids, f, ensure_ascii=False, indent=4)

    print('Calendar game ids updated')
    return calendar_game_ids


def generate_tonight_games(year,
                           path_to_calendar_file='data/calendar/calendar_game_ids.json',
                           today_date=datetime.datetime.utcnow().date()):
    if path_to_calendar_file is not None:
        try:
            with open('data/calendar/calendar_game_ids.json') as f:
                data_calendar_game_ids = json.load(f)
        except FileNotFoundError:
            data_calendar_game_ids = get_calendar_game_ids(year)  # Much longer
    else:
        data_calendar_game_ids = get_calendar_game_ids(year)  # Much longer

    for game_date in data_calendar_game_ids.keys():
        if datetime.datetime.strptime(game_date, '%Y%m%d').date() >= today_date:
            tonight_games = {game_date: data_calendar_game_ids[game_date],
                             'updateTime': datetime.datetime.now().__str__()}
            with open('data/calendar/tonight_games.json', 'w', encoding='utf-8') as f:
                json.dump(tonight_games, f, ensure_ascii=False, indent=4)

            return tonight_games


if __name__ == '__main__':
    get_calendar_nb_games('2021')

    get_calendar_game_ids('2021')
    generate_tonight_games('2021')
