-- Donnees de demonstration pour les scenarios LLM/chat et agents LIMAGRAIN Vegetable Seeds.
-- Contexte client base sur les informations officielles de la ligne de metier
-- LIMAGRAIN Vegetable Seeds et sur les marques officielles HM.CLAUSE, Hazera,
-- Vilmorin-Mikado et Vilmorin.

INSERT INTO territories (territory_id, territory_name, territory_code, region_name, risk_level, logistics_pressure_score, notes) VALUES (1, 'Auvergne', 'AUVERGNE', 'France', 'MEDIUM', 64.20, 'Territoire d ancrage cooperatif et de coordination centrale du groupe');
INSERT INTO territories (territory_id, territory_name, territory_code, region_name, risk_level, logistics_pressure_score, notes) VALUES (2, 'Europe du Sud', 'SOUTH_EU', 'EMEA', 'HIGH', 79.40, 'Campagne printaniere de semences potageres sous tension avec sequencement complexe et flux transfrontaliers');
INSERT INTO territories (territory_id, territory_name, territory_code, region_name, risk_level, logistics_pressure_score, notes) VALUES (3, 'Amerique du Nord', 'NORTH_AM', 'Americas', 'MEDIUM', 68.10, 'Zone importante pour le marche, le processing et la coordination des essais varietaux');
INSERT INTO territories (territory_id, territory_name, territory_code, region_name, risk_level, logistics_pressure_score, notes) VALUES (4, 'Asie-Pacifique', 'APAC', 'APAC', 'HIGH', 82.70, 'Region prioritaire pour les lancements export avec flux de semences sensibles a la conformite documentaire');

INSERT INTO filieres (filiere_id, filiere_name, filiere_code, category, strategic_priority, active_flag) VALUES (1, 'Selection semences potageres', 'VEG_BREEDING', 'Recherche', 'CRITICAL', 'Y');
INSERT INTO filieres (filiere_id, filiere_name, filiere_code, category, strategic_priority, active_flag) VALUES (2, 'Production semences potageres', 'VEG_PRODUCTION', 'Operations semences', 'CRITICAL', 'Y');
INSERT INTO filieres (filiere_id, filiere_name, filiere_code, category, strategic_priority, active_flag) VALUES (3, 'Processing et qualite semences potageres', 'VEG_PROCESSING', 'Qualite industrielle', 'HIGH', 'Y');
INSERT INTO filieres (filiere_id, filiere_name, filiere_code, category, strategic_priority, active_flag) VALUES (4, 'Distribution commerciale semences potageres', 'VEG_DISTRIBUTION', 'Operations commerciales', 'HIGH', 'Y');

INSERT INTO brands (brand_id, brand_name, brand_code, business_line, export_flag, quality_sensitivity) VALUES (1, 'HM.CLAUSE', 'HM_CLAUSE', 'Semences potageres', 'Y', 'CRITICAL');
INSERT INTO brands (brand_id, brand_name, brand_code, business_line, export_flag, quality_sensitivity) VALUES (2, 'Hazera', 'HAZERA', 'Semences potageres', 'Y', 'CRITICAL');
INSERT INTO brands (brand_id, brand_name, brand_code, business_line, export_flag, quality_sensitivity) VALUES (3, 'Vilmorin-Mikado', 'VILMORIN_MIKADO', 'Semences potageres', 'Y', 'HIGH');
INSERT INTO brands (brand_id, brand_name, brand_code, business_line, export_flag, quality_sensitivity) VALUES (4, 'Vilmorin', 'VILMORIN', 'Semences potageres', 'Y', 'HIGH');
INSERT INTO brands (brand_id, brand_name, brand_code, business_line, export_flag, quality_sensitivity) VALUES (5, 'Limagrain Vegetable Seeds', 'LG_VEG_SEEDS', 'Portefeuille global semences potageres', 'Y', 'CRITICAL');

INSERT INTO campaigns (campaign_id, campaign_name, campaign_year, season_name, start_date, end_date, status) VALUES (1, 'Campagne mondiale printemps 2026 semences potageres', 2026, 'PRINTEMPS', DATE '2026-02-15', DATE '2026-06-30', 'ACTIVE');
INSERT INTO campaigns (campaign_id, campaign_name, campaign_year, season_name, start_date, end_date, status) VALUES (2, 'Campagne ete 2026 production et processing semences', 2026, 'ETE', DATE '2026-05-15', DATE '2026-09-30', 'ACTIVE');
INSERT INTO campaigns (campaign_id, campaign_name, campaign_year, season_name, start_date, end_date, status) VALUES (3, 'Planification automne 2026 des expeditions export', 2026, 'AUTOMNE', DATE '2026-08-15', DATE '2026-11-30', 'PLANNED');
INSERT INTO campaigns (campaign_id, campaign_name, campaign_year, season_name, start_date, end_date, status) VALUES (4, 'Essais mondiaux et nouvelles varietes 2026', 2026, 'ANNUEL', DATE '2026-01-01', DATE '2026-12-31', 'ACTIVE');

INSERT INTO sites (site_id, site_name, site_code, site_type, territory_id, filiere_id, city_name, capacity_tons, status) VALUES (1, 'Hub de coordination portefeuille Auvergne', 'AUV-HQ-01', 'HQ', 1, 4, 'Clermont-Ferrand', 0, 'ACTIVE');
INSERT INTO sites (site_id, site_name, site_code, site_type, territory_id, filiere_id, city_name, capacity_tons, status) VALUES (2, 'Centre selection et essais Europe du Sud', 'SEU-RD-01', 'R_AND_D', 2, 1, 'Valencia', 120, 'WATCH');
INSERT INTO sites (site_id, site_name, site_code, site_type, territory_id, filiere_id, city_name, capacity_tons, status) VALUES (3, 'Plateforme nord-americaine de processing semences', 'NAM-PRC-01', 'PROCESSING', 3, 3, 'Woodland', 1800, 'ACTIVE');
INSERT INTO sites (site_id, site_name, site_code, site_type, territory_id, filiere_id, city_name, capacity_tons, status) VALUES (4, 'Hub de distribution export Asie-Pacifique', 'APC-LOG-01', 'HUB', 4, 4, 'Bangkok', 950, 'WATCH');
INSERT INTO sites (site_id, site_name, site_code, site_type, territory_id, filiere_id, city_name, capacity_tons, status) VALUES (5, 'Reseau production semences EMEA', 'SEU-PROD-01', 'PRODUCTION', 2, 2, 'Murcia', 2400, 'WATCH');
INSERT INTO sites (site_id, site_name, site_code, site_type, territory_id, filiere_id, city_name, capacity_tons, status) VALUES (6, 'Centre global qualite et conformite', 'AUV-QLT-01', 'QUALITY', 1, 3, 'Chappes', 600, 'ACTIVE');

INSERT INTO brand_filieres (brand_id, filiere_id, importance_level) VALUES (1, 1, 'CRITICAL');
INSERT INTO brand_filieres (brand_id, filiere_id, importance_level) VALUES (1, 4, 'HIGH');
INSERT INTO brand_filieres (brand_id, filiere_id, importance_level) VALUES (2, 2, 'CRITICAL');
INSERT INTO brand_filieres (brand_id, filiere_id, importance_level) VALUES (2, 3, 'HIGH');
INSERT INTO brand_filieres (brand_id, filiere_id, importance_level) VALUES (3, 1, 'HIGH');
INSERT INTO brand_filieres (brand_id, filiere_id, importance_level) VALUES (3, 4, 'HIGH');
INSERT INTO brand_filieres (brand_id, filiere_id, importance_level) VALUES (4, 4, 'HIGH');
INSERT INTO brand_filieres (brand_id, filiere_id, importance_level) VALUES (5, 1, 'CRITICAL');
INSERT INTO brand_filieres (brand_id, filiere_id, importance_level) VALUES (5, 2, 'CRITICAL');
INSERT INTO brand_filieres (brand_id, filiere_id, importance_level) VALUES (5, 3, 'CRITICAL');
INSERT INTO brand_filieres (brand_id, filiere_id, importance_level) VALUES (5, 4, 'CRITICAL');

INSERT INTO brand_sites (brand_id, site_id, role_name) VALUES (1, 2, 'Coordination selection et essais regionaux');
INSERT INTO brand_sites (brand_id, site_id, role_name) VALUES (1, 3, 'Support processing pour lancements commerciaux');
INSERT INTO brand_sites (brand_id, site_id, role_name) VALUES (2, 5, 'Coordination production semences');
INSERT INTO brand_sites (brand_id, site_id, role_name) VALUES (2, 4, 'Distribution marches export');
INSERT INTO brand_sites (brand_id, site_id, role_name) VALUES (3, 2, 'Evaluation varietale et essais');
INSERT INTO brand_sites (brand_id, site_id, role_name) VALUES (3, 4, 'Distribution commerciale en Asie-Pacifique');
INSERT INTO brand_sites (brand_id, site_id, role_name) VALUES (4, 1, 'Coordination portefeuille et marque');
INSERT INTO brand_sites (brand_id, site_id, role_name) VALUES (4, 6, 'Gouvernance qualite et documentation');
INSERT INTO brand_sites (brand_id, site_id, role_name) VALUES (5, 1, 'Coordination globale de la ligne de metier');
INSERT INTO brand_sites (brand_id, site_id, role_name) VALUES (5, 6, 'Supervision qualite globale');

INSERT INTO operational_alerts (alert_id, alert_code, alert_title, alert_type, severity, status, filiere_id, territory_id, site_id, campaign_id, opened_at, expected_resolution_at, impact_summary, impact_units, impact_unit_label, cause_summary, assigned_team, escalation_required)
VALUES (1, 'ALT-SEED-001', 'Variabilite de germination detectee sur des lots strategiques tomate et poivron pour la campagne de printemps', 'QUALITY', 'CRITICAL', 'IN_ANALYSIS', 3, 2, 6, 1, DATE '2026-03-22', DATE '2026-03-28', 'Six lots a forte valeur necessitent un renforcement des controles avant allocation commerciale aux producteurs', 6, 'LOTS', 'Les premiers controles laboratoire montrent une performance de germination irreguliere par rapport a la cible interne de liberation', 'Equipe qualite globale semences potageres', 'Y');
INSERT INTO operational_alerts (alert_id, alert_code, alert_title, alert_type, severity, status, filiere_id, territory_id, site_id, campaign_id, opened_at, expected_resolution_at, impact_summary, impact_units, impact_unit_label, cause_summary, assigned_team, escalation_required)
VALUES (2, 'ALT-SEED-002', 'Retard sur les mouvements transfrontaliers de lots de production semences en Europe du Sud', 'LOGISTIQUE', 'HIGH', 'MITIGATING', 2, 2, 5, 2, DATE '2026-03-21', DATE '2026-03-26', 'Environ 320 tonnes de stocks de production doivent etre replannifiees entre sites de production et de processing', 320, 'TONNES', 'Les contraintes de sequencing transport et les revues documentaires douanieres ralentissent les transferts entre sites', 'Planification operations semences EMEA', 'Y');
INSERT INTO operational_alerts (alert_id, alert_code, alert_title, alert_type, severity, status, filiere_id, territory_id, site_id, campaign_id, opened_at, expected_resolution_at, impact_summary, impact_units, impact_unit_label, cause_summary, assigned_team, escalation_required)
VALUES (3, 'ALT-SEED-003', 'Ecart de conformite export identifie sur des expeditions de lancement en Asie-Pacifique', 'TRACABILITE', 'HIGH', 'OPEN', 4, 4, 4, 3, DATE '2026-03-23', DATE '2026-03-27', 'Trois expeditions export restent en attente de liberation finale jusqu a reconciliation des documents phytosanitaires et des references lot', 3, 'EXPEDITIONS', 'Discordance entre les references des listes colisage et le dossier final de conformite export', 'Operations clients et conformite APAC', 'Y');
INSERT INTO operational_alerts (alert_id, alert_code, alert_title, alert_type, severity, status, filiere_id, territory_id, site_id, campaign_id, opened_at, expected_resolution_at, impact_summary, impact_units, impact_unit_label, cause_summary, assigned_team, escalation_required)
VALUES (4, 'ALT-SEED-004', 'Tension sur la capacite d essais pour l evaluation de nouvelles varietes avant decisions commerciales', 'CAPACITY', 'MEDIUM', 'MONITORING', 1, 3, 2, 4, DATE '2026-03-20', DATE '2026-04-05', 'Environ 180 essais doivent etre repriorises entre equipes de selection et fenetres agronomiques regionales', 180, 'ESSAIS', 'La charge d essais atteint un pic car plusieurs programmes strategiques convergent sur la meme fenetre de planification', 'Equipe excellence selection globale', 'N');
INSERT INTO operational_alerts (alert_id, alert_code, alert_title, alert_type, severity, status, filiere_id, territory_id, site_id, campaign_id, opened_at, expected_resolution_at, impact_summary, impact_units, impact_unit_label, cause_summary, assigned_team, escalation_required)
VALUES (5, 'ALT-SEED-005', 'Tension de niveau de service sur les livraisons de semences potageres vers des distributeurs prioritaires en Asie-Pacifique', 'SERVICE_LEVEL', 'HIGH', 'OPEN', 4, 4, 4, 1, DATE '2026-03-24', DATE '2026-03-29', 'La performance de livraison a l heure pourrait passer sous la cible pour plusieurs assortiments prioritaires', 5, 'DISTRIBUTEURS', 'L accumulation de lancements, de revues documentaires et de contraintes capacitaires sur le hub pese sur la semaine', 'Control tower distribution APAC', 'Y');

INSERT INTO alert_brand_impacts (alert_id, brand_id, impact_level, impact_description) VALUES (1, 1, 'CRITICAL', 'Les liberations commerciales HM.CLAUSE sur tomate et poivron peuvent etre retardees en attente de revue germination renforcee');
INSERT INTO alert_brand_impacts (alert_id, brand_id, impact_level, impact_description) VALUES (1, 2, 'HIGH', 'Hazera est impactee sur les protocoles communs de liberation qualite de lots strategiques');
INSERT INTO alert_brand_impacts (alert_id, brand_id, impact_level, impact_description) VALUES (1, 5, 'CRITICAL', 'Le portefeuille global semences potageres est expose sur la credibilite qualite de la campagne de printemps');
INSERT INTO alert_brand_impacts (alert_id, brand_id, impact_level, impact_description) VALUES (2, 2, 'CRITICAL', 'Les transferts de production Hazera en Europe du Sud sont directement exposes a la replannification et a l usage de stocks tampons');
INSERT INTO alert_brand_impacts (alert_id, brand_id, impact_level, impact_description) VALUES (2, 5, 'HIGH', 'Limagrain Vegetable Seeds subit une pression plus large sur le planning de production EMEA');
INSERT INTO alert_brand_impacts (alert_id, brand_id, impact_level, impact_description) VALUES (3, 3, 'HIGH', 'Les expeditions de lancement Vilmorin-Mikado vers l APAC peuvent glisser jusqu a reconciliation documentaire complete');
INSERT INTO alert_brand_impacts (alert_id, brand_id, impact_level, impact_description) VALUES (3, 4, 'MEDIUM', 'Les equipes Vilmorin peuvent devoir resequencer les allocations clients sur certains marches export');
INSERT INTO alert_brand_impacts (alert_id, brand_id, impact_level, impact_description) VALUES (4, 1, 'MEDIUM', 'Les equipes selection HM.CLAUSE doivent reprioriser les essais et le support agronomique local');
INSERT INTO alert_brand_impacts (alert_id, brand_id, impact_level, impact_description) VALUES (4, 3, 'MEDIUM', 'Les calendriers d evaluation varietale Vilmorin-Mikado sont sous tension');
INSERT INTO alert_brand_impacts (alert_id, brand_id, impact_level, impact_description) VALUES (5, 2, 'HIGH', 'La performance de distribution Hazera en APAC peut se degrader sur des assortiments cle semences potageres');
INSERT INTO alert_brand_impacts (alert_id, brand_id, impact_level, impact_description) VALUES (5, 3, 'HIGH', 'Les niveaux de service Vilmorin-Mikado sont exposes sur des livraisons distributeurs tres sensibles au delai');
INSERT INTO alert_brand_impacts (alert_id, brand_id, impact_level, impact_description) VALUES (5, 5, 'HIGH', 'La ligne de metier est exposee sur la satisfaction client et la bonne execution des lancements en APAC');

INSERT INTO logistics_flows (flow_id, flow_code, flow_name, filiere_id, brand_id, origin_site_id, destination_site_id, campaign_id, transport_mode, service_level_pct, on_time_delivery_pct, backlog_tons, weekly_volume_tons, weather_risk_level, flow_status, notes)
VALUES (1, 'FLOW-SEED-001', 'Flux production Europe du Sud vers processing Amerique du Nord', 2, 2, 5, 3, 2, 'CONTAINER', 86.40, 83.90, 72, 210, 'MEDIUM', 'DEGRADED', 'Flux cle Hazera sous pression de replannification');
INSERT INTO logistics_flows (flow_id, flow_code, flow_name, filiere_id, brand_id, origin_site_id, destination_site_id, campaign_id, transport_mode, service_level_pct, on_time_delivery_pct, backlog_tons, weekly_volume_tons, weather_risk_level, flow_status, notes)
VALUES (2, 'FLOW-SEED-002', 'Flux processing Amerique du Nord vers distribution APAC pour lancements HM.CLAUSE', 4, 1, 3, 4, 1, 'AIR_FREIGHT', 88.10, 84.70, 18, 55, 'LOW', 'WATCH', 'Flux rapide sensible au timing de liberation et a la documentation export');
INSERT INTO logistics_flows (flow_id, flow_code, flow_name, filiere_id, brand_id, origin_site_id, destination_site_id, campaign_id, transport_mode, service_level_pct, on_time_delivery_pct, backlog_tons, weekly_volume_tons, weather_risk_level, flow_status, notes)
VALUES (3, 'FLOW-SEED-003', 'Flux echantillons selection Europe du Sud vers distribution APAC', 1, 3, 2, 4, 4, 'AIR_FREIGHT', 90.20, 87.50, 9, 16, 'LOW', 'WATCH', 'Flux Vilmorin-Mikado pour introductions regionales et support lancement');
INSERT INTO logistics_flows (flow_id, flow_code, flow_name, filiere_id, brand_id, origin_site_id, destination_site_id, campaign_id, transport_mode, service_level_pct, on_time_delivery_pct, backlog_tons, weekly_volume_tons, weather_risk_level, flow_status, notes)
VALUES (4, 'FLOW-SEED-004', 'Flux liberation qualite Auvergne vers hub export APAC', 3, 5, 6, 4, 3, 'EXPRESS', 84.60, 81.20, 12, 28, 'LOW', 'DEGRADED', 'Les validations globales sont ralenties par les reconciliations documentaires');
INSERT INTO logistics_flows (flow_id, flow_code, flow_name, filiere_id, brand_id, origin_site_id, destination_site_id, campaign_id, transport_mode, service_level_pct, on_time_delivery_pct, backlog_tons, weekly_volume_tons, weather_risk_level, flow_status, notes)
VALUES (5, 'FLOW-SEED-005', 'Flux coordination portefeuille Auvergne vers planification production Europe du Sud', 4, 4, 1, 5, 1, 'DIGITAL_WORKFLOW', 94.30, 92.80, 0, 0, 'LOW', 'NORMAL', 'Instructions de portefeuille et de planification pour les assortiments semences potageres');

INSERT INTO lots (lot_id, lot_code, filiere_id, brand_id, source_site_id, current_site_id, campaign_id, production_date, expiration_date, quantity, quantity_unit, traceability_status, quality_status, destination_market, export_flag)
VALUES (1, 'LOT-HMC-TOM-2603', 3, 1, 5, 6, 1, DATE '2026-03-14', DATE '2028-03-14', 2400, 'UNITES_SEMENCES', 'AT_RISK', 'REVIEW', 'APAC', 'Y');
INSERT INTO lots (lot_id, lot_code, filiere_id, brand_id, source_site_id, current_site_id, campaign_id, production_date, expiration_date, quantity, quantity_unit, traceability_status, quality_status, destination_market, export_flag)
VALUES (2, 'LOT-HAZ-PEP-2603', 2, 2, 5, 3, 2, DATE '2026-03-16', DATE '2028-03-16', 3100, 'UNITES_SEMENCES', 'WATCH', 'REVIEW', 'EMEA', 'Y');
INSERT INTO lots (lot_id, lot_code, filiere_id, brand_id, source_site_id, current_site_id, campaign_id, production_date, expiration_date, quantity, quantity_unit, traceability_status, quality_status, destination_market, export_flag)
VALUES (3, 'LOT-VMK-CAR-2603', 4, 3, 3, 4, 3, DATE '2026-03-18', DATE '2028-03-18', 1800, 'UNITES_SEMENCES', 'AT_RISK', 'CONFORMING', 'APAC', 'Y');
INSERT INTO lots (lot_id, lot_code, filiere_id, brand_id, source_site_id, current_site_id, campaign_id, production_date, expiration_date, quantity, quantity_unit, traceability_status, quality_status, destination_market, export_flag)
VALUES (4, 'LOT-VIL-LET-2603', 4, 4, 6, 4, 1, DATE '2026-03-17', DATE '2028-03-17', 2200, 'UNITES_SEMENCES', 'WATCH', 'CONFORMING', 'APAC', 'Y');
INSERT INTO lots (lot_id, lot_code, filiere_id, brand_id, source_site_id, current_site_id, campaign_id, production_date, expiration_date, quantity, quantity_unit, traceability_status, quality_status, destination_market, export_flag)
VALUES (5, 'LOT-LGV-MEL-2603', 1, 5, 2, 2, 4, DATE '2026-03-12', DATE '2028-03-12', 950, 'UNITES_ESSAIS', 'CLEAR', 'CONFORMING', 'GLOBAL', 'N');

INSERT INTO quality_issues (quality_issue_id, issue_code, lot_id, site_id, brand_id, issue_category, severity, status, detected_at, owner_name, summary, action_required)
VALUES (1, 'QI-HMC-01', 1, 6, 1, 'GERMINATION_VARIABILITY', 'CRITICAL', 'UNDER_REVIEW', DATE '2026-03-22', 'Responsable qualite globale HM.CLAUSE', 'Le lot strategique tomate HM.CLAUSE montre une dispersion de germination par rapport a la cible de liberation', 'Maintenir le lot en attente, etendre les controles laboratoire et valider les options de reallocation avec le commerce');
INSERT INTO quality_issues (quality_issue_id, issue_code, lot_id, site_id, brand_id, issue_category, severity, status, detected_at, owner_name, summary, action_required)
VALUES (2, 'QI-HAZ-02', 2, 3, 2, 'PRODUCTION_TRANSFER_DELAY', 'HIGH', 'OPEN', DATE '2026-03-21', 'Responsable operations semences Hazera', 'Le lot poivron Hazera accuse un retard entre noeuds de production et de processing', 'Replanifier les transferts, valider les clients prioritaires et proteger les dates de liberation des assortiments engages');
INSERT INTO quality_issues (quality_issue_id, issue_code, lot_id, site_id, brand_id, issue_category, severity, status, detected_at, owner_name, summary, action_required)
VALUES (3, 'QI-VMK-03', 3, 4, 3, 'EXPORT_DOCUMENT_ALIGNMENT', 'HIGH', 'ESCALATED', DATE '2026-03-23', 'Responsable conformite APAC Vilmorin-Mikado', 'Le dossier export ne s aligne pas completement avec les references finales de lot pour le lancement APAC', 'Reconciler les identifiants lot, completer le dossier de conformite et confirmer la sequence de lancement par distributeur');

INSERT INTO traceability_checks (check_id, lot_id, site_id, check_date, check_status, indicator_name, indicator_value, threshold_value, unit_label, finding_summary, document_complete_flag)
VALUES (1, 1, 6, DATE '2026-03-22', 'FAIL', 'Performance de germination', 82, 90, 'PCT', 'Le lot HM.CLAUSE reste sous le seuil interne de liberation sur un cycle de verification', 'Y');
INSERT INTO traceability_checks (check_id, lot_id, site_id, check_date, check_status, indicator_name, indicator_value, threshold_value, unit_label, finding_summary, document_complete_flag)
VALUES (2, 1, 6, DATE '2026-03-22', 'WARNING', 'Completude documentaire de liberation lot', 94, 100, 'PCT', 'Les pieces de support sont presque completes mais la preuve finale de liberation reste en attente', 'N');
INSERT INTO traceability_checks (check_id, lot_id, site_id, check_date, check_status, indicator_name, indicator_value, threshold_value, unit_label, finding_summary, document_complete_flag)
VALUES (3, 2, 3, DATE '2026-03-21', 'WARNING', 'Delai de transfert', 11, 7, 'JOURS', 'Le lot Hazera depasse le delai cible entre production et processing', 'Y');
INSERT INTO traceability_checks (check_id, lot_id, site_id, check_date, check_status, indicator_name, indicator_value, threshold_value, unit_label, finding_summary, document_complete_flag)
VALUES (4, 3, 4, DATE '2026-03-23', 'FAIL', 'Completude dossier export', 78, 98, 'PCT', 'Le dossier d expedition APAC est incomplet pour une liberation finale', 'N');
INSERT INTO traceability_checks (check_id, lot_id, site_id, check_date, check_status, indicator_name, indicator_value, threshold_value, unit_label, finding_summary, document_complete_flag)
VALUES (5, 5, 2, DATE '2026-03-20', 'PASS', 'Conformite identite semences essais', 99, 98, 'PCT', 'Le materiel d essai global reste conforme pour la planification varietale', 'Y');

INSERT INTO reference_documents (document_id, document_code, document_title, document_type, related_filiere_id, related_brand_id, related_lot_id, related_alert_id, version_label, owner_name, document_status, created_at)
VALUES (1, 'DOC-LGVS-01', 'Procedure globale de liberation et revue germination semences potageres', 'PROCEDURE', 3, 5, 1, 1, 'v3', 'Cellule qualite globale semences potageres', 'ACTIVE', DATE '2026-01-18');
INSERT INTO reference_documents (document_id, document_code, document_title, document_type, related_filiere_id, related_brand_id, related_lot_id, related_alert_id, version_label, owner_name, document_status, created_at)
VALUES (2, 'DOC-HAZ-02', 'Checklist de mitigation des transferts semences Europe du Sud', 'CHECKLIST', 2, 2, 2, 2, 'v2', 'Planification operations semences EMEA', 'ACTIVE', DATE '2026-02-12');
INSERT INTO reference_documents (document_id, document_code, document_title, document_type, related_filiere_id, related_brand_id, related_lot_id, related_alert_id, version_label, owner_name, document_status, created_at)
VALUES (3, 'DOC-VMK-03', 'Guide de conformite export APAC pour les expeditions de lancement semences potageres', 'GUIDE', 4, 3, 3, 3, 'v1', 'Cellule conformite APAC', 'ACTIVE', DATE '2026-02-25');
INSERT INTO reference_documents (document_id, document_code, document_title, document_type, related_filiere_id, related_brand_id, related_lot_id, related_alert_id, version_label, owner_name, document_status, created_at)
VALUES (4, 'DOC-HMC-04', 'Note de priorisation des essais pour les programmes strategiques de selection', 'NOTE', 1, 1, 5, 4, 'v1', 'Equipe excellence selection globale', 'ACTIVE', DATE '2026-03-01');

INSERT INTO action_plans (action_plan_id, action_code, alert_id, brand_id, site_id, owner_name, priority, due_at, status, action_summary, horizon_hours)
VALUES (1, 'ACT-LGVS-001', 1, 1, 6, 'Directeur qualite global semences potageres', 'CRITICAL', DATE '2026-03-25', 'IN_PROGRESS', 'Finaliser la decision de germination renforcee pour les lots HM.CLAUSE et confirmer liberation commerciale ou quarantaine', 72);
INSERT INTO action_plans (action_plan_id, action_code, alert_id, brand_id, site_id, owner_name, priority, due_at, status, action_summary, horizon_hours)
VALUES (2, 'ACT-LGVS-002', 1, 5, 6, 'Responsable gouvernance qualite de la ligne de metier', 'CRITICAL', DATE '2026-03-25', 'OPEN', 'Preparer une communication portefeuille et des options de remplacement pour les lots de la campagne de printemps', 72);
INSERT INTO action_plans (action_plan_id, action_code, alert_id, brand_id, site_id, owner_name, priority, due_at, status, action_summary, horizon_hours)
VALUES (3, 'ACT-LGVS-003', 2, 2, 5, 'Responsable operations semences EMEA', 'HIGH', DATE '2026-03-26', 'IN_PROGRESS', 'Resequencer les transferts de production Hazera et proteger d abord les engagements clients a plus forte valeur', 96);
INSERT INTO action_plans (action_plan_id, action_code, alert_id, brand_id, site_id, owner_name, priority, due_at, status, action_summary, horizon_hours)
VALUES (4, 'ACT-LGVS-004', 3, 3, 4, 'Responsable conformite APAC', 'CRITICAL', DATE '2026-03-24', 'OPEN', 'Fermer les ecarts documentaires APAC sur les expeditions Vilmorin-Mikado et autoriser le depart', 24);
INSERT INTO action_plans (action_plan_id, action_code, alert_id, brand_id, site_id, owner_name, priority, due_at, status, action_summary, horizon_hours)
VALUES (5, 'ACT-LGVS-005', 4, 1, 2, 'Directeur programmes selection globale', 'MEDIUM', DATE '2026-03-31', 'OPEN', 'Prioriser les essais et reaffecter la capacite agronomique sur les programmes de selection les plus strategiques', 168);
INSERT INTO action_plans (action_plan_id, action_code, alert_id, brand_id, site_id, owner_name, priority, due_at, status, action_summary, horizon_hours)
VALUES (6, 'ACT-LGVS-006', 5, 2, 4, 'Responsable operations clients APAC', 'HIGH', DATE '2026-03-26', 'OPEN', 'Proteger les niveaux de service distributeurs Hazera en resequencant les expeditions et les vagues de livraison', 48);
INSERT INTO action_plans (action_plan_id, action_code, alert_id, brand_id, site_id, owner_name, priority, due_at, status, action_summary, horizon_hours)
VALUES (7, 'ACT-LGVS-007', 5, 3, 4, 'Responsable lancements commerciaux APAC', 'HIGH', DATE '2026-03-26', 'IN_PROGRESS', 'Reconfirmer les priorites de lancement Vilmorin-Mikado et aligner les promesses distributeurs avec la capacite hub', 48);
INSERT INTO action_plans (action_plan_id, action_code, alert_id, brand_id, site_id, owner_name, priority, due_at, status, action_summary, horizon_hours)
VALUES (8, 'ACT-LGVS-008', 5, 5, 4, 'Responsable satisfaction client globale', 'HIGH', DATE '2026-03-27', 'OPEN', 'Escalader la watchlist de risque livraison APAC et coordonner une mitigation portefeuille pour les distributeurs prioritaires', 72);

COMMIT;
