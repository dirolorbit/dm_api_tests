def test_put_v1_account_email(
        account_helper,
        prepare_user
):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    new_email = f"{login}_new@gmail.com"

    # Register user
    account_helper.register_new_user(login=login, password=password, email=email)

    # Activate user
    account_helper.activate_user(login=login, email=email, new_user=True)

    # Successful User login
    response = account_helper.user_login(login=login, password=password)
    assert response.status_code == 200, f"User is not logged in: {response.json()}"

    # Change user email
    account_helper.update_user_email(login=login, email=new_email, password=password)

    # User login, attempt is failed
    response = account_helper.user_login(login=login, password=password)
    assert response.status_code == 403, (f"User {login} should be inactive and login should be forbidden "
                                         f"until confirmation of email change")

    # Activate user
    account_helper.activate_user(login=login, email=new_email, new_user=False)

    # User login, attempt is successful
    response = account_helper.user_login(login=login, password=password)
    assert response.status_code == 200, f"User is not logged in: {response.json()}"
