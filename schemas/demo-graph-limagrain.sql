-- Oracle Property Graph definition for LIMAGRAIN Vegetable Seeds demo operations.
-- Requires the relational objects from demo-schema.sql and demo-data-limagrain.sql.
-- Syntax aligned with Oracle CREATE PROPERTY GRAPH grammar.

CREATE OR REPLACE PROPERTY GRAPH limagrain_operations
  VERTEX TABLES (
    territories KEY (territory_id)
      LABEL TERRITORY PROPERTIES (
        territory_id, territory_name, territory_code, region_name, risk_level,
        logistics_pressure_score, notes
      ),
    filieres KEY (filiere_id)
      LABEL FILIERE PROPERTIES (
        filiere_id, filiere_name, filiere_code, category, strategic_priority, active_flag
      ),
    brands KEY (brand_id)
      LABEL BRAND PROPERTIES (
        brand_id, brand_name, brand_code, business_line, export_flag, quality_sensitivity
      ),
    campaigns KEY (campaign_id)
      LABEL CAMPAIGN PROPERTIES (
        campaign_id, campaign_name, campaign_year, season_name, start_date, end_date, status
      ),
    sites KEY (site_id)
      LABEL SITE PROPERTIES (
        site_id, site_name, site_code, site_type, territory_id, filiere_id,
        city_name, capacity_tons, status
      ),
    operational_alerts KEY (alert_id)
      LABEL OPERATIONAL_ALERT PROPERTIES (
        alert_id, alert_code, alert_title, alert_type, severity, status, filiere_id,
        territory_id, site_id, campaign_id, opened_at, expected_resolution_at,
        impact_summary, impact_units, impact_unit_label, cause_summary,
        assigned_team, escalation_required
      ),
    logistics_flows KEY (flow_id)
      LABEL LOGISTICS_FLOW PROPERTIES (
        flow_id, flow_code, flow_name, filiere_id, brand_id, origin_site_id,
        destination_site_id, campaign_id, transport_mode, service_level_pct,
        on_time_delivery_pct, backlog_tons, weekly_volume_tons,
        weather_risk_level, flow_status, notes
      ),
    lots KEY (lot_id)
      LABEL LOT PROPERTIES (
        lot_id, lot_code, filiere_id, brand_id, source_site_id, current_site_id,
        campaign_id, production_date, expiration_date, quantity, quantity_unit,
        traceability_status, quality_status, destination_market, export_flag
      ),
    quality_issues KEY (quality_issue_id)
      LABEL QUALITY_ISSUE PROPERTIES (
        quality_issue_id, issue_code, lot_id, site_id, brand_id, issue_category,
        severity, status, detected_at, owner_name, summary, action_required
      ),
    traceability_checks KEY (check_id)
      LABEL TRACEABILITY_CHECK PROPERTIES (
        check_id, lot_id, site_id, check_date, check_status, indicator_name,
        indicator_value, threshold_value, unit_label, finding_summary,
        document_complete_flag
      ),
    reference_documents KEY (document_id)
      LABEL REFERENCE_DOCUMENT PROPERTIES (
        document_id, document_code, document_title, document_type,
        related_filiere_id, related_brand_id, related_lot_id, related_alert_id,
        version_label, owner_name, document_status, created_at
      ),
    action_plans KEY (action_plan_id)
      LABEL ACTION_PLAN PROPERTIES (
        action_plan_id, action_code, alert_id, brand_id, site_id, owner_name,
        priority, due_at, status, action_summary, horizon_hours
      )
  )
  EDGE TABLES (
    sites AS site_in_territory
      KEY (site_id)
      SOURCE KEY (site_id) REFERENCES sites(site_id)
      DESTINATION KEY (territory_id) REFERENCES territories(territory_id)
      LABEL SITE_IN_TERRITORY PROPERTIES (
        site_id, site_name, site_code, site_type, territory_id, filiere_id,
        city_name, capacity_tons, status
      ),
    sites AS site_supports_filiere
      KEY (site_id)
      SOURCE KEY (site_id) REFERENCES sites(site_id)
      DESTINATION KEY (filiere_id) REFERENCES filieres(filiere_id)
      LABEL SITE_SUPPORTS_FILIERE PROPERTIES (
        site_id, site_name, site_code, site_type, territory_id, filiere_id,
        city_name, capacity_tons, status
      ),
    brand_filieres AS brand_in_filiere
      KEY (brand_id, filiere_id)
      SOURCE KEY (brand_id) REFERENCES brands(brand_id)
      DESTINATION KEY (filiere_id) REFERENCES filieres(filiere_id)
      LABEL BRAND_IN_FILIERE PROPERTIES (
        brand_id, filiere_id, importance_level
      ),
    brand_sites AS brand_present_at_site
      KEY (brand_id, site_id)
      SOURCE KEY (brand_id) REFERENCES brands(brand_id)
      DESTINATION KEY (site_id) REFERENCES sites(site_id)
      LABEL BRAND_PRESENT_AT_SITE PROPERTIES (
        brand_id, site_id, role_name
      ),
    operational_alerts AS alert_on_filiere
      KEY (alert_id)
      SOURCE KEY (alert_id) REFERENCES operational_alerts(alert_id)
      DESTINATION KEY (filiere_id) REFERENCES filieres(filiere_id)
      LABEL ALERT_ON_FILIERE PROPERTIES (
        alert_id, alert_code, alert_title, alert_type, severity, status, filiere_id,
        territory_id, site_id, campaign_id, opened_at, expected_resolution_at,
        impact_summary, impact_units, impact_unit_label, cause_summary,
        assigned_team, escalation_required
      ),
    operational_alerts AS alert_in_territory
      KEY (alert_id)
      SOURCE KEY (alert_id) REFERENCES operational_alerts(alert_id)
      DESTINATION KEY (territory_id) REFERENCES territories(territory_id)
      LABEL ALERT_IN_TERRITORY PROPERTIES (
        alert_id, alert_code, alert_title, alert_type, severity, status, filiere_id,
        territory_id, site_id, campaign_id, opened_at, expected_resolution_at,
        impact_summary, impact_units, impact_unit_label, cause_summary,
        assigned_team, escalation_required
      ),
    operational_alerts AS alert_at_site
      KEY (alert_id)
      SOURCE KEY (alert_id) REFERENCES operational_alerts(alert_id)
      DESTINATION KEY (site_id) REFERENCES sites(site_id)
      LABEL ALERT_AT_SITE PROPERTIES (
        alert_id, alert_code, alert_title, alert_type, severity, status, filiere_id,
        territory_id, site_id, campaign_id, opened_at, expected_resolution_at,
        impact_summary, impact_units, impact_unit_label, cause_summary,
        assigned_team, escalation_required
      ),
    operational_alerts AS alert_during_campaign
      KEY (alert_id)
      SOURCE KEY (alert_id) REFERENCES operational_alerts(alert_id)
      DESTINATION KEY (campaign_id) REFERENCES campaigns(campaign_id)
      LABEL ALERT_DURING_CAMPAIGN PROPERTIES (
        alert_id, alert_code, alert_title, alert_type, severity, status, filiere_id,
        territory_id, site_id, campaign_id, opened_at, expected_resolution_at,
        impact_summary, impact_units, impact_unit_label, cause_summary,
        assigned_team, escalation_required
      ),
    alert_brand_impacts AS alert_impacts_brand
      KEY (alert_id, brand_id)
      SOURCE KEY (alert_id) REFERENCES operational_alerts(alert_id)
      DESTINATION KEY (brand_id) REFERENCES brands(brand_id)
      LABEL ALERT_IMPACTS_BRAND PROPERTIES (
        alert_id, brand_id, impact_level, impact_description
      ),
    logistics_flows AS flow_for_filiere
      KEY (flow_id)
      SOURCE KEY (flow_id) REFERENCES logistics_flows(flow_id)
      DESTINATION KEY (filiere_id) REFERENCES filieres(filiere_id)
      LABEL FLOW_FOR_FILIERE PROPERTIES (
        flow_id, flow_code, flow_name, filiere_id, brand_id, origin_site_id,
        destination_site_id, campaign_id, transport_mode, service_level_pct,
        on_time_delivery_pct, backlog_tons, weekly_volume_tons,
        weather_risk_level, flow_status, notes
      ),
    logistics_flows AS flow_for_brand
      KEY (flow_id)
      SOURCE KEY (flow_id) REFERENCES logistics_flows(flow_id)
      DESTINATION KEY (brand_id) REFERENCES brands(brand_id)
      LABEL FLOW_FOR_BRAND PROPERTIES (
        flow_id, flow_code, flow_name, filiere_id, brand_id, origin_site_id,
        destination_site_id, campaign_id, transport_mode, service_level_pct,
        on_time_delivery_pct, backlog_tons, weekly_volume_tons,
        weather_risk_level, flow_status, notes
      ),
    logistics_flows AS flow_origin_site
      KEY (flow_id)
      SOURCE KEY (flow_id) REFERENCES logistics_flows(flow_id)
      DESTINATION KEY (origin_site_id) REFERENCES sites(site_id)
      LABEL FLOW_ORIGIN_SITE PROPERTIES (
        flow_id, flow_code, flow_name, filiere_id, brand_id, origin_site_id,
        destination_site_id, campaign_id, transport_mode, service_level_pct,
        on_time_delivery_pct, backlog_tons, weekly_volume_tons,
        weather_risk_level, flow_status, notes
      ),
    logistics_flows AS flow_destination_site
      KEY (flow_id)
      SOURCE KEY (flow_id) REFERENCES logistics_flows(flow_id)
      DESTINATION KEY (destination_site_id) REFERENCES sites(site_id)
      LABEL FLOW_DESTINATION_SITE PROPERTIES (
        flow_id, flow_code, flow_name, filiere_id, brand_id, origin_site_id,
        destination_site_id, campaign_id, transport_mode, service_level_pct,
        on_time_delivery_pct, backlog_tons, weekly_volume_tons,
        weather_risk_level, flow_status, notes
      ),
    lots AS lot_for_filiere
      KEY (lot_id)
      SOURCE KEY (lot_id) REFERENCES lots(lot_id)
      DESTINATION KEY (filiere_id) REFERENCES filieres(filiere_id)
      LABEL LOT_FOR_FILIERE PROPERTIES (
        lot_id, lot_code, filiere_id, brand_id, source_site_id, current_site_id,
        campaign_id, production_date, expiration_date, quantity, quantity_unit,
        traceability_status, quality_status, destination_market, export_flag
      ),
    lots AS lot_for_brand
      KEY (lot_id)
      SOURCE KEY (lot_id) REFERENCES lots(lot_id)
      DESTINATION KEY (brand_id) REFERENCES brands(brand_id)
      LABEL LOT_FOR_BRAND PROPERTIES (
        lot_id, lot_code, filiere_id, brand_id, source_site_id, current_site_id,
        campaign_id, production_date, expiration_date, quantity, quantity_unit,
        traceability_status, quality_status, destination_market, export_flag
      ),
    lots AS lot_source_site
      KEY (lot_id)
      SOURCE KEY (lot_id) REFERENCES lots(lot_id)
      DESTINATION KEY (source_site_id) REFERENCES sites(site_id)
      LABEL LOT_SOURCE_SITE PROPERTIES (
        lot_id, lot_code, filiere_id, brand_id, source_site_id, current_site_id,
        campaign_id, production_date, expiration_date, quantity, quantity_unit,
        traceability_status, quality_status, destination_market, export_flag
      ),
    lots AS lot_current_site
      KEY (lot_id)
      SOURCE KEY (lot_id) REFERENCES lots(lot_id)
      DESTINATION KEY (current_site_id) REFERENCES sites(site_id)
      LABEL LOT_CURRENT_SITE PROPERTIES (
        lot_id, lot_code, filiere_id, brand_id, source_site_id, current_site_id,
        campaign_id, production_date, expiration_date, quantity, quantity_unit,
        traceability_status, quality_status, destination_market, export_flag
      ),
    quality_issues AS quality_issue_on_lot
      KEY (quality_issue_id)
      SOURCE KEY (quality_issue_id) REFERENCES quality_issues(quality_issue_id)
      DESTINATION KEY (lot_id) REFERENCES lots(lot_id)
      LABEL QUALITY_ISSUE_ON_LOT PROPERTIES (
        quality_issue_id, issue_code, lot_id, site_id, brand_id, issue_category,
        severity, status, detected_at, owner_name, summary, action_required
      ),
    quality_issues AS quality_issue_for_brand
      KEY (quality_issue_id)
      SOURCE KEY (quality_issue_id) REFERENCES quality_issues(quality_issue_id)
      DESTINATION KEY (brand_id) REFERENCES brands(brand_id)
      LABEL QUALITY_ISSUE_FOR_BRAND PROPERTIES (
        quality_issue_id, issue_code, lot_id, site_id, brand_id, issue_category,
        severity, status, detected_at, owner_name, summary, action_required
      ),
    quality_issues AS quality_issue_at_site
      KEY (quality_issue_id)
      SOURCE KEY (quality_issue_id) REFERENCES quality_issues(quality_issue_id)
      DESTINATION KEY (site_id) REFERENCES sites(site_id)
      LABEL QUALITY_ISSUE_AT_SITE PROPERTIES (
        quality_issue_id, issue_code, lot_id, site_id, brand_id, issue_category,
        severity, status, detected_at, owner_name, summary, action_required
      ),
    traceability_checks AS traceability_check_on_lot
      KEY (check_id)
      SOURCE KEY (check_id) REFERENCES traceability_checks(check_id)
      DESTINATION KEY (lot_id) REFERENCES lots(lot_id)
      LABEL TRACEABILITY_CHECK_ON_LOT PROPERTIES (
        check_id, lot_id, site_id, check_date, check_status, indicator_name,
        indicator_value, threshold_value, unit_label, finding_summary,
        document_complete_flag
      ),
    traceability_checks AS traceability_check_at_site
      KEY (check_id)
      SOURCE KEY (check_id) REFERENCES traceability_checks(check_id)
      DESTINATION KEY (site_id) REFERENCES sites(site_id)
      LABEL TRACEABILITY_CHECK_AT_SITE PROPERTIES (
        check_id, lot_id, site_id, check_date, check_status, indicator_name,
        indicator_value, threshold_value, unit_label, finding_summary,
        document_complete_flag
      ),
    reference_documents AS document_for_filiere
      KEY (document_id)
      SOURCE KEY (document_id) REFERENCES reference_documents(document_id)
      DESTINATION KEY (related_filiere_id) REFERENCES filieres(filiere_id)
      LABEL DOCUMENT_FOR_FILIERE PROPERTIES (
        document_id, document_code, document_title, document_type,
        related_filiere_id, related_brand_id, related_lot_id, related_alert_id,
        version_label, owner_name, document_status, created_at
      ),
    reference_documents AS document_for_brand
      KEY (document_id)
      SOURCE KEY (document_id) REFERENCES reference_documents(document_id)
      DESTINATION KEY (related_brand_id) REFERENCES brands(brand_id)
      LABEL DOCUMENT_FOR_BRAND PROPERTIES (
        document_id, document_code, document_title, document_type,
        related_filiere_id, related_brand_id, related_lot_id, related_alert_id,
        version_label, owner_name, document_status, created_at
      ),
    reference_documents AS document_for_lot
      KEY (document_id)
      SOURCE KEY (document_id) REFERENCES reference_documents(document_id)
      DESTINATION KEY (related_lot_id) REFERENCES lots(lot_id)
      LABEL DOCUMENT_FOR_LOT PROPERTIES (
        document_id, document_code, document_title, document_type,
        related_filiere_id, related_brand_id, related_lot_id, related_alert_id,
        version_label, owner_name, document_status, created_at
      ),
    reference_documents AS document_for_alert
      KEY (document_id)
      SOURCE KEY (document_id) REFERENCES reference_documents(document_id)
      DESTINATION KEY (related_alert_id) REFERENCES operational_alerts(alert_id)
      LABEL DOCUMENT_FOR_ALERT PROPERTIES (
        document_id, document_code, document_title, document_type,
        related_filiere_id, related_brand_id, related_lot_id, related_alert_id,
        version_label, owner_name, document_status, created_at
      ),
    action_plans AS action_for_alert
      KEY (action_plan_id)
      SOURCE KEY (action_plan_id) REFERENCES action_plans(action_plan_id)
      DESTINATION KEY (alert_id) REFERENCES operational_alerts(alert_id)
      LABEL ACTION_FOR_ALERT PROPERTIES (
        action_plan_id, action_code, alert_id, brand_id, site_id, owner_name,
        priority, due_at, status, action_summary, horizon_hours
      ),
    action_plans AS action_for_brand
      KEY (action_plan_id)
      SOURCE KEY (action_plan_id) REFERENCES action_plans(action_plan_id)
      DESTINATION KEY (brand_id) REFERENCES brands(brand_id)
      LABEL ACTION_FOR_BRAND PROPERTIES (
        action_plan_id, action_code, alert_id, brand_id, site_id, owner_name,
        priority, due_at, status, action_summary, horizon_hours
      ),
    action_plans AS action_at_site
      KEY (action_plan_id)
      SOURCE KEY (action_plan_id) REFERENCES action_plans(action_plan_id)
      DESTINATION KEY (site_id) REFERENCES sites(site_id)
      LABEL ACTION_AT_SITE PROPERTIES (
        action_plan_id, action_code, alert_id, brand_id, site_id, owner_name,
        priority, due_at, status, action_summary, horizon_hours
      )
  );

SELECT COUNT(*) AS graph_count
FROM user_property_graphs
WHERE graph_name = UPPER('limagrain_operations');
