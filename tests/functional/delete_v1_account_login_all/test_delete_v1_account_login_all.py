def test_delete_v1_account_login(
        auth_account_helper
):
    response = auth_account_helper.account_helper.dm_account_api.login_api.delete_v1_account_login_all()
    assert response.status_code == 204, f"User should be authenticated"