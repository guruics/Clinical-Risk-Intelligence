# Clinical Risk Intelligence Platform
## Risk Taxonomy (Foundational Document)

---

## 1. Purpose

The Risk Taxonomy defines the foundational classification system used by the Clinical Risk Intelligence platform to identify, categorize, evaluate, and explain risk across healthcare systems.

This taxonomy provides:
- A common language for risk
- A structured model for rule evaluation
- A consistent scoring framework
- Explainability for stakeholders (clinical, compliance, executive)

This document will evolve to include:
- Case studies
- Compliance mappings (HIPAA, HITRUST, etc.)
- Industry benchmarks

---

## 2. Core Concepts

### 2.1 Event
A raw activity generated from a source system such as Athenahealth, EHRs, or billing platforms.

Examples:
- Patient record access
- Patient search
- Record modification
- Data export

Attributes:
- event_id
- event_type
- timestamp
- user_id
- resource_id
- metadata

---

### 2.2 Unified Event
A normalized representation of events across systems.

Purpose:
- Enable cross-platform analysis
- Support consistent rule evaluation

Examples:
- PATIENT_ACCESS
- RECORD_UPDATE
- DATA_EXPORT

---

### 2.3 Finding
A Finding is generated when a rule is triggered on a Unified Event.

Structure:
- rule_name
- category
- severity
- event_id

Findings are the atomic units of risk.

---

## 3. Risk Categories

### 3.1 PHI_ACCESS
Unauthorized or suspicious access to Protected Health Information.

Examples:
- Access without proper authorization
- High-frequency patient lookups
- Access outside assigned patient panel

---

### 3.2 DATA_EXFILTRATION
Potential extraction or leakage of sensitive data.

Examples:
- Bulk exports
- Repeated downloads
- API scraping patterns

---

### 3.3 COMPLIANCE_VIOLATION
Violations of regulatory or organizational policies.

Examples:
- Missing audit logs
- Access outside permitted hours
- Improper role usage

---

### 3.4 ANOMALOUS_BEHAVIOR
Behavior that deviates from established patterns.

Examples:
- Sudden spike in activity
- Access across multiple locations
- Unusual workflow sequences

---

## 4. Severity Levels

Severity defines the impact level of a finding.

| Severity | Description |
|----------|------------|
| LOW | Informational or low risk |
| MODERATE | Requires review |
| HIGH | Likely policy violation |
| CRITICAL | Immediate action required |

---

## 5. Risk Scoring Model

Risk Score is computed as the weighted sum of findings.

### 5.1 Weight Mapping

| Severity | Weight |
|----------|--------|
| LOW | 10 |
| MODERATE | 20 |
| HIGH | 40 |
| CRITICAL | 80 |

### 5.2 Risk Levels

| Score Range | Risk Level |
|-------------|-----------|
| 0–20 | LOW |
| 21–50 | MODERATE |
| 51–80 | HIGH |
| 81+ | CRITICAL |

---

## 6. Rule Framework

Rules evaluate Unified Events and generate Findings.

### Rule Components
- Rule Name
- Condition (logic)
- Category
- Severity

### Example Rule

IF event_type == PATIENT_ACCESS AND role == SYSTEM_API
THEN Unauthorized PHI Access (HIGH)

---

## 7. Top Drivers

Top Drivers are the highest contributing findings to the overall risk score.

Purpose:
- Explainability
- Prioritization
- Dashboard insights

Structure:
- rule
- category
- severity
- weighted_score
- event_id

---

## 8. Terminology Summary

| Term | Definition |
|------|-----------|
| Event | Raw system activity |
| Unified Event | Normalized event format |
| Rule | Logic applied to events |
| Finding | Rule-triggered risk indicator |
| Category | Type of risk |
| Severity | Impact level |
| Risk Score | Aggregated weighted score |
| Risk Level | Interpreted risk band |
| Top Drivers | Key contributors to risk |

---

## 9. End-to-End Risk Flow

1. Connector fetches raw data
2. Mapper converts to Unified Events
3. Rules Engine evaluates events
4. Findings are generated
5. Scoring Engine calculates risk score
6. API exposes results
7. Dashboard visualizes insights

---

## 10. Future Enhancements

This taxonomy will be extended with:

### 10.1 Case Studies
- Insider misuse scenarios
- Data breach simulations
- Compliance audit cases

### 10.2 Compliance Mapping
- HIPAA Security Rule
- HIPAA Privacy Rule
- HITRUST controls
- SOC2 alignment

### 10.3 Advanced Risk Models
- Behavioral baselines
- Machine learning anomaly detection
- Predictive risk scoring

---

## 11. Versioning

Version: 1.0
Status: Foundational

This document will evolve as the platform matures.

