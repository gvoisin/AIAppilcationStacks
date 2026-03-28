-- Demo seed data for Terrena LLM/chat and agent sample questions.

INSERT INTO territories (territory_id, territory_name, territory_code, region_name, risk_level, logistics_pressure_score, notes) VALUES (1, 'Vendee', 'VENDEE', 'Pays de la Loire', 'CRITICAL', 91.50, 'Zone avicole sous surveillance sanitaire renforcee');
INSERT INTO territories (territory_id, territory_name, territory_code, region_name, risk_level, logistics_pressure_score, notes) VALUES (2, 'Ancenis', 'ANCENIS', 'Pays de la Loire', 'HIGH', 77.20, 'Retards de collecte et saturation transport ponctuelle');
INSERT INTO territories (territory_id, territory_name, territory_code, region_name, risk_level, logistics_pressure_score, notes) VALUES (3, 'Saumur', 'SAUMUR', 'Pays de la Loire', 'MEDIUM', 58.10, 'Flux export vins sensibles a la conformite documentaire');
INSERT INTO territories (territory_id, territory_name, territory_code, region_name, risk_level, logistics_pressure_score, notes) VALUES (4, 'Loire-Atlantique Nord', 'LANORD', 'Pays de la Loire', 'MEDIUM', 63.40, 'Zone logistique multi-marques a capacite variable');

INSERT INTO filieres (filiere_id, filiere_name, filiere_code, category, strategic_priority, active_flag) VALUES (1, 'Volailles', 'VOLAILLES', 'Elevage', 'CRITICAL', 'Y');
INSERT INTO filieres (filiere_id, filiere_name, filiere_code, category, strategic_priority, active_flag) VALUES (2, 'Grandes cultures', 'GRANDES_CULTURES', 'Collecte', 'HIGH', 'Y');
INSERT INTO filieres (filiere_id, filiere_name, filiere_code, category, strategic_priority, active_flag) VALUES (3, 'Vins', 'VINS', 'Boissons', 'HIGH', 'Y');
INSERT INTO filieres (filiere_id, filiere_name, filiere_code, category, strategic_priority, active_flag) VALUES (4, 'Semences', 'SEMENCES', 'Intrants', 'MEDIUM', 'Y');

INSERT INTO brands (brand_id, brand_name, brand_code, business_line, export_flag, quality_sensitivity) VALUES (1, 'Pere Dodu', 'PERE_DODU', 'Produits avicoles', 'N', 'CRITICAL');
INSERT INTO brands (brand_id, brand_name, brand_code, business_line, export_flag, quality_sensitivity) VALUES (2, 'Ackerman', 'ACKERMAN', 'Vins effervescents', 'Y', 'HIGH');
INSERT INTO brands (brand_id, brand_name, brand_code, business_line, export_flag, quality_sensitivity) VALUES (3, 'Douce France', 'DOUCE_FRANCE', 'Produits avicoles', 'N', 'HIGH');
INSERT INTO brands (brand_id, brand_name, brand_code, business_line, export_flag, quality_sensitivity) VALUES (4, 'La Nouvelle Agriculture', 'LNA', 'Produits agricoles sous cahier', 'N', 'HIGH');
INSERT INTO brands (brand_id, brand_name, brand_code, business_line, export_flag, quality_sensitivity) VALUES (5, 'Gastronome Professionnels', 'GASTRONOME_PRO', 'Restauration avicole', 'N', 'HIGH');
INSERT INTO brands (brand_id, brand_name, brand_code, business_line, export_flag, quality_sensitivity) VALUES (6, 'Fermier d Ancenis', 'FERMIER_ANCENIS', 'Marque locale avicole', 'N', 'MEDIUM');
INSERT INTO brands (brand_id, brand_name, brand_code, business_line, export_flag, quality_sensitivity) VALUES (7, 'Tendre et plus', 'TENDRE_PLUS', 'Produits elabores', 'N', 'MEDIUM');
INSERT INTO brands (brand_id, brand_name, brand_code, business_line, export_flag, quality_sensitivity) VALUES (8, 'D Anvial', 'D_ANVIAL', 'Distribution specialisee', 'N', 'MEDIUM');

INSERT INTO campaigns (campaign_id, campaign_name, campaign_year, season_name, start_date, end_date, status) VALUES (1, 'Campagne avicole printemps 2026', 2026, 'PRINTEMPS', DATE '2026-03-01', DATE '2026-06-30', 'ACTIVE');
INSERT INTO campaigns (campaign_id, campaign_name, campaign_year, season_name, start_date, end_date, status) VALUES (2, 'Collecte grandes cultures 2026', 2026, 'ETE', DATE '2026-06-01', DATE '2026-10-15', 'ACTIVE');
INSERT INTO campaigns (campaign_id, campaign_name, campaign_year, season_name, start_date, end_date, status) VALUES (3, 'Expeditions vins export 2026', 2026, 'ANNUEL', DATE '2026-01-01', DATE '2026-12-31', 'ACTIVE');
INSERT INTO campaigns (campaign_id, campaign_name, campaign_year, season_name, start_date, end_date, status) VALUES (4, 'Campagne semences hiver 2026', 2026, 'HIVER', DATE '2026-10-01', DATE '2027-02-28', 'PLANNED');

INSERT INTO sites (site_id, site_name, site_code, site_type, territory_id, filiere_id, city_name, capacity_tons, status) VALUES (1, 'Elevages cooperatifs Vendee Nord', 'VEN-AVL-01', 'ELEVAGE', 1, 1, 'Les Herbiers', 1800, 'DISRUPTED');
INSERT INTO sites (site_id, site_name, site_code, site_type, territory_id, filiere_id, city_name, capacity_tons, status) VALUES (2, 'Plateforme logistique Ancenis', 'ANC-LOG-01', 'PLATEFORME', 2, 2, 'Ancenis', 6200, 'WATCH');
INSERT INTO sites (site_id, site_name, site_code, site_type, territory_id, filiere_id, city_name, capacity_tons, status) VALUES (3, 'Cave export Saumur', 'SAU-VIN-01', 'CAVE', 3, 3, 'Saumur', 4100, 'WATCH');
INSERT INTO sites (site_id, site_name, site_code, site_type, territory_id, filiere_id, city_name, capacity_tons, status) VALUES (4, 'Abattoir et conditionnement Ouest', 'LAN-AVI-01', 'USINE', 4, 1, 'Ancenis-Saint-Gereon', 3500, 'ACTIVE');
INSERT INTO sites (site_id, site_name, site_code, site_type, territory_id, filiere_id, city_name, capacity_tons, status) VALUES (5, 'Silo central grandes cultures', 'ANC-GC-01', 'SILO', 2, 2, 'Mouzeil', 9200, 'WATCH');
INSERT INTO sites (site_id, site_name, site_code, site_type, territory_id, filiere_id, city_name, capacity_tons, status) VALUES (6, 'Hub distribution Loire', 'LAN-DIS-01', 'HUB', 4, NULL, 'Carquefou', 5400, 'ACTIVE');

INSERT INTO brand_filieres (brand_id, filiere_id, importance_level) VALUES (1, 1, 'CRITICAL');
INSERT INTO brand_filieres (brand_id, filiere_id, importance_level) VALUES (2, 3, 'CRITICAL');
INSERT INTO brand_filieres (brand_id, filiere_id, importance_level) VALUES (3, 1, 'HIGH');
INSERT INTO brand_filieres (brand_id, filiere_id, importance_level) VALUES (4, 2, 'CRITICAL');
INSERT INTO brand_filieres (brand_id, filiere_id, importance_level) VALUES (4, 4, 'MEDIUM');
INSERT INTO brand_filieres (brand_id, filiere_id, importance_level) VALUES (5, 1, 'HIGH');
INSERT INTO brand_filieres (brand_id, filiere_id, importance_level) VALUES (6, 1, 'MEDIUM');
INSERT INTO brand_filieres (brand_id, filiere_id, importance_level) VALUES (7, 1, 'MEDIUM');
INSERT INTO brand_filieres (brand_id, filiere_id, importance_level) VALUES (8, 1, 'MEDIUM');

INSERT INTO brand_sites (brand_id, site_id, role_name) VALUES (1, 1, 'Approvisionnement elevages');
INSERT INTO brand_sites (brand_id, site_id, role_name) VALUES (1, 4, 'Transformation principale');
INSERT INTO brand_sites (brand_id, site_id, role_name) VALUES (2, 3, 'Conditionnement export');
INSERT INTO brand_sites (brand_id, site_id, role_name) VALUES (2, 6, 'Hub expeditions');
INSERT INTO brand_sites (brand_id, site_id, role_name) VALUES (3, 4, 'Conditionnement marque');
INSERT INTO brand_sites (brand_id, site_id, role_name) VALUES (4, 2, 'Pilotage collecte');
INSERT INTO brand_sites (brand_id, site_id, role_name) VALUES (4, 5, 'Stockage central');
INSERT INTO brand_sites (brand_id, site_id, role_name) VALUES (5, 1, 'Approvisionnement elevages');
INSERT INTO brand_sites (brand_id, site_id, role_name) VALUES (6, 4, 'Transformation locale');
INSERT INTO brand_sites (brand_id, site_id, role_name) VALUES (7, 6, 'Distribution');
INSERT INTO brand_sites (brand_id, site_id, role_name) VALUES (8, 6, 'Distribution');

INSERT INTO operational_alerts (alert_id, alert_code, alert_title, alert_type, severity, status, filiere_id, territory_id, site_id, campaign_id, opened_at, expected_resolution_at, impact_summary, impact_units, impact_unit_label, cause_summary, assigned_team, escalation_required)
VALUES (1, 'ALT-AVI-001', 'Controle sanitaire renforce pour la filiere volailles en Vendee', 'SANITAIRE', 'CRITICAL', 'IN_ANALYSIS', 1, 1, 1, 1, DATE '2026-03-22', DATE '2026-03-27', '86000 animaux sous protocole renforce avec risque de desorganisation des flux amont', 86000, 'ANIMAUX', 'Renforcement preventif sanitaire sur trois elevages alimentant les lignes avicoles', 'Equipe qualite volaille Pere Dodu', 'Y');
INSERT INTO operational_alerts (alert_id, alert_code, alert_title, alert_type, severity, status, filiere_id, territory_id, site_id, campaign_id, opened_at, expected_resolution_at, impact_summary, impact_units, impact_unit_label, cause_summary, assigned_team, escalation_required)
VALUES (2, 'ALT-LOG-002', 'Retard de collecte La Nouvelle Agriculture sur Ancenis', 'LOGISTIQUE', 'HIGH', 'MITIGATING', 2, 2, 2, 2, DATE '2026-03-21', DATE '2026-03-25', '1200 tonnes de collecte a replanifier avec tension sur les navettes entre plateforme et silo', 1200, 'TONNES', 'Pluies soutenues et capacite transport sous tension sur la zone Ancenis', 'Cellule logistique Ouest', 'Y');
INSERT INTO operational_alerts (alert_id, alert_code, alert_title, alert_type, severity, status, filiere_id, territory_id, site_id, campaign_id, opened_at, expected_resolution_at, impact_summary, impact_units, impact_unit_label, cause_summary, assigned_team, escalation_required)
VALUES (3, 'ALT-TRC-003', 'Anomalie de tracabilite sur lot export Ackerman', 'TRACABILITE', 'HIGH', 'OPEN', 3, 3, 3, 3, DATE '2026-03-23', DATE '2026-03-26', 'Lot export bloque jusqu a verification documentaire complete', 1, 'LOT', 'Ecarts documentaires entre certificat de lot et expedition export', 'Qualite vins Ackerman', 'Y');
INSERT INTO operational_alerts (alert_id, alert_code, alert_title, alert_type, severity, status, filiere_id, territory_id, site_id, campaign_id, opened_at, expected_resolution_at, impact_summary, impact_units, impact_unit_label, cause_summary, assigned_team, escalation_required)
VALUES (4, 'ALT-SVC-004', 'Tension de service sur la marque Douce France a 72 heures', 'SERVICE_LEVEL', 'MEDIUM', 'OPEN', 1, 4, 4, 1, DATE '2026-03-24', DATE '2026-03-27', 'Risque de baisse de taux de service si arbitrages charge/capacite non lances rapidement', 72, 'HEURES', 'Accumulation de retards amont et pression de conditionnement sur les references avicoles', 'Coordination aval Douce France', 'Y');
INSERT INTO operational_alerts (alert_id, alert_code, alert_title, alert_type, severity, status, filiere_id, territory_id, site_id, campaign_id, opened_at, expected_resolution_at, impact_summary, impact_units, impact_unit_label, cause_summary, assigned_team, escalation_required)
VALUES (5, 'ALT-SUP-005', 'Suivi multi-marques sur Loire-Atlantique Nord', 'SUPPLY_CHAIN', 'MEDIUM', 'MONITORING', 1, 4, 6, 1, DATE '2026-03-20', DATE '2026-03-28', 'Coordination necessaire entre Fermier d Ancenis, Tendre et plus et D Anvial pour lisser les expeditions', 3, 'MARQUES', 'Capacite hub variable et priorisation quotidienne des quais', 'Supply chain Loire', 'N');

INSERT INTO alert_brand_impacts (alert_id, brand_id, impact_level, impact_description) VALUES (1, 1, 'CRITICAL', 'Approvisionnement Pere Dodu fragilise par le protocole sanitaire');
INSERT INTO alert_brand_impacts (alert_id, brand_id, impact_level, impact_description) VALUES (1, 5, 'HIGH', 'Gastronome Professionnels expose a une tension de volumes sur 72 heures');
INSERT INTO alert_brand_impacts (alert_id, brand_id, impact_level, impact_description) VALUES (1, 3, 'HIGH', 'Douce France peut subir des arbitrages de capacite en conditionnement');
INSERT INTO alert_brand_impacts (alert_id, brand_id, impact_level, impact_description) VALUES (2, 4, 'CRITICAL', 'La Nouvelle Agriculture subit des retards de collecte et des reports de stockage');
INSERT INTO alert_brand_impacts (alert_id, brand_id, impact_level, impact_description) VALUES (3, 2, 'CRITICAL', 'Ackerman a un lot export bloque en attente de preuve documentaire');
INSERT INTO alert_brand_impacts (alert_id, brand_id, impact_level, impact_description) VALUES (4, 3, 'HIGH', 'Douce France risque une baisse de niveau de service a court terme');
INSERT INTO alert_brand_impacts (alert_id, brand_id, impact_level, impact_description) VALUES (5, 6, 'MEDIUM', 'Fermier d Ancenis depend du lissage des quais du hub Loire');
INSERT INTO alert_brand_impacts (alert_id, brand_id, impact_level, impact_description) VALUES (5, 7, 'MEDIUM', 'Tendre et plus depend des memes slots de preparation');
INSERT INTO alert_brand_impacts (alert_id, brand_id, impact_level, impact_description) VALUES (5, 8, 'MEDIUM', 'D Anvial partage les capacites aval et les tournees');

INSERT INTO logistics_flows (flow_id, flow_code, flow_name, filiere_id, brand_id, origin_site_id, destination_site_id, campaign_id, transport_mode, service_level_pct, on_time_delivery_pct, backlog_tons, weekly_volume_tons, weather_risk_level, flow_status, notes)
VALUES (1, 'FLOW-AVI-001', 'Flux volailles Vendee vers conditionnement Ouest', 1, 1, 1, 4, 1, 'CAMION_FRIGO', 88.40, 84.20, 95, 420, 'MEDIUM', 'DEGRADED', 'Flux cle pour Pere Dodu avec controle sanitaire renforce');
INSERT INTO logistics_flows (flow_id, flow_code, flow_name, filiere_id, brand_id, origin_site_id, destination_site_id, campaign_id, transport_mode, service_level_pct, on_time_delivery_pct, backlog_tons, weekly_volume_tons, weather_risk_level, flow_status, notes)
VALUES (2, 'FLOW-AVI-002', 'Flux volailles Vendee vers restauration professionnelle', 1, 5, 1, 6, 1, 'CAMION_FRIGO', 90.10, 86.50, 60, 250, 'MEDIUM', 'WATCH', 'Flux de bascule partielle possible vers Gastronome Professionnels');
INSERT INTO logistics_flows (flow_id, flow_code, flow_name, filiere_id, brand_id, origin_site_id, destination_site_id, campaign_id, transport_mode, service_level_pct, on_time_delivery_pct, backlog_tons, weekly_volume_tons, weather_risk_level, flow_status, notes)
VALUES (3, 'FLOW-GC-003', 'Collecte grandes cultures Ancenis vers silo central', 2, 4, 2, 5, 2, 'BENNE', 81.70, 79.30, 430, 1600, 'HIGH', 'DEGRADED', 'Performance logistique affaiblie par la pluie et la rotation des bennes');
INSERT INTO logistics_flows (flow_id, flow_code, flow_name, filiere_id, brand_id, origin_site_id, destination_site_id, campaign_id, transport_mode, service_level_pct, on_time_delivery_pct, backlog_tons, weekly_volume_tons, weather_risk_level, flow_status, notes)
VALUES (4, 'FLOW-VIN-004', 'Expeditions vins Ackerman vers hub Loire', 3, 2, 3, 6, 3, 'CAMION', 93.20, 91.40, 28, 210, 'LOW', 'WATCH', 'Flux export penalise par les blocages documentaires sur certains lots');
INSERT INTO logistics_flows (flow_id, flow_code, flow_name, filiere_id, brand_id, origin_site_id, destination_site_id, campaign_id, transport_mode, service_level_pct, on_time_delivery_pct, backlog_tons, weekly_volume_tons, weather_risk_level, flow_status, notes)
VALUES (5, 'FLOW-AVI-005', 'Distribution Douce France depuis conditionnement Ouest', 1, 3, 4, 6, 1, 'CAMION_FRIGO', 87.10, 85.80, 75, 310, 'LOW', 'WATCH', 'Flux sensible aux arbitrages de quai et aux retards amont');

INSERT INTO lots (lot_id, lot_code, filiere_id, brand_id, source_site_id, current_site_id, campaign_id, production_date, expiration_date, quantity, quantity_unit, traceability_status, quality_status, destination_market, export_flag)
VALUES (1, 'LOT-ACK-2403', 3, 2, 3, 3, 3, DATE '2026-03-18', DATE '2027-03-18', 18000, 'BOUTEILLES', 'AT_RISK', 'REVIEW', 'EXPORT', 'Y');
INSERT INTO lots (lot_id, lot_code, filiere_id, brand_id, source_site_id, current_site_id, campaign_id, production_date, expiration_date, quantity, quantity_unit, traceability_status, quality_status, destination_market, export_flag)
VALUES (2, 'LOT-PD-7821', 1, 1, 1, 4, 1, DATE '2026-03-20', DATE '2026-04-15', 24000, 'KG', 'WATCH', 'REVIEW', 'FRANCE', 'N');
INSERT INTO lots (lot_id, lot_code, filiere_id, brand_id, source_site_id, current_site_id, campaign_id, production_date, expiration_date, quantity, quantity_unit, traceability_status, quality_status, destination_market, export_flag)
VALUES (3, 'LOT-DF-6104', 1, 3, 1, 4, 1, DATE '2026-03-21', DATE '2026-04-12', 17500, 'KG', 'WATCH', 'CONFORMING', 'FRANCE', 'N');
INSERT INTO lots (lot_id, lot_code, filiere_id, brand_id, source_site_id, current_site_id, campaign_id, production_date, expiration_date, quantity, quantity_unit, traceability_status, quality_status, destination_market, export_flag)
VALUES (4, 'LOT-LNA-9030', 2, 4, 2, 5, 2, DATE '2026-03-19', DATE '2026-09-30', 980, 'TONNES', 'CLEAR', 'CONFORMING', 'FRANCE', 'N');
INSERT INTO lots (lot_id, lot_code, filiere_id, brand_id, source_site_id, current_site_id, campaign_id, production_date, expiration_date, quantity, quantity_unit, traceability_status, quality_status, destination_market, export_flag)
VALUES (5, 'LOT-FDA-3302', 1, 6, 4, 6, 1, DATE '2026-03-22', DATE '2026-04-11', 8400, 'KG', 'CLEAR', 'CONFORMING', 'FRANCE', 'N');

INSERT INTO quality_issues (quality_issue_id, issue_code, lot_id, site_id, brand_id, issue_category, severity, status, detected_at, owner_name, summary, action_required)
VALUES (1, 'QI-ACK-01', 1, 3, 2, 'TRACABILITE_EXPORT', 'HIGH', 'ESCALATED', DATE '2026-03-23', 'Responsable qualite Ackerman', 'Piece documentaire manquante sur le lot export Ackerman', 'Valider le dossier documentaire et notifier le responsable export');
INSERT INTO quality_issues (quality_issue_id, issue_code, lot_id, site_id, brand_id, issue_category, severity, status, detected_at, owner_name, summary, action_required)
VALUES (2, 'QI-PD-02', 2, 4, 1, 'SANITAIRE_AMONT', 'CRITICAL', 'UNDER_REVIEW', DATE '2026-03-22', 'Equipe qualite volaille Pere Dodu', 'Suspicion de non-conformite sanitaire sur lots amont Vendee', 'Maintenir les controles renforces et reprioriser les ordres de fabrication');
INSERT INTO quality_issues (quality_issue_id, issue_code, lot_id, site_id, brand_id, issue_category, severity, status, detected_at, owner_name, summary, action_required)
VALUES (3, 'QI-DF-03', 3, 4, 3, 'SERVICE_NIVEAU', 'MEDIUM', 'OPEN', DATE '2026-03-24', 'Responsable qualite Douce France', 'Tension entre niveau de service et capacite de verification finale', 'Remonter les sujets sensibles au responsable qualite et ajuster le plan de controle');

INSERT INTO traceability_checks (check_id, lot_id, site_id, check_date, check_status, indicator_name, indicator_value, threshold_value, unit_label, finding_summary, document_complete_flag)
VALUES (1, 1, 3, DATE '2026-03-23', 'FAIL', 'Taux de completude documentaire', 72, 98, 'PCT', 'Le dossier export Ackerman est incomplet pour un certificat', 'N');
INSERT INTO traceability_checks (check_id, lot_id, site_id, check_date, check_status, indicator_name, indicator_value, threshold_value, unit_label, finding_summary, document_complete_flag)
VALUES (2, 1, 3, DATE '2026-03-23', 'WARNING', 'Score de correspondance lot-expedition', 89, 95, 'PCT', 'Correspondance partielle entre etiquette lot et expedition', 'N');
INSERT INTO traceability_checks (check_id, lot_id, site_id, check_date, check_status, indicator_name, indicator_value, threshold_value, unit_label, finding_summary, document_complete_flag)
VALUES (3, 2, 4, DATE '2026-03-22', 'WARNING', 'Delai de remontee terrain', 14, 8, 'HEURES', 'Les remontees terrain prennent plus de temps que la cible', 'Y');
INSERT INTO traceability_checks (check_id, lot_id, site_id, check_date, check_status, indicator_name, indicator_value, threshold_value, unit_label, finding_summary, document_complete_flag)
VALUES (4, 3, 4, DATE '2026-03-24', 'PASS', 'Conformite etiquetage final', 99, 98, 'PCT', 'Etiquetage final conforme sur le lot Douce France', 'Y');
INSERT INTO traceability_checks (check_id, lot_id, site_id, check_date, check_status, indicator_name, indicator_value, threshold_value, unit_label, finding_summary, document_complete_flag)
VALUES (5, 4, 5, DATE '2026-03-21', 'PASS', 'Tracabilite collecte', 97, 95, 'PCT', 'La collecte LNA reste conforme malgre les retards', 'Y');

INSERT INTO reference_documents (document_id, document_code, document_title, document_type, related_filiere_id, related_brand_id, related_lot_id, related_alert_id, version_label, owner_name, document_status, created_at)
VALUES (1, 'DOC-AVI-01', 'Procedure de gestion sanitaire volailles Vendee', 'PROCEDURE', 1, 1, 2, 1, 'v3', 'Direction qualite volailles', 'ACTIVE', DATE '2026-01-15');
INSERT INTO reference_documents (document_id, document_code, document_title, document_type, related_filiere_id, related_brand_id, related_lot_id, related_alert_id, version_label, owner_name, document_status, created_at)
VALUES (2, 'DOC-VIN-02', 'Checklist export et tracabilite Ackerman', 'CHECKLIST', 3, 2, 1, 3, 'v2', 'Qualite vins Ackerman', 'ACTIVE', DATE '2026-02-10');
INSERT INTO reference_documents (document_id, document_code, document_title, document_type, related_filiere_id, related_brand_id, related_lot_id, related_alert_id, version_label, owner_name, document_status, created_at)
VALUES (3, 'DOC-LNA-03', 'Guide collecte et arbitrage logistique La Nouvelle Agriculture', 'GUIDE', 2, 4, 4, 2, 'v1', 'Coordination collecte', 'ACTIVE', DATE '2026-02-20');
INSERT INTO reference_documents (document_id, document_code, document_title, document_type, related_filiere_id, related_brand_id, related_lot_id, related_alert_id, version_label, owner_name, document_status, created_at)
VALUES (4, 'DOC-DF-04', 'Points de vigilance qualite Douce France', 'NOTE', 1, 3, 3, 4, 'v1', 'Responsable qualite Douce France', 'ACTIVE', DATE '2026-03-01');

INSERT INTO action_plans (action_plan_id, action_code, alert_id, brand_id, site_id, owner_name, priority, due_at, status, action_summary, horizon_hours)
VALUES (1, 'ACT-001', 1, 1, 4, 'Directeur filiere volailles', 'CRITICAL', DATE '2026-03-25', 'IN_PROGRESS', 'Securiser les volumes Pere Dodu et recalibrer les affectations de lots sur 72 heures', 72);
INSERT INTO action_plans (action_plan_id, action_code, alert_id, brand_id, site_id, owner_name, priority, due_at, status, action_summary, horizon_hours)
VALUES (2, 'ACT-002', 1, 5, 6, 'Supply chain restauration professionnelle', 'HIGH', DATE '2026-03-25', 'OPEN', 'Preparer un plan de bascule de volumes pour Gastronome Professionnels', 72);
INSERT INTO action_plans (action_plan_id, action_code, alert_id, brand_id, site_id, owner_name, priority, due_at, status, action_summary, horizon_hours)
VALUES (3, 'ACT-003', 2, 4, 2, 'Responsable collecte LNA', 'HIGH', DATE '2026-03-25', 'IN_PROGRESS', 'Prioriser les navettes et sites tampons pour proteger la collecte La Nouvelle Agriculture', 48);
INSERT INTO action_plans (action_plan_id, action_code, alert_id, brand_id, site_id, owner_name, priority, due_at, status, action_summary, horizon_hours)
VALUES (4, 'ACT-004', 3, 2, 3, 'Responsable export Ackerman', 'CRITICAL', DATE '2026-03-24', 'OPEN', 'Lever le blocage documentaire du lot export Ackerman et reprogrammer l expedition', 24);
INSERT INTO action_plans (action_plan_id, action_code, alert_id, brand_id, site_id, owner_name, priority, due_at, status, action_summary, horizon_hours)
VALUES (5, 'ACT-005', 4, 3, 4, 'Directeur service client Douce France', 'HIGH', DATE '2026-03-26', 'OPEN', 'Prioriser les actions pour proteger le niveau de service Douce France sur 72 heures', 72);
INSERT INTO action_plans (action_plan_id, action_code, alert_id, brand_id, site_id, owner_name, priority, due_at, status, action_summary, horizon_hours)
VALUES (6, 'ACT-006', 5, 6, 6, 'Coordinateur supply chain Loire', 'MEDIUM', DATE '2026-03-26', 'IN_PROGRESS', 'Coordonner Fermier d Ancenis, Tendre et plus et D Anvial sur les quais disponibles', 72);
INSERT INTO action_plans (action_plan_id, action_code, alert_id, brand_id, site_id, owner_name, priority, due_at, status, action_summary, horizon_hours)
VALUES (7, 'ACT-007', 5, 7, 6, 'Coordinateur supply chain Loire', 'MEDIUM', DATE '2026-03-26', 'OPEN', 'Ajuster les vagues de preparation Tendre et plus selon la capacite du hub', 72);
INSERT INTO action_plans (action_plan_id, action_code, alert_id, brand_id, site_id, owner_name, priority, due_at, status, action_summary, horizon_hours)
VALUES (8, 'ACT-008', 5, 8, 6, 'Coordinateur supply chain Loire', 'MEDIUM', DATE '2026-03-26', 'OPEN', 'Sequencer les expeditions D Anvial pour limiter les congestions de quai', 72);

COMMIT;