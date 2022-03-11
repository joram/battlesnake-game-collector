#!/usr/bin/python3
import time

from utils.games import list_recent_games, arena_leaderboard_snakes


def collect():
    print("running collector")
    for snake in list(arena_leaderboard_snakes())[:10]:
        print(snake.snake_name)
        for game in list_recent_games(snake):
            print(game.game_url)


while True:
    collect()
    time.sleep(60*30)  # wait 30min
