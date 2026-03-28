"""Adaptation des donnees traditionnelles LIMAGRAIN Vegetable Seeds en messages A2A."""
from core.traditional_data_provider import (
    get_traditional_outage_data,
    get_traditional_energy_data,
    get_traditional_industry_data,
)

LOCATION_COORDINATES = {
    "Clermont-Ferrand, coordination portefeuille": (45.7772, 3.0870),
    "Murcia, production semences EMEA": (37.9922, -1.1307),
    "Valencia, essais et selection": (39.4699, -0.3763),
    "Woodland, processing semences": (38.6785, -121.7733),
    "Bangkok, hub export APAC": (13.7563, 100.5018),
    "Chappes, centre qualite": (45.8686, 3.2250),
}

STATUS_ORDER = ["Ouverte", "En analyse", "Resolue", "Planifiee", "Sous surveillance"]
SEVERITY_ORDER = ["Critique", "Elevee", "Moyenne", "Faible"]
MONTH_LABELS = ["Jan", "Fev", "Mar", "Avr", "Mai", "Jun", "Jul", "Aou", "Sep", "Oct", "Nov", "Dec"]
MONTH_NAMES = [
    "Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin",
    "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Decembre",
]


def _split_alerts_by_status(alerts):
    return {status: [item for item in alerts if item.get("status") == status] for status in STATUS_ORDER}


def _severity_breakdown(alerts):
    if not alerts:
        return "Aucune"
    counts = {severity: len([item for item in alerts if item.get("severity") == severity]) for severity in SEVERITY_ORDER}
    return ", ".join(f"{severity}: {counts[severity]}" for severity in SEVERITY_ORDER if counts[severity])


def _top_locations(alerts, limit=3):
    if not alerts:
        return "Aucune"
    return ", ".join(item["location"].split(",")[0] for item in alerts[:limit])


def _main_causes(alerts, limit=2):
    if not alerts:
        return "Aucune"
    causes = []
    for alert in alerts:
        cause = alert["cause"]
        if cause not in causes:
            causes.append(cause)
        if len(causes) >= limit:
            break
    return ", ".join(causes)


def _impact_total(alerts):
    return sum(item["affected_customers"] for item in alerts)


async def get_traditional_outage_messages():
    """Retourne le tableau de bord operationnel principal."""
    data = await get_traditional_outage_data()
    operations_data = await get_traditional_energy_data()

    alerts = data["outages"]
    alerts_by_status = _split_alerts_by_status(alerts)

    summary = [
        {"key": str(index), "valueNumber": len(alerts_by_status[status])}
        for index, status in enumerate(STATUS_ORDER)
    ]
    summary_labels = [
        {"key": str(index), "valueString": status}
        for index, status in enumerate(STATUS_ORDER)
    ]
    summary_details = [
        {"key": "0", "valueMap": [
            {"key": "status", "valueString": "Ouverte"},
            {"key": "customersAffected", "valueNumber": _impact_total(alerts_by_status["Ouverte"])},
            {"key": "severityBreakdown", "valueString": _severity_breakdown(alerts_by_status["Ouverte"])},
            {"key": "topAreas", "valueString": _top_locations(alerts_by_status["Ouverte"])},
            {"key": "mainCauses", "valueString": _main_causes(alerts_by_status["Ouverte"])},
            {"key": "priority", "valueString": "Priorite immediate sur portefeuille, production et allocations clients"},
        ]},
        {"key": "1", "valueMap": [
            {"key": "status", "valueString": "En analyse"},
            {"key": "customersAffected", "valueNumber": _impact_total(alerts_by_status["En analyse"])},
            {"key": "severityBreakdown", "valueString": _severity_breakdown(alerts_by_status["En analyse"])},
            {"key": "topAreas", "valueString": _top_locations(alerts_by_status["En analyse"])},
            {"key": "mainCauses", "valueString": _main_causes(alerts_by_status["En analyse"])},
            {"key": "estimatedResolution", "valueString": "Diagnostic qualite et logistique en cours"},
        ]},
        {"key": "2", "valueMap": [
            {"key": "status", "valueString": "Resolue"},
            {"key": "customersRestored", "valueNumber": _impact_total(alerts_by_status["Resolue"])},
            {"key": "resolutionRate", "valueString": "Impacts maitrises et flux relances"},
            {"key": "topAreas", "valueString": _top_locations(alerts_by_status["Resolue"])},
            {"key": "mainCauses", "valueString": _main_causes(alerts_by_status["Resolue"])},
            {"key": "avgResolutionTime", "valueString": "7 h 40 en moyenne"},
        ]},
        {"key": "3", "valueMap": [
            {"key": "status", "valueString": "Planifiee"},
            {"key": "plannedCustomers", "valueNumber": _impact_total(alerts_by_status["Planifiee"])},
            {"key": "scheduledWindow", "valueString": "Dans les prochaines 24 heures"},
            {"key": "topAreas", "valueString": _top_locations(alerts_by_status["Planifiee"])},
            {"key": "maintenanceType", "valueString": "Maintenance preventive et lissage des flux"},
            {"key": "notificationSent", "valueString": "Oui - parties prenantes notifiees"},
        ]},
        {"key": "4", "valueMap": [
            {"key": "status", "valueString": "Sous surveillance"},
            {"key": "customersWatched", "valueNumber": _impact_total(alerts_by_status["Sous surveillance"])},
            {"key": "monitoringLevel", "valueString": "Controle renforce terrain et qualite"},
            {"key": "topAreas", "valueString": _top_locations(alerts_by_status["Sous surveillance"])},
            {"key": "lastChecked", "valueString": "Mise a jour il y a 12 minutes"},
            {"key": "alertThreshold", "valueString": "Escalade automatique si deviation supplementaire"},
        ]},
    ]

    alert_table = []
    alert_table_details = []
    map_markers = []

    for index, alert in enumerate(alerts):
        alert_id = f"ALT-{str(index + 1).zfill(3)}"
        alert_table.append({
            "key": str(index),
            "valueMap": [
                {"key": "id", "valueString": alert_id},
                {"key": "location", "valueString": alert["location"]},
                {"key": "status", "valueString": alert["status"]},
                {"key": "severity", "valueString": alert["severity"]},
                {"key": "startTime", "valueString": alert["start_time"]},
                {"key": "estimatedRestoration", "valueString": alert["estimated_restoration"]},
                {"key": "affectedCustomers", "valueNumber": alert["affected_customers"]},
            ],
        })
        alert_table_details.append({
            "key": str(index),
            "valueMap": [
                {"key": "outageId", "valueString": alert_id},
                {"key": "cause", "valueString": alert["cause"]},
                {"key": "crewAssigned", "valueString": alert["crew_assigned"]},
                {"key": "priority", "valueString": alert["priority"]},
                {"key": "notes", "valueString": alert["notes"]},
                {"key": "customerImpact", "valueString": f"{alert['affected_customers']} exploitations, lots ou unites impactes"},
                {"key": "restorationWindow", "valueString": f"{alert['start_time']} a {alert['estimated_restoration']}"},
            ],
        })
        lat, lng = LOCATION_COORDINATES.get(alert["location"], (47.4667, -0.5500))
        map_markers.append({
            "key": str(index),
            "valueMap": [
                {"key": "name", "valueString": alert["location"]},
                {"key": "latitude", "valueNumber": lat},
                {"key": "longitude", "valueNumber": lng},
                {"key": "description", "valueString": f"{alert['status']} - {alert['cause']}"},
                {"key": "status", "valueString": alert["status"]},
                {"key": "severity", "valueString": alert["severity"]},
                {"key": "affectedCustomers", "valueNumber": alert["affected_customers"]},
                {"key": "crew", "valueString": alert["crew_assigned"]},
            ],
        })

    open_alerts = len(alerts_by_status["Ouverte"]) + len(alerts_by_status["En analyse"])
    impacted_scope = sum(alert["affected_customers"] for alert in alerts)
    operations_kpis = [
        {"key": "0", "valueMap": [
            {"key": "label", "valueString": "Volumes de semences pilotes"},
            {"key": "value", "valueNumber": operations_data["production"]["total_mwh"]},
            {"key": "unit", "valueString": "t"},
            {"key": "change", "valueNumber": 6.2},
            {"key": "changeLabel", "valueString": "vs periode precedente"},
            {"key": "icon", "valueString": "🌾"},
            {"key": "colorTheme", "valueString": "cyan"},
            {"key": "trend", "valueString": operations_data["kpi_details"]["total_production"]["trend"]},
            {"key": "forecast", "valueString": operations_data["kpi_details"]["total_production"]["forecast"]},
            {"key": "breakdown", "valueString": operations_data["kpi_details"]["total_production"]["breakdown"]},
        ]},
        {"key": "1", "valueMap": [
            {"key": "label", "valueString": "Alertes ouvertes"},
            {"key": "value", "valueNumber": open_alerts},
            {"key": "unit", "valueString": ""},
            {"key": "change", "valueNumber": -14.0},
            {"key": "changeLabel", "valueString": "vs hier"},
            {"key": "icon", "valueString": "🚜"},
            {"key": "colorTheme", "valueString": "coral"},
            {"key": "trend", "valueString": operations_data["kpi_details"]["renewable"]["trend"]},
            {"key": "breakdown", "valueString": operations_data["kpi_details"]["renewable"]["breakdown"]},
        ]},
        {"key": "2", "valueMap": [
            {"key": "label", "valueString": "Perimetre impacte"},
            {"key": "value", "valueNumber": impacted_scope},
            {"key": "unit", "valueString": ""},
            {"key": "change", "valueNumber": -9.0},
            {"key": "changeLabel", "valueString": "vs pic de semaine"},
            {"key": "icon", "valueString": "🧬"},
            {"key": "colorTheme", "valueString": "teal"},
            {"key": "trend", "valueString": operations_data["kpi_details"]["fossil"]["trend"]},
            {"key": "affectedDistricts", "valueString": "HM.CLAUSE, Hazera, Vilmorin-Mikado et Limagrain Vegetable Seeds"},
        ]},
        {"key": "3", "valueMap": [
            {"key": "label", "valueString": "Service logistique"},
            {"key": "value", "valueNumber": operations_data["efficiency_metrics"]["grid_efficiency"]},
            {"key": "unit", "valueString": "%"},
            {"key": "change", "valueNumber": 1.1},
            {"key": "changeLabel", "valueString": "vs objectif"},
            {"key": "icon", "valueString": "📦"},
            {"key": "colorTheme", "valueString": "green"},
            {"key": "trend", "valueString": operations_data["kpi_details"]["grid_efficiency"]["trend"]},
            {"key": "factors", "valueString": operations_data["kpi_details"]["grid_efficiency"]["factors"]},
        ]},
    ]

    return [{
        "dataModelUpdate": {
            "surfaceId": "default",
            "path": "/",
            "contents": [
                {"key": "outageSummary", "valueMap": summary},
                {"key": "outageSummaryLabels", "valueMap": summary_labels},
                {"key": "outageSummaryDetails", "valueMap": summary_details},
                {"key": "outageTable", "valueMap": alert_table},
                {"key": "outageTableDetails", "valueMap": alert_table_details},
                {"key": "mapMarkers", "valueMap": map_markers},
                {"key": "energyKPIs", "valueMap": operations_kpis},
            ],
        }
    }]


async def get_traditional_energy_trends_messages():
    """Retourne les tendances de campagnes et filieres."""
    trend_details = [
        {"key": str(index), "valueMap": [
            {"key": "period", "valueString": MONTH_NAMES[index]},
            {"key": "trend", "valueString": trend},
            {"key": "forecast", "valueString": forecast},
            {"key": "mainDriver", "valueString": driver},
        ]}
        for index, (trend, forecast, driver) in enumerate([
            ("Suivi des stocks hivernaux et preparation des semis", "Legere hausse des commandes de semences", "Mise en place des plans de campagne"),
            ("Acceleration des travaux de printemps", "Hausse des besoins logistiques attendue", "Fenetre de semis plus favorable"),
            ("Montee en charge des interventions agronomiques", "Volumes semences au dessus du plan", "Conditions meteo plus stables"),
            ("Arbitrage capacitaire entre selection et processing", "Reequilibrage des flux de lots strategiques", "Charge varietale heterogene selon les regions"),
            ("Preparation des campagnes de lancement et des plans de stockage", "Pic d activite logistique a anticiper", "Coordination hub et transport"),
            ("Demarrage des lots ete et du processing", "Forte tension sur les capacites de traitement", "Qualite et conformite a surveiller"),
            ("Pic de processing et de preparation export", "Maintien d un niveau eleve attendu", "Disponibilite hubs et capacites logistiques"),
            ("Lissage post-pic et tri qualite", "Repli progressif des flux", "Arbitrages qualite destination"),
            ("Relance des plans de distribution export", "Hausse des commandes sur les marches prioritaires", "Constitution des stocks d automne"),
            ("Stabilisation des flux et plans commerciaux", "Activite soutenue sur HM.CLAUSE, Hazera et Vilmorin-Mikado", "Demande distributeurs et export"),
            ("Preparation des campagnes d hiver", "Remontee des besoins varietaux et commerciaux", "Pilotage budgetaire portefeuille"),
            ("Consolidation annuelle et projections", "Redemarrage progressif en janvier", "Bouclage des plans marques et filieres"),
        ])
    ]

    trend_series = [
        {"key": "collecte", "valueMap": [
            {"key": "name", "valueString": "Coordination portefeuille semences potageres"},
            {"key": "color", "valueString": "#D4A017"},
            {"key": "values", "valueMap": [{"key": str(i), "valueNumber": value} for i, value in enumerate([82, 88, 95, 101, 110, 124, 138, 132, 118, 109, 97, 90])]},
        ]},
        {"key": "export", "valueMap": [
            {"key": "name", "valueString": "Distribution export"},
            {"key": "color", "valueString": "#4ECDC4"},
            {"key": "values", "valueMap": [{"key": str(i), "valueNumber": value} for i, value in enumerate([96, 94, 98, 102, 106, 108, 111, 109, 107, 104, 101, 99])]},
        ]},
        {"key": "production", "valueMap": [
            {"key": "name", "valueString": "Production HM.CLAUSE / Hazera"},
            {"key": "color", "valueString": "#FF7F50"},
            {"key": "values", "valueMap": [{"key": str(i), "valueNumber": value} for i, value in enumerate([90, 91, 93, 95, 99, 104, 108, 107, 105, 103, 101, 98])]},
        ]},
        {"key": "marques", "valueMap": [
            {"key": "name", "valueString": "Commandes semences et filieres marqueses"},
            {"key": "color", "valueString": "#2E8B57"},
            {"key": "values", "valueMap": [{"key": str(i), "valueNumber": value} for i, value in enumerate([72, 78, 89, 98, 104, 99, 86, 79, 84, 96, 108, 115])]},
        ]},
    ]

    return [{
        "dataModelUpdate": {
            "surfaceId": "default",
            "path": "/trends",
            "contents": [
                {"key": "energyTrend", "valueMap": trend_series},
                {"key": "energyTrendLabels", "valueMap": [{"key": str(i), "valueString": label} for i, label in enumerate(MONTH_LABELS)]},
                {"key": "energyTrendDetails", "valueMap": trend_details},
            ],
        }
    }]


async def get_traditional_timeline_messages():
    """Retourne la chronologie des evenements de campagne."""
    data = await get_traditional_outage_data()
    alerts = data["outages"]
    timeline_events = []
    timeline_event_details = []

    from datetime import datetime

    for index, alert in enumerate(alerts):
        start = datetime.fromisoformat(alert["start_time"].replace("Z", "+00:00"))
        end = datetime.fromisoformat(alert["estimated_restoration"].replace("Z", "+00:00"))
        hours = round((end - start).total_seconds() / 3600, 1)
        timeline_events.append({
            "key": str(index),
            "valueMap": [
                {"key": "date", "valueString": alert["start_time"]},
                {"key": "title", "valueString": f"Alerte terrain - {alert['location']}"},
                {"key": "description", "valueString": alert["cause"]},
                {"key": "category", "valueString": alert["status"]},
            ],
        })
        timeline_event_details.append({
            "key": str(index),
            "valueMap": [
                {"key": "status", "valueString": alert["status"]},
                {"key": "affectedCustomers", "valueNumber": alert["affected_customers"]},
                {"key": "location", "valueString": alert["location"]},
                {"key": "assignedCrew", "valueString": alert["crew_assigned"]},
                {"key": "estimatedDuration", "valueString": f"{hours} heures"},
                {"key": "estimatedRestoration", "valueString": alert["estimated_restoration"]},
            ],
        })

    return [{
        "dataModelUpdate": {
            "surfaceId": "default",
            "path": "/timeline",
            "contents": [
                {"key": "timelineEvents", "valueMap": timeline_events},
                {"key": "timelineEventDetails", "valueMap": timeline_event_details},
            ],
        }
    }]


async def get_traditional_energy_messages():
    """Retourne les indicateurs de synthese de l activite cooperatrice."""
    data = await get_traditional_energy_data()
    return [{
        "dataModelUpdate": {
            "surfaceId": "default",
            "path": "/",
            "contents": [
                {"key": "energyConsumption", "valueMap": [
                    {"key": "total", "valueNumber": data["production"]["total_mwh"]},
                    {"key": "renewable", "valueNumber": data["production"]["by_type"]["wind"]},
                    {"key": "fossil", "valueNumber": data["production"]["by_type"]["hydro"]},
                    {"key": "nuclear", "valueNumber": data["production"]["by_type"]["solar"]},
                ]},
                {"key": "energyProduction", "valueMap": [
                    {"key": "total", "valueNumber": data["production"]["total_mwh"]},
                    {"key": "solar", "valueNumber": data["production"]["by_type"]["solar"]},
                    {"key": "wind", "valueNumber": data["production"]["by_type"]["wind"]},
                    {"key": "hydro", "valueNumber": data["production"]["by_type"]["hydro"]},
                    {"key": "coal", "valueNumber": data["production"]["by_type"]["coal"]},
                    {"key": "natural_gas", "valueNumber": data["production"]["by_type"]["natural_gas"]},
                    {"key": "nuclear", "valueNumber": data["production"]["by_type"]["nuclear"]},
                ]},
            ],
        }
    }]


async def get_traditional_industry_messages():
    """Retourne les performances par filiere."""
    data = await get_traditional_industry_data()
    industry_table = []
    industry_table_details = []
    for index, industry in enumerate(data["industries"]):
        growth_rate = industry["growth_rate"]
        efficiency_score = industry["key_metrics"]["efficiency_score"]
        growth_band = "Croissance forte" if growth_rate >= 7 else "Croissance moderee" if growth_rate >= 4 else "Croissance stable"
        efficiency_band = "Excellente maitrise" if efficiency_score >= 92 else "Bonne maitrise" if efficiency_score >= 86 else "Sous vigilance"
        industry_table.append({
            "key": str(index),
            "valueMap": [
                {"key": "name", "valueString": industry["name"]},
                {"key": "productionIndex", "valueNumber": industry["production_index"]},
                {"key": "employment", "valueNumber": industry["employment"]},
                {"key": "growthRate", "valueNumber": industry["growth_rate"]},
                {"key": "outputValue", "valueNumber": industry["key_metrics"]["output_value"]},
                {"key": "efficiencyScore", "valueNumber": industry["key_metrics"]["efficiency_score"]},
            ],
        })
        share = round((industry["employment"] / data["overall_metrics"]["total_employment"]) * 100, 1)
        industry_table_details.append({
            "key": str(index),
            "valueMap": [
                {"key": "industry", "valueString": industry["name"]},
                {"key": "growthBand", "valueString": growth_band},
                {"key": "efficiencyBand", "valueString": efficiency_band},
                {"key": "outputValueBillion", "valueString": f"{industry['key_metrics']['output_value']} Md EUR"},
                {"key": "employmentShare", "valueString": f"{share}% des effectifs considers"},
                {"key": "summary", "valueString": f"{industry['name']} progresse de {growth_rate}% avec un score de maitrise de {efficiency_score}"},
            ],
        })

    return [{
        "dataModelUpdate": {
            "surfaceId": "default",
            "path": "/industry",
            "contents": [
                {"key": "industryTable", "valueMap": industry_table},
                {"key": "industryTableDetails", "valueMap": industry_table_details},
                {"key": "industryMetrics", "valueMap": [
                    {"key": "total_employment", "valueNumber": data["overall_metrics"]["total_employment"]},
                    {"key": "average_growth", "valueNumber": data["overall_metrics"]["average_growth"]},
                    {"key": "top_performing_industry", "valueString": data["overall_metrics"]["top_performing_industry"]},
                ]},
            ],
        }
    }]
