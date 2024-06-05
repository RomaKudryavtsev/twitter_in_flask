from dataclasses import dataclass


@dataclass
class TwitterUserInfo:
    id: int
    username: str
    name: str
    followers_count: int
    following_count: int
    tweet_count: int
