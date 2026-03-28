-- Truncate all data from shared demo tables in foreign-key-safe order.
-- SQLcl / SQL*Plus friendly.
-- Usage:
--   @schemas/demo-truncate.sql

PROMPT === Truncating demo table data ===
TRUNCATE TABLE action_plans;
TRUNCATE TABLE reference_documents;
TRUNCATE TABLE traceability_checks;
TRUNCATE TABLE quality_issues;
TRUNCATE TABLE lots;
TRUNCATE TABLE logistics_flows;
TRUNCATE TABLE alert_brand_impacts;
TRUNCATE TABLE operational_alerts;
TRUNCATE TABLE brand_sites;
TRUNCATE TABLE brand_filieres;
TRUNCATE TABLE sites;
TRUNCATE TABLE campaigns;
TRUNCATE TABLE brands;
TRUNCATE TABLE filieres;
TRUNCATE TABLE territories;

PROMPT === Demo tables truncated ===
