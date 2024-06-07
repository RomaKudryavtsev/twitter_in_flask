import os


class Config:
    # This shall be specified anew in X Developer Profile
    CALLBACK_URL = (
        "https://ac3f-2a01-73c0-950-cc4a-5dcc-63d8-549c-c55d.ngrok-free.app/callback"
    )
    # Below data is available via X Developer Profile
    CLIENT_ID = os.environ.get("CLIENT_ID")
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
    CONSUMER_API_KEY = os.environ.get("CONSUMER_API_KEY")
    CONSUMER_API_SECRET = os.environ.get("CONSUMER_API_SECRET")
    # Below data is required for client API
    SCREEN_NAME = os.environ.get("SCREEN_NAME")
    SCREEN_PWD = os.environ.get("SCREEN_PWD")
    # This is for Flask only
    APP_SECRET = os.environ.get("INTERNAL_APP_SECRET")


config = Config()
