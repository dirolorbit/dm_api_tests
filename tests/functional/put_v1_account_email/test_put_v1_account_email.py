import datetime

from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as DmApiConfiguration
from restclient.configuration import Configuration as MailhogApiConfiguration
from services.api_mailhog import MailHogApi
from services.dm_api_account import DMApiAccount


def test_put_v1_account_email():
    # Facade class for API Client and Proxy Classes
    dm_api_configuration = DmApiConfiguration(host="http://5.63.153.31:5051", disable_log=False)
    account = DMApiAccount(configuration=dm_api_configuration)
    mailhog_api_configuration = MailhogApiConfiguration(host="http://5.63.153.31:5025")
    mailhog = MailHogApi(configuration=mailhog_api_configuration)

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    # User data, dt_now some unique value for test purposes
    dt_now = datetime.datetime.now().microsecond
    login = f"guest_{dt_now}"
    password = f"password_{dt_now}"
    email = f"{login}@gmail.com"
    new_email = f"{login}_new@gmail.com"

    # Register user
    account_helper.register_new_user(login=login, password=password, email=email)

    # Activate user
    account_helper.activate_user(login=login, email=email, new_user=True)

    # Successful User login
    response = account_helper.user_login(login=login, password=password)
    assert response.status_code == 200, f"User is not logged in: {response.json()}"

    # Change user email
    account_helper.update_user_email(login=login, email=new_email, password=password)

    # User login, attempt is failed
    response = account_helper.user_login(login=login, password=password)
    assert response.status_code == 403, (f"User {login} should be inactive and login should be forbidden "
                                         f"until confirmation of email change")

    # Activate user
    account_helper.activate_user(login=login, email=new_email, new_user=False)

    # User login, attempt is successful
    response = account_helper.user_login(login=login, password=password)
    assert response.status_code == 200, f"User is not logged in: {response.json()}"
