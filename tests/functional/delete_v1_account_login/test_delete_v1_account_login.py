import allure


@allure.parent_suite("Login API")
@allure.suite("DELETE /v1/account/login")
class TestDeleteV1AccountLogin:

    @allure.sub_suite("Positive check")
    @allure.description("Logout as current user")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_delete_v1_account_login(
            self,
            auth_account_helper
    ):
        auth_account_helper.account_helper.user_logout()
