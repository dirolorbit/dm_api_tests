from dm_api_account.models.change_email import ChangeEmail
from dm_api_account.models.change_password import ChangePassword
from dm_api_account.models.registration import Registration
from dm_api_account.models.reset_password import ResetPassword
from dm_api_account.models.user_details_envelope import UserDetailsEnvelope
from dm_api_account.models.user_envelope import UserEnvelope
from restclient.client import RestClient


class AccountApi(RestClient):

    def post_v1_account(
            self,
            registration: Registration
    ):
        """
        POST /v1/account Register new user
        :param registration:
        :return:
        """
        response = self.post(
            path="/v1/account",
            json=registration.model_dump(exclude_none=True, by_alias=True)
        )
        return response

    def put_v1_account_token(
            self,
            token,
            validate_response=True
    ):
        """
        PUT /v1/account/{token} Activate registered user
        :param validate_response:
        :param token:
        :return:
        """
        headers = {
            "accept": "text/plain",
        }
        response = self.put(
            path=f"/v1/account/{token}",
            headers=headers
        )
        if validate_response:
            UserEnvelope(**response.json())
        return response

    def put_v1_account_email(
            self,
            change_email: ChangeEmail,
            validate_response=True
    ):
        """
        PUT /v1/account/email Change registered user email
        :param validate_response:
        :param change_email:
        :return:
        """
        response = self.put(
            path="/v1/account/email",
            json=change_email.model_dump(exclude_none=True, by_alias=True)
        )
        if validate_response:
            UserEnvelope(**response.json())
        return response

    def get_v1_account(
            self,
            validate_response=True,
            **kwargs
    ):
        """
        GET /v1/account Get current user
        :param validate_response:
        :param kwargs:
        :return:
        """
        response = self.get(
            path="/v1/account",
            **kwargs
        )
        if validate_response:
            UserDetailsEnvelope(**response.json())
        return response

    def post_v1_account_password(
            self,
            reset_password: ResetPassword,
            validate_response=True,
            **kwargs
    ):
        """
        POST /v1/account/password Reset registered user password
        :param validate_response:
        :param reset_password:
        :param kwargs:
        :return:
        """
        response = self.post(
            path="/v1/account/password",
            json=reset_password.model_dump(exclude_none=True, by_alias=True),
            **kwargs
        )
        if validate_response:
            UserEnvelope(**response.json())
        return response

    def put_v1_account_password(
            self,
            change_password: ChangePassword,
            validate_response=True,
            **kwargs
    ):
        """
        PUT /v1/account/password Change registered user password
        :param validate_response:
        :param change_password:
        :param kwargs:
        :return:
        """
        response = self.put(
            path="/v1/account/password",
            json=change_password.model_dump(exclude_none=True, by_alias=True),
            **kwargs
        )
        if validate_response:
            UserEnvelope(**response.json())
        return response
