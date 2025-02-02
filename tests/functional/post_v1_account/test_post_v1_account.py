import string
from random import random

import pytest
from hamcrest import (
    has_entries,
    assert_that,
)

from checkers.http_checkers import check_status_code_http


def test_post_v1_account(
        account_helper,
        prepare_user
):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    with check_status_code_http(expected_status_code=201):
        account_helper.register_new_user(login=login, password=password, email=email)


@pytest.mark.parametrize(
    "login, email, password, validation_error",
    [
        # Short password
        ("guest1", "guest1@yahoo.com", "123", {
            "Password": ["Short"]
        }),
        # Short login
        ("1", "guest1@yahoo.com", "password_guest1", {
            "Login": ["Short"]
        }),
        # Invalid email
        ("guest1", "guest1#yahoo.com", "password_guest1", {
            "Email": ["Invalid"]
        }),
    ]
)
def test_post_v1_account_negative(
        account_helper,
        login,
        email,
        password,
        validation_error
):
    with check_status_code_http(expected_status_code=400, expected_message="Validation failed"):
        response = account_helper.register_new_user(login=login, password=password, email=email)
        assert_that(response, has_entries("errors", has_entries(validation_error)))
