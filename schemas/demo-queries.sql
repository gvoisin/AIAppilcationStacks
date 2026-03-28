-- Demo Oracle queries mapped to Terrena sample questions.
-- Load order:
--   1. @schemas/demo-schema.sql
--   2. @schemas/demo-data.sql
--   3. Run the queries below as needed

--------------------------------------------------------------------------------
-- 1) Quelles sont les alertes operationnelles les plus prioritaires ce matin ?
--------------------------------------------------------------------------------
SELECT
    oa.alert_code,
    oa.alert_title,
    oa.alert_type,
    oa.severity,
    oa.status,
    t.territory_name,
    f.filiere_name,
    oa.assigned_team,
    oa.impact_summary
FROM operational_alerts oa
LEFT JOIN territories t ON t.territory_id = oa.territory_id
LEFT JOIN filieres f ON f.filiere_id = oa.filiere_id
ORDER BY
    CASE oa.severity
        WHEN 'CRITICAL' THEN 1
        WHEN 'HIGH' THEN 2
        WHEN 'MEDIUM' THEN 3
        ELSE 4
    END,
    oa.opened_at DESC
FETCH FIRST 10 ROWS ONLY;

--------------------------------------------------------------------------------
-- 2) Resume les impacts sur la filiere volailles en Vendee.
--------------------------------------------------------------------------------
SELECT
    f.filiere_name,
    t.territory_name,
    oa.alert_code,
    oa.alert_title,
    oa.severity,
    oa.status,
    oa.impact_units,
    oa.impact_unit_label,
    oa.impact_summary,
    LISTAGG(b.brand_name || ' (' || abi.impact_level || ')', ', ')
        WITHIN GROUP (ORDER BY b.brand_name) AS impacted_brands
FROM operational_alerts oa
JOIN filieres f ON f.filiere_id = oa.filiere_id
JOIN territories t ON t.territory_id = oa.territory_id
LEFT JOIN alert_brand_impacts abi ON abi.alert_id = oa.alert_id
LEFT JOIN brands b ON b.brand_id = abi.brand_id
WHERE f.filiere_code = 'VOLAILLES'
  AND t.territory_code = 'VENDEE'
GROUP BY
    f.filiere_name,
    t.territory_name,
    oa.alert_code,
    oa.alert_title,
    oa.severity,
    oa.status,
    oa.impact_units,
    oa.impact_unit_label,
    oa.impact_summary
ORDER BY oa.opened_at DESC
FETCH FIRST 10 ROWS ONLY;

--------------------------------------------------------------------------------
-- 3) Quels territoires menacent Pere Dodu ou Ackerman ?
--------------------------------------------------------------------------------
SELECT
    b.brand_name,
    t.territory_name,
    oa.alert_code,
    oa.alert_title,
    abi.impact_level,
    oa.severity,
    oa.status,
    oa.cause_summary
FROM alert_brand_impacts abi
JOIN brands b ON b.brand_id = abi.brand_id
JOIN operational_alerts oa ON oa.alert_id = abi.alert_id
LEFT JOIN territories t ON t.territory_id = oa.territory_id
WHERE b.brand_name IN ('Pere Dodu', 'Ackerman')
ORDER BY
    b.brand_name,
    CASE abi.impact_level
        WHEN 'CRITICAL' THEN 1
        WHEN 'HIGH' THEN 2
        WHEN 'MEDIUM' THEN 3
        ELSE 4
    END,
    oa.opened_at DESC
FETCH FIRST 10 ROWS ONLY;

--------------------------------------------------------------------------------
-- 4) Compare la performance logistique entre grandes cultures et volailles.
--------------------------------------------------------------------------------
SELECT
    f.filiere_name,
    ROUND(AVG(lf.service_level_pct), 2) AS avg_service_level_pct,
    ROUND(AVG(lf.on_time_delivery_pct), 2) AS avg_on_time_delivery_pct,
    ROUND(SUM(lf.backlog_tons), 2) AS total_backlog_tons,
    ROUND(SUM(lf.weekly_volume_tons), 2) AS total_weekly_volume_tons,
    COUNT(*) AS flow_count
FROM logistics_flows lf
JOIN filieres f ON f.filiere_id = lf.filiere_id
WHERE f.filiere_code IN ('GRANDES_CULTURES', 'VOLAILLES')
GROUP BY f.filiere_name
ORDER BY f.filiere_name
FETCH FIRST 10 ROWS ONLY;

--------------------------------------------------------------------------------
-- 5) Quels indicateurs montrent un risque sur la tracabilite ?
--------------------------------------------------------------------------------
SELECT
    l.lot_code,
    b.brand_name,
    tc.check_date,
    tc.indicator_name,
    tc.indicator_value,
    tc.threshold_value,
    tc.unit_label,
    tc.check_status,
    tc.document_complete_flag,
    tc.finding_summary
FROM traceability_checks tc
JOIN lots l ON l.lot_id = tc.lot_id
LEFT JOIN brands b ON b.brand_id = l.brand_id
WHERE tc.check_status IN ('WARNING', 'FAIL')
   OR tc.document_complete_flag = 'N'
ORDER BY
    CASE tc.check_status
        WHEN 'FAIL' THEN 1
        WHEN 'WARNING' THEN 2
        ELSE 3
    END,
    tc.check_date DESC
FETCH FIRST 10 ROWS ONLY;

--------------------------------------------------------------------------------
-- 6) Donne moi une synthese des risques pouvant affecter La Nouvelle Agriculture.
--------------------------------------------------------------------------------
SELECT
    b.brand_name,
    oa.alert_code,
    oa.alert_title,
    oa.alert_type,
    abi.impact_level,
    oa.status,
    t.territory_name,
    oa.impact_summary
FROM alert_brand_impacts abi
JOIN brands b ON b.brand_id = abi.brand_id
JOIN operational_alerts oa ON oa.alert_id = abi.alert_id
LEFT JOIN territories t ON t.territory_id = oa.territory_id
WHERE b.brand_name = 'La Nouvelle Agriculture'
ORDER BY
    CASE abi.impact_level
        WHEN 'CRITICAL' THEN 1
        WHEN 'HIGH' THEN 2
        WHEN 'MEDIUM' THEN 3
        ELSE 4
    END,
    oa.opened_at DESC
FETCH FIRST 10 ROWS ONLY;

--------------------------------------------------------------------------------
-- 7) Quels incidents pourraient impacter les livraisons de Pere Dodu cette semaine ?
--------------------------------------------------------------------------------
SELECT
    b.brand_name,
    oa.alert_code,
    oa.alert_title,
    oa.alert_type,
    oa.severity,
    oa.status,
    s.site_name,
    oa.expected_resolution_at,
    oa.impact_summary
FROM alert_brand_impacts abi
JOIN brands b ON b.brand_id = abi.brand_id
JOIN operational_alerts oa ON oa.alert_id = abi.alert_id
LEFT JOIN sites s ON s.site_id = oa.site_id
WHERE b.brand_name = 'Pere Dodu'
  AND oa.status IN ('OPEN', 'IN_ANALYSIS', 'MITIGATING', 'MONITORING')
ORDER BY
    CASE oa.severity
        WHEN 'CRITICAL' THEN 1
        WHEN 'HIGH' THEN 2
        WHEN 'MEDIUM' THEN 3
        ELSE 4
    END,
    oa.expected_resolution_at
FETCH FIRST 10 ROWS ONLY;

--------------------------------------------------------------------------------
-- 8) Y a t il un risque pour les expeditions Ackerman ?
--------------------------------------------------------------------------------
SELECT
    b.brand_name,
    l.lot_code,
    lf.flow_name,
    oa.alert_title,
    tc.check_status,
    qi.status AS quality_issue_status,
    oa.status AS alert_status,
    oa.impact_summary
FROM brands b
LEFT JOIN lots l ON l.brand_id = b.brand_id
LEFT JOIN logistics_flows lf ON lf.brand_id = b.brand_id
LEFT JOIN alert_brand_impacts abi ON abi.brand_id = b.brand_id
LEFT JOIN operational_alerts oa ON oa.alert_id = abi.alert_id
LEFT JOIN traceability_checks tc ON tc.lot_id = l.lot_id
LEFT JOIN quality_issues qi ON qi.lot_id = l.lot_id
WHERE b.brand_name = 'Ackerman'
ORDER BY
    CASE oa.severity
        WHEN 'CRITICAL' THEN 1
        WHEN 'HIGH' THEN 2
        WHEN 'MEDIUM' THEN 3
        ELSE 4
    END,
    tc.check_date DESC NULLS LAST
FETCH FIRST 10 ROWS ONLY;

--------------------------------------------------------------------------------
-- 9) Quels sujets doivent etre remontes a un responsable qualite pour Douce France ?
--------------------------------------------------------------------------------
SELECT
    b.brand_name,
    qi.issue_code,
    qi.issue_category,
    qi.severity,
    qi.status,
    qi.summary,
    qi.action_required,
    rd.document_title AS related_document
FROM quality_issues qi
JOIN brands b ON b.brand_id = qi.brand_id
LEFT JOIN reference_documents rd
    ON rd.related_brand_id = qi.brand_id
   AND rd.document_type IN ('NOTE', 'PROCEDURE', 'CHECKLIST')
WHERE b.brand_name = 'Douce France'
  AND qi.status IN ('OPEN', 'UNDER_REVIEW', 'ESCALATED')
ORDER BY
    CASE qi.severity
        WHEN 'CRITICAL' THEN 1
        WHEN 'HIGH' THEN 2
        WHEN 'MEDIUM' THEN 3
        ELSE 4
    END,
    qi.detected_at DESC
FETCH FIRST 10 ROWS ONLY;

--------------------------------------------------------------------------------
-- 10) Fais une synthese executive en 5 points pour un directeur de filiere Terrena.
-- Returns five concise executive lines from current open risk topics.
--------------------------------------------------------------------------------
SELECT summary_line
FROM (
    SELECT '1. Alertes critiques ouvertes: ' || COUNT(*) AS summary_line, 1 AS seq
    FROM operational_alerts
    WHERE severity = 'CRITICAL' AND status IN ('OPEN', 'IN_ANALYSIS', 'MITIGATING', 'MONITORING')

    UNION ALL

    SELECT '2. Filiere la plus sous tension logistique: ' ||
           MAX(filiere_name) KEEP (DENSE_RANK FIRST ORDER BY avg_service_level_pct) AS summary_line,
           2 AS seq
    FROM (
        SELECT f.filiere_name, AVG(lf.service_level_pct) AS avg_service_level_pct
        FROM logistics_flows lf
        JOIN filieres f ON f.filiere_id = lf.filiere_id
        GROUP BY f.filiere_name
    )

    UNION ALL

    SELECT '3. Marque la plus exposee aux alertes: ' ||
           MAX(brand_name) KEEP (DENSE_RANK FIRST ORDER BY impact_score DESC) AS summary_line,
           3 AS seq
    FROM (
        SELECT b.brand_name,
               SUM(CASE abi.impact_level
                       WHEN 'CRITICAL' THEN 4
                       WHEN 'HIGH' THEN 3
                       WHEN 'MEDIUM' THEN 2
                       ELSE 1
                   END) AS impact_score
        FROM alert_brand_impacts abi
        JOIN brands b ON b.brand_id = abi.brand_id
        GROUP BY b.brand_name
    )

    UNION ALL

    SELECT '4. Lots a risque en tracabilite: ' || COUNT(*) AS summary_line,
           4 AS seq
    FROM lots
    WHERE traceability_status IN ('WATCH', 'AT_RISK', 'BLOCKED')

    UNION ALL

    SELECT '5. Actions prioritaires a echeance <= 72h: ' || COUNT(*) AS summary_line,
           5 AS seq
    FROM action_plans
    WHERE priority IN ('HIGH', 'CRITICAL')
      AND NVL(horizon_hours, 999999) <= 72
      AND status IN ('OPEN', 'IN_PROGRESS', 'BLOCKED')
)
ORDER BY seq;

--------------------------------------------------------------------------------
-- 11) Construis un espace de pilotage pour un risque sanitaire sur la filiere
--     volailles avec impacts potentiels sur Pere Dodu et Gastronome Professionnels.
--------------------------------------------------------------------------------
SELECT
    oa.alert_code,
    oa.alert_title,
    oa.severity,
    oa.status,
    t.territory_name,
    s.site_name,
    b.brand_name,
    abi.impact_level,
    ap.action_summary,
    ap.status AS action_status
FROM operational_alerts oa
JOIN filieres f ON f.filiere_id = oa.filiere_id
LEFT JOIN territories t ON t.territory_id = oa.territory_id
LEFT JOIN sites s ON s.site_id = oa.site_id
LEFT JOIN alert_brand_impacts abi ON abi.alert_id = oa.alert_id
LEFT JOIN brands b ON b.brand_id = abi.brand_id
LEFT JOIN action_plans ap ON ap.alert_id = oa.alert_id AND ap.brand_id = abi.brand_id
WHERE f.filiere_code = 'VOLAILLES'
  AND b.brand_name IN ('Pere Dodu', 'Gastronome Professionnels')
ORDER BY
    CASE oa.severity
        WHEN 'CRITICAL' THEN 1
        WHEN 'HIGH' THEN 2
        ELSE 3
    END,
    b.brand_name
FETCH FIRST 10 ROWS ONLY;

--------------------------------------------------------------------------------
-- 12) Prepare un cockpit de suivi des expeditions vins pour Ackerman avec alertes
--     de tracabilite, lots a risque et priorites de traitement.
--------------------------------------------------------------------------------
SELECT
    b.brand_name,
    lf.flow_name,
    l.lot_code,
    l.traceability_status,
    qi.severity AS quality_severity,
    qi.status AS quality_status,
    tc.check_status,
    ap.priority,
    ap.action_summary
FROM brands b
JOIN logistics_flows lf ON lf.brand_id = b.brand_id
LEFT JOIN lots l ON l.brand_id = b.brand_id
LEFT JOIN quality_issues qi ON qi.lot_id = l.lot_id
LEFT JOIN traceability_checks tc ON tc.lot_id = l.lot_id
LEFT JOIN action_plans ap ON ap.brand_id = b.brand_id
WHERE b.brand_name = 'Ackerman'
ORDER BY
    CASE l.traceability_status
        WHEN 'BLOCKED' THEN 1
        WHEN 'AT_RISK' THEN 2
        WHEN 'WATCH' THEN 3
        ELSE 4
    END,
    CASE ap.priority
        WHEN 'CRITICAL' THEN 1
        WHEN 'HIGH' THEN 2
        ELSE 3
    END
FETCH FIRST 10 ROWS ONLY;

--------------------------------------------------------------------------------
-- 13) Cree une vue de pilotage des filieres sous marque La Nouvelle Agriculture
--     avec qualite, tracabilite, logistique et points de vigilance.
--------------------------------------------------------------------------------
SELECT
    b.brand_name,
    f.filiere_name,
    lf.service_level_pct,
    lf.on_time_delivery_pct,
    l.lot_code,
    l.traceability_status,
    l.quality_status,
    oa.alert_title,
    oa.severity
FROM brands b
JOIN brand_filieres bf ON bf.brand_id = b.brand_id
JOIN filieres f ON f.filiere_id = bf.filiere_id
LEFT JOIN logistics_flows lf ON lf.brand_id = b.brand_id AND lf.filiere_id = f.filiere_id
LEFT JOIN lots l ON l.brand_id = b.brand_id AND l.filiere_id = f.filiere_id
LEFT JOIN alert_brand_impacts abi ON abi.brand_id = b.brand_id
LEFT JOIN operational_alerts oa ON oa.alert_id = abi.alert_id
WHERE b.brand_name = 'La Nouvelle Agriculture'
ORDER BY f.filiere_name, oa.opened_at DESC NULLS LAST
FETCH FIRST 10 ROWS ONLY;

--------------------------------------------------------------------------------
-- 14) Genere un tableau de priorisation des actions pour proteger le niveau de
--     service de Douce France sur 72 heures.
--------------------------------------------------------------------------------
SELECT
    b.brand_name,
    ap.action_code,
    ap.priority,
    ap.status,
    ap.horizon_hours,
    ap.owner_name,
    ap.action_summary,
    oa.alert_title
FROM action_plans ap
JOIN brands b ON b.brand_id = ap.brand_id
LEFT JOIN operational_alerts oa ON oa.alert_id = ap.alert_id
WHERE b.brand_name = 'Douce France'
  AND NVL(ap.horizon_hours, 999999) <= 72
ORDER BY
    CASE ap.priority
        WHEN 'CRITICAL' THEN 1
        WHEN 'HIGH' THEN 2
        WHEN 'MEDIUM' THEN 3
        ELSE 4
    END,
    ap.due_at
FETCH FIRST 10 ROWS ONLY;

--------------------------------------------------------------------------------
-- 15) Assemble un espace de coordination pour un responsable supply chain qui
--     doit suivre Fermier d Ancenis, Tendre et plus et D Anvial.
--------------------------------------------------------------------------------
SELECT
    b.brand_name,
    oa.alert_title,
    oa.status AS alert_status,
    ap.priority,
    ap.status AS action_status,
    s.site_name,
    oa.impact_summary,
    ap.action_summary
FROM brands b
LEFT JOIN alert_brand_impacts abi ON abi.brand_id = b.brand_id
LEFT JOIN operational_alerts oa ON oa.alert_id = abi.alert_id
LEFT JOIN action_plans ap ON ap.brand_id = b.brand_id AND ap.alert_id = oa.alert_id
LEFT JOIN sites s ON s.site_id = COALESCE(ap.site_id, oa.site_id)
WHERE b.brand_name IN ('Fermier d Ancenis', 'Tendre et plus', 'D Anvial')
ORDER BY
    b.brand_name,
    CASE ap.priority
        WHEN 'CRITICAL' THEN 1
        WHEN 'HIGH' THEN 2
        WHEN 'MEDIUM' THEN 3
        ELSE 4
    END,
    oa.opened_at DESC
FETCH FIRST 10 ROWS ONLY;
