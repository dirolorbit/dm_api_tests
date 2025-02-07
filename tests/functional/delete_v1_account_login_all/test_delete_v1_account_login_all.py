import allure


@allure.parent_suite("Login API")
@allure.suite("DELETE /v1/account/login/all")
class TestDeleteV1AccountLoginAll:

    @allure.sub_suite("Positive check")
    @allure.description("Logout from every device")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_v1_account_login_all(
            self,
            auth_account_helper
    ):
        auth_account_helper.account_helper.user_logout_from_all_devices()
