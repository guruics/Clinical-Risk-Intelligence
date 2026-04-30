# Clinical Risk Intelligence Platform

---

# 1. Executive Summary

## Overview
The Clinical Risk Intelligence Platform is designed to identify, analyze, and score risk events derived from healthcare systems such as Athenahealth. The system ingests raw operational data, normalizes it into a unified format, evaluates it using rule-based intelligence, and produces actionable risk insights via APIs and a dashboard UI.

## Key Capabilities
- Integration with external EHR systems (Athena)
- Event normalization into a unified schema
- Rule-based detection of compliance and security risks
- Quantitative risk scoring
- API-driven architecture
- Interactive dashboard visualization

## Business Value
- Improves detection of PHI access violations
- Enables proactive compliance monitoring
- Provides explainable risk scoring
- Serves as a foundation for AI-driven risk analytics

---

# 2. System Architecture Overview

## High-Level Flow

Connector → Mapper → Event Mapper → Rule Engine → Risk Scoring → API Layer → Frontend Dashboard

---

# 3. Developer Documentation

## 3.1 Connectors Layer

### Purpose
Responsible for integrating with external systems (e.g., Athena API).

### Components
- `AthenaClient`
- `AthenaAuth`
- `AthenaConfig`

### Responsibilities
- API authentication
- Data retrieval (patients, events)
- Handling API request/response

---

## 3.2 Mapper Layer (Connector Mapper)

### Purpose
Transforms raw API responses into structured intermediate formats.

### Example
- `connectors/athena/mapper.py`

### Role
- Lightweight transformation
- Keeps connector logic clean

---

## 3.3 Event Mapper (Normalization Layer)

### Purpose
Converts external system data into a unified internal event model.

### Example
- `normalization/athena_event_mapper.py`

### Output
- `UnifiedEvent`

### Responsibilities
- Standardize fields across systems
- Add metadata
- Normalize timestamps and identifiers

---

## 3.4 Rule Engine

### Purpose
Evaluates events against predefined rules.

### Responsibilities
- Detect suspicious or non-compliant behavior
- Generate findings

### Output
- List of findings

### Example Rule
- Unauthorized PHI Access

---

## 3.5 Risk Scoring Engine

### Purpose
Aggregates findings into a numerical risk score.

### Responsibilities
- Assign weights to severity levels
- Compute overall risk score
- Categorize risk levels (LOW, MODERATE, HIGH, CRITICAL)

### Output
```
{
  "risk_score": number,
  "risk_level": string,
  "breakdown": []
}
```

---

## 3.6 Pipeline Layer

### File
- `athena_pipeline.py`

### Responsibilities
- Orchestrates end-to-end flow:
  1. Fetch data
  2. Map to events
  3. Run rules
  4. Score risk

---

## 3.7 State Management

### File
- `risk_state.py`

### Purpose
- Maintain latest findings in memory

### Key Variable
- `LATEST_FINDINGS`

---

## 3.8 API Layer (FastAPI)

### Endpoints

#### GET `/risk/summary`
Returns computed risk summary

#### POST `/risk/run`
Triggers pipeline execution

#### POST `/risk/update`
Updates findings manually

### Responsibilities
- Serve risk data to frontend
- Trigger backend processing

---

## 3.9 Frontend (React Dashboard)

### Features
- Risk score visualization
- Risk breakdown charts
- Findings list
- Pipeline execution trigger

### Technologies
- React
- Vite
- Recharts

---

# 4. Data Flow Walkthrough

1. Athena API returns patient data
2. Connector retrieves data
3. Mapper structures response
4. Event Mapper creates UnifiedEvents
5. Rule Engine generates findings
6. Risk Scoring computes score
7. API exposes results
8. Frontend visualizes data

---

# 5. Current State of Implementation

## Completed
- Athena integration
- Event normalization
- Rule engine (basic rules)
- Risk scoring
- FastAPI backend
- React dashboard UI

## Known Gaps
- Limited rule coverage
- No persistence layer (in-memory only)
- No user-level attribution
- Minimal error handling

---

# 6. Future Enhancements

## Short Term
- Expand rule library
- Improve scoring model
- Add drill-down UI

## Medium Term
- Add database (PostgreSQL)
- Introduce user/entity tracking
- Role-based dashboards

## Long Term
- Machine learning-based anomaly detection
- Real-time streaming (WebSockets)
- Multi-system integration (Epic, Cerner)

---

# 7. Architecture Diagrams

## 7.1 High-Level Architecture

```
+-------------------+      +--------------------+      +---------------------+
|   External EHR    | ---> |     Connectors     | ---> |   Connector Mapper  |
| (Athena, others)  |      | (Auth + Client)    |      | (light transform)   |
+-------------------+      +--------------------+      +---------------------+
                                                                |
                                                                v
                                                     +-----------------------+
                                                     |   Event Mapper        |
                                                     | (Normalization Layer) |
                                                     | -> UnifiedEvent       |
                                                     +-----------------------+
                                                                |
                                                                v
                                                     +-----------------------+
                                                     |     Rule Engine       |
                                                     |  (detections)         |
                                                     |  -> Findings[]        |
                                                     +-----------------------+
                                                                |
                                                                v
                                                     +-----------------------+
                                                     |  Risk Scoring Engine  |
                                                     | -> score, level,      |
                                                     |    breakdown          |
                                                     +-----------------------+
                                                                |
                                                                v
                                                     +-----------------------+
                                                     |      API Layer        |
                                                     | (FastAPI endpoints)   |
                                                     +-----------------------+
                                                                |
                                                                v
                                                     +-----------------------+
                                                     |   Frontend Dashboard  |
                                                     | (React + Charts)      |
                                                     +-----------------------+
```

---

## 7.2 Detailed Data Flow (Sequence)

```
User/UI            API Layer            Pipeline            Connector          Athena API
   |                   |                    |                    |                    |
   | POST /risk/run    |                    |                    |                    |
   |------------------>|                    |                    |                    |
   |                   |  run_pipeline()    |                    |                    |
   |                   |------------------->|                    |                    |
   |                   |                    |  get_patients()    |                    |
   |                   |                    |------------------->|   HTTP GET         |
   |                   |                    |                    |------------------->|
   |                   |                    |                    |<-------------------|
   |                   |                    |<-------------------|   JSON response    |
   |                   |                    | map -> events      |                    |
   |                   |                    |------------------------------>          |
   |                   |                    | run rules -> findings[]                  |
   |                   |                    | score -> summary                         |
   |                   |<-------------------| result                                   |
   | 200 OK            |                    |                    |                    |
   |<------------------|                    |                    |                    |
   | GET /risk/summary |                    |                    |                    |
   |------------------>|  read LATEST_FINDINGS -> score -> JSON                       |
   |<------------------|                                                        
```

---

## 7.3 Module Interaction (Component View)

```
[ AthenaClient ] ---> [ Athena Mapper ] ---> [ AthenaEventMapper ] ---> [ UnifiedEvent ]
                                                         |
                                                         v
                                                [ Rule Engine ] ---> Findings[]
                                                         |
                                                         v
                                                [ Risk Scoring ] ---> Summary
                                                         |
                                                         v
                                                   [ Risk State ]
                                                         |
                                                         v
                                                   [ FastAPI ]
                                                         |
                                                         v
                                                   [ React UI ]
```

---

## 7.4 Data Model Relationships

```
Raw Athena JSON
   |
   v
Patient Object (dict)
   |
   v
UnifiedEvent {
  event_id
  event_type
  system
  resource_type
  resource_id
  user_id
  timestamp
  metadata {...}
}
   |
   v
Finding {
  rule_name
  category
  severity
  event_id
}
   |
   v
Risk Summary {
  risk_score
  risk_level
  breakdown[]
}
```

---

## 7.5 Deployment Architecture (Local Dev)

```
+----------------------+        HTTP        +-----------------------+
|  React (Vite :5173)  | <----------------> |  FastAPI (Uvicorn)    |
|  Dashboard UI        |                    |  :8000                |
+----------------------+                    +-----------------------+
                                                     |
                                                     v
                                           +-----------------------+
                                           |  Pipeline + Engines   |
                                           |  (in-process)         |
                                           +-----------------------+
                                                     |
                                                     v
                                           +-----------------------+
                                           | Athena External API   |
                                           +-----------------------+
```

---

## 7.6 Future Target Architecture (Scalable)

```
                 +-------------------+
                 |  Multiple EHRs    |
                 | (Athena/Epic/...) |
                 +---------+---------+
                           |
                           v
                   +------------------+
                   |  Connector Hub   |
                   +------------------+
                           |
                           v
                   +------------------+
                   |  Event Bus       |  (Kafka / PubSub)
                   +------------------+
                           |
          +----------------+----------------+
          |                                 |
          v                                 v
+------------------+               +------------------+
| Rule Engine Svc  |               | ML Anomaly Svc   |
+------------------+               +------------------+
          |                                 |
          +---------------+-----------------+
                          v
                 +------------------+
                 | Scoring Service  |
                 +------------------+
                          |
                          v
                 +------------------+
                 |  Data Store      | (Postgres/Elastic)
                 +------------------+
                          |
                          v
                 +------------------+
                 |   API Gateway    |
                 +------------------+
                          |
                          v
                 +------------------+
                 |  Web Dashboard   |
                 +------------------+
```

---

# 8. Conclusion

The platform establishes a strong foundation for healthcare risk intelligence by integrating data ingestion, normalization, rule evaluation, and visualization into a cohesive system. It is extensible, modular, and ready for scaling into enterprise-grade compliance and security analytics.

