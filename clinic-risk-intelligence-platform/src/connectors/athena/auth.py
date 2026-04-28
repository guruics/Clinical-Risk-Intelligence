import requests
from datetime import datetime, timedelta

from src.connectors.athena.config import (
    CLIENT_ID,
    CLIENT_SECRET,
    TOKEN_URL
)


class AthenaAuth:

    def __init__(self):
        self.token = None
        self.expiry = None

    def get_token(self):

        if self.token and self.expiry and self.expiry > datetime.now():
            return self.token

        payload = {
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "scope": "athena/service/Athenanet.MDP.*"   # or sandbox-required scope
        }

        response = requests.post(TOKEN_URL, data=payload)

        if response.status_code != 200:
            raise Exception(f"Auth failed: {response.text}")

        data = response.json()

        self.token = data["access_token"]
        self.expiry = datetime.now() + timedelta(
            seconds=data.get("expires_in", 3600)
        )

        return self.token