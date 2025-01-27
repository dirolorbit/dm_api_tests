def test_get_v1_account_non_auth(
        account_helper
):
    response = account_helper.dm_account_api.account_api.get_v1_account()
    assert response.status_code == 401, "User should not be be authenticated"


def test_get_v1_account_auth(
        auth_account_helper
):
    account_helper = auth_account_helper.account_helper
    user = auth_account_helper.auth_user
    response = account_helper.dm_account_api.account_api.get_v1_account()
    assert response.status_code == 200, f"User {user.login} should be authenticated"
