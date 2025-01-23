from json import loads

import datetime

from dm_api_account.apis.account_api import AccountApi
from dm_api_account.apis.login_api import LoginApi
from api_mailhog.apis.mailhog_api import MailhogApi

from restclient.configuration import Configuration as DmApiConfiguration
from restclient.configuration import Configuration as MailhogApiConfiguration


def test_put_v1_account_email():
    # API Client and Proxy Classes
    dm_api_configuration = DmApiConfiguration(host="http://5.63.153.31:5051", disable_log=False)
    account_api = AccountApi(configuration=dm_api_configuration)
    login_api = LoginApi(configuration=dm_api_configuration)
    mailhog_api_configuration = MailhogApiConfiguration(host="http://5.63.153.31:5025")
    mailhog_api = MailhogApi(mailhog_api_configuration)

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
    assert response.status_code == 201, f"User is not created: {response.json()}"

    # Retrieve users emails
    response = mailhog_api.get_v2_messages(limit=50)
    assert response.status_code == 200, f"Mails are not received: {response.json()}"

    # Retrieve activation token
    token = get_activation_token_by_login(login=login, response=response)
    assert token is not None, f"Activation token for user {login} is not generated"

    # Activate token
    response = account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, f"Token is not activated: {response.json()}"

    # User login
    response = login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 200, f"User is not logged in: {response.json()}"

    # Change user email
    new_email = f"{login}_new@gmail.com"

    json_data = {
        "login": login,
        "email": new_email,
        "password": password
    }

    response = account_api.put_v1_account_email(token=token, json_data=json_data)
    assert response.status_code == 200, f"Email for user {login} is not updated: {response.json()}"

    # User login, attempt is failed
    response = login_api.post_v1_account_login(json_data=json_data)
    assert response.status_code == 403, (f"User {login} should be inactive and login should be forbidden "
                                         f"until confirmation of email change")

    # Retrieve users emails
    response = mailhog_api.get_v2_messages(limit=50)
    assert response.status_code == 200, f"Mails are not received: {response.json()}"

    # Retrieve activation token to confirm email change
    new_token = get_activation_token_by_email_and_login(login=login, email=new_email, response=response)
    assert new_token is not None, f"Activation token for user {login} to confirm email change is not generated"

    # Activate new token
    response = account_api.put_v1_account_token(token=new_token)
    assert response.status_code == 200, f"Token is not activated: {response.json()}"

    # User login, attempt is successful
    response = login_api.post_v1_account_login(json_data=json_data)
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


def get_activation_token_by_email_and_login(
        login,
        email,
        response
):
    """
    Helper function to get activation token from the confirmation of the email change letter
    :param login:
    :param email:
    :param response:
    :return:
    """
    token = None
    for item in response.json()["items"]:
        if email in item["Content"]["Headers"]["To"]:
            user_data = loads(item["Content"]["Body"])
            user_login = user_data["Login"]
            if user_login == login:
                token = user_data["ConfirmationLinkUrl"].split('/')[-1]
    return token
