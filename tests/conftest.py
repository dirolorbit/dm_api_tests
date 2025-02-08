import datetime
import os
from collections import namedtuple
from pathlib import Path

import pytest
import structlog
from swagger_coverage_py.reporter import CoverageReporter
from vyper import v

from helpers.account_helper import AccountHelper
from packages.notifier.bot import send_file
from packages.restclient.configuration import Configuration as DmApiConfiguration
from packages.restclient.configuration import Configuration as MailhogApiConfiguration
from services.api_mailhog import MailHogApi
from services.dm_api_account import DMApiAccount

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            sort_keys=True
        )
    ]
)

options = (
    'service.dm_api_account',
    'service.mailhog',
    'telegram.chat_id',
    'telegram.token'
)


@pytest.fixture(scope="session", autouse=True)
def setup_swagger_coverage():
    reporter = CoverageReporter(api_name="dm-api-account", host=v.get("service.dm_api_account"))
    reporter.setup("/swagger/Account/swagger.json")
    yield
    reporter.generate_report()
    reporter.cleanup_input_files()
    send_file()


@pytest.fixture(scope="session", autouse=True)
def set_config(
        request
):
    config = Path(__file__).joinpath("../../").joinpath("config")
    config_name = request.config.getoption("--env")
    v.set_config_name(config_name)
    v.add_config_path(config)
    v.read_in_config()
    for option in options:
        v.set(f"{option}", request.config.getoption(f"--{option}"))
    os.environ["TELEGRAM_BOT_CHAT_ID"] = v.get("telegram.chat_id")
    os.environ["TELEGRAM_BOT_ACCESS_TOKEN"] = v.get("telegram.token")
    request.config.stash["telegram-notifier-addfields"]["environment"] = config_name
    request.config.stash["telegram-notifier-addfields"]["report"] = "https://dirolorbit.github.io/dm_api_tests/"


def pytest_addoption(
        parser
):
    parser.addoption("--env", action="store", default="stg", help="run stg")
    for option in options:
        parser.addoption(f"--{option}", action="store", default=None)


@pytest.fixture(scope='session')
def mailhog_api():
    mailhog_api_configuration = MailhogApiConfiguration(host=v.get("service.mailhog"))
    mailhog_client = MailHogApi(configuration=mailhog_api_configuration)
    return mailhog_client


@pytest.fixture(scope='session')
def account_api():
    dm_api_configuration = DmApiConfiguration(host=v.get("service.dm_api_account"), disable_log=False)
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
    dm_api_configuration = DmApiConfiguration(host=v.get("service.dm_api_account"), disable_log=False)
    account_client = DMApiAccount(configuration=dm_api_configuration)
    account_helper = AccountHelper(dm_account_api=account_client, mailhog=mailhog_api)

    # User data
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.activate_user(login=login, email=email)

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
