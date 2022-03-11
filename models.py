import dataclasses
from typing import List


@dataclasses.dataclass
class Snake:
    arena: str
    tier: int
    snake_name: str
    snake_id: str
    games: int
    wins: int
    losses: int
    win_rate: float
    snake_url: str
    author_url: str
    author_name: str
    tech_tags: str
    country: str
    joined: str


@dataclasses.dataclass
class Game:
    game_url: str
    point_change: str
    result: str
    score_change: str
    tier_change: str
    turns: int
    frames: List[dict]

    @classmethod
    def from_json(cls, data:dict) -> "Game":
        return Game(
            game_url=data["game_url"],
            point_change=data["point_change"],
            result=data["result"],
            score_change=data["score_change"],
            tier_change=data["tier_change"],
            turns=data["turns"],
            frames=data["frames"],
        )

    @classmethod
    def to_json(cls, game: "Game") -> dict:
        return {
            "game_url":game.game_url,
            "point_change":game.point_change,
            "result":game.result,
            "score_change":game.score_change,
            "tier_change":game.tier_change,
            "turns":game.turns,
            "frames":game.frames,
        }

