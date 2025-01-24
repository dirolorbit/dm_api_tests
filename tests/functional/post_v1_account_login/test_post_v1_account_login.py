from json import loads

import datetime

from restclient.configuration import Configuration as DmApiConfiguration
from restclient.configuration import Configuration as MailhogApiConfiguration
from services.api_mailhog import MailHogApi
from services.dm_api_account import DMApiAccount


def test_post_v1_account_login():
    # Facade class for API Client and Proxy Classes
    dm_api_configuration = DmApiConfiguration(host="http://5.63.153.31:5051", disable_log=False)
    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog_api_configuration = MailhogApiConfiguration(host="http://5.63.153.31:5025")
    mailhog = MailHogApi(configuration=mailhog_api_configuration)

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
    response = account.account_api.post_v1_account(json_data=json_data)
    assert response.status_code == 201, f"User is not created: {response.json()}"

    # Retrieve users emails
    response = mailhog.mailhog_api.get_v2_messages(limit=50)
    assert response.status_code == 200, f"Mails are not received: {response.json()}"

    # Retrieve activation token
    token = get_activation_token_by_login(login, response)
    assert token is not None, f"Activation token for user {login} is not generated"

    # Activate token
    response = account.account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, f"Token is not activated: {response.json()}"

    # User login
    response = account.login_api.post_v1_account_login(json_data=json_data)
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
