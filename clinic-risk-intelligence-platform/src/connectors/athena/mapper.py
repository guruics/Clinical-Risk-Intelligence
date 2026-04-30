import time

class AthenaEventMapper:

    @staticmethod
    def from_patients(patients: list):
        events = []

        for p in patients:
            event = {
                "event_id": f"athena-patient-{p.get('patientid')}-{time.time()}",
                "event_type": "PATIENT_ACCESS",
                "source": "ATHENA",
                "timestamp": time.time(),

                # Core fields for rule engine
                "patient_id": p.get("patientid"),
                "patient_name": f"{p.get('firstname', '')} {p.get('lastname', '')}".strip(),

                # Risk-relevant attributes
                "has_ssn": "ssn" in p and p.get("ssn") not in [None, "", "*****"],
                "has_address": "address1" in p,
                "has_phone": "mobilephone" in p or "homephone" in p,

                # Raw payload (optional, useful later)
                "raw": p
            }

            events.append(event)

        return events