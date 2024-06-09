class WebIntentProvider:

    INTENT_URL = "https://x.com/intent/post"

    @classmethod
    def _prepare_text(cls, text: str):
        return text.replace(" ", "%20")

    @classmethod
    def get_tweet_intent_url(cls, text: str):
        formatted_text = cls._prepare_text(text=text)
        return f"{cls.INTENT_URL}?text={formatted_text}"
