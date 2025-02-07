import allure
import pytest
from hamcrest import (
    has_entries,
    assert_that,
)

from checkers.http_checkers import check_status_code_http


@allure.parent_suite("Account API")
@allure.suite("POST /v1/account")
class TestPostV1Account:

    @allure.sub_suite("Positive check")
    @allure.description("Register new user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_post_v1_account(
            self,
            account_helper,
            prepare_user
    ):
        login = prepare_user.login
        password = prepare_user.password
        email = prepare_user.email

        with check_status_code_http(expected_status_code=201):
            account_helper.register_new_user(login=login, password=password, email=email)

    @allure.sub_suite("Negative check")
    @allure.description("Validate input parameters during user registration")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.parametrize(
        "login, email, password, validation_error",
        [
            pytest.param(
                "guest1",
                "guest1@yahoo.com", "123",
                {
                    "Password": ["Short"]
                },
                id="Short password"
            ),

            pytest.param(
                "1",
                "guest1@yahoo.com",
                "password_guest1",
                {
                    "Login": ["Short"]
                },
                id="Short login"
            ),
            pytest.param(
                "guest1",
                "guest1#yahoo.com",
                "password_guest1",
                {
                    "Email": ["Invalid"]
                },
                id="Invalid email"
            ),
        ]
    )
    def test_post_v1_account_negative(
            self,
            account_helper,
            login,
            email,
            password,
            validation_error
    ):
        with check_status_code_http(expected_status_code=400, expected_message="Validation failed"):
            response = account_helper.register_new_user(login=login, password=password, email=email)
            assert_that(response, has_entries("errors", has_entries(validation_error)))
