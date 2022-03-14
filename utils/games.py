import json
import os
import time
from typing import List, Generator, Optional

import bs4
import requests
from websocket import create_connection

from models import Game, Snake


def arena_leaderboard_snakes(url="https://play.battlesnake.com/arena/global/") -> List[Snake]:
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, features="lxml")
    table_rows = soup.find_all("tr", {"class": "ladder-row"})
    for row in table_rows:
        data = row.attrs
        yield Snake(
            arena=data["data-arena"],
            tier=data["data-tier"],
            snake_name=data["data-snake-name"],
            snake_id=data["data-snake-id"],
            games=data["data-games"],
            wins=int(data["data-wins"].replace(",", "")),
            losses=int(data["data-losses"].replace(",", "")),
            win_rate=float(data["data-win-rate"]),
            snake_url=data["data-snake-url"],
            author_url=data["data-author-url"],
            author_name=data["data-author-name"],
            tech_tags=data["data-tech-tags"],
            country=data["data-country"],
            joined=data["data-joined"],
        )


def list_recent_won_games(snake: Snake) -> Generator[Game, None, None]:
    url = f"https://play.battlesnake.com/arena/details/{snake.snake_id}/"
    response = requests.get(url)
    data = response.json()
    for data in data["recent_games"]:
        if data["result"] != "won":
            continue
        yield get_game(
            snake=snake,
            game_url=data["game_url"],
            point_change=data["point_change"],
            result=data["result"],
            score_change=data["score_change"],
            tier_change=data["tier_change"],
            turns=int(data["turns"]),
        )


def _cache_dir(snake: Snake, game_id, depth=3) -> str:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    directory = os.path.join(dir_path, "../data/")
    directory = os.path.join(directory, snake.snake_name.replace("/", "_"))
    for i in range(0, depth):
        char = game_id[0]
        game_id = game_id[1:]
        directory = os.path.join(directory, char)
    return directory


def _get_cached_game(snake: Snake, game_id: str) -> Optional[Game]:
    # directory exists
    directory = _cache_dir(snake, game_id)

    # cache hits
    filepath = os.path.join(directory, f"{game_id}.json")
    if os.path.exists(filepath):
        with open(filepath) as f:
            return Game.from_json(json.loads(f.read()))

    # cache miss
    return None


def _get_game_frames(game_id: str) -> List[dict]:
    url = f"wss://engine.battlesnake.com/games/{game_id}/events"
    ws = create_connection(url)
    frames = []
    while True:
        result = ws.recv()
        try:
            frame = json.loads(result)
        except Exception as e:
            print(e)
            print(result)
        if frame["Type"] == "frame":
            frames.append(frame)
        if frame["Type"] == "game_end":
            break
    ws.close()
    return frames


def get_game(snake: Snake, game_url:str, point_change:str, result:str, score_change:str, tier_change:str, turns:int):
    game_id = game_url.replace("/g/", "").replace("/", "")

    # cache hit
    game = _get_cached_game(snake, game_id)
    if game is not None:
        return game

    # cache miss
    print("cache miss")
    time.sleep(5)
    game = Game(
        game_url=game_url,
        point_change=point_change,
        result=result,
        score_change=score_change,
        tier_change=tier_change,
        turns=turns,
        frames=_get_game_frames(game_id),
    )

    # populate cache
    directory = _cache_dir(snake, game_id)
    filepath = os.path.join(directory, f"{game_id}.json")
    os.makedirs(directory, exist_ok=True)
    with open(filepath, "w") as f:
        f.write(json.dumps(Game.to_json(game),indent=1, sort_keys=True))

    return game
