from dataclasses import dataclass


@dataclass
class XUserInfo:
    id: int
    username: str
    name: str
    followers_count: int
    tweet_count: int
    following_count: int | None = None
