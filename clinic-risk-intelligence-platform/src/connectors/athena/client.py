import requests
from src.connectors.athena.config import ATHENA_BASE_URL, practice_id
from src.connectors.athena.auth import AthenaAuth


class AthenaConfig:
    def __init__(self):
        self.base_url = ATHENA_BASE_URL
        self.practice_id = practice_id


class AthenaClient:

    def __init__(self, token=None):
        self.token = token
        self.config = AthenaConfig()
        self.auth = AthenaAuth()

    def _headers(self):
        return {
            "Authorization": f"Bearer {self.auth.get_token()}",
            "Content-Type": "application/json"
        }

    def get_patients(self, searchterm: str = "SMITH", limit: int = 50):
        """
        Returns CLEAN list[dict], NOT raw response
        """

        pid = self.config.practice_id

        url = f"{self.config.base_url}/v1/{pid}/patients/search"

        response = requests.get(
            url,
            headers=self._headers(),
             params={
            "searchterm": searchterm   # ✅ REQUIRED BY ATHENA
        }
        )

        response.raise_for_status()

        data = response.json()

        # 🔴 CRITICAL FIX: return ONLY list
        return data.get("patients", [])