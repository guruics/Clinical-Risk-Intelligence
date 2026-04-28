import requests
from src.connectors.athena.auth import AthenaAuth
from src.connectors.athena.config import ATHENA_BASE_URL, practice_id


REQUIRED_FIELDS = ["patientid", "firstname", "lastname"]


def validate_patient_schema(patient: dict):
    missing = [f for f in REQUIRED_FIELDS if f not in patient]

    if missing:
        return {
            "valid": False,
            "missing_fields": missing,
            "patient_id": patient.get("patientid")
        }

    return {"valid": True, "patient_id": patient["patientid"]}


def test_athena_patient_search():
    auth = AthenaAuth()
    token = auth.get_token()

    url = f"{ATHENA_BASE_URL}/v1/{practice_id}/patients/search"

    headers = {
        "Authorization": f"Bearer {token}",
        "accept": "application/json"
    }

    params = {
        "searchterm": "smith"
    }

    response = requests.get(url, headers=headers, params=params)

    print("STATUS:", response.status_code)

    if not response.ok:
        print("ERROR:", response.text)
        return

    data = response.json()
    patients = data.get("patients", [])

    print(f"TOTAL PATIENTS FOUND: {len(patients)}")

    validation_results = []

    for p in patients:
        result = validate_patient_schema(p)
        validation_results.append(result)

    # Summary report
    invalid = [r for r in validation_results if not r["valid"]]

    print("\n--- VALIDATION SUMMARY ---")
    print("Valid records:", len(patients) - len(invalid))
    print("Invalid records:", len(invalid))

    if invalid:
        print("\nINVALID RECORDS DETAIL:")
        for i in invalid:
            print(i)


if __name__ == "__main__":
    test_athena_patient_search()
    