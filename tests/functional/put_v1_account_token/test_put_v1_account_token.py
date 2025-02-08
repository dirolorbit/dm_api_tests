import allure

from checkers.http_checkers import check_status_code_http

@allure.parent_suite("Account API")
@allure.suite("PUT /v1/account/{token}")
class TestPutV1AccountToken:

    @allure.sub_suite("Positive check")
    @allure.description("Activate registered user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_put_v1_account_token(
            self,
            account_helper,
            prepare_user
    ):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        account_helper.register_new_user(login=login, password=password, email=email)

        with check_status_code_http(expected_status_code=200):
            account_helper.activate_user(login=login, email=email)
