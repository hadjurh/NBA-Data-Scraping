import os
import sys
import json
import requests
import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from request_nba_data.constants import HEADERS, TEAMS_URL


def get_teams(year):
    teams_request = requests.get(TEAMS_URL.format(year=year),
                                 headers=HEADERS,
                                 proxies=None)

    teams_data = teams_request.json()
    teams_data['updateTime'] = str(datetime.datetime.now())[:19]

    if not os.path.exists('data/teams'):
        os.makedirs('data/teams')

    with open(f'data/teams/teams_{year}.json', 'w', encoding='utf-8') as f:
        json.dump(teams_data, f, ensure_ascii=False, indent=4)

    print('Teams updated')
    return teams_data


if __name__ == '__main__':
    from request_nba_data.get_league_info import get_league_info

    season_stage, year, display_year, current_date = get_league_info()
    get_teams(year)
