from contextlib import contextmanager

import requests
from requests.exceptions import HTTPError

SUCCESS_CODES = [requests.codes.OK, requests.codes.CREATED, requests.codes.NO_CONTENT]


@contextmanager
def check_status_code_http(
        expected_status_code: requests.codes = requests.codes.OK,
        expected_message: str = ""
):
    try:
        yield
        if expected_status_code not in SUCCESS_CODES:
            raise AssertionError(f"Expected status code should be equal {expected_status_code}")
        if expected_message:
            raise AssertionError(f"Expected message should be equal {expected_message}, but request is successful")
    except HTTPError as err:
        assert err.response.status_code == expected_status_code
        assert err.response.json()["title"] == expected_message
