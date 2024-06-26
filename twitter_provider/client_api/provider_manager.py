import csv
import time
import logging
from threading import Lock
from .client_api import ClientApiProvider
from .util import get_proxy_url, ProviderInitData


class ClientAPIProviderManager:
    def __init__(self, retries_num: int = 5):
        init_providers: list[ClientApiProvider] = []
        with open("provider_workers.csv", newline="") as workers_creds:
            reader = csv.reader(workers_creds, delimiter=",")
            for row in reader:
                init_providers.append(
                    ClientApiProvider(
                        init_data=ProviderInitData(
                            screen_name=row[0],
                            screen_pwd=row[1],
                            proxy_url=get_proxy_url(row[2], row[3]),
                        )
                    )
                )
        self.providers = {provider: Lock() for provider in init_providers}
        self.retries_num = retries_num

    def _get_provider(self):
        available_provider = None
        while not available_provider:
            for provider, lock in self.providers.items():
                if not lock.locked() and lock.acquire(blocking=False):
                    available_provider = provider
                    break
            time.sleep(0.4)
        logging.warning(f"PROVIDER LAUNCHED: {available_provider.screen_name}")
        return available_provider

    def _release_provider(self, screen_name):
        for provider, lock in self.providers.items():
            if provider.screen_name == screen_name:
                if lock.locked():
                    lock.release()
                    logging.warning(f"PROVIDER RELEASED: {screen_name}")
                return

    def execute_w_retry(self, attr, **params):
        provider = self._get_provider()
        provider_name = provider.screen_name
        func = getattr(provider, attr)
        result = None
        tries = 0
        while result is None:
            if tries >= self.retries_num:
                self._release_provider(provider_name)
                raise RuntimeError("Unable to retrieve data via Client API")
            result = func(**params)
            tries += 1
            if result is None:
                curr_provider_name = provider_name
                provider = self._get_provider()
                provider_name = provider.screen_name
                self._release_provider(curr_provider_name)
        self._release_provider(provider_name)
        return result
