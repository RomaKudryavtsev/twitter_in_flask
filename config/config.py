import os


class Config:
    # This shall be specified anew in X Developer Profile
    CALLBACK_URL = (
        "https://d241-2a00-a041-789f-ba00-bd72-d6ec-3af9-fda8.ngrok-free.app/callback"
    )
    # Below data is available via X Developer Profile
    CLIENT_ID = os.environ.get("CLIENT_ID")
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
    CONSUMER_API_KEY = os.environ.get("CONSUMER_API_KEY")
    CONSUMER_API_SECRET = os.environ.get("CONSUMER_API_SECRET")
    # Below data is required for Client API
    SCREEN_NAME = os.environ.get("SCREEN_NAME")
    SCREEN_PWD = os.environ.get("SCREEN_PWD")
    # This is for Flask only
    APP_SECRET = os.environ.get("INTERNAL_APP_SECRET")


config = Config()
