def test_put_v1_account_helper(
        auth_account_helper
):
    login = auth_account_helper.auth_user.login
    email = auth_account_helper.auth_user.email
    old_password = auth_account_helper.auth_user.password
    new_password = f"{old_password}#new"

    auth_account_helper.account_helper.change_user_password(
        login=login, email=email,
        old_password=old_password, new_password=new_password
    )
    response = auth_account_helper.account_helper.user_login(login=login, password=new_password)
    assert response.status_code == 200, f"User is not logged in: {response.json()}"
