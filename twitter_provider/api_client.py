from tweepy import Client, Response
from .model import TwitterUserInfo
from dataclasses import asdict


class TwitterApiProvider:
    def get_user_info(
        self, consumer_key, consumer_secret, access_token, access_token_secret
    ):
        client = Client(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
        )
        response: Response = client.get_me(user_fields=["public_metrics"])
        response_data = response.data
        return asdict(
            TwitterUserInfo(
                username=response_data["username"],
                name=response_data["name"],
                followers_count=response_data["public_metrics"]["followers_count"],
                following_count=response_data["public_metrics"]["following_count"],
                tweet_count=response_data["public_metrics"]["tweet_count"],
            )
        )
