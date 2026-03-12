WIDGET_NAME = "Table"
WIDGET_DESCRIPTION = """Component designed to display tabular data with configurable columns.
REQUIRED: dataPath (path to array of record objects), columns (header/field/type definitions).
OPTIONAL: detailsPath (path to array of detail objects aligned by row index; each detail object is shown in expanded row and side detail panel), title, expandable, showDetailPanel.
Use detailsPath to provide rich row-level context without duplicating visible table columns."""
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
          "detailsPath": "/tableDetails",
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
        }},
        {{
          "key": "tableDetails",
          "valueMap": [
            {{
              "key": "0",
              "valueMap": [
                {{ "key": "rootCause", "valueString": "Transformer overload" }},
                {{ "key": "affectedCustomers", "valueNumber": 1280 }},
                {{ "key": "assignedCrew", "valueString": "Team Alpha" }},
                {{ "key": "nextUpdate", "valueString": "In 30 minutes" }}
              ]
            }},
            {{
              "key": "1",
              "valueMap": [
                {{ "key": "rootCause", "valueString": "Scheduled maintenance window" }},
                {{ "key": "affectedCustomers", "valueNumber": 420 }},
                {{ "key": "assignedCrew", "valueString": "Team Delta" }},
                {{ "key": "nextUpdate", "valueString": "After completion checkpoint" }}
              ]
            }}
          ]
        }}
      ]
    }}
  }}
]"""
