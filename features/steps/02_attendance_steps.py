import requests
from behave import when, then, given


@when("I manual check-in")
def step_manual_check_in(context):
    context.response = requests.post(
        f"{context.base_url}/api/v1/users/{context.user_uuid}/attendance/check-in",
        headers=context.headers,
    )


@when("I manual check-out")
def step_manual_check_out(context):
    context.response = requests.post(
        f"{context.base_url}/api/v1/users/{context.user_uuid}/attendance/check-out",
        headers=context.headers,
    )


@given("I have checked in manually")
def step_given_checked_in(context):
    requests.post(
        f"{context.base_url}/api/v1/users/{context.user_uuid}/attendance/check-in",
        headers=context.headers,
    )


@when("I send geo attendance with latitude {latitude:f} and longitude {longitude:f}")
def step_geo_attendance(context, latitude, longitude):
    context.response = requests.post(
        f"{context.base_url}/api/v1/users/{context.user_uuid}/attendance/geo",
        json={"latitude": latitude, "longitude": longitude},
        headers=context.headers,
    )


@given("I have geo checked in")
def step_given_geo_checked_in(context):
    requests.post(
        f"{context.base_url}/api/v1/users/{context.user_uuid}/attendance/geo",
        json={"latitude": 35.123444, "longitude": 51.123444},
        headers=context.headers,
    )


@when("I get my attendance list")
def step_get_attendance(context):
    context.response = requests.get(
        f"{context.base_url}/api/v1/users/{context.user_uuid}/attendance",
        headers=context.headers,
    )


@when('I get my attendance list with date_from "{date_from}" and date_to "{date_to}"')
def step_get_attendance_filtered(context, date_from, date_to):
    context.response = requests.get(
        f"{context.base_url}/api/v1/users/{context.user_uuid}/attendance",
        params={"date_from": date_from, "date_to": date_to},
        headers=context.headers,
    )
