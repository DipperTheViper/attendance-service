import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("TEST_URL", "http://localhost:8100")
USER_USERNAME = os.getenv("TEST_USER_USERNAME", "testuser")
USER_PASSWORD = os.getenv("TEST_USER_PASSWORD", "Test@1234")
ADMIN_USERNAME = os.getenv("TEST_ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("TEST_ADMIN_PASSWORD", "Admin@1234")


def login(username: str, password: str) -> dict:
    resp = requests.post(
        f"{BASE_URL}/api/v1/auth/login",
        json={"username": username, "password": password},
        headers={"Content-Type": "application/json"},
    )
    resp.raise_for_status()
    data = resp.json()
    return {
        "access_token": data["access_token"],
        "user_uuid": str(data["user_uuid"]),
    }


def before_all(context):
    context.base_url = BASE_URL

    user_auth = login(USER_USERNAME, USER_PASSWORD)
    context.access_token = user_auth["access_token"]
    context.user_uuid = user_auth["user_uuid"]
    context.headers = {
        "Authorization": f"Bearer {context.access_token}",
        "Content-Type": "application/json",
    }

    admin_auth = login(ADMIN_USERNAME, ADMIN_PASSWORD)
    context.admin_access_token = admin_auth["access_token"]
    context.admin_uuid = admin_auth["user_uuid"]
    context.admin_headers = {
        "Authorization": f"Bearer {context.admin_access_token}",
        "Content-Type": "application/json",
    }


def before_scenario(context, scenario):
    user_auth = login(USER_USERNAME, USER_PASSWORD)
    context.access_token = user_auth["access_token"]
    context.user_uuid = user_auth["user_uuid"]
    context.headers = {
        "Authorization": f"Bearer {context.access_token}",
        "Content-Type": "application/json",
    }
