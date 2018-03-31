from ch.client import RussellHttpClient
from ch.model.user import User


class AuthClient(RussellHttpClient):
    """
    Auth/User specific client
    """

    def __init__(self):
        self.url = "/user"
        self.token_url = "/token"
        super(AuthClient, self).__init__()

    def get_user(self, access_token):
        user_dict = self.request("GET", url=self.url, access_token=access_token)
        return User.from_dict(user_dict)

    def get_token(self, username, password):
        token_dict = self.request("GET",
                                  url=self.token_url,
                                  auth=(username, password))
        return token_dict
