import time
from json import loads

from services.api_mailhog import MailHogApi
from services.dm_api_account import DMApiAccount


def retry(
        function
):
    def wrapper(
            *args,
            **kwargs
    ):
        token = None
        count = 0
        while token is None:
            print(f"Attempt to retrieve token #{count}")
            token = function(*args, **kwargs)
            count += 1
            if count == 5:
                raise AssertionError("Exceeded retry attempts")
            if token:
                return token
            time.sleep(1)

    return wrapper


class AccountHelper:
    def __init__(
            self,
            dm_account_api: DMApiAccount = None,
            mailhog: MailHogApi = None
    ):
        self.dm_account_api = dm_account_api
        self.mailhog = mailhog

    def register_new_user(
            self,
            login: str,
            password: str,
            email: str
    ):
        json_data = {
            "login": login,
            "email": email,
            "password": password
        }

        response = self.dm_account_api.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, f"User is not created: {response.json()}"

    def activate_user(
            self,
            login: str,
            email: str,
            new_user: bool
    ):
        # Retrieve users emails
        # response = self.mailhog.mailhog_api.get_v2_messages(limit=50)
        # assert response.status_code == 200, f"Mails are not received: {response.json()}"

        # Retrieve activation token
        token = self.get_activation_token(login=login, email=email, new_user=new_user)
        assert token is not None, f"Activation token for user {login} is not generated"

        # Activate token
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, f"Token is not activated: {response.json()}"

        return response

    def user_login(
            self,
            login: str,
            password: str,
            rememberme: bool = True
    ):
        json_data = {
            "login": login,
            "password": password,
            "rememberMe": rememberme
        }
        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        return response

    def update_user_email(
            self,
            login: str,
            email: str,
            password: str
    ):
        json_data = {
            "login": login,
            "email": email,
            "password": password
        }
        response = self.dm_account_api.account_api.put_v1_account_email(json_data=json_data)
        assert response.status_code == 200, f"Email for user {login} is not updated: {response.json()}"

    def get_activation_token(
            self,
            login: str,
            new_user: bool,
            email: str = None
    ):
        if new_user:
            # get activation token from the welcome letter
            token = self.get_activation_token_by_login(login=login)
        else:
            # get activation token from the confirmation of the email change letter
            token = self.get_activation_token_by_email_and_login(login=login, email=email)
        return token

    @retry
    def get_activation_token_by_login(
            self,
            login: str
    ):
        """
        Helper function to get activation token from the welcome letter
        :param login:
        :return:
        """
        token = None
        response = self.mailhog.mailhog_api.get_v2_messages(limit=50)
        for item in response.json()["items"]:
            user_data = loads(item["Content"]["Body"])
            user_login = user_data["Login"]
            if user_login == login:
                token = user_data["ConfirmationLinkUrl"].split('/')[-1]
            return token

    @retry
    def get_activation_token_by_email_and_login(
            self,
            login: str,
            email: str
    ):
        """
        Helper function to get activation token from the confirmation of the email change letter
        :param login:
        :param email:
        :return:
        """
        token = None
        response = self.mailhog.mailhog_api.get_v2_messages(limit=50)
        for item in response.json()["items"]:
            if email in item["Content"]["Headers"]["To"]:
                user_data = loads(item["Content"]["Body"])
                user_login = user_data["Login"]
                if user_login == login:
                    token = user_data["ConfirmationLinkUrl"].split('/')[-1]
        return token
