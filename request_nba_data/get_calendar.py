import json
import requests
import os
import sys
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from request_nba_data.constants import HEADERS, SEASONS_DATES


# Outdated
def get_calendar_nb_games(year):
    path_to_calendar_nb_games = f'data/{year}/calendar/calendar_nb_games_{year}.json'
    try:
        with open(path_to_calendar_nb_games) as f:
            calendar_nb_games = json.load(f)

            if calendar_nb_games['updateTime'][:10] == datetime.date.today().__str__():
                return calendar_nb_games
    except FileNotFoundError:
        pass

    calendar_requests = requests.get('http://data.nba.net/10s/prod/v1/calendar.json',
                                     headers=HEADERS,
                                     proxies=None)

    if not os.path.exists(f'data/{year}/calendar'):
        os.makedirs(f'data/{year}/calendar')

    calendar_nb_games = calendar_requests.json()
    calendar_nb_games['updateTime'] = datetime.datetime.now().__str__()

    with open(path_to_calendar_nb_games, 'w', encoding='utf-8') as f:
        json.dump(calendar_nb_games, f, ensure_ascii=False, indent=4)

    print('Calendar nb games updated')
    return calendar_requests.json()


def load_season_dates(year):
    start = SEASONS_DATES[f'{year}-{str(int(year) + 1)[2:]}']['start_date']
    end = SEASONS_DATES[f'{year}-{str(int(year) + 1)[2:]}']['end_date']
    return start, end


def get_calendar_game_ids(year):
    # Using http://data.nba.net/prod/v1/{year}/schedule.json,
    # which only requires 1 request.
    path = f'data/{year}/calendar/calendar_game_ids_{year}.json'
    try:
        with open(path) as f:
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

    with open(path, 'w', encoding='utf-8') as f:
        json.dump(calendar_game_ids, f, ensure_ascii=False, indent=4)

    print('Calendar game ids updated')
    return calendar_game_ids


def generate_tonight_games(year,
                           path_to_calendar_file='data/{}/calendar/calendar_game_ids_{}.json',
                           today_date=datetime.datetime.utcnow().date()):
    if path_to_calendar_file is not None:
        try:
            with open(path_to_calendar_file.format(year, year)) as f:
                data_calendar_game_ids = json.load(f)
        except FileNotFoundError:
            data_calendar_game_ids = get_calendar_game_ids(year)  # Much longer
    else:
        data_calendar_game_ids = get_calendar_game_ids(year)  # Much longer

    for game_date in data_calendar_game_ids.keys():
        if game_date.isdigit() and datetime.datetime.strptime(game_date, '%Y%m%d').date() >= today_date:
            tonight_games = {game_date: data_calendar_game_ids[game_date],
                             'updateTime': datetime.datetime.now().__str__()}
            with open(f'data/{year}/calendar/tonight_games.json', 'w', encoding='utf-8') as f:
                json.dump(tonight_games, f, ensure_ascii=False, indent=4)

            return tonight_games


if __name__ == '__main__':
    year = 2022
    get_calendar_nb_games(year)
    get_calendar_game_ids(year)
    generate_tonight_games(year, f'data/calendar/{year}/calendar_game_ids_{year}.json')
