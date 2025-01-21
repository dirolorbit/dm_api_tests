from json import loads

import datetime

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi


def test_post_v1_account_login():
    # API Client Classes
    account_api = AccountApi(host="http://5.63.153.31:5051")
    login_api = LoginApi(host="http://5.63.153.31:5051")
    mailhog_api = MailhogApi(host="http://5.63.153.31:5025")

    # User data, dt_now some unique value for test purposes
    dt_now = datetime.datetime.now().microsecond
    login = f"guest_{dt_now}"
    password = f"password_{dt_now}"
    email = f"{login}@gmail.com"

    json_data = {
        "login": login,
        "email": email,
        "password": password
    }

    # Register user
    response = account_api.post_v1_account(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 201, f"User is not created: {response.json()}"

    # Retrieve users emails
    response = mailhog_api.get_v2_messages(limit=50)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, f"Mails are not received: {response.json()}"

    # Retrieve activation token
    token = get_activation_token_by_login(login, response)
    assert token is not None, f"Activation token for user {login} is not generated"

    # Activate token
    response = account_api.put_v1_account_token(token=token)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, f"Token is not activated: {response.json()}"

    # User login
    response = login_api.post_v1_account_login(json_data=json_data)
    print(response.status_code)
    print(response.text)
    assert response.status_code == 200, f"User is not logged in: {response.json()}"


def get_activation_token_by_login(
        login,
        response
):
    """
    Helper function to get activation token from the welcome letter
    :param login:
    :param response:
    :return:
    """
    token = None
    for item in response.json()["items"]:
        user_data = loads(item["Content"]["Body"])
        user_login = user_data["Login"]
        if user_login == login:
            token = user_data["ConfirmationLinkUrl"].split('/')[-1]
    return token
