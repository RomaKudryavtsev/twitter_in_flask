from tweepy import OAuth1UserHandler


class TwitterAuthHandler:
    def __init__(self, consumer_api_key, consumer_api_secret, callback_url):
        self.auth_handler = OAuth1UserHandler(
            consumer_api_key, consumer_api_secret, callback=callback_url
        )

    def get_user_auth_url(self):
        return self.auth_handler.get_authorization_url()

    def get_user_auth_data(self, oauth_verifier):
        return self.auth_handler.get_access_token(oauth_verifier)
