"""Data provider for traditional application - contains comprehensive data independently"""

# Outage data for traditional application
OUTAGE_DATA = {
    "outages": [
        {
            "location": "Downtown Seattle, WA",
            "start_time": "2024-02-12 14:30",
            "estimated_restoration": "2024-02-12 18:00",
            "affected_customers": 2500,
            "cause": "Transformer failure due to storm damage",
            "crew_assigned": "Team Alpha - 5 technicians",
            "priority": "Critical - Hospital in area",
            "notes": "Emergency backup generators activated at local hospital. Replacement transformer en route.",
            "status": "Active",
            "severity": "High"
        },
        {
            "location": "Portland Suburb, OR",
            "start_time": "2024-02-12 13:15",
            "estimated_restoration": "2024-02-12 16:30",
            "affected_customers": 1800,
            "cause": "Tree branch on power lines",
            "crew_assigned": "Team Beta - 3 technicians",
            "priority": "Standard residential area",
            "notes": "Diagnostic team analyzing sensor data. May require equipment replacement.",
            "status": "Investigating",
            "severity": "Medium"
        },
        {
            "location": "San Francisco Bay Area, CA",
            "start_time": "2024-02-12 12:00",
            "estimated_restoration": "2024-02-12 15:00",
            "affected_customers": 3200,
            "cause": "Equipment malfunction",
            "crew_assigned": "Team Charlie - 4 technicians",
            "priority": "Elevated - Commercial district",
            "notes": "Multiple substations affected. Rolling blackouts implemented to manage load.",
            "status": "Active",
            "severity": "High"
        },
        {
            "location": "Los Angeles Downtown, CA",
            "start_time": "2024-02-12 11:45",
            "estimated_restoration": "2024-02-12 14:30",
            "affected_customers": 4100,
            "cause": "Cable damage during construction",
            "crew_assigned": "Team Delta - 6 technicians",
            "priority": "High - Financial district impact",
            "notes": "Construction crew secured site. Cable splicing equipment deployed.",
            "status": "Active",
            "severity": "Medium"
        }
    ],
    "total_outages": 4,
    "total_affected": 11600
}

# Energy data for traditional application
ENERGY_DATA = {
    "consumption": {
        "total_mwh": 850000,
        "by_source": {
            "renewable": 420000,
            "fossil": 380000,
            "nuclear": 50000
        }
    },
    "production": {
        "total_mwh": 880000,
        "by_type": {
            "solar": 180000,
            "wind": 150000,
            "hydro": 120000,
            "coal": 200000,
            "natural_gas": 180000,
            "nuclear": 50000
        }
    },
    "efficiency_metrics": {
        "grid_efficiency": 94.2,
        "renewable_percentage": 49.5
    },
    "kpi_details": {
        "total_production": {
            "trend": "rising steadily over Q4",
            "forecast": "950000 MWh expected next month",
            "breakdown": "Solar: 45%, Wind: 30%, Hydro: 25%"
        },
        "renewable": {
            "trend": "above target of 55% renewable mix",
            "forecast": "450000 MWh expected next month",
            "breakdown": "Solar: 60%, Wind: 25%, Hydro: 15%"
        },
        "fossil": {
            "trend": "gradually decreasing as renewables increase",
            "forecast": "350000 MWh expected next month",
            "breakdown": "Natural Gas: 65%, Coal: 35%"
        },
        "nuclear": {
            "trend": "stable baseline contribution",
            "forecast": "52000 MWh expected next month",
            "breakdown": "Single reactor facility at full capacity"
        },
        "grid_efficiency": {
            "trend": "above target of 92%",
            "forecast": "95.1% expected next month",
            "factors": "Smart grid upgrades, load balancing improvements"
        }
    }
}

# Industry data for traditional application
INDUSTRY_DATA = {
    "industries": [
        {
            "name": "Manufacturing",
            "production_index": 112.5,
            "employment": 125000,
            "growth_rate": 3.2,
            "key_metrics": {
                "output_value": 450000000,
                "efficiency_score": 87.3
            }
        },
        {
            "name": "Technology",
            "production_index": 145.8,
            "employment": 98000,
            "growth_rate": 8.7,
            "key_metrics": {
                "output_value": 380000000,
                "efficiency_score": 92.1
            }
        },
        {
            "name": "Healthcare",
            "production_index": 118.3,
            "employment": 156000,
            "growth_rate": 4.1,
            "key_metrics": {
                "output_value": 520000000,
                "efficiency_score": 89.5
            }
        },
        {
            "name": "Energy",
            "production_index": 108.9,
            "employment": 67000,
            "growth_rate": 2.8,
            "key_metrics": {
                "output_value": 290000000,
                "efficiency_score": 85.7
            }
        },
        {
            "name": "Transportation",
            "production_index": 115.2,
            "employment": 89000,
            "growth_rate": 3.9,
            "key_metrics": {
                "output_value": 340000000,
                "efficiency_score": 88.2
            }
        }
    ],
    "overall_metrics": {
        "total_employment": 535000,
        "average_growth": 4.5,
        "top_performing_industry": "Technology"
    }
}

async def get_traditional_outage_data():
    """Get traditional outage data - independent from other applications"""
    # Return a copy to prevent external modifications
    import json
    return json.loads(json.dumps(OUTAGE_DATA))

async def get_traditional_energy_data():
    """Get traditional energy data - independent from other applications"""
    import json
    return json.loads(json.dumps(ENERGY_DATA))

async def get_traditional_industry_data():
    """Get traditional industry data - independent from other applications"""
    import json
    return json.loads(json.dumps(INDUSTRY_DATA))
