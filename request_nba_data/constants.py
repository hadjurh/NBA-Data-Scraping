import datetime

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'x-nba-stats-origin': 'stats',
    'x-nba-stats-token': 'true',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
}

GLOSSARY_URL = 'https://cdn.nba.com/static/json/staticData/scheduleLeagueV2.json'
BOXSCORE_URL = 'https://cdn.nba.com/static/json/liveData/boxscore/boxscore_{game_id}.json'
PLAY_BY_PLAY_URL = 'https://cdn.nba.com/static/json/liveData/playbyplay/playbyplay_{game_id}.json'
# SCOREBOARD_URL = 'http://data.nba.net/10s/prod/v2/{date}/scoreboard.json'
# PLAYERS_URL = 'http://data.nba.net/10s/prod/v1/{year}/players.json'
# TEAMS_URL = 'http://data.nba.net/10s/prod/v2/{year}/teams.json'
# SCHEDULE_URL = 'http://data.nba.net/prod/v1/{year}/schedule.json'

SEASONS_DATES = {
    '2023-24': {
        'start_date': datetime.date(2023, 10, 24),
        'end_date': datetime.date(2024, 4, 14)
    },
    '2022-23': {
        'start_date': datetime.date(2022, 10, 18),
        'end_date': datetime.date(2023, 4, 9)
    },
    '2021-22': {
        'start_date': datetime.date(2021, 10, 19),
        'end_date': datetime.date(2022, 4, 10)
    },
    '2020-21': {
        'start_date': datetime.date(2020, 12, 22),
        'end_date': datetime.date(2021, 5, 16)
    },
    '2019-20': {
        'start_date': datetime.date(2019, 10, 22),
        'end_date': datetime.date(2020, 4, 15)
    },
    '2018-19': {
        'start_date': datetime.date(2018, 10, 16),
        'end_date': datetime.date(2019, 4, 10)
    },
    '2017-18': {
        'start_date': datetime.date(2017, 10, 16),
        'end_date': datetime.date(2018, 4, 11)
    },
    '2016-17': {
        'start_date': datetime.date(2016, 10, 25),
        'end_date': datetime.date(2017, 4, 12)
    },
    '2015-16': {
        'start_date': datetime.date(2015, 10, 27),
        'end_date': datetime.date(2016, 4, 13)
    },
    '2014-15': {
        'start_date': datetime.date(2014, 10, 28),
        'end_date': datetime.date(2015, 4, 15)
    },
    '2013-14': {
        'start_date': datetime.date(2013, 10, 29),
        'end_date': datetime.date(2014, 4, 16)
    },
    '2012-13': {
        'start_date': datetime.date(2012, 10, 30),
        'end_date': datetime.date(2013, 4, 17)
    },
    '2011-12': {
        'start_date': datetime.date(2011, 12, 25),
        'end_date': datetime.date(2012, 4, 26)
    },
    '2010-11': {
        'start_date': datetime.date(2010, 10, 26),
        'end_date': datetime.date(2011, 4, 13)
    },
    '2009-10': {
        'start_date': datetime.date(2009, 10, 27),
        'end_date': datetime.date(2010, 4, 14)
    },
    '2008-09': {
        'start_date': datetime.date(2008, 10, 28),
        'end_date': datetime.date(2009, 4, 16)
    },
    '2007-08': {
        'start_date': datetime.date(2007, 10, 30),
        'end_date': datetime.date(2008, 4, 16)
    },
    '2006-07': {
        'start_date': datetime.date(2006, 10, 31),
        'end_date': datetime.date(2007, 4, 18)
    },
    '2005-06': {
        'start_date': datetime.date(2005, 11, 1),
        'end_date': datetime.date(2006, 4, 19)
    },
    '2004-05': {
        'start_date': datetime.date(2004, 11, 2),
        'end_date': datetime.date(2005, 4, 20)
    },
    '2003-04': {
        'start_date': datetime.date(2003, 10, 28),
        'end_date': datetime.date(2004, 4, 14)
    },
    '2002-03': {
        'start_date': datetime.date(2002, 10, 29),
        'end_date': datetime.date(2003, 4, 16)
    },
    '2001-02': {
        'start_date': datetime.date(2001, 10, 30),
        'end_date': datetime.date(2002, 4, 17)
    },
    '2000-01': {
        'start_date': datetime.date(2000, 10, 31),
        'end_date': datetime.date(2001, 4, 18)
    },
    '1999-00': {
        'start_date': datetime.date(1999, 11, 2),
        'end_date': datetime.date(2000, 4, 19)
    },
    '1998-99': {
        'start_date': datetime.date(1999, 2, 5),
        'end_date': datetime.date(1999, 5, 5)
    },
    '1997-98': {
        'start_date': datetime.date(1997, 10, 31),
        'end_date': datetime.date(1998, 4, 19)
    },
    '1996-97': {
        'start_date': datetime.date(1996, 11, 1),
        'end_date': datetime.date(1997, 4, 20)
    }
}
