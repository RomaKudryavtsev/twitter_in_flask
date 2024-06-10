import csv
import time
from threading import Lock
from .client_api import ClientApiProvider


class ClientAPIProviderManager:
    def __init__(self, retries_num: int = 5):
        creds_map = {}
        with open("provider_workers.csv", newline="") as workers_creds:
            reader = csv.reader(workers_creds, delimiter=",")
            for row in reader:
                creds_map[row[0]] = row[1]
        self.providers = {
            ClientApiProvider(screen_name=name, screen_pwd=pwd): Lock()
            for (name, pwd) in creds_map.items()
        }
        self.retries_num = retries_num

    def _get_provider(self):
        available_provider = None
        while not available_provider:
            for provider, lock in self.providers.items():
                if not lock.locked() and lock.acquire(blocking=False):
                    available_provider = provider
                    break
            time.sleep(0.4)
        return available_provider

    def _release_provider(self, screen_name):
        for provider, lock in self.providers.items():
            if provider.screen_name == screen_name:
                if lock.locked():
                    lock.release()
                return

    def execute_w_retry(self, attr, **params):
        provider = self._get_provider()
        provider_name = provider.screen_name
        func = getattr(provider, attr)
        result = None
        tries = 0
        while not result:
            if self.retries_num == tries:
                raise RuntimeError("Unable to retrieve data via Client API")
            try:
                result = func(**params)
            finally:
                tries += 1
                self._release_provider(provider_name)
            if not result:
                provider = self._get_provider()
                provider_name = provider.screen_name
        return result
