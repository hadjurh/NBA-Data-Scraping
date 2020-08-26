import sys
import os
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
from request_nba_data.constants import GLOSSARY_URL, HEADERS


def get_glossary_info():
    return requests.get(GLOSSARY_URL,
                        headers=HEADERS,
                        proxies=None).json()


def get_league_info():
    glossary = get_glossary_info()

    season_stage = glossary['teamSitesOnly']['seasonStage']
    year = glossary['teamSitesOnly']['seasonYear']
    display_year = glossary['teamSitesOnly']['displayYear']
    current_date = glossary['links']['currentDate']

    return season_stage, year, display_year, current_date


if __name__ == '__main__':
    g = get_glossary_info()
    print(g)
