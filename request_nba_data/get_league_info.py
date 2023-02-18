import sys
import os
import requests
import json
from datetime import datetime, timedelta

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from request_nba_data.constants import GLOSSARY_URL, HEADERS


def get_glossary_info():
    return requests.get(GLOSSARY_URL, headers=HEADERS, timeout=3).json()


def get_league_info():
    glossary = get_glossary_info()

    league_schedule = glossary['leagueSchedule']['gameDates']
    try:
        league_schedule = [{'gameDate': datetime.strptime(s['gameDate'], '%m/%d/%Y %H:%M:%S %p').date(),
                        'games': s['games']}
                         for s in league_schedule]
    except ValueError:
        league_schedule = [{'gameDate': datetime.strptime(s['gameDate'], '%m/%d/%Y %H:%M:%S').date(),
                            'games': s['games']}
                           for s in league_schedule]
    today_date = datetime.today().date()
    games_within_range = [s['games'] for s in league_schedule if
                          today_date - timedelta(days=3) <= s['gameDate'] <= today_date + timedelta(days=3)]
    season_stage_within_range = [int(g_dict['gameId'][3]) for g_list in games_within_range for g_dict in g_list]
    if len(set(season_stage_within_range)) != 1:
        print('Season stage is not consistent, please check')
        season_stage = None
    else:
        season_stage = season_stage_within_range[0]

    display_year = glossary['leagueSchedule']['seasonYear']
    year = display_year[:4]

    league_schedule = {str(s['gameDate']).replace('-', ''): s['games'] for s in league_schedule}
    with open(f'data/{year}/calendar/calendar_{year}.json', 'w', encoding='utf-8') as f:
        json.dump(league_schedule, f, ensure_ascii=False, indent=4)

    return season_stage, year, display_year, today_date, league_schedule


if __name__ == '__main__':
    g = get_glossary_info()
    print(g)
