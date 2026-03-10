WIDGET_NAME = "BarGraph"
WIDGET_DESCRIPTION = """Interactive bar chart component for comparing data values with category labels.
REQUIRED: dataPath (path to numeric values array), labelPath (path to category labels array).
OPTIONAL: detailsPath (path to array of detail objects - each object contains custom key-value pairs to display in the expanded details panel when a bar is clicked, e.g., trend info, forecasts, breakdowns), title (chart heading), interactive (enables hover tooltips and click details panel, default true), 
colorful (uses different colors per bar, default true), orientation ('vertical' or 'horizontal').
Features: hover tooltips showing value/percentage, click to show detailed panel with custom agent-provided details or default stats (rank/comparison). 
Data format: valueMap with key/valueNumber for data, key/valueString for labels, and key/valueMap containing detail key-value pairs for each bar's extra information."""

WIDGET_SCHEMA = """
[
  {{ "beginRendering": {{ "surfaceId": "bar-chart-view","root": "main-container" }} }},
  {{ "surfaceUpdate": {{
    "surfaceId": "bar-chart-view",
      "components": [
        {{ "id": "main-container", "component": {{ "Column": {{ "children": {{ "explicitList": ["bar-chart"] }} }} }} }},
        {{ "id": "bar-chart", "component": {{ "BarGraph": {{
          "dataPath": "/chartData",
          "labelPath": "/chartLabels",
          "detailsPath": "/chartDetails",
          "title": "Outages comparison by regions",
          "interactive": true,
          "colorful": true,
          "orientation": "vertical"
        }} }} }}
      ]
    }}
  }},
  {{ "dataModelUpdate": {{
      "surfaceId": "bar-chart-view",
      "path": "/",
      "contents": [
        {{
          "key": "chartData",
          "valueMap": [
            {{ "key": "0", "valueNumber": 150 }},
            {{ "key": "1", "valueNumber": 200 }},
            {{ "key": "2", "valueNumber": 100 }},
            {{ "key": "3", "valueNumber": 300 }}
          ]
        }},
        {{
          "key": "chartLabels",
          "valueMap": [
            {{ "key": "0", "valueString": "Q1" }},
            {{ "key": "1", "valueString": "Q2" }},
            {{ "key": "2", "valueString": "Q3" }},
            {{ "key": "3", "valueString": "Q4" }}
          ]
        }},
        {{
          "key": "chartDetails",
          "valueMap": [
            {{ "key": "0", "valueMap": [
              {{ "key": "trend", "valueString": "Increasing" }},
              {{ "key": "forecast", "valueString": "Expected to grow 15%" }},
              {{ "key": "primaryCause", "valueString": "Weather events" }}
            ] }},
            {{ "key": "1", "valueMap": [
              {{ "key": "trend", "valueString": "Stable" }},
              {{ "key": "forecast", "valueString": "No significant change" }},
              {{ "key": "primaryCause", "valueString": "Equipment aging" }}
            ] }},
            {{ "key": "2", "valueMap": [
              {{ "key": "trend", "valueString": "Decreasing" }},
              {{ "key": "forecast", "valueString": "Expected to drop 10%" }},
              {{ "key": "primaryCause", "valueString": "Maintenance completed" }}
            ] }},
            {{ "key": "3", "valueMap": [
              {{ "key": "trend", "valueString": "Peak period" }},
              {{ "key": "forecast", "valueString": "High demand season" }},
              {{ "key": "primaryCause", "valueString": "Grid overload" }}
            ] }}
          ]
        }}
      ]
    }}
  }}
]"""
