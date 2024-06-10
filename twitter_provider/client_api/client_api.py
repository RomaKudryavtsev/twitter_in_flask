from tweepy_authlib import CookieSessionUserHandler
from twitter_openapi_python import (
    ItemResult,
    TwitterOpenapiPython,
)
from pathlib import Path
import json
from dataclasses import asdict
from .model import ClientUserInfo


class ClientApiProvider:
    def __init__(self, screen_name: str, screen_pwd: str, default_count: int = 100):
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
        self.default_count = default_count

    def get_user_info_by_screen_name(self, screen_name: str):
        resp = self.user_api.get_user_by_screen_name(screen_name=screen_name)
        return asdict(
            ClientUserInfo(
                id=resp.data.user.rest_id,
                name=resp.data.user.legacy.name,
                followers_count=resp.data.user.legacy.followers_count,
                banner_url=resp.data.user.legacy.profile_banner_url,
            )
        )

    def get_user_following(self, current_screen_name: str, count: int | None = None):
        target_user_id = self.get_user_info_by_screen_name(
            screen_name=current_screen_name
        )["id"]
        resp = self.user_list_api.get_following(
            user_id=target_user_id, count=count or self.default_count
        )
        users_data = resp.data.data
        following_screen_names = []
        for user_data in users_data:
            following_screen_names.append(user_data.user.legacy.screen_name)
        return following_screen_names

    def search_user_tweets(
        self, search_text: str, user_id: str, count: int | None = None
    ):
        resp = self.tweet_api.get_user_tweets(
            user_id=user_id, count=count or self.default_count
        )
        tweets_data = resp.data.data
        return [
            tweet.tweet.legacy.full_text
            for tweet in tweets_data
            if search_text in tweet.tweet.legacy.full_text
        ]

    def get_user_likes(self, user_id: str, count: int | None = None):
        resp = self.tweet_api.get_likes(
            user_id=user_id, count=count or self.default_count
        )
        tweets_data = resp.data.data
        liked_tweets = []
        for tweet_data in tweets_data:
            liked_tweets.append(tweet_data.tweet.rest_id)
        return liked_tweets

    def get_user_retweets(self, user_id: str, count: int | None = None):
        resp = self.tweet_api.get_user_tweets_and_replies(
            user_id=user_id, count=count or self.default_count
        )
        tweets_data = resp.data.data
        retweeted = []
        for tweet_data in tweets_data:
            tweet_data_legacy = tweet_data.tweet.legacy
            if (
                tweet_data_legacy
                and tweet_data_legacy.retweeted
                and tweet_data_legacy.retweeted_status_result
            ):
                original_tweet: ItemResult = tweet_data_legacy.retweeted_status_result
                origanal_tweet_id = original_tweet.to_dict()["result"]["rest_id"]
                retweeted.append(origanal_tweet_id)
        return retweeted
