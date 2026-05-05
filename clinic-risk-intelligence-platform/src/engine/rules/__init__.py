from src.engine.rules.Patient.access_rules import SystemBulkAccessRule
from src.engine.rules.Patient.access_rules import UnauthorizedPHIAccessRule
from src.engine.rules.Patient.access_rules import UnauthorizedRoleAccessRule
from src.engine.rules.Patient.access_rules import AfterHoursAccessRule
from src.engine.rules.Patient.access_rules import RepeatedLastNameAccessRule
from src.engine.rules.Patient.access_rules import NoEncounterAccessRule
from src.engine.rules.Patient.anamoly_rules import ExcessivePatientSearchRule
from src.engine.rules.Patient.anamoly_rules import BulkPatientEnumerationRule
from src.engine.rules.Patient.anamoly_rules import CrossPatientRapidAccessRule
from src.engine.rules.Patient.clinical_context_rules import MissingEncounterContextRule


ALL_RULE_CLASSES = [
    SystemBulkAccessRule,
    UnauthorizedPHIAccessRule,
    UnauthorizedRoleAccessRule,
    BulkPatientEnumerationRule,
    AfterHoursAccessRule,
    NoEncounterAccessRule,
    ExcessivePatientSearchRule,
    RepeatedLastNameAccessRule,
    CrossPatientRapidAccessRule,
    MissingEncounterContextRule
]

