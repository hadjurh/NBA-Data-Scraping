import json
import requests
import os
import sys
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from request_nba_data.constants import HEADERS, PLAYERS_URL


def get_players(year):
    players_request = requests.get(PLAYERS_URL.format(year=year),
                                   headers=HEADERS,
                                   proxies=None)

    players_data = players_request.json()
    players_data['updateTime'] = str(datetime.datetime.now())[:19]

    if not os.path.exists('data/players'):
        os.makedirs('data/players')

    with open(f'data/players/players_{year}.json', 'w', encoding='utf-8') as f:
        json.dump(players_data, f, ensure_ascii=False, indent=4)

    print('Players updated')
    return players_data


if __name__ == '__main__':
    from request_nba_data.get_league_info import get_league_info

    season_stage, year, display_year, current_date = get_league_info()
    get_players(year)
