from dataclasses import dataclass


@dataclass
class ClientUserInfo:
    id: str
    followers_count: int
    name: str
    banner_url: str | None = None
