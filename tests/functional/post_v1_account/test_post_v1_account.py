import datetime

from dm_api_account.apis.account_api import AccountApi


def test_post_v1_account():
    # API Client Classes
    account_api = AccountApi(host="http://5.63.153.31:5051")

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
