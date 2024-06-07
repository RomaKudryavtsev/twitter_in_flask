from tweepy import OAuth1UserHandler


class XApiAuthHandler:
    def __init__(self, consumer_api_key: str, consumer_api_secret: str, callback_url: str):
        self.auth_handler = OAuth1UserHandler(
            consumer_api_key, consumer_api_secret, callback=callback_url
        )

    def get_user_auth_url(self):
        return self.auth_handler.get_authorization_url()

    def get_user_auth_data(self, oauth_verifier: str):
        return self.auth_handler.get_access_token(oauth_verifier)
