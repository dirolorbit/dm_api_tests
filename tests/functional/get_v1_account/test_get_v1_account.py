from datetime import datetime

from hamcrest import (
    assert_that,
    equal_to,
    all_of,
    starts_with,
    has_property,
    instance_of,
    has_properties,
    has_items,
    is_in,
)

from checkers.http_checkers import check_status_code_http
from dm_api_account.models.user_details_envelope import (
    UserDetailsEnvelope
)


def test_get_v1_account_non_auth(
        account_helper
):
    with check_status_code_http(expected_status_code=401, expected_message="User must be authenticated"):
        account_helper.dm_account_api.account_api.get_v1_account(validate_response=False)


def test_get_v1_account_auth(
        auth_account_helper
):
    with check_status_code_http(expected_status_code=200):
        account_helper = auth_account_helper.account_helper
        response = account_helper.dm_account_api.account_api.get_v1_account()
        user_details = UserDetailsEnvelope(**response.json())
        assert_that(
            user_details, all_of(
                has_property("resource", has_property("login", starts_with("guest"))),
                has_property("resource", has_property("online", instance_of(datetime))),
                has_property("resource", has_property("registration", instance_of(datetime))),
                has_property(
                    "resource", has_property(
                        "rating",
                        has_properties(
                            {
                                "enabled": equal_to(True),
                                "quality": equal_to(0),
                                "quantity": equal_to(0)
                            }
                        )
                    )
                ),
                has_property("resource", has_property("roles", has_items("Guest", "Player"))),
                has_property(
                    "resource", has_property(
                        "settings",
                        has_property("colorSchema", is_in(["Modern", "Pale", "Classic", "ClassicPale", "Night"]))
                    )
                ),
                has_property(
                    "resource", has_property(
                        "settings",
                        has_property(
                            "paging",
                            has_properties(
                                {
                                    "posts_per_page": equal_to(10),
                                    "comments_per_page": equal_to(10),
                                    "topics_per_page": equal_to(10),
                                    "messages_per_page": equal_to(10),
                                    "entities_per_page": equal_to(10)
                                }
                            )
                        )
                    )
                )
            )
        )
