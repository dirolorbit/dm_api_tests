from restclient.client import RestClient


class AccountApi(RestClient):

    def post_v1_account(
            self,
            json_data
    ):
        """
        POST /v1/account Register new user
        :param json_data:
        :return:
        """
        response = self.post(
            path="/v1/account",
            json=json_data
        )
        return response

    def put_v1_account_token(
            self,
            token
    ):
        """
        PUT /v1/account/{token} Activate registered user
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
        return response

    def put_v1_account_email(
            self,
            token,
            json_data
    ):
        """
        PUT /v1/account/email Change registered user email
        :param token:
        :param json_data:
        :return:
        """
        headers = {
            "accept": "text/plain",
            "X-Dm-Auth-Token": token
        }
        response = self.put(
            path="/v1/account/email",
            headers=headers,
            json=json_data
        )
        return response
