import requests
from behave import when, then, given
from features.environment import login, USER_USERNAME, USER_PASSWORD


@when("admin gets attendance list")
def step_admin_get_attendance(context):
    context.response = requests.get(
        f"{context.base_url}/api/v1/admin/attendance",
        headers=context.admin_headers,
    )


@when("admin gets attendance list filtered by user")
def step_admin_get_attendance_by_user(context):
    context.response = requests.get(
        f"{context.base_url}/api/v1/admin/attendance",
        params={"user_uuid": context.user_uuid},
        headers=context.admin_headers,
    )


@when('admin gets attendance list with date_from "{date_from}" and date_to "{date_to}"')
def step_admin_get_attendance_by_date(context, date_from, date_to):
    context.response = requests.get(
        f"{context.base_url}/api/v1/admin/attendance",
        params={"date_from": date_from, "date_to": date_to},
        headers=context.admin_headers,
    )


@given("there is an attendance record")
def step_given_attendance_record(context):
    # create 3 check-ins
    for _ in range(3):
        user_auth = login(USER_USERNAME, USER_PASSWORD)
        token = user_auth["access_token"]
        user_uuid = user_auth["user_uuid"]
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        requests.post(
            f"{context.base_url}/api/v1/users/{user_uuid}/attendance/check-in",
            headers=headers,
        )
        requests.post(
            f"{context.base_url}/api/v1/users/{user_uuid}/attendance/check-out",
            headers=headers,
        )

    resp = requests.get(
        f"{context.base_url}/api/v1/admin/attendance",
        headers=context.admin_headers,
    )
    records = resp.json().get("records", [])
    context.target_attendance_uuid = records[0]["attendance_uuid"]


@when("admin deletes the attendance record")
def step_admin_delete_attendance(context):
    context.response = requests.delete(
        f"{context.base_url}/api/v1/admin/attendance/{context.target_attendance_uuid}",
        headers=context.admin_headers,
    )


@given("admin has deleted an attendance record")
def step_given_admin_deleted(context):
    for _ in range(3):
        user_auth = login(USER_USERNAME, USER_PASSWORD)
        token = user_auth["access_token"]
        user_uuid = user_auth["user_uuid"]
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        requests.post(
            f"{context.base_url}/api/v1/users/{user_uuid}/attendance/check-in",
            headers=headers,
        )
        requests.post(
            f"{context.base_url}/api/v1/users/{user_uuid}/attendance/check-out",
            headers=headers,
        )

    resp = requests.get(
        f"{context.base_url}/api/v1/admin/attendance",
        headers=context.admin_headers,
    )
    records = resp.json().get("records", [])
    context.deleted_attendance_uuid = records[0]["attendance_uuid"]
    requests.delete(
        f"{context.base_url}/api/v1/admin/attendance/{context.deleted_attendance_uuid}",
        headers=context.admin_headers,
    )


@then("the deleted record should not be in the list")
def step_check_deleted_record(context):
    resp = requests.get(
        f"{context.base_url}/api/v1/admin/attendance",
        headers=context.admin_headers,
    )
    records = resp.json().get("records", [])
    uuids = [r["attendance_uuid"] for r in records]
    assert context.deleted_attendance_uuid not in uuids


@when("I access admin attendance list without admin token")
def step_access_admin_without_token(context):
    context.response = requests.get(
        f"{context.base_url}/api/v1/admin/attendance",
        headers=context.headers,
    )
