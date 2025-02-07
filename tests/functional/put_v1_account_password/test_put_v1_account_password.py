import allure


@allure.parent_suite("Account API")
@allure.suite("PUT /v1/account/password")
class TestPutV1AccountPassword:

    @allure.sub_suite("Positive check")
    @allure.description("Change registered user password")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_put_v1_account_password(
            self,
            auth_account_helper
    ):
        login = auth_account_helper.auth_user.login
        email = auth_account_helper.auth_user.email
        old_password = auth_account_helper.auth_user.password
        new_password = f"{old_password}#new"

        auth_account_helper.account_helper.change_user_password(
            login=login,
            email=email,
            old_password=old_password,
            new_password=new_password
        )
        # Successful login after password change
        auth_account_helper.account_helper.user_login(login=login, password=new_password)
