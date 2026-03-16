# region Component Definition
WIDGET_NAME = "KpiCard"
WIDGET_DESCRIPTION = """Component designed to display key performance indicators in card format with values, labels, icons, change indicators, and detailed information in a pop-out panel.
REQUIRED: dataPath (path to KPI data object with label and value).
OPTIONAL: unit (suffix like %, kWh), change (percentage delta), changeLabel (period comparison text), icon (emoji or keyword), color (theme: cyan/coral/teal/yellow/purple/green/pink/orange).
DETAILS FEATURE: Include additional fields like trend, forecast, breakdown, factors, methodology, or any contextual information. These extra fields automatically appear in the details pop-out panel when users click the KPI card. Use descriptive key names that will display well in the details panel."""

WIDGET_SCHEMA = """
[
  {{ "beginRendering": {{ "surfaceId": "kpi-dashboard","root": "main-container" }} }},
  {{ "surfaceUpdate": {{
    "surfaceId": "kpi-dashboard",
      "components": [
        {{ "id": "main-container", "component": {{ "Column": {{ "children": {{ "explicitList": ["title", "kpi-row"] }} }} }} }},
        {{ "id": "title","component": {{ "Text": {{ "usageHint": "h2", "text": {{ "literalString": "Key Performance Indicators" }} }} }} }},
        {{ "id": "kpi-row", "component": {{ "Row": {{
          "children": {{ "explicitList": ["kpi-1", "kpi-2", "kpi-3", "kpi-4"] }},
          "distribution": "spaceEvenly",
          "alignment": "stretch"
        }} }} }},
        {{ "id": "kpi-1", "weight": 1, "component": {{ "KpiCard": {{ "dataPath": "/kpi/activeOutages" }} }} }},
        {{ "id": "kpi-2", "weight": 1, "component": {{ "KpiCard": {{ "dataPath": "/kpi/customersAffected" }} }} }},
        {{ "id": "kpi-3", "weight": 1, "component": {{ "KpiCard": {{ "dataPath": "/kpi/avgResolutionTime" }} }} }},
        {{ "id": "kpi-4", "weight": 1, "component": {{ "KpiCard": {{ "dataPath": "/kpi/systemUptime" }} }} }}
      ]
    }}
  }},
  {{ "dataModelUpdate": {{
      "surfaceId": "kpi-dashboard",
      "path": "/",
      "contents": [
        {{
          "key": "kpi",
          "valueMap": [
            {{
              "key": "activeOutages",
              "valueMap": [
                {{ "key": "label", "valueString": "Active Outages" }},
                {{ "key": "value", "valueNumber": 3 }},
                {{ "key": "icon", "valueString": "warning" }},
                {{ "key": "change", "valueNumber": -25 }},
                {{ "key": "changeLabel", "valueString": "vs yesterday" }},
                {{ "key": "color", "valueString": "coral" }},
                {{ "key": "trend", "valueString": "Decreasing after storm recovery period" }},
                {{ "key": "breakdown", "valueString": "High severity: 1, Medium: 1, Low: 1" }},
                {{ "key": "primaryCause", "valueString": "Weather-related equipment failures" }}
              ]
            }},
            {{
              "key": "customersAffected",
              "valueMap": [
                {{ "key": "label", "valueString": "Customers Affected" }},
                {{ "key": "value", "valueNumber": 17550 }},
                {{ "key": "icon", "valueString": "users" }},
                {{ "key": "change", "valueNumber": -12 }},
                {{ "key": "changeLabel", "valueString": "vs yesterday" }},
                {{ "key": "color", "valueString": "yellow" }},
                {{ "key": "trend", "valueString": "Restoration in progress, improving hourly" }},
                {{ "key": "affectedAreas", "valueString": "Downtown, North District, East District" }},
                {{ "key": "estimatedRestoration", "valueString": "85% within 4 hours" }}
              ]
            }},
            {{
              "key": "avgResolutionTime",
              "valueMap": [
                {{ "key": "label", "valueString": "Avg Resolution Time" }},
                {{ "key": "value", "valueNumber": 4.2 }},
                {{ "key": "unit", "valueString": "hrs" }},
                {{ "key": "icon", "valueString": "clock" }},
                {{ "key": "change", "valueNumber": 8 }},
                {{ "key": "changeLabel", "valueString": "vs last week" }},
                {{ "key": "color", "valueString": "teal" }},
                {{ "key": "trend", "valueString": "Slightly higher due to complex outages" }},
                {{ "key": "fastestResolution", "valueString": "0.5 hrs (minor equipment)" }},
                {{ "key": "slowestResolution", "valueString": "12 hrs (substation repair)" }},
                {{ "key": "methodology", "valueString": "Rolling 7-day average" }}
              ]
            }},
            {{
              "key": "systemUptime",
              "valueMap": [
                {{ "key": "label", "valueString": "System Uptime" }},
                {{ "key": "value", "valueNumber": 99.7 }},
                {{ "key": "unit", "valueString": "%" }},
                {{ "key": "icon", "valueString": "check" }},
                {{ "key": "change", "valueNumber": 0.2 }},
                {{ "key": "changeLabel", "valueString": "vs last month" }},
                {{ "key": "color", "valueString": "cyan" }},
                {{ "key": "trend", "valueString": "Stable with gradual improvement" }},
                {{ "key": "targetUptime", "valueString": "99.9% (SLA target)" }},
                {{ "key": "lastDowntime", "valueString": "March 5, 2026 - 23 minutes" }},
                {{ "key": "factors", "valueString": "Improved monitoring, faster response teams" }}
              ]
            }}
          ]
        }}
      ]
    }}
  }}
]"""
# endregion Component Definition

