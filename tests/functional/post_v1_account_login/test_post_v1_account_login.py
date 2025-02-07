import allure

from checkers.http_checkers import check_status_code_http


@allure.parent_suite("Login API")
@allure.suite("POST /v1/account/login")
class TestPostV1AccountLogin:

    @allure.sub_suite("Positive check")
    @allure.description("Authenticate via credentials")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_post_v1_account_login(
            self,
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
