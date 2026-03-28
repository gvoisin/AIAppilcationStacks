-- Reset and load LIMAGRAIN Vegetable Seeds demo schema/data, then run smoke checks.
-- Usage from SQLcl / SQL*Plus, started at repo root or from schemas/ with path adjusted:
--   @schemas/demo-load-limagrain.sql

PROMPT === Dropping previous demo objects if present ===
@schemas/demo-drop.sql

PROMPT === Creating demo schema ===
@schemas/demo-schema.sql

PROMPT === Loading LIMAGRAIN demo data ===
@schemas/demo-data-limagrain.sql

COMMIT;

PROMPT === Smoke check: table row counts ===
SELECT 'territories' AS table_name, COUNT(*) AS row_count FROM territories
UNION ALL
SELECT 'filieres', COUNT(*) FROM filieres
UNION ALL
SELECT 'brands', COUNT(*) FROM brands
UNION ALL
SELECT 'campaigns', COUNT(*) FROM campaigns
UNION ALL
SELECT 'sites', COUNT(*) FROM sites
UNION ALL
SELECT 'operational_alerts', COUNT(*) FROM operational_alerts
UNION ALL
SELECT 'alert_brand_impacts', COUNT(*) FROM alert_brand_impacts
UNION ALL
SELECT 'logistics_flows', COUNT(*) FROM logistics_flows
UNION ALL
SELECT 'lots', COUNT(*) FROM lots
UNION ALL
SELECT 'quality_issues', COUNT(*) FROM quality_issues
UNION ALL
SELECT 'traceability_checks', COUNT(*) FROM traceability_checks
UNION ALL
SELECT 'reference_documents', COUNT(*) FROM reference_documents
UNION ALL
SELECT 'action_plans', COUNT(*) FROM action_plans;

PROMPT === Smoke check: highest priority alerts ===
SELECT
    alert_code,
    alert_title,
    severity,
    status
FROM operational_alerts
ORDER BY
    CASE severity
        WHEN 'CRITICAL' THEN 1
        WHEN 'HIGH' THEN 2
        WHEN 'MEDIUM' THEN 3
        ELSE 4
    END,
    opened_at DESC
FETCH FIRST 5 ROWS ONLY;

PROMPT === Smoke check: Vilmorin-Mikado export traceability risk ===
SELECT
    b.brand_name,
    l.lot_code,
    tc.check_status,
    tc.finding_summary
FROM brands b
JOIN lots l ON l.brand_id = b.brand_id
JOIN traceability_checks tc ON tc.lot_id = l.lot_id
WHERE b.brand_name = 'Vilmorin-Mikado'
ORDER BY tc.check_date DESC
FETCH FIRST 5 ROWS ONLY;

PROMPT === Smoke check: HM.CLAUSE quality issues ===
SELECT
    b.brand_name,
    qi.issue_code,
    qi.severity,
    qi.status,
    qi.summary
FROM brands b
JOIN quality_issues qi ON qi.brand_id = b.brand_id
WHERE b.brand_name = 'HM.CLAUSE'
ORDER BY qi.detected_at DESC
FETCH FIRST 5 ROWS ONLY;

PROMPT === LIMAGRAIN demo load complete ===
