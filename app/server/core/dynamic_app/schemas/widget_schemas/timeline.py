# region Component Definition
WIDGET_NAME = "TimelineComponent"
WIDGET_DESCRIPTION = """Component designed to show events over time.
REQUIRED: dataPath with core timeline fields (date, title, optional description/category).
OPTIONAL: detailsPath (array of custom detail objects aligned by event index for expanded panel), expandable, compactPreview (keep collapsed cards concise and show description in expanded panel), action.
For consistent userAction handling, set action.name to 'queue_timeline_event' for the timeline action button."""
WIDGET_SCHEMA = """
[
  {{ "beginRendering": {{ "surfaceId": "timeline-view","root": "main-column" }} }},
  {{ "surfaceUpdate": {{
    "surfaceId": "timeline-view",
      "components": [
        {{ "id": "main-column", "component": {{ "Column": {{ "children": {{ "explicitList": ["title", "event-timeline"] }} }} }} }},
        {{ "id": "title","component": {{ "Text": {{ "usageHint": "h2", "text": {{ "literalString": "Event Timeline" }} }} }} }},
        {{ "id": "event-timeline", "component": {{ "TimelineComponent": {{
          "dataPath": "/timelineData",
          "detailsPath": "/timelineDetails",
          "expandable": true,
          "compactPreview": true,
          "action": {{ "name": "queue_timeline_event" }},
          "actionLabel": "Queue Event"
        }} }} }}
      ]
    }}
  }},
  {{ "dataModelUpdate": {{
      "surfaceId": "timeline-view",
      "path": "/",
      "contents": [
        {{
          "key": "timelineData",
          "valueMap": [
            {{
              "key": "0",
              "valueMap": [
                {{
                  "key": "date",
                  "valueString": "2023-01-15"
                }},
                {{
                  "key": "title",
                  "valueString": "Project Start"
                }},
                {{
                  "key": "description",
                  "valueString": "Initial project kickoff"
                }},
                {{
                  "key": "category",
                  "valueString": "Planning"
                }}
              ]
            }},
            {{
              "key": "1",
              "valueMap": [
                {{
                  "key": "date",
                  "valueString": "2023-06-01"
                }},
                {{
                  "key": "title",
                  "valueString": "First Release"
                }},
                {{
                  "key": "description",
                  "valueString": "Beta version released"
                }},
                {{
                  "key": "category",
                  "valueString": "Release"
                }}
              ]
            }}
          ]
        }},
        {{
          "key": "timelineDetails",
          "valueMap": [
            {{
              "key": "0",
              "valueMap": [
                {{ "key": "owner", "valueString": "Program Management" }},
                {{ "key": "impact", "valueString": "Project officially started" }},
                {{ "key": "nextMilestone", "valueString": "Requirements freeze" }}
              ]
            }},
            {{
              "key": "1",
              "valueMap": [
                {{ "key": "owner", "valueString": "Release Engineering" }},
                {{ "key": "impact", "valueString": "Beta feedback collection began" }},
                {{ "key": "nextMilestone", "valueString": "General availability prep" }}
              ]
            }}
          ]
        }}
      ]
    }}
  }}
]"""
# endregion Component Definition

