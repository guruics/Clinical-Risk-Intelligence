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

    # --- Patient APIs ---
    def get_patient_demographics(self, patient_id: str):
        """Fetch patient demographic details."""
        pass

    def get_patient_chart(self, patient_id: str):
        """Fetch patient chart information."""
        pass

    def get_patient_insurance(self, patient_id: str):
        """Fetch patient insurance details."""
        pass

    def get_patient_documents(self, patient_id: str):
        """Fetch documents for a patient."""
        pass

    # --- Encounter APIs ---
    def get_encounter_details(self, encounter_id: str):
        """Fetch details for a specific encounter."""
        pass

    def get_encounter_diagnoses(self, encounter_id: str):
        """Fetch diagnoses for a specific encounter."""
        pass

    def get_encounter_orders(self, encounter_id: str):
        """Fetch orders for a specific encounter."""
        pass

    def get_encounter_procedures(self, encounter_id: str):
        """Fetch procedures for a specific encounter."""
        pass

    # --- Provider APIs ---
    def get_providers(self):
        """Fetch provider directory."""
        pass

    # --- Appointment/Scheduling APIs ---
    def get_appointment_details(self, appointment_id: str):
        """Fetch details for a specific appointment."""
        pass

    def get_appointment_history(self, patient_id: str):
        """Fetch appointment history for a patient."""
        pass

    # --- Billing APIs ---
    def get_claims(self, patient_id: str):
        """Fetch claims for a patient."""
        pass

    def get_payments(self, patient_id: str):
        """Fetch payment history for a patient."""
        pass

    def get_charges(self, patient_id: str):
        """Fetch charges for a patient."""
        pass

    # --- Audit & Security APIs ---
    def get_audit_logs(self, start_date: str, end_date: str):
        """Fetch audit logs for a date range."""
        pass

    def get_user_access_logs(self, user_id: str, start_date: str, end_date: str):
        """Fetch access logs for a user."""
        pass

    # --- Document APIs ---
    def get_clinical_documents(self, patient_id: str):
        """Fetch clinical documents for a patient."""
        pass

    def get_attachments(self, patient_id: str):
        """Fetch attachments for a patient."""
        pass