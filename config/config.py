import os


class Config:
    # This shall be specified anew in X Developer Profile
    CALLBACK_URL = (
        "https://9893-2a00-a041-789f-ba00-80e7-ae22-4dc9-efb5.ngrok-free.app/callback"
    )
    # Below data is available via X Developer Profile
    CLIENT_ID = os.environ.get("CLIENT_ID")
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
    CONSUMER_API_KEY = os.environ.get("CONSUMER_API_KEY")
    CONSUMER_API_SECRET = os.environ.get("CONSUMER_API_SECRET")
    # This is for Flask only
    APP_SECRET = os.environ.get("INTERNAL_APP_SECRET")


config = Config()
