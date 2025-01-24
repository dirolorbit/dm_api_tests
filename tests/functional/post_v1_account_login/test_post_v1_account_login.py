import datetime

from helpers.account_helper import AccountHelper
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

    account_helper = AccountHelper(dm_account_api=account, mailhog=mailhog)

    # User data, dt_now some unique value for test purposes
    dt_now = datetime.datetime.now().microsecond
    login = f"guest_{dt_now}"
    password = f"password_{dt_now}"
    email = f"{login}@gmail.com"

    # Register user
    account_helper.register_new_user(login=login, password=password, email=email)

    # Activate user
    account_helper.activate_user(login=login, email=email, new_user=True)

    # Successful User login
    account_helper.user_successful_login(login=login, password=password)
