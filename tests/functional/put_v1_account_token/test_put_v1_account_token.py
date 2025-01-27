def test_put_v1_account_token(
        account_helper,
        prepare_user
):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    # Register user
    account_helper.register_new_user(login=login, password=password, email=email)

    # Activate user
    account_helper.activate_user(login=login, email=email, new_user=True)
