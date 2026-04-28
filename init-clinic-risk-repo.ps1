# Clinic Risk Intelligence Platform - Repo Bootstrap Script
# Run this from the directory where you want the project folder created

$root = "clinic-risk-intelligence-platform"

Write-Host "Creating project structure in $root ..." -ForegroundColor Green

# -------------------------
# Root folder
# -------------------------
New-Item -ItemType Directory -Force -Path $root | Out-Null

# -------------------------
# Core folders
# -------------------------
$dirs = @(
    "$root/docs",
    "$root/configs",
    "$root/src/api/routes",
    "$root/src/core",
    "$root/src/models",
    "$root/src/connectors",
    "$root/src/normalization",
    "$root/src/engine/rules",
    "$root/src/scoring",
    "$root/src/storage",
    "$root/src/services",
    "$root/src/dashboard_api",
    "$root/src/utils",
    "$root/workers",
    "$root/db/migrations",
    "$root/tests/test_connectors",
    "$root/tests/test_rules",
    "$root/tests/test_scoring",
    "$root/tests/test_api",
    "$root/scripts",
    "$root/ui/dashboard",
    "$root/ui/components"
)

foreach ($dir in $dirs) {
    New-Item -ItemType Directory -Force -Path $dir | Out-Null
}

# -------------------------
# Helper function to create file with placeholder content
# -------------------------
function Create-File($path, $content) {
    if (-not (Test-Path $path)) {
        $content | Out-File -Encoding UTF8 $path
    }
}

# -------------------------
# Root files
# -------------------------
Create-File "$root/README.md" "# Clinic Risk Intelligence Platform`n"
Create-File "$root/requirements.txt" "# Python dependencies"
Create-File "$root/pyproject.toml" "# Project config"
Create-File "$root/.env.example" "# Environment variables"
Create-File "$root/docker-compose.yml" "# Docker compose setup"
Create-File "$root/Dockerfile" "# Docker build file"

# -------------------------
# Docs
# -------------------------
Create-File "$root/docs/architecture.md" "# Architecture Overview"
Create-File "$root/docs/risk-taxonomy.md" "# Risk Taxonomy"
Create-File "$root/docs/data-model.md" "# Data Model"
Create-File "$root/docs/api-spec.md" "# API Specification"

# -------------------------
# Configs
# -------------------------
Create-File "$root/configs/app_config.yaml" "app: config"
Create-File "$root/configs/risk_rules.yaml" "rules: []"
Create-File "$root/configs/connectors.yaml" "connectors: []"
Create-File "$root/configs/scoring_weights.yaml" "weights: {}"

# -------------------------
# Source bootstrap
# -------------------------
Create-File "$root/src/main.py" "# FastAPI entry point"
Create-File "$root/src/api/routes/risk.py" "# Risk API routes"
Create-File "$root/src/api/routes/events.py" "# Event API routes"
Create-File "$root/src/api/routes/users.py" "# User API routes"

Create-File "$root/src/core/config.py" "# App config loader"
Create-File "$root/src/core/logging.py" "# Logging setup"
Create-File "$root/src/core/security.py" "# Security utilities"

Create-File "$root/src/models/event.py" "# Unified event schema"
Create-File "$root/src/models/risk.py" "# Risk model"
Create-File "$root/src/models/user.py" "# User model"
Create-File "$root/src/models/system.py" "# System model"

Create-File "$root/src/connectors/base_connector.py" "# Base connector interface"
Create-File "$root/src/connectors/openemr_connector.py" "# OpenEMR connector"
Create-File "$root/src/connectors/athena_connector.py" "# Athena connector"
Create-File "$root/src/connectors/ecw_connector.py" "# eCW connector"
Create-File "$root/src/connectors/kareo_connector.py" "# Kareo connector"
Create-File "$root/src/connectors/hl7_listener.py" "# HL7 listener"

Create-File "$root/src/normalization/event_mapper.py" "# Event normalization"
Create-File "$root/src/normalization/identity_resolver.py" "# Identity mapping"
Create-File "$root/src/normalization/schema_validator.py" "# Schema validation"

Create-File "$root/src/engine/rule_engine.py" "# Rule engine core"
Create-File "$root/src/engine/rules/access_rules.py" "# Access rules"
Create-File "$root/src/engine/rules/billing_rules.py" "# Billing rules"
Create-File "$root/src/engine/rules/workflow_rules.py" "# Workflow rules"
Create-File "$root/src/engine/rules/clinical_pattern_rules.py" "# Clinical pattern rules"

Create-File "$root/src/scoring/risk_calculator.py" "# Risk scoring logic"
Create-File "$root/src/scoring/domain_weights.py" "# Risk weights"
Create-File "$root/src/scoring/aggregation.py" "# Score aggregation"

Create-File "$root/src/storage/database.py" "# DB connection"
Create-File "$root/src/storage/models_sql.py" "# SQL models"
Create-File "$root/src/storage/repository.py" "# Data access layer"

Create-File "$root/src/services/event_service.py" "# Event service"
Create-File "$root/src/services/risk_service.py" "# Risk service"
Create-File "$root/src/services/reporting_service.py" "# Reporting service"
Create-File "$root/src/services/alert_service.py" "# Alert service"

Create-File "$root/src/dashboard_api/summary_service.py" "# Summary API"
Create-File "$root/src/dashboard_api/clinic_dashboard.py" "# Dashboard API"
Create-File "$root/src/dashboard_api/user_risk_profile.py" "# User risk profile API"

Create-File "$root/src/utils/datetime_utils.py" "# Date utilities"
Create-File "$root/src/utils/id_utils.py" "# ID utilities"
Create-File "$root/src/utils/encryption.py" "# Encryption helpers"

# -------------------------
# Workers
# -------------------------
Create-File "$root/workers/event_ingestion_worker.py" "# Event ingestion worker"
Create-File "$root/workers/risk_scoring_worker.py" "# Risk scoring worker"
Create-File "$root/workers/connector_polling_worker.py" "# Connector polling worker"

# -------------------------
# DB
# -------------------------
Create-File "$root/db/schema.sql" "-- Database schema"
Create-File "$root/db/seed_data.sql" "-- Seed data"

# -------------------------
# Scripts
# -------------------------
Create-File "$root/scripts/run_dev.sh" "# Run dev environment"
Create-File "$root/scripts/init_db.sh" "# Initialize database"
Create-File "$root/scripts/load_sample_data.py" "# Load sample data"

# -------------------------
# UI placeholders
# -------------------------
Create-File "$root/ui/dashboard/README.md" "# Dashboard UI"
Create-File "$root/ui/components/README.md" "# UI Components"

Write-Host "Project structure created successfully!" -ForegroundColor Cyan
Write-Host "Next step: cd $root && git init" -ForegroundColor Yellow