import time

class AthenaEventMapper:

    print("I  am in Mapper.AthenaEventMapper _ 0")

    @staticmethod
    def from_patients(patients: list):
        events = []

        for p in patients:
            print("I  am in Mapper.AthenaEventMapper _ 1"),
            event = {
                
                "event_id": f"athena-patient-{p.get('patientid')}-{time.time()}",
                "event_type": "ACCESS",
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