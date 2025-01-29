def test_post_v1_account_login(
        account_helper,
        prepare_user
):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.activate_user(login=login, email=email)
    # Successful User login
    response = account_helper.user_login(login=login, password=password)
    assert response.status_code == 200, f"User is not logged in: {response.json()}"
