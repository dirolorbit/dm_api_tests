from datetime import datetime

from hamcrest import (
    assert_that,
    all_of,
    has_property,
    starts_with,
    instance_of,
    has_properties,
    equal_to,
    has_items,
    is_in,
)


class GetV1Account:
    @classmethod
    def check_response_values(
            cls,
            response
    ):
        assert_that(
            response, all_of(
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
