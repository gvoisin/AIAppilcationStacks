# region Imports
import textwrap
# endregion Imports

# region Prompt Templates
SQL_SCHEMA_DESCRIPTION = textwrap.dedent(
    """
    You are an expert Oracle SQL generator. The user asks questions about
    the LIMAGRAIN Vegetable Seeds operations database schema which contains:

      • territories(territory_id, territory_name, territory_code, region_name, risk_level, logistics_pressure_score, notes)
      • filieres(filiere_id, filiere_name, filiere_code, category, strategic_priority, active_flag)
      • brands(brand_id, brand_name, brand_code, business_line, export_flag, quality_sensitivity)
      • campaigns(campaign_id, campaign_name, campaign_year, season_name, start_date, end_date, status)
      • sites(site_id, site_name, site_code, site_type, territory_id, filiere_id, city_name, capacity_tons, status)
      • brand_filieres(brand_id, filiere_id, importance_level)
      • brand_sites(brand_id, site_id, role_name)
      • operational_alerts(alert_id, alert_code, alert_title, alert_type, severity, status, filiere_id, territory_id, site_id, campaign_id, opened_at, expected_resolution_at, impact_summary, impact_units, impact_unit_label, cause_summary, assigned_team, escalation_required)
      • alert_brand_impacts(alert_id, brand_id, impact_level, impact_description)
      • logistics_flows(flow_id, flow_code, flow_name, filiere_id, brand_id, origin_site_id, destination_site_id, campaign_id, transport_mode, service_level_pct, on_time_delivery_pct, backlog_tons, weekly_volume_tons, weather_risk_level, flow_status, notes)
      • lots(lot_id, lot_code, filiere_id, brand_id, source_site_id, current_site_id, campaign_id, production_date, expiration_date, quantity, quantity_unit, traceability_status, quality_status, destination_market, export_flag)
      • quality_issues(quality_issue_id, issue_code, lot_id, site_id, brand_id, issue_category, severity, status, detected_at, owner_name, summary, action_required)
      • traceability_checks(check_id, lot_id, site_id, check_date, check_status, indicator_name, indicator_value, threshold_value, unit_label, finding_summary, document_complete_flag)
      • reference_documents(document_id, document_code, document_title, document_type, related_filiere_id, related_brand_id, related_lot_id, related_alert_id, version_label, owner_name, document_status, created_at)
      • action_plans(action_plan_id, action_code, alert_id, brand_id, site_id, owner_name, priority, due_at, status, action_summary, horizon_hours)

    Key Relationships:
      sites.territory_id = territories.territory_id
      sites.filiere_id = filieres.filiere_id
      brand_filieres.brand_id = brands.brand_id
      brand_filieres.filiere_id = filieres.filiere_id
      brand_sites.brand_id = brands.brand_id
      brand_sites.site_id = sites.site_id
      operational_alerts.filiere_id = filieres.filiere_id
      operational_alerts.territory_id = territories.territory_id
      operational_alerts.site_id = sites.site_id
      operational_alerts.campaign_id = campaigns.campaign_id
      alert_brand_impacts.alert_id = operational_alerts.alert_id
      alert_brand_impacts.brand_id = brands.brand_id
      logistics_flows.filiere_id = filieres.filiere_id
      logistics_flows.brand_id = brands.brand_id
      logistics_flows.origin_site_id = sites.site_id
      logistics_flows.destination_site_id = sites.site_id
      logistics_flows.campaign_id = campaigns.campaign_id
      lots.filiere_id = filieres.filiere_id
      lots.brand_id = brands.brand_id
      lots.source_site_id = sites.site_id
      lots.current_site_id = sites.site_id
      lots.campaign_id = campaigns.campaign_id
      quality_issues.lot_id = lots.lot_id
      quality_issues.site_id = sites.site_id
      quality_issues.brand_id = brands.brand_id
      traceability_checks.lot_id = lots.lot_id
      traceability_checks.site_id = sites.site_id
      reference_documents.related_filiere_id = filieres.filiere_id
      reference_documents.related_brand_id = brands.brand_id
      reference_documents.related_lot_id = lots.lot_id
      reference_documents.related_alert_id = operational_alerts.alert_id
      action_plans.alert_id = operational_alerts.alert_id
      action_plans.brand_id = brands.brand_id
      action_plans.site_id = sites.site_id

    The schema supports LIMAGRAIN Vegetable Seeds business questions about semences potageres,
    la logistique, la qualite, la tracabilite, les lots, les sites,
    les campagnes, les marques et les alertes operationnelles.

    Return valid SQL only. Your output will be directly fed to the oracle database.
    dont include backquotes as they would interfere
    Always limit your queries to the first top 10 rows of the results and consider this in the information retrieval.
    When the user asks for the most important, most priority, top, or highest-priority alerts,
    do not filter severity to only one level unless the user explicitly asks for a specific severity.
    Instead rank severities with CRITICAL first, then HIGH, then MEDIUM, then LOW.
    For time-sensitive phrases like ce matin, aujourd hui, or recent, prefer filtering on opened_at
    while still preserving severity ranking rather than excluding CRITICAL alerts.
    """
)

SQL_FEW_SHOT_EXAMPLES = [
    {
        "q": "Quelles sont les alertes operationnelles les plus prioritaires ?",
        "sql": (
            "SELECT alert_code, alert_title, severity, status, opened_at\n"
            "FROM operational_alerts\n"
            "ORDER BY CASE severity\n"
            "           WHEN 'CRITICAL' THEN 1\n"
            "           WHEN 'HIGH' THEN 2\n"
            "           WHEN 'MEDIUM' THEN 3\n"
            "           ELSE 4\n"
            "         END, opened_at DESC\n"
            "FETCH FIRST 10 ROWS ONLY;"
        ),
    },
    {
        "q": "Quels territoires menacent HM.CLAUSE ou Hazera ?",
        "sql": (
            "SELECT b.brand_name, t.territory_name, oa.alert_title, abi.impact_level\n"
            "FROM alert_brand_impacts abi\n"
            "JOIN brands b ON b.brand_id = abi.brand_id\n"
            "JOIN operational_alerts oa ON oa.alert_id = abi.alert_id\n"
            "LEFT JOIN territories t ON t.territory_id = oa.territory_id\n"
            "WHERE b.brand_name IN ('HM.CLAUSE', 'Hazera')\n"
            "ORDER BY abi.impact_level DESC, oa.opened_at DESC\n"
            "FETCH FIRST 10 ROWS ONLY;"
        ),
    },
    {
        "q": "Compare la performance logistique entre la production et la distribution commerciale des semences potageres",
        "sql": (
            "SELECT f.filiere_name,\n"
            "       ROUND(AVG(lf.service_level_pct), 2) AS avg_service_level_pct,\n"
            "       ROUND(AVG(lf.on_time_delivery_pct), 2) AS avg_on_time_delivery_pct,\n"
            "       ROUND(SUM(lf.backlog_tons), 2) AS total_backlog_tons\n"
            "FROM logistics_flows lf\n"
            "JOIN filieres f ON f.filiere_id = lf.filiere_id\n"
            "WHERE f.filiere_code IN ('VEG_PRODUCTION', 'VEG_DISTRIBUTION')\n"
            "GROUP BY f.filiere_name\n"
            "ORDER BY avg_service_level_pct DESC\n"
            "FETCH FIRST 10 ROWS ONLY;"
        ),
    },
    {
        "q": "Quels indicateurs montrent un risque sur la tracabilite ?",
        "sql": (
            "SELECT l.lot_code, tc.check_date, tc.indicator_name, tc.check_status, tc.finding_summary\n"
            "FROM traceability_checks tc\n"
            "JOIN lots l ON l.lot_id = tc.lot_id\n"
            "WHERE tc.check_status IN ('WARNING', 'FAIL')\n"
            "   OR tc.document_complete_flag = 'N'\n"
            "ORDER BY tc.check_date DESC\n"
            "FETCH FIRST 10 ROWS ONLY;"
        ),
    },
    {
        "q": "Quels sujets doivent etre remontes a un responsable qualite pour HM.CLAUSE ?",
        "sql": (
            "SELECT qi.issue_code, qi.issue_category, qi.severity, qi.status, qi.summary\n"
            "FROM quality_issues qi\n"
            "JOIN brands b ON b.brand_id = qi.brand_id\n"
            "WHERE b.brand_name = 'HM.CLAUSE'\n"
            "  AND qi.status IN ('OPEN', 'UNDER_REVIEW', 'ESCALATED')\n"
            "ORDER BY qi.detected_at DESC\n"
            "FETCH FIRST 10 ROWS ONLY;"
        ),
    },
    {
        "q": "Quels lots export Vilmorin-Mikado sont a risque ?",
        "sql": (
            "SELECT l.lot_code, l.traceability_status, l.quality_status, qi.status AS quality_issue_status\n"
            "FROM lots l\n"
            "LEFT JOIN quality_issues qi ON qi.lot_id = l.lot_id\n"
            "JOIN brands b ON b.brand_id = l.brand_id\n"
            "WHERE b.brand_name = 'Vilmorin-Mikado'\n"
            "  AND (l.traceability_status IN ('AT_RISK', 'BLOCKED', 'WATCH')\n"
            "       OR qi.status IN ('OPEN', 'UNDER_REVIEW', 'ESCALATED'))\n"
            "ORDER BY l.traceability_status DESC\n"
            "FETCH FIRST 10 ROWS ONLY;"
        ),
    },
]
# endregion Prompt Templates
