from tweepy_authlib import CookieSessionUserHandler
from twitter_openapi_python import TwitterOpenapiPython, UserApiUtilsData, UserResults





auth_handler = CookieSessionUserHandler(
    screen_name="rmnzndlr",
    password="280596Lada!",
)
cookies_dict = auth_handler.get_cookies().get_dict()

# get client from cookies
open_client = TwitterOpenapiPython().get_client_from_cookies(cookies=cookies_dict)

# # get user info
# response = 𝕏.get_user_api().get_user_by_screen_name("elonmusk")
# print(response.data)

resp = open_client.get_user_list_api().get_following(user_id="1583585351104348160")
timeline_resp = resp.data
users_data = timeline_resp.data
user_data: UserApiUtilsData = users_data[0]
res: UserResults = user_data.raw
print(res.to_dict()["result"]["legacy"]["screen_name"])

# resp = open_client.get_tweet_api().get_likes(user_id="1583585351104348160")
# tweets_data = resp.data.data
# for tweet_data in tweets_data:
#     print(tweet_data)
