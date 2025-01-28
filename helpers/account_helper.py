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

    def auth_client(
            self,
            login: str,
            password: str
    ):
        json_data = {
            "login": login,
            "password": password
        }
        response = self.dm_account_api.login_api.post_v1_account_login(json_data=json_data)
        auth_token = {
            "X-Dm-Auth-Token": response.headers["X-Dm-Auth-Token"]
        }
        self.dm_account_api.account_api.set_headers(auth_token)
        self.dm_account_api.login_api.set_headers(auth_token)

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
            email: str
    ):

        token = self.get_activation_token(login=login, email=email)
        assert token is not None, f"Activation token for user {login} is not generated"

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

    def change_user_password(
            self,
            login: str,
            email: str,
            old_password: str,
            new_password: str
    ):
        # Reset password
        json_data = {
            "login": login,
            "email": email
        }
        response = self.dm_account_api.account_api.post_v1_account_password(json_data=json_data)
        assert response.status_code == 200, f"Password reset for {login} is failed: {response.json()}"

        token = self.get_activation_token(login=login, email=email, password_reset=True)

        # Change password
        json_data = {
            "login": login,
            "token": token,
            "oldPassword": old_password,
            "newPassword": new_password
        }
        response = self.dm_account_api.account_api.put_v1_account_password(json_data=json_data)
        assert response.status_code == 200, f"Password change for {login} is failed: {response.json()}"

    @retry
    def get_activation_token(
            self,
            login: str,
            email: str,
            password_reset: bool = False
    ):
        """
        Helper function to retrieve activation token from the last user email
        :param login:
        :param email:
        :param password_reset:
        :return:
        """
        token = None
        token_key = "ConfirmationLinkUri" if password_reset else "ConfirmationLinkUrl"
        response = self.mailhog.mailhog_api.get_v2_messages(limit=50)
        for item in response.json()["items"]:
            if email in item["Content"]["Headers"]["To"]:
                user_data = loads(item["Content"]["Body"])
                user_login = user_data["Login"]
                if user_login == login:
                    if user_data.get(token_key):
                        return user_data.get(token_key).split('/')[-1]
        return token

    def user_logout(
            self
    ):
        response = self.dm_account_api.login_api.delete_v1_account_login()
        assert response.status_code == 204, f"User should be authenticated"

    def user_logout_from_all_devices(
            self
    ):
        response = self.dm_account_api.login_api.delete_v1_account_login_all()
        assert response.status_code == 204, f"User should be authenticated"
