""" this file is for giving the client side the information about outages """
from core.traditional_data_provider import (
    get_traditional_outage_data,
    get_traditional_energy_data,
    get_traditional_industry_data
)

# Hardcoded coordinates for locations (lat, lng)
LOCATION_COORDINATES = {
    "Downtown Seattle, WA": (47.6062, -122.3321),
    "Portland Suburb, OR": (45.5152, -122.6784),
    "San Francisco Bay Area, CA": (37.7749, -122.4194),
    "Los Angeles Downtown, CA": (34.0522, -118.2437)
}

async def get_traditional_outage_messages():
    """Get formatted initial outage data as A2A ServerToClientMessage array"""

    data = await get_traditional_outage_data()

    outages = data["outages"]
    total_outages = data["total_outages"]

    # Count outages by status (including Monitoring)
    status_counts = {"Active": 0, "Investigating": 0, "Resolved": 0, "Scheduled": 0, "Monitoring": 0}
    for outage in outages:
        status = outage.get("status", "Active")
        if status in status_counts:
            status_counts[status] += 1

    outage_summary = [
        {"key": "0", "valueNumber": status_counts["Active"]},
        {"key": "1", "valueNumber": status_counts["Investigating"]},
        {"key": "2", "valueNumber": status_counts["Resolved"]},
        {"key": "3", "valueNumber": status_counts["Scheduled"]},
        {"key": "4", "valueNumber": status_counts["Monitoring"]}
    ]

    outage_summary_labels = [
        {"key": "0", "valueString": "Active"},
        {"key": "1", "valueString": "Investigating"},
        {"key": "2", "valueString": "Resolved"},
        {"key": "3", "valueString": "Scheduled"},
        {"key": "4", "valueString": "Monitoring"}
    ]

    # Build detailed information for each status category
    active_outages_list = [o for o in outages if o.get("status") == "Active"]
    investigating_outages_list = [o for o in outages if o.get("status") == "Investigating"]
    resolved_outages_list = [o for o in outages if o.get("status") == "Resolved"]
    scheduled_outages_list = [o for o in outages if o.get("status") == "Scheduled"]
    monitoring_outages_list = [o for o in outages if o.get("status") == "Monitoring"]

    def get_top_locations(outage_list, limit=3):
        if not outage_list:
            return "None"
        locations = [o["location"].split(",")[0] for o in outage_list[:limit]]
        return ", ".join(locations)

    def get_total_affected(outage_list):
        return sum(o["affected_customers"] for o in outage_list)

    def get_severity_breakdown(outage_list):
        if not outage_list:
            return "N/A"
        high = len([o for o in outage_list if o.get("severity") == "High"])
        medium = len([o for o in outage_list if o.get("severity") == "Medium"])
        low = len([o for o in outage_list if o.get("severity") == "Low"])
        return f"High: {high}, Medium: {medium}, Low: {low}"

    def get_main_causes(outage_list, limit=2):
        if not outage_list:
            return "None"
        causes = list(set([o["cause"] for o in outage_list]))[:limit]
        return ", ".join(causes) if causes else "Various"

    outage_summary_details = [
        {"key": "0", "valueMap": [
            {"key": "status", "valueString": "Active"},
            {"key": "customersAffected", "valueNumber": get_total_affected(active_outages_list)},
            {"key": "severityBreakdown", "valueString": get_severity_breakdown(active_outages_list)},
            {"key": "topAreas", "valueString": get_top_locations(active_outages_list)},
            {"key": "mainCauses", "valueString": get_main_causes(active_outages_list)},
            {"key": "priority", "valueString": "Immediate response required"}
        ]},
        {"key": "1", "valueMap": [
            {"key": "status", "valueString": "Investigating"},
            {"key": "customersAffected", "valueNumber": get_total_affected(investigating_outages_list)},
            {"key": "severityBreakdown", "valueString": get_severity_breakdown(investigating_outages_list)},
            {"key": "topAreas", "valueString": get_top_locations(investigating_outages_list)},
            {"key": "mainCauses", "valueString": get_main_causes(investigating_outages_list)},
            {"key": "estimatedResolution", "valueString": "Under assessment"}
        ]},
        {"key": "2", "valueMap": [
            {"key": "status", "valueString": "Resolved"},
            {"key": "customersRestored", "valueNumber": get_total_affected(resolved_outages_list)},
            {"key": "resolutionRate", "valueString": "100% service restored"},
            {"key": "topAreas", "valueString": get_top_locations(resolved_outages_list)},
            {"key": "mainCauses", "valueString": get_main_causes(resolved_outages_list)},
            {"key": "avgResolutionTime", "valueString": "2.5 hours"}
        ]},
        {"key": "3", "valueMap": [
            {"key": "status", "valueString": "Scheduled"},
            {"key": "plannedCustomers", "valueNumber": get_total_affected(scheduled_outages_list)},
            {"key": "scheduledWindow", "valueString": "Next 48 hours"},
            {"key": "topAreas", "valueString": get_top_locations(scheduled_outages_list)},
            {"key": "maintenanceType", "valueString": "Preventive maintenance"},
            {"key": "notificationSent", "valueString": "Yes - 72hrs advance"}
        ]},
        {"key": "4", "valueMap": [
            {"key": "status", "valueString": "Monitoring"},
            {"key": "customersWatched", "valueNumber": get_total_affected(monitoring_outages_list)},
            {"key": "monitoringLevel", "valueString": "Standard observation"},
            {"key": "topAreas", "valueString": get_top_locations(monitoring_outages_list)},
            {"key": "lastChecked", "valueString": "5 minutes ago"},
            {"key": "alertThreshold", "valueString": "Auto-escalate if no improvement"}
        ]}
    ]

    outage_table = []
    outage_table_details = []
    map_markers = []

    for i, outage in enumerate(outages):
        outage_id = f"OUT-{str(i+1).zfill(3)}"

        outage_table.append({
            "key": str(i),
            "valueMap": [
                {"key": "id", "valueString": outage_id},
                {"key": "location", "valueString": outage["location"]},
                {"key": "status", "valueString": outage.get("status", "Active")},
                {"key": "severity", "valueString": outage.get("severity", "High")},
                {"key": "startTime", "valueString": outage["start_time"]},
                {"key": "estimatedRestoration", "valueString": outage["estimated_restoration"]},
                {"key": "affectedCustomers", "valueNumber": outage["affected_customers"]}
            ]
        })

        outage_table_details.append({
            "key": str(i),
            "valueMap": [
                {"key": "outageId", "valueString": outage_id},
                {"key": "cause", "valueString": outage["cause"]},
                {"key": "crewAssigned", "valueString": outage["crew_assigned"]},
                {"key": "priority", "valueString": outage["priority"]},
                {"key": "notes", "valueString": outage["notes"]},
                {"key": "customerImpact", "valueString": f"{outage['affected_customers']} customers impacted"},
                {"key": "restorationWindow", "valueString": f"{outage['start_time']} to {outage['estimated_restoration']}"}
            ]
        })

        lat, lng = LOCATION_COORDINATES.get(outage["location"], (40.7589, -73.9851))
        map_markers.append({
            "key": str(i),
            "valueMap": [
                {"key": "name", "valueString": outage["location"]},
                {"key": "latitude", "valueNumber": lat},
                {"key": "longitude", "valueNumber": lng},
                {"key": "description", "valueString": f"{outage.get('status', 'Active')} outage affecting {outage['affected_customers']} customers"},
                {"key": "status", "valueString": outage.get("status", "Active")},
                {"key": "severity", "valueString": outage.get("severity", "High")},
                {"key": "affectedCustomers", "valueNumber": outage["affected_customers"]},
                {"key": "crew", "valueString": outage["crew_assigned"]}
            ]
        })

    energy_data = await get_traditional_energy_data()

    # Calculate some derived values
    active_outages = status_counts["Active"] + status_counts["Investigating"]
    customers_affected = sum(outage["affected_customers"] for outage in outages)

    energy_kpis = [
        {"key": "0", "valueMap": [
            {"key": "label", "valueString": "Total Production"},
            {"key": "value", "valueNumber": energy_data["production"]["total_mwh"]},
            {"key": "unit", "valueString": "MWh"},
            {"key": "change", "valueNumber": 12.5},
            {"key": "changeLabel", "valueString": "vs last month"},
            {"key": "icon", "valueString": "⚡"},
            {"key": "colorTheme", "valueString": "cyan"},
            {"key": "trend", "valueString": energy_data["kpi_details"]["total_production"]["trend"]},
            {"key": "forecast", "valueString": energy_data["kpi_details"]["total_production"]["forecast"]},
            {"key": "breakdown", "valueString": energy_data["kpi_details"]["total_production"]["breakdown"]}
        ]},
        {"key": "1", "valueMap": [
            {"key": "label", "valueString": "Active Outages"},
            {"key": "value", "valueNumber": active_outages},
            {"key": "unit", "valueString": ""},
            {"key": "change", "valueNumber": -8},
            {"key": "changeLabel", "valueString": "vs yesterday"},
            {"key": "icon", "valueString": "🔌"},
            {"key": "colorTheme", "valueString": "coral"},
            {"key": "trend", "valueString": "decreasing after storm recovery"},
            {"key": "breakdown", "valueString": f"High: {len([o for o in outages if o.get('severity') == 'High'])}, Medium: {len([o for o in outages if o.get('severity') == 'Medium'])}, Low: {len([o for o in outages if o.get('severity') == 'Low'])}"}
        ]},
        {"key": "2", "valueMap": [
            {"key": "label", "valueString": "Customers Affected"},
            {"key": "value", "valueNumber": customers_affected},
            {"key": "unit", "valueString": ""},
            {"key": "change", "valueNumber": -22},
            {"key": "changeLabel", "valueString": "vs peak"},
            {"key": "icon", "valueString": "👥"},
            {"key": "colorTheme", "valueString": "teal"},
            {"key": "trend", "valueString": "restoration in progress"},
            {"key": "affectedDistricts", "valueString": "Downtown, North, East District"}
        ]},
        {"key": "3", "valueMap": [
            {"key": "label", "valueString": "Grid Efficiency"},
            {"key": "value", "valueNumber": energy_data["efficiency_metrics"]["grid_efficiency"]},
            {"key": "unit", "valueString": "%"},
            {"key": "change", "valueNumber": 1.8},
            {"key": "changeLabel", "valueString": "vs baseline"},
            {"key": "icon", "valueString": "📊"},
            {"key": "colorTheme", "valueString": "green"},
            {"key": "trend", "valueString": energy_data["kpi_details"]["grid_efficiency"]["trend"]},
            {"key": "factors", "valueString": energy_data["kpi_details"]["grid_efficiency"]["factors"]}
        ]}
    ]

    messages = [
        {
            "dataModelUpdate": {
                "surfaceId": "default",
                "path": "/",
                "contents": [
                    {
                        "key": "outageSummary",
                        "valueMap": outage_summary
                    },
                    {
                        "key": "outageSummaryLabels",
                        "valueMap": outage_summary_labels
                    },
                    {
                        "key": "outageSummaryDetails",
                        "valueMap": outage_summary_details
                    },
                    {
                        "key": "outageTable",
                        "valueMap": outage_table
                    },
                    {
                        "key": "outageTableDetails",
                        "valueMap": outage_table_details
                    },
                    {
                        "key": "mapMarkers",
                        "valueMap": map_markers
                    },
                    {
                        "key": "energyKPIs",
                        "valueMap": energy_kpis
                    }
                ]
            }
        }
    ]

    return messages

async def get_traditional_energy_trends_messages():
    """Get formatted energy trends data as A2A ServerToClientMessage array"""
    energy_data = await get_traditional_energy_data()

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    base_production = energy_data["production"]
    energy_trend_details = [
        {"key": "0", "valueMap": [
            {"key": "period", "valueString": "January"},
            {"key": "trend", "valueString": "Lower winter generation baseline"},
            {"key": "forecast", "valueString": "Expected gradual increase"},
            {"key": "mainDriver", "valueString": "Seasonal irradiation and wind stability"}
        ]},
        {"key": "1", "valueMap": [
            {"key": "period", "valueString": "February"},
            {"key": "trend", "valueString": "Early seasonal ramp-up"},
            {"key": "forecast", "valueString": "Continued growth expected"},
            {"key": "mainDriver", "valueString": "Improving weather conditions"}
        ]},
        {"key": "2", "valueMap": [
            {"key": "period", "valueString": "March"},
            {"key": "trend", "valueString": "Strong spring momentum"},
            {"key": "forecast", "valueString": "Above-average production likely"},
            {"key": "mainDriver", "valueString": "Higher daylight hours"}
        ]},
        {"key": "3", "valueMap": [
            {"key": "period", "valueString": "April"},
            {"key": "trend", "valueString": "Peak spring acceleration"},
            {"key": "forecast", "valueString": "Near-summer levels expected"},
            {"key": "mainDriver", "valueString": "High renewable utilization"}
        ]},
        {"key": "4", "valueMap": [
            {"key": "period", "valueString": "May"},
            {"key": "trend", "valueString": "High output period"},
            {"key": "forecast", "valueString": "Stable high generation"},
            {"key": "mainDriver", "valueString": "Consistent solar and wind performance"}
        ]},
        {"key": "5", "valueMap": [
            {"key": "period", "valueString": "June"},
            {"key": "trend", "valueString": "Summer peak onset"},
            {"key": "forecast", "valueString": "Potential short-term maximum"},
            {"key": "mainDriver", "valueString": "Maximum solar contribution"}
        ]},
        {"key": "6", "valueMap": [
            {"key": "period", "valueString": "July"},
            {"key": "trend", "valueString": "Sustained summer peak"},
            {"key": "forecast", "valueString": "Slight taper expected in August"},
            {"key": "mainDriver", "valueString": "High demand and strong generation"}
        ]},
        {"key": "7", "valueMap": [
            {"key": "period", "valueString": "August"},
            {"key": "trend", "valueString": "Post-peak normalization"},
            {"key": "forecast", "valueString": "Gradual decline expected"},
            {"key": "mainDriver", "valueString": "Seasonal normalization"}
        ]},
        {"key": "8", "valueMap": [
            {"key": "period", "valueString": "September"},
            {"key": "trend", "valueString": "Early autumn decline"},
            {"key": "forecast", "valueString": "Further reduction likely"},
            {"key": "mainDriver", "valueString": "Reduced daylight and milder wind"}
        ]},
        {"key": "9", "valueMap": [
            {"key": "period", "valueString": "October"},
            {"key": "trend", "valueString": "Autumn stabilization"},
            {"key": "forecast", "valueString": "Low-volatility period expected"},
            {"key": "mainDriver", "valueString": "Balanced mixed-source output"}
        ]},
        {"key": "10", "valueMap": [
            {"key": "period", "valueString": "November"},
            {"key": "trend", "valueString": "Pre-winter lower output"},
            {"key": "forecast", "valueString": "Seasonal low likely in December"},
            {"key": "mainDriver", "valueString": "Shorter daylight window"}
        ]},
        {"key": "11", "valueMap": [
            {"key": "period", "valueString": "December"},
            {"key": "trend", "valueString": "Winter trough"},
            {"key": "forecast", "valueString": "Recovery expected in Q1"},
            {"key": "mainDriver", "valueString": "Seasonal generation constraints"}
        ]}
    ]
    energy_trend = [
        {"key": "solar", "valueMap": [
            {"key": "name", "valueString": "Solar"},
            {"key": "color", "valueString": "#FFE66D"},
            {"key": "values", "valueMap": [
                {"key": "0", "valueNumber": int(base_production["by_type"]["solar"] * 0.8)},
                {"key": "1", "valueNumber": int(base_production["by_type"]["solar"] * 0.9)},
                {"key": "2", "valueNumber": int(base_production["by_type"]["solar"] * 1.1)},
                {"key": "3", "valueNumber": int(base_production["by_type"]["solar"] * 1.2)},
                {"key": "4", "valueNumber": int(base_production["by_type"]["solar"] * 1.3)},
                {"key": "5", "valueNumber": int(base_production["by_type"]["solar"] * 1.4)},
                {"key": "6", "valueNumber": int(base_production["by_type"]["solar"] * 1.5)},
                {"key": "7", "valueNumber": int(base_production["by_type"]["solar"] * 1.3)},
                {"key": "8", "valueNumber": int(base_production["by_type"]["solar"] * 1.1)},
                {"key": "9", "valueNumber": int(base_production["by_type"]["solar"] * 0.9)},
                {"key": "10", "valueNumber": int(base_production["by_type"]["solar"] * 0.8)},
                {"key": "11", "valueNumber": int(base_production["by_type"]["solar"] * 0.7)}
            ]}
        ]},
        {"key": "wind", "valueMap": [
            {"key": "name", "valueString": "Wind"},
            {"key": "color", "valueString": "#4ECDC4"},
            {"key": "values", "valueMap": [
                {"key": "0", "valueNumber": int(base_production["by_type"]["wind"] * 0.9)},
                {"key": "1", "valueNumber": int(base_production["by_type"]["wind"] * 0.95)},
                {"key": "2", "valueNumber": int(base_production["by_type"]["wind"] * 1.0)},
                {"key": "3", "valueNumber": int(base_production["by_type"]["wind"] * 1.05)},
                {"key": "4", "valueNumber": int(base_production["by_type"]["wind"] * 1.1)},
                {"key": "5", "valueNumber": int(base_production["by_type"]["wind"] * 1.15)},
                {"key": "6", "valueNumber": int(base_production["by_type"]["wind"] * 1.1)},
                {"key": "7", "valueNumber": int(base_production["by_type"]["wind"] * 1.05)},
                {"key": "8", "valueNumber": int(base_production["by_type"]["wind"] * 1.0)},
                {"key": "9", "valueNumber": int(base_production["by_type"]["wind"] * 0.95)},
                {"key": "10", "valueNumber": int(base_production["by_type"]["wind"] * 0.9)},
                {"key": "11", "valueNumber": int(base_production["by_type"]["wind"] * 0.85)}
            ]}
        ]},
        {"key": "hydro", "valueMap": [
            {"key": "name", "valueString": "Hydro"},
            {"key": "color", "valueString": "#00D4FF"},
            {"key": "values", "valueMap": [
                {"key": "0", "valueNumber": int(base_production["by_type"]["hydro"] * 0.85)},
                {"key": "1", "valueNumber": int(base_production["by_type"]["hydro"] * 0.9)},
                {"key": "2", "valueNumber": int(base_production["by_type"]["hydro"] * 0.95)},
                {"key": "3", "valueNumber": int(base_production["by_type"]["hydro"] * 1.0)},
                {"key": "4", "valueNumber": int(base_production["by_type"]["hydro"] * 1.05)},
                {"key": "5", "valueNumber": int(base_production["by_type"]["hydro"] * 1.1)},
                {"key": "6", "valueNumber": int(base_production["by_type"]["hydro"] * 1.0)},
                {"key": "7", "valueNumber": int(base_production["by_type"]["hydro"] * 0.95)},
                {"key": "8", "valueNumber": int(base_production["by_type"]["hydro"] * 0.9)},
                {"key": "9", "valueNumber": int(base_production["by_type"]["hydro"] * 0.85)},
                {"key": "10", "valueNumber": int(base_production["by_type"]["hydro"] * 0.8)},
                {"key": "11", "valueNumber": int(base_production["by_type"]["hydro"] * 0.75)}
            ]}
        ]}
    ]

    messages = [
        {
            "dataModelUpdate": {
                "surfaceId": "default",
                "path": "/trends",
                "contents": [
                    {
                        "key": "energyTrend",
                        "valueMap": energy_trend
                    },
                    {
                        "key": "energyTrendLabels",
                        "valueMap": [{"key": str(i), "valueString": month} for i, month in enumerate(months)]
                    },
                    {
                        "key": "energyTrendDetails",
                        "valueMap": energy_trend_details
                    }
                ]
            }
        }
    ]

    return messages

async def get_traditional_timeline_messages():
    """Get formatted timeline data as A2A ServerToClientMessage array"""

    data = await get_traditional_outage_data()

    outages = data["outages"]

    timeline_events = []
    timeline_event_details = []

    for i, outage in enumerate(outages):
        # Calculate estimated duration (rough estimate based on restoration time - start time)
        from datetime import datetime
        start = datetime.fromisoformat(outage["start_time"].replace('Z', '+00:00'))
        end = datetime.fromisoformat(outage["estimated_restoration"].replace('Z', '+00:00'))
        duration_hours = int((end - start).total_seconds() / 3600)

        timeline_events.append({
            "key": str(i),
            "valueMap": [
                {"key": "date", "valueString": outage["start_time"]},
                {"key": "title", "valueString": f"Outage Reported in {outage['location']}"},
                {"key": "description", "valueString": outage["cause"]},
                {"key": "category", "valueString": outage.get("status", "Active")}
            ]
        })

        timeline_event_details.append({
            "key": str(i),
            "valueMap": [
                {"key": "status", "valueString": outage.get("status", "Active")},
                {"key": "affectedCustomers", "valueNumber": outage["affected_customers"]},
                {"key": "location", "valueString": outage["location"]},
                {"key": "assignedCrew", "valueString": outage["crew_assigned"]},
                {"key": "estimatedDuration", "valueString": f"{duration_hours} hours"},
                {"key": "estimatedRestoration", "valueString": outage["estimated_restoration"]}
            ]
        })

    messages = [
        {
            "dataModelUpdate": {
                "surfaceId": "default",
                "path": "/timeline",
                "contents": [
                    {
                        "key": "timelineEvents",
                        "valueMap": timeline_events
                    },
                    {
                        "key": "timelineEventDetails",
                        "valueMap": timeline_event_details
                    }
                ]
            }
        }
    ]

    return messages

async def get_traditional_energy_messages():
    """Get formatted energy data as A2A ServerToClientMessage array"""
    data = await get_traditional_energy_data()

    messages = [
        {
            "dataModelUpdate": {
                "surfaceId": "default",
                "path": "/",
                "contents": [
                    {
                        "key": "energyConsumption",
                        "valueMap": [
                            {"key": "total", "valueNumber": data["consumption"]["total_mwh"]},
                            {"key": "renewable", "valueNumber": data["consumption"]["by_source"]["renewable"]},
                            {"key": "fossil", "valueNumber": data["consumption"]["by_source"]["fossil"]},
                            {"key": "nuclear", "valueNumber": data["consumption"]["by_source"]["nuclear"]}
                        ]
                    },
                    {
                        "key": "energyProduction",
                        "valueMap": [
                            {"key": "total", "valueNumber": data["production"]["total_mwh"]},
                            {"key": "solar", "valueNumber": data["production"]["by_type"]["solar"]},
                            {"key": "wind", "valueNumber": data["production"]["by_type"]["wind"]},
                            {"key": "hydro", "valueNumber": data["production"]["by_type"]["hydro"]},
                            {"key": "coal", "valueNumber": data["production"]["by_type"]["coal"]},
                            {"key": "natural_gas", "valueNumber": data["production"]["by_type"]["natural_gas"]},
                            {"key": "nuclear", "valueNumber": data["production"]["by_type"]["nuclear"]}
                        ]
                    }
                ]
            }
        }
    ]

    return messages

async def get_traditional_industry_messages():
    """Get formatted industry data as A2A ServerToClientMessage array"""
    data = await get_traditional_industry_data()

    industry_table = []
    industry_table_details = []
    for i, industry in enumerate(data["industries"]):
        growth_rate = industry['growth_rate']
        efficiency_score = industry['key_metrics']['efficiency_score']
        growth_band = "High growth" if growth_rate >= 15 else "Moderate growth" if growth_rate >= 8 else "Stable growth"
        efficiency_band = "Excellent" if efficiency_score >= 92 else "Good" if efficiency_score >= 85 else "Needs improvement"

        industry_table.append({
            "key": str(i),
            "valueMap": [
                {"key": "name", "valueString": industry["name"]},
                {"key": "productionIndex", "valueNumber": industry['production_index']},
                {"key": "employment", "valueNumber": industry['employment']},
                {"key": "growthRate", "valueNumber": industry['growth_rate']},
                {"key": "outputValue", "valueNumber": industry['key_metrics']['output_value']},
                {"key": "efficiencyScore", "valueNumber": industry['key_metrics']['efficiency_score']}
            ]
        })

        industry_table_details.append({
            "key": str(i),
            "valueMap": [
                {"key": "industry", "valueString": industry["name"]},
                {"key": "growthBand", "valueString": growth_band},
                {"key": "efficiencyBand", "valueString": efficiency_band},
                {"key": "outputValueBillion", "valueString": f"{industry['key_metrics']['output_value']} B"},
                {"key": "employmentShare", "valueString": f"{round((industry['employment'] / data['overall_metrics']['total_employment']) * 100, 1)}% of total workforce"},
                {"key": "summary", "valueString": f"{industry['name']} has {growth_rate}% growth with an efficiency score of {efficiency_score}"}
            ]
        })

    messages = [
        {
            "dataModelUpdate": {
                "surfaceId": "default",
                "path": "/industry",
                "contents": [
                    {
                        "key": "industryTable",
                        "valueMap": industry_table
                    },
                    {
                        "key": "industryTableDetails",
                        "valueMap": industry_table_details
                    },
                    {
                        "key": "industryMetrics",
                        "valueMap": [
                            {"key": "total_employment", "valueNumber": data["overall_metrics"]["total_employment"]},
                            {"key": "average_growth", "valueNumber": data["overall_metrics"]["average_growth"]},
                            {"key": "top_performing_industry", "valueString": data["overall_metrics"]["top_performing_industry"]}
                        ]
                    }
                ]
            }
        }
    ]

    return messages
