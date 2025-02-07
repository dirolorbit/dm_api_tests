from checkers.http_checkers import check_status_code_http


def test_put_v1_account_email(
        account_helper,
        prepare_user
):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    new_email = f"{login}_new@gmail.com"

    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.activate_user(login=login, email=email)

    # Successful User login with initial data
    account_helper.user_login(login=login, password=password)

    account_helper.update_user_email(login=login, email=new_email, password=password)

    # User login, attempt is failed until new email confirmation
    with check_status_code_http(
            expected_status_code=403,
            expected_message="User is inactive. Address the technical support for more details"
    ):
        account_helper.user_login(login=login, password=password, validate_response=False)

    account_helper.activate_user(login=login, email=new_email)

    # User login, attempt is successful after new email confirmation
    account_helper.user_login(login=login, password=password)
