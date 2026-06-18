import requests
from behave import when, then, given


@when('I login with username "{username}" and password "{password}"')
def step_login(context, username, password):
    context.response = requests.post(
        f"{context.base_url}/api/v1/auth/login",
        json={"username": username, "password": password},
        headers={"Content-Type": "application/json"},
    )


@when("I get my profile without token")
def step_get_profile_no_token(context):
    context.response = requests.get(
        f"{context.base_url}/api/v1/users/{context.user_uuid}",
    )


@when("I get my profile")
def step_get_profile(context):
    context.response = requests.get(
        f"{context.base_url}/api/v1/users/{context.user_uuid}",
        headers=context.headers,
    )


@when("I logout")
def step_logout(context):
    context.response = requests.post(
        f"{context.base_url}/api/v1/auth/logout",
        json={"access_token": context.access_token},
        headers=context.headers,
    )


@given("I have logged out")
def step_given_logged_out(context):
    requests.post(
        f"{context.base_url}/api/v1/auth/logout",
        json={"access_token": context.access_token},
        headers=context.headers,
    )


@then("the response status should be {status_code:d}")
def step_check_status(context, status_code):
    assert (
        context.response.status_code == status_code
    ), f"Expected {status_code}, got {context.response.status_code}: {context.response.text}"


@then('the response should contain "{key}"')
def step_check_response_contains(context, key):
    data = context.response.json()
    assert key in data, f"Expected '{key}' in response, got: {data}"
