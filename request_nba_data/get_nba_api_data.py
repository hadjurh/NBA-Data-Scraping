from nba_api.live.nba.endpoints import boxscore, scoreboard

# Today's Score Board
games = scoreboard.ScoreBoard()

# print(games.get_dict()['game']['actions'])