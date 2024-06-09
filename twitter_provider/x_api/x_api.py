from tweepy import Client, Response
from .model import XUserInfo
from dataclasses import asdict


class XApiProvider:
    def __init__(
        self, consumer_key: str, consumer_secret: str, default_count: int = 100
    ):
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.default_count = default_count

    def _get_client(self, access_token: str, access_token_secret: str):
        return Client(
            consumer_key=self.consumer_key,
            consumer_secret=self.consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
        )

    def get_user_me(self, access_token: str, access_token_secret: str):
        client = self._get_client(access_token, access_token_secret)
        response: Response = client.get_me(
            user_fields=["public_metrics", "profile_image_url"]
        )
        response_data = response.data
        return asdict(
            XUserInfo(
                id=response_data["id"],
                username=response_data["username"],
                name=response_data["name"],
                followers_count=response_data["public_metrics"]["followers_count"],
                following_count=response_data["public_metrics"]["following_count"],
                tweet_count=response_data["public_metrics"]["tweet_count"],
                profile_image_url=response_data["profile_image_url"],
            )
        )

    # From X API:
    # "connection_status": ["follow_request_received", "follow_request_sent", "blocking", "followed_by", "following", "muting"]
    def get_connection_status(
        self, username: str, access_token: str, access_token_secret: str
    ):
        client = self._get_client(access_token, access_token_secret)
        response: Response = client.get_user(
            username=username, user_fields=["connection_status"], user_auth=True
        )
        if response and response.data:
            try:
                statuses = response.data["connection_status"]
                return statuses[0] if statuses else "No Connection Between Users"
            except KeyError:
                return "No Connection Between Users"
        else:
            return "Unable to Get Data"

    def search_user_tweets(
        self,
        user_id: str,
        search_text: str,
        access_token: str,
        access_token_secret: str,
        count: int | None = None,
    ):
        client = self._get_client(access_token, access_token_secret)
        response: Response = client.get_users_tweets(
            id=user_id,
            max_results=(
                count if count and count <= self.default_count else self.default_count
            ),
            user_auth=True,
        )
        if response and response.data:
            return [data for data in response.data if search_text in data["text"]] or []
        else:
            return []

    def get_tweet_likes(
        self, tweet_id: str, access_token: str, access_token_secret: str
    ):
        client = self._get_client(access_token, access_token_secret)
        response: Response = client.get_liking_users(id=tweet_id, user_auth=True)
        if response and response.data:
            liking_usernames = [data["username"] for data in response.data]
            return liking_usernames or []
        else:
            return []

    def get_tweet_retweets(
        self, tweet_id: str, access_token: str, access_token_secret: str
    ):
        client = self._get_client(access_token, access_token_secret)
        response: Response = client.get_retweeters(id=tweet_id, user_auth=True)
        if response and response.data:
            retweeters_usernames = [data["username"] for data in response.data]
            return retweeters_usernames or []
        else:
            return []
