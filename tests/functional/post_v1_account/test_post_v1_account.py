import datetime

from dm_api_account.apis.account_api import AccountApi
import structlog
from restclient.configuration import Configuration as DmApiConfiguration

structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            sort_keys=True
        )
    ]
)


def test_post_v1_account():
    # API Client and Proxy Classes
    dm_api_configuration = DmApiConfiguration(host="http://5.63.153.31:5051", disable_log=False)
    account_api = AccountApi(configuration=dm_api_configuration)

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
