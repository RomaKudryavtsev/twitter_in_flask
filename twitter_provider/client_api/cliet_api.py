from tweepy_authlib import CookieSessionUserHandler
from twitter_openapi_python import TwitterOpenapiPython, UserResults
from pathlib import Path
import json


class ClientApiProvider:
    def __init__(self, screen_name, screen_pwd):
        cookies_dict = dict()
        if Path("cookie.json").exists():
            with open("cookie.json", "r") as f:
                cookies_dict = json.load(f)
        else:
            auth_handler = CookieSessionUserHandler(
                screen_name=screen_name,
                password=screen_pwd,
            )
            cookies_dict = auth_handler.get_cookies().get_dict()
            with open("cookie.json", "w") as f:
                f.write(json.dumps(cookies_dict))
        client_api = TwitterOpenapiPython().get_client_from_cookies(
            cookies=cookies_dict
        )
        self.user_api = client_api.get_user_api()
        self.user_list_api = client_api.get_user_list_api()
        self.tweet_api = client_api.get_tweet_api()

    def get_user_id_by_screen_name(self, screen_name: str):
        resp = self.user_api.get_user_by_screen_name(screen_name=screen_name)
        user_res: UserResults = resp.data.data[0].raw
        return user_res.to_dict()["result"]["legacy"]["rest_id"]

    def get_user_following(self, target_screen_name: str):
        target_user_id = self.get_user_id_by_screen_name(screen_name=target_screen_name)
        resp = self.user_list_api.get_following(user_id=target_user_id)
        users_data = resp.data.data
        following_screen_names = []
        for user_data in users_data:
            user_res: UserResults = user_data.raw
            following_screen_names.append(
                user_res.to_dict()["result"]["legacy"]["screen_name"]
            )
        return following_screen_names

    def get_user_likes(self, user_id: str):
        resp = self.tweet_api.get_likes(user_id=user_id)

    def get_retweets(self, tweet_id):
        resp = self.tweet_api.get_tweet_detail(focal_tweet_id=tweet_id)
