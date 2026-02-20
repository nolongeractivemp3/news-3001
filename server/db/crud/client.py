import os

import pocketbase


def create_authenticated_client(url: str):
    client = pocketbase.Client(url)
    admin_email = os.getenv("POCKETBASE_ADMIN_EMAIL")
    admin_password = os.getenv("POCKETBASE_ADMIN_PASSWORD")
    if not admin_email or not admin_password:
        raise RuntimeError(
            "Missing POCKETBASE_ADMIN_EMAIL or POCKETBASE_ADMIN_PASSWORD environment variables."
        )
    client.admins.auth_with_password(admin_email, admin_password)
    return client
