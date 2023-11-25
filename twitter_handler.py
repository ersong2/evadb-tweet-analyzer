# currently unused fi
# may contain import or syntax errors
# modeled after existing third party handlers in evadb

from evadb.third_party.types import DBHandler, DBHandlerStatus, DBHandlerResponse
import tweepy
from tweepy import Client
class TweetHandler(DBHandler):
    def __init__(self, name:str, **kwargs):
        super().__init__(name)
        self.token = kwargs.get("token")
        self.secret = kwargs.get("secret")

    def connect(self):
        try:
            self.client = Client(token = self.token)
            self.auth = tweepy.OAuth2AppHandler(self.token, self.secret)
            self.api = tweepy.API(self.auth)
            return DBHandlerStatus(status = True)
        except Exception as e:
            return DBHandlerStatus(status = False, error = str(e))

    def disconnect(self):
        """
        not yet supported
        """
        raise NotImplementedError()

    def check_connection(self)->DBHandlerStatus:
        """
        not supported; tweepy.api does not seem to have a method to simply check status
        """
        raise NotImplementedError()

    def get_tables(self, table_name: str)->DBHandlerResponse:
        columns = [
            "id",
            "name",
            "username",
            "text",
            "created_at",
            "retweet_count",
            "like_count"
        ]
        columns.df = pd.DataFrame(columns, columns=["column_name"])
        return DBHandlerResponse(data=columns.df)

    def post_tweet(self, text)->DBHandlerResponse:
        try:
            tweet = self.api.update_status(text)
            return DBHandlerResponse(data=tweet["text"])
        except Exception as e:
            assert e.response["ok"] is False
            assert e.response["error"]
            return DBHandlerResponse(data=None, error=e.response["error"])

    def delete_tweet(self, id)->DBHandlerResponse:
        try:
            self.api.destroy_status(id)
        except Exception as e:
            assert e.response["ok"] is False
            assert e.response["error"]
            return DBHandlerResponse(data=None, error=e.response["error"])

    def convert_json_response_to_DataFrame_(self, json_response):
        tweets = json_response["tweets"]
        columns = ["username", "text", "created_at"]
        data_df = pd.DataFrame(columns=columns)
        for tweet in tweets:
            if tweet["username"] and tweet["text"] and tweet["created_at"]:
                data_df.loc[len(data_df.index)] = [
                    tweet["username"],
                    tweet["text"],
                    tweet["created_at"],
                ]
        return data_df
