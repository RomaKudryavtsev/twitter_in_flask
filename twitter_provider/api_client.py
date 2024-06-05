from tweepy import Client, Response
from .model import XUserInfo
from dataclasses import asdict


class TwitterApiProvider:
    def _get_client(
        self, consumer_key, consumer_secret, access_token, access_token_secret
    ):
        return Client(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
        )

    def get_user_info(
        self, consumer_key, consumer_secret, access_token, access_token_secret
    ):
        client = self._get_client(
            consumer_key, consumer_secret, access_token, access_token_secret
        )
        response: Response = client.get_me(user_fields=["public_metrics"])
        response_data = response.data
        return asdict(
            XUserInfo(
                id=response_data["id"],
                username=response_data["username"],
                name=response_data["name"],
                followers_count=response_data["public_metrics"]["followers_count"],
                following_count=response_data["public_metrics"]["following_count"],
                tweet_count=response_data["public_metrics"]["tweet_count"],
            )
        )

    # From Twitter API:
    # "connection_status": ["follow_request_received", "follow_request_sent", "blocking", "followed_by", "following", "muting"]
    def get_connection_status(
        self, username, consumer_key, consumer_secret, access_token, access_token_secret
    ):
        client = self._get_client(
            consumer_key, consumer_secret, access_token, access_token_secret
        )
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

    def get_tweet_likes(
        self, tweet_id, consumer_key, consumer_secret, access_token, access_token_secret
    ):
        client = self._get_client(
            consumer_key, consumer_secret, access_token, access_token_secret
        )
        response: Response = client.get_liking_users(id=tweet_id, user_auth=True)
        if response and response.data:
            liking_usernames = [data["username"] for data in response.data]
            return liking_usernames or []
        else:
            return []

    def get_tweet_retweets(
        self, tweet_id, consumer_key, consumer_secret, access_token, access_token_secret
    ):
        client = self._get_client(
            consumer_key, consumer_secret, access_token, access_token_secret
        )
        response: Response = client.get_retweeters(id=tweet_id, user_auth=True)
        if response and response.data:
            retweeters_usernames = [data["username"] for data in response.data]
            return retweeters_usernames or []
        else:
            return []
