from json import loads

from services.api_mailhog import MailHogApi
from services.dm_api_account import DMApiAccount


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
        """
        Helper function to cover common scenario: Register user
        :param login:
        :param password:
        :param email:
        :return:
        """
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
        response = self.mailhog.mailhog_api.get_v2_messages(limit=50)
        assert response.status_code == 200, f"Mails are not received: {response.json()}"

        # Retrieve activation token
        # token = self.dm_account_api.account_api.get_activation_token(
        token = self.get_activation_token(
            login=login, email=email, response=response, new_user=new_user
        )
        assert token is not None, f"Activation token for user {login} is not generated"

        # Activate token
        response = self.dm_account_api.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, f"Token is not activated: {response.json()}"

        return response

    def user_successful_login(
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
        assert response.status_code == 200, f"User is not logged in: {response.json()}"
        return response

    def user_failed_login(
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
        assert response.status_code == 403, (f"User {login} should be inactive and login should be forbidden "
                                             f"until confirmation of email change")
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

    @staticmethod
    def get_activation_token(
            login: str,
            response,
            new_user: bool,
            email: str = None
    ):
        if new_user:
            # get activation token from the welcome letter
            token = AccountHelper.get_activation_token_by_login(login=login, response=response)
        else:
            # get activation token from the confirmation of the email change letter
            token = AccountHelper.get_activation_token_by_email_and_login(login=login, email=email, response=response)
        return token

    @staticmethod
    def get_activation_token_by_login(
            login: str,
            response
    ):
        """
        Helper function to get activation token from the welcome letter
        :param login:
        :param response:
        :return:
        """
        token = None
        for item in response.json()["items"]:
            user_data = loads(item["Content"]["Body"])
            user_login = user_data["Login"]
            if user_login == login:
                token = user_data["ConfirmationLinkUrl"].split('/')[-1]
            return token

    @staticmethod
    def get_activation_token_by_email_and_login(
            login: str,
            email: str,
            response
    ):
        """
        Helper function to get activation token from the confirmation of the email change letter
        :param login:
        :param email:
        :param response:
        :return:
        """
        token = None
        for item in response.json()["items"]:
            if email in item["Content"]["Headers"]["To"]:
                user_data = loads(item["Content"]["Body"])
                user_login = user_data["Login"]
                if user_login == login:
                    token = user_data["ConfirmationLinkUrl"].split('/')[-1]
        return token
