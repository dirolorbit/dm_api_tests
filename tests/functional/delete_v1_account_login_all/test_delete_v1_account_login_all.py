from checkers.http_checkers import check_status_code_http


def test_delete_v1_account_login(
        auth_account_helper
):
    auth_account_helper.account_helper.user_logout_from_all_devices()
