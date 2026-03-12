WIDGET_NAME = "MapComponent"
WIDGET_DESCRIPTION = "Interactive map component to display location markers with a side panel showing marker details. Each marker requires coordinates (latitude/longitude), a name, and optionally: description, status, and any additional key-value pairs that will be displayed as details in the side panel when a marker is selected. For consistent userAction handling, MapComponent should define action.name as 'flag_circuit' for the flag button interaction."
WIDGET_SCHEMA = """
[
  {{ "beginRendering": {{ "surfaceId": "map-view","root": "main-column" }} }},
  {{ "surfaceUpdate": {{
    "surfaceId": "map-view",
      "components": [
        {{ "id": "main-column", "component": {{ "Column": {{ "children": {{ "explicitList": ["title", "location-map"] }} }} }} }},
        {{ "id": "title","component": {{ "Text": {{ "usageHint": "h2", "text": {{ "literalString": "Location Map" }} }} }} }},
        {{ "id": "location-map", "component": {{ "MapComponent": {{
          "dataPath": "/mapData",
          "centerLat": 40.7128,
          "centerLng": -74.0060,
          "zoom": 10,
          "showInfoPanel": true,
          "action": {{
            "name": "flag_circuit"
          }}
        }} }} }}
      ]
    }}
  }},
  {{ "dataModelUpdate": {{
      "surfaceId": "map-view",
      "path": "/",
      "contents": [
        {{
          "key": "mapData",
          "valueMap": [
            {{
              "key": "0",
              "valueMap": [
                {{
                  "key": "name",
                  "valueString": "New York Office"
                }},
                {{
                  "key": "latitude",
                  "valueNumber": 40.7128
                }},
                {{
                  "key": "longitude",
                  "valueNumber": -74.0060
                }},
                {{
                  "key": "description",
                  "valueString": "Main headquarters location"
                }},
                {{
                  "key": "status",
                  "valueString": "Active"
                }},
                {{
                  "key": "category",
                  "valueString": "Headquarters"
                }},
                {{
                  "key": "employees",
                  "valueNumber": 500
                }}
              ]
            }},
            {{
              "key": "1",
              "valueMap": [
                {{
                  "key": "name",
                  "valueString": "Boston Branch"
                }},
                {{
                  "key": "latitude",
                  "valueNumber": 42.3601
                }},
                {{
                  "key": "longitude",
                  "valueNumber": -71.0589
                }},
                {{
                  "key": "description",
                  "valueString": "Regional office for Northeast operations"
                }},
                {{
                  "key": "status",
                  "valueString": "Active"
                }},
                {{
                  "key": "category",
                  "valueString": "Regional Office"
                }},
                {{
                  "key": "employees",
                  "valueNumber": 120
                }}
              ]
            }}
          ]
        }}
      ]
    }}
  }}
]"""
