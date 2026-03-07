WIDGET_NAME = "Table"
WIDGET_DESCRIPTION = "component designed to display tabular data with configurable columns. Requires array of record objects and column definitions specifying headers, fields, and types."
WIDGET_SCHEMA = """
[
  {{ "beginRendering": {{ "surfaceId": "table-view","root": "main-container" }} }},
  {{ "surfaceUpdate": {{
    "surfaceId": "table-view",
      "components": [
        {{ "id": "main-container", "component": {{ "Column": {{ "children": {{ "explicitList": ["title", "data-table"] }} }} }} }},
        {{ "id": "title","component": {{ "Text": {{ "usageHint": "h2", "text": {{ "literalString": "Data Table" }} }} }} }},
        {{ "id": "data-table", "component": {{ "Table": {{
          "dataPath": "/tableData",
          "title": "Data Table",
          "columns": [
            {{ "header": "ID", "field": "id", "type": "string" }},
            {{ "header": "Name", "field": "name", "type": "string" }},
            {{ "header": "Value", "field": "value", "type": "number" }},
            {{ "header": "Status", "field": "status", "type": "status" }},
            {{ "header": "Severity", "field": "severity", "type": "severity" }},
            {{ "header": "Date", "field": "date", "type": "date" }}
          ]
        }} }} }}
      ]
    }}
  }},
  {{ "dataModelUpdate": {{
      "surfaceId": "table-view",
      "path": "/",
      "contents": [
        {{
          "key": "tableData",
          "valueMap": [
            {{
              "key": "0",
              "valueMap": [
                {{ "key": "id", "valueString": "1" }},
                {{ "key": "name", "valueString": "Item A" }},
                {{ "key": "value", "valueNumber": 100 }},
                {{ "key": "status", "valueString": "Active" }},
                {{ "key": "severity", "valueString": "High" }},
                {{ "key": "date", "valueString": "2024-01-15T14:30:00Z" }}
              ]
            }},
            {{
              "key": "1",
              "valueMap": [
                {{ "key": "id", "valueString": "2" }},
                {{ "key": "name", "valueString": "Item B" }},
                {{ "key": "value", "valueNumber": 200 }},
                {{ "key": "status", "valueString": "Resolved" }},
                {{ "key": "severity", "valueString": "Low" }},
                {{ "key": "date", "valueString": "2024-01-16T09:15:00Z" }}
              ]
            }}
          ]
        }}
      ]
    }}
  }}
]"""
