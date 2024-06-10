from dataclasses import dataclass


@dataclass
class ProviderInitData:
    screen_name: str
    screen_pwd: str
    proxy_url: str | None = None


def get_proxy_url(proxy_ip: str, proxy_port: str):
    return f"https://{proxy_ip}:{proxy_port}" if proxy_ip and proxy_port else None
