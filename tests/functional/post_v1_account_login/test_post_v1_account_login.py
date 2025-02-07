from checkers.http_checkers import check_status_code_http


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
    with check_status_code_http(expected_status_code=200):
        account_helper.user_login(login=login, password=password)
