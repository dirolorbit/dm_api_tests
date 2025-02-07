from checkers.get_v1_account import GetV1Account
from checkers.http_checkers import check_status_code_http
from dm_api_account.models.user_details_envelope import (
    UserDetailsEnvelope
)


def test_get_v1_account_non_auth(
        account_helper
):
    with check_status_code_http(expected_status_code=401, expected_message="User must be authenticated"):
        account_helper.dm_account_api.account_api.get_v1_account(validate_response=False)


def test_get_v1_account_auth(
        auth_account_helper
):
    with check_status_code_http(expected_status_code=200):
        account_helper = auth_account_helper.account_helper
        response = account_helper.dm_account_api.account_api.get_v1_account()
        user_details = UserDetailsEnvelope(**response.json())
        GetV1Account.check_response_values(user_details)
