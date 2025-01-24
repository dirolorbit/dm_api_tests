import datetime

from helpers.account_helper import AccountHelper
from restclient.configuration import Configuration as DmApiConfiguration
from services.dm_api_account import DMApiAccount


def test_post_v1_account():
    # Facade class for API Client and Proxy Classes
    dm_api_configuration = DmApiConfiguration(host="http://5.63.153.31:5051", disable_log=False)
    account = DMApiAccount(configuration=dm_api_configuration)

    account_helper = AccountHelper(dm_account_api=account)

    # User data, dt_now some unique value for test purposes
    dt_now = datetime.datetime.now().microsecond
    login = f"guest_{dt_now}"
    password = f"password_{dt_now}"
    email = f"{login}@gmail.com"

    # Register user
    account_helper.register_new_user(login=login, password=password, email=email)
