import datetime
from collections import namedtuple

import pytest
import structlog

from helpers.account_helper import AccountHelper
from services.api_mailhog import MailHogApi
from services.dm_api_account import DMApiAccount
from restclient.configuration import Configuration as DmApiConfiguration
from restclient.configuration import Configuration as MailhogApiConfiguration

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            sort_keys=True
        )
    ]
)


@pytest.fixture(scope='session')
def mailhog_api():
    mailhog_api_configuration = MailhogApiConfiguration(host="http://5.63.153.31:5025")
    mailhog_client = MailHogApi(configuration=mailhog_api_configuration)
    return mailhog_client


@pytest.fixture(scope='session')
def account_api():
    dm_api_configuration = DmApiConfiguration(host="http://5.63.153.31:5051", disable_log=False)
    account_client = DMApiAccount(configuration=dm_api_configuration)
    return account_client


@pytest.fixture
def account_helper(
        account_api,
        mailhog_api
):
    account_helper = AccountHelper(dm_account_api=account_api, mailhog=mailhog_api)
    return account_helper


@pytest.fixture
def auth_account_helper(
        prepare_user,
        mailhog_api
):
    dm_api_configuration = DmApiConfiguration(host="http://5.63.153.31:5051", disable_log=False)
    account_client = DMApiAccount(configuration=dm_api_configuration)
    account_helper = AccountHelper(dm_account_api=account_client, mailhog=mailhog_api)

    # User data
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    # Register user
    account_helper.register_new_user(login=login, password=password, email=email)
    # Activate user
    account_helper.activate_user(login=login, email=email, new_user=True)

    account_helper.auth_client(
        login=login,
        password=password
    )
    AuthClient = namedtuple(typename="AuthClient", field_names=["account_helper", "auth_user"])
    auth_client = AuthClient(account_helper=account_helper, auth_user=prepare_user)
    return auth_client


@pytest.fixture
def prepare_user():
    dt_now = datetime.datetime.now().microsecond
    login = f"guest_{dt_now}"
    password = f"password_{dt_now}"
    email = f"{login}@gmail.com"
    User = namedtuple(typename="User", field_names=["login", "password", "email"])
    user = User(login=login, password=password, email=email)
    return user
