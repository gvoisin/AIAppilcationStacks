import { componentRegistry } from "@a2ui/lit/ui";
import { BarGraph } from "./bar-graph.js";
import { LineGraph } from "./line-graph.js";
import { MapComponent } from "./map.js";
import { TimelineComponent } from "./timeline.js";
import { Table } from "./table.js";
import { KpiCard, KpiCardGroup } from "./kpi-card.js";
import { DetailModal } from "./detail-modal.js";

export function registerShellComponents() {
  componentRegistry.register("BarGraph", BarGraph, "bar-graph", {
    type: "object",
    properties: {
      dataPath: { type: "string", description: "Path to numeric values array" },
      labelPath: { type: "string", description: "Path to category labels array" },
      detailsPath: { type: "string", description: "Path to array of detail objects for each bar (optional). Each object contains key-value pairs to display in the details panel when a bar is clicked." },
      title: { type: "string", description: "Chart title text" },
      orientation: { type: "string", enum: ["vertical", "horizontal"] },
      barWidth: { type: "number" },
      gap: { type: "number" },
      interactive: { type: "boolean", description: "Enable hover and click interactions" },
      colorful: { type: "boolean", description: "Use different colors for each bar" },
    },
    required: ["dataPath", "labelPath"],
  });

  componentRegistry.register("LineGraph", LineGraph, "line-graph", {
    type: "object",
    properties: {
      dataPath: { type: "string", description: "Path to single series data (for backward compatibility)" },
      labelPath: { type: "string", description: "Path to x-axis labels array" },
      seriesPath: { type: "string", description: "Path to array of series objects [{name, values, color}]" },
      title: { type: "string", description: "Chart title text" },
      showPoints: { type: "boolean", description: "Show data points on the line" },
      showArea: { type: "boolean", description: "Fill area under the line" },
      strokeWidth: { type: "number", description: "Line stroke width" },
      animated: { type: "boolean", description: "Enable line drawing animation" },
      interactive: { type: "boolean", description: "Enable tooltips and point selection" },
    },
    required: ["labelPath"],
  });

  componentRegistry.register("MapComponent", MapComponent, "map-component", {
    type: "object",
    properties: {
      dataPath: { type: "string", description: "Path to array of map marker objects. Each marker object should contain: name (string), lat/latitude (number), lng/longitude (number), description (string, optional), status (string, optional), and any additional key-value pairs will be displayed as details in the side panel." },
      centerLat: { type: "number", description: "Initial center latitude of the map" },
      centerLng: { type: "number", description: "Initial center longitude of the map" },
      zoom: { type: "number", description: "Initial zoom level of the map" },
      showInfoPanel: { type: "boolean", description: "Show side info panel with marker list and details" },
    },
    required: ["dataPath"],
  });

  componentRegistry.register("TimelineComponent", TimelineComponent, "timeline-component", {
    type: "object",
    properties: {
      dataPath: { type: "string" },
      expandable: { type: "boolean", description: "Enable expandable detail panels" },
    },
    required: [],
  });

  componentRegistry.register("Table", Table, "data-table", {
    type: "object",
    properties: {
      dataPath: { type: "string", description: "Path to array of table records" },
      title: { type: "string", description: "Table title" },
      columns: {
        type: "array",
        description: "Column definitions for the table",
        items: {
          type: "object",
          properties: {
            header: { type: "string", description: "Column header text" },
            field: { type: "string", description: "Field name in the data records" },
            type: { type: "string", enum: ["string", "number", "date", "status", "severity"], description: "Data type for formatting" }
          },
          required: ["header", "field", "type"]
        }
      },
      showPagination: { type: "boolean", description: "Show pagination controls" },
      pageSize: { type: "number", description: "Number of records per page" },
      expandable: { type: "boolean", description: "Enable expandable rows" },
      showDetailPanel: { type: "boolean", description: "Show side detail panel on row selection" },
    },
    required: ["dataPath", "columns"],
  });

  componentRegistry.register("KpiCard", KpiCard, "kpi-card", {
    type: "object",
    properties: {
      dataPath: { type: "string", description: "Path to KPI data object. The data object can include: label, value, unit, change, changeLabel, icon, colorTheme, and any additional fields which will be shown as details in the pop-out panel when clicked." },
      label: { type: "string", description: "KPI label text" },
      value: { type: "number", description: "KPI value" },
      unit: { type: "string", description: "Unit suffix (e.g., %, kWh)" },
      change: { type: "number", description: "Percentage change from previous period" },
      changeLabel: { type: "string", description: "Change period label (e.g., vs last month)" },
      icon: { type: "string", description: "Icon character or emoji" },
      colorTheme: { type: "string", enum: ["cyan", "coral", "teal", "yellow", "purple", "green", "pink", "orange"] },
      compact: { type: "boolean", description: "Use compact sizing" },
      clickable: { type: "boolean", description: "Enable click to show details" },
      details: { 
        type: "object", 
        description: "Additional key-value pairs to display in the details pop-out panel when the KPI card is clicked. Use this to provide contextual information like trend analysis, forecasts, breakdowns, contributing factors, or any relevant extended information about the metric.",
        additionalProperties: true
      },
    },
    required: [],
  });

  componentRegistry.register("KpiCardGroup", KpiCardGroup, "kpi-card-group", {
    type: "object",
    properties: {
      dataPath: { type: "string", description: "Path to array of KPI data objects" },
      title: { type: "string", description: "Group title" },
      compact: { type: "boolean", description: "Use compact sizing for all cards" },
    },
    required: ["dataPath"],
  });

  componentRegistry.register("DetailModal", DetailModal, "detail-modal", {
    type: "object",
    properties: {
      open: { type: "boolean", description: "Whether the modal is visible" },
      title: { type: "string", description: "Modal title" },
      position: { type: "string", enum: ["modal", "panel", "inline"], description: "Display mode" },
      data: { type: "object", description: "Data to display in the modal" },
    },
    required: [],
  });
}
