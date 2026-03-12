import { html, css, svg } from "lit";
import { property, customElement, state } from "lit/decorators.js";
import { Root } from "@a2ui/lit/ui";
import { colors } from "../../theme/design-tokens.js";

interface SeriesData {
  name: string;
  values: number[];
  color: string;
}

interface DetailRecord {
  [key: string]: any;
}

interface ChartPoint {
  x: number;
  y: number;
  value: number;
  label: string;
  index?: number;
  seriesName?: string;
  seriesColor?: string;
}

interface TooltipData {
  x: number;
  y: number;
  point: ChartPoint;
  visible: boolean;
}

const SERIES_COLORS = [
  colors.oracle.primary,
  colors.oracle.secondary,
  colors.semantic.success, 
  colors.oracle.accent, 
  colors.chat.bgSecondary,    
  colors.semantic.warning,    
  colors.chat.bg,             
  colors.semantic.error,     
];

@customElement('line-graph')
export class LineGraph extends Root {
  @property({ attribute: false }) accessor dataPath: any = "";
  @property({ attribute: false }) accessor labelPath: any = "";
  @property({ attribute: false }) accessor seriesPath: any = "";
  @property({ attribute: false }) accessor detailsPath: any = "";
  @property({ attribute: false }) accessor title: string = "Trend Analysis";
  @property({ attribute: false }) accessor showPoints: boolean = true;
  @property({ attribute: false }) accessor showArea: boolean = false;
  @property({ attribute: false }) accessor strokeWidth: number = 2;
  @property({ attribute: false }) accessor animated: boolean = true;
  @property({ attribute: false }) accessor interactive: boolean = true;

  @state() accessor tooltip: TooltipData = { x: 0, y: 0, point: { x: 0, y: 0, value: 0, label: '' }, visible: false };
  @state() accessor selectedPoint: ChartPoint | null = null;
  @state() accessor hoveredSeries: string | null = null;
  @state() accessor showDetails: boolean = false;
  @state() accessor detailsData: { point: ChartPoint, series: SeriesData, allSeries: SeriesData[], customDetails?: DetailRecord } | null = null;

  static styles = [
    ...Root.styles,
    css`
      :host {
        display: block;
        background: var(--module-agent-bg);
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-lg);
        padding: var(--space-xl);
        margin: var(--space-xs);
        overflow: hidden;
      }

      .line-chart {
        width: 100%;
        font-family: var(--font-family);
      }

      .chart-title {
        text-align: center;
        margin-bottom: var(--space-xl);
        font-size: 20px;
        font-weight: var(--font-weight-semibold);
        color: var(--text-primary);
        letter-spacing: 0.5px;
      }

      .chart-wrapper {
        display: flex;
        align-items: flex-start;
      }

      .y-axis-labels {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 260px;
        padding-right: 10px;
        padding-top: 5px;
        padding-bottom: 5px;
      }

      .y-label {
        font-size: 11px;
        color: var(--text-secondary);
        text-align: right;
        min-width: 35px;
      }

      .chart-area {
        flex: 1;
        display: flex;
        flex-direction: column;
      }

      .chart-container {
        position: relative;
        width: 100%;
        height: 260px;
        border-left: 1px solid var(--border-primary);
        border-bottom: 1px solid var(--border-primary);
      }

      .chart-svg {
        width: 100%;
        height: 100%;
        overflow: visible;
      }

      .grid-line {
        stroke: var(--border-secondary);
        stroke-width: 1;
        stroke-dasharray: 3, 6;
      }

      .data-line {
        fill: none;
        stroke-linecap: round;
        stroke-linejoin: round;
      }

      .data-line.animated {
        stroke-dasharray: 2000;
        stroke-dashoffset: 2000;
        animation: drawLine 1.5s ease-out forwards;
      }

      @keyframes drawLine {
        to {
          stroke-dashoffset: 0;
        }
      }

      .data-area {
        opacity: 0.15;
      }

      .data-area.animated {
        opacity: 0;
        animation: fadeInArea 0.8s ease-out 1s forwards;
      }

      @keyframes fadeInArea {
        to {
          opacity: 0.15;
        }
      }

      .data-point {
        cursor: pointer;
        transition: transform var(--transition-normal);
      }

      .data-point:hover {
        transform: scale(1.5);
      }

      .data-point.animated {
        opacity: 0;
        animation: fadeInPoint 0.3s ease-out forwards;
      }

      @keyframes fadeInPoint {
        to {
          opacity: 1;
        }
      }

      .x-axis-labels {
        display: flex;
        justify-content: space-between;
        padding-top: var(--space-sm);
        padding-left: 0;
        padding-right: 0;
      }

      .x-label {
        font-size: 11px;
        color: var(--text-secondary);
        text-align: center;
        flex: 1;
      }

      .empty-state {
        text-align: center;
        color: var(--text-muted);
        padding: 40px var(--space-lg);
        font-style: italic;
      }

      .legend {
        display: flex;
        justify-content: center;
        flex-wrap: wrap;
        gap: var(--space-lg);
        margin-top: var(--space-xl);
        padding-top: var(--space-md);
        border-top: 1px solid var(--border-primary);
      }

      .legend-item {
        display: flex;
        align-items: center;
        gap: var(--space-sm);
        font-size: 13px;
        color: var(--text-secondary);
        cursor: pointer;
        padding: 6px 12px;
        border-radius: var(--radius-xl);
        background: var(--surface-secondary);
        transition: all var(--transition-normal);
      }

      .legend-item:hover {
        background: var(--surface-elevated);
        transform: translateY(-2px);
      }

      .legend-dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
      }

      .legend-line {
        width: 24px;
        height: 3px;
        border-radius: var(--radius-sm);
      }

      /* Tooltip styles */
      .chart-tooltip {
        position: absolute;
        background: var(--surface-elevated);
        border: 1px solid var(--border-primary);
        border-radius: var(--radius-md);
        padding: var(--space-sm) var(--space-md);
        box-shadow: var(--shadow-lg);
        pointer-events: none;
        z-index: 100;
        transform: translate(-50%, -100%);
        margin-top: -10px;
        opacity: 0;
        visibility: hidden;
        transition: opacity var(--transition-normal), visibility var(--transition-normal);
        min-width: 120px;
      }

      .chart-tooltip.visible {
        opacity: 1;
        visibility: visible;
      }

      .tooltip-series {
        display: flex;
        align-items: center;
        gap: var(--space-xs);
        font-size: 11px;
        font-weight: var(--font-weight-semibold);
        color: var(--text-secondary);
        margin-bottom: 4px;
      }

      .tooltip-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
      }

      .tooltip-value {
        font-size: 18px;
        font-weight: var(--font-weight-bold);
        color: var(--text-primary);
      }

      .tooltip-label {
        font-size: 11px;
        color: var(--text-secondary);
        margin-top: 2px;
      }

      /* Selected point styles */
      .data-point.selected {
        stroke-width: 0.6;
        stroke: var(--text-primary);
        filter: drop-shadow(0 0 4px currentColor);
      }

      /* Legend interactivity */
      .legend-item.active {
        background: var(--surface-elevated);
        box-shadow: var(--shadow-md);
      }

      .legend-item.dimmed {
        opacity: 0.4;
      }

      /* Crosshair line */
      .crosshair-line {
        stroke: var(--border-primary);
        stroke-width: 1;
        stroke-dasharray: 4, 4;
        opacity: 0;
        transition: opacity var(--transition-normal);
      }

      .crosshair-line.visible {
        opacity: 1;
      }

      /* Details panel */
      .details-panel {
        background: var(--surface-secondary);
        border: 1px solid var(--border-primary);
        border-radius: var(--radius-md);
        margin-top: var(--space-md);
        overflow: hidden;
        max-height: 0;
        opacity: 0;
        transition: all 0.3s ease;
      }

      .details-panel.open {
        max-height: 500px;
        opacity: 1;
      }

      .details-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: var(--space-md);
        background: var(--surface-tertiary);
        border-bottom: 1px solid var(--border-primary);
      }

      .details-title {
        font-size: 16px;
        font-weight: var(--font-weight-semibold);
        color: var(--text-primary);
        display: flex;
        align-items: center;
        gap: var(--space-sm);
      }

      .details-dot {
        width: 12px;
        height: 12px;
        border-radius: 50%;
      }

      .details-close {
        background: transparent;
        border: none;
        color: var(--text-secondary);
        cursor: pointer;
        padding: var(--space-xs);
        border-radius: var(--radius-sm);
        font-size: 18px;
        transition: all var(--transition-normal);
      }

      .details-close:hover {
        background: var(--hover-overlay);
        color: var(--text-primary);
      }

      .details-body {
        padding: var(--space-md);
      }

      .details-main {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
        gap: var(--space-md);
        margin-bottom: var(--space-md);
      }

      .detail-item {
        display: flex;
        flex-direction: column;
        gap: var(--space-xs);
      }

      .detail-label {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: var(--text-secondary);
      }

      .detail-value {
        font-size: 22px;
        font-weight: var(--font-weight-bold);
        color: var(--text-primary);
      }

      .detail-value.highlight {
        color: var(--oracle-primary);
      }

      .detail-value.small {
        font-size: 14px;
        font-weight: var(--font-weight-medium);
      }

      .compare-section {
        border-top: 1px solid var(--border-primary);
        padding-top: var(--space-md);
      }

      .compare-title {
        font-size: 12px;
        font-weight: var(--font-weight-semibold);
        color: var(--text-secondary);
        margin-bottom: var(--space-sm);
      }

      .compare-items {
        display: flex;
        flex-wrap: wrap;
        gap: var(--space-sm);
      }

      .compare-item {
        display: flex;
        align-items: center;
        gap: var(--space-xs);
        background: var(--surface-tertiary);
        padding: var(--space-xs) var(--space-sm);
        border-radius: var(--radius-sm);
        font-size: 12px;
      }

      .compare-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
      }

      .compare-name {
        color: var(--text-secondary);
      }

      .compare-value {
        font-weight: var(--font-weight-semibold);
        color: var(--text-primary);
      }
    `,
  ];

  render() {
    let series: SeriesData[] = [];
    let labels: string[] = [];
    let details: DetailRecord[] = [];

    // Resolve dataPath, labelPath, and seriesPath
    if (this.processor) {
      // Get labels
      if (this.labelPath && typeof this.labelPath === 'string') {
        let rawLabels = this.processor.getData(this.component, this.labelPath, this.surfaceId ?? 'default') as any;
        if (rawLabels instanceof Map) {
          labels = Array.from(rawLabels.values()).map(String);
        } else if (Array.isArray(rawLabels)) {
          labels = rawLabels.map((item: any) => {
            if (typeof item === 'object' && 'valueString' in item) return item.valueString;
            if (typeof item === 'object' && 'valueNumber' in item) return String(item.valueNumber);
            return String(item);
          });
        }
      }

      // Get series data - expects array of {name, values, color?}
      if (this.seriesPath && typeof this.seriesPath === 'string') {
        let rawSeries = this.processor.getData(this.component, this.seriesPath, this.surfaceId ?? 'default') as any;
        
        if (rawSeries instanceof Map) {
          rawSeries = Array.from(rawSeries.values());
        }

        if (Array.isArray(rawSeries)) {
          series = rawSeries.map((s: any, idx: number) => {
            let name = 'Series ' + (idx + 1);
            let values: number[] = [];
            let color = SERIES_COLORS[idx % SERIES_COLORS.length];

            if (s instanceof Map) {
              name = s.get('name') || name;
              color = s.get('color') || color;
              const vals = s.get('values');
              if (vals instanceof Map) {
                values = Array.from(vals.values()).map((v: any) => {
                  if (typeof v === 'object' && 'valueNumber' in v) return v.valueNumber;
                  return typeof v === 'number' ? v : parseFloat(v) || 0;
                });
              } else if (Array.isArray(vals)) {
                values = vals.map((v: any) => {
                  if (typeof v === 'object' && 'valueNumber' in v) return v.valueNumber;
                  return typeof v === 'number' ? v : parseFloat(v) || 0;
                });
              }
            } else if (typeof s === 'object') {
              name = s.name || s.valueString || name;
              color = s.color || color;
              
              // Handle nested valueMap structure
              if (Array.isArray(s)) {
                for (const kv of s) {
                  if (kv.key === 'name') name = kv.valueString || name;
                  if (kv.key === 'color') color = kv.valueString || color;
                  if (kv.key === 'values' && kv.valueMap) {
                    values = kv.valueMap.map((v: any) => v.valueNumber || 0);
                  }
                }
              } else if (s.valueMap) {
                for (const kv of s.valueMap) {
                  if (kv.key === 'name') name = kv.valueString || name;
                  if (kv.key === 'color') color = kv.valueString || color;
                  if (kv.key === 'values' && kv.valueMap) {
                    values = kv.valueMap.map((v: any) => v.valueNumber || 0);
                  }
                }
              } else {
                // Direct object with values array
                const vals = s.values;
                if (Array.isArray(vals)) {
                  values = vals.map((v: any) => {
                    if (typeof v === 'object' && 'valueNumber' in v) return v.valueNumber;
                    return typeof v === 'number' ? v : parseFloat(v) || 0;
                  });
                }
              }
            }

            return { name, values, color };
          });
        }
      } else if (this.dataPath && typeof this.dataPath === 'string') {
        // Fallback: single series from dataPath for backward compatibility
        let values = this.processor.getData(this.component, this.dataPath, this.surfaceId ?? 'default') as any;
        
        if (values instanceof Map) {
          values = Array.from(values.values());
        }
        
        if (Array.isArray(values)) {
          const numericValues = values.map((v: any) => {
            if (typeof v === 'object' && 'valueNumber' in v) return v.valueNumber;
            return typeof v === 'number' ? v : parseFloat(v) || 0;
          });
          series = [{ name: 'Data', values: numericValues, color: SERIES_COLORS[0] }];
        }
      }

      if (this.detailsPath && typeof this.detailsPath === 'string') {
        details = this.parseRecordsFromPath(this.detailsPath);
      }
    }

    if (series.length === 0 || labels.length === 0) {
      return html`
        <div class="empty-state">
          No chart data available
        </div>
      `;
    }

    // Calculate min/max across all series
    const allValues = series.flatMap(s => s.values);
    const maxValue = Math.max(...allValues);
    const minValue = Math.min(0, Math.min(...allValues)); // Always include 0
    const valueRange = maxValue - minValue || 1;

    // Add 10% padding to max
    const paddedMax = maxValue + valueRange * 0.1;
    const paddedRange = paddedMax - minValue;

    // Chart dimensions
    const chartWidth = 100; // percentage
    const chartHeight = 100; // percentage

    // Calculate points for each series
    const seriesPoints = series.map(s => {
      return s.values.map((value, i) => {
        const x = labels.length > 1 ? (i / (labels.length - 1)) * chartWidth : chartWidth / 2;
        const y = chartHeight - ((value - minValue) / paddedRange) * chartHeight;
        return { x, y, value, label: labels[i] || '' };
      });
    });

    // Y-axis labels (5 divisions)
    const yLabels = Array.from({ length: 5 }, (_, i) => {
      const value = minValue + (paddedRange * (4 - i) / 4);
      return Math.round(value * 10) / 10;
    });

    return html`
      <div class="line-chart">
        <div class="chart-title">${this.title}</div>
        <div class="chart-wrapper">
          <div class="y-axis-labels">
            ${yLabels.map(v => html`<span class="y-label">${this.formatValue(v)}</span>`)}
          </div>
          <div class="chart-area">
            <div class="chart-container" @mouseleave=${this.hideTooltip}>
              <svg class="chart-svg" viewBox="0 0 100 100" preserveAspectRatio="none">
                <!-- Grid lines -->
                ${[0, 25, 50, 75, 100].map(y => svg`
                  <line class="grid-line" x1="0" y1="${y}" x2="100" y2="${y}" vector-effect="non-scaling-stroke" />
                `)}
                
                <!-- Crosshair line -->
                ${this.interactive ? svg`
                  <line 
                    class="crosshair-line ${this.tooltip.visible ? 'visible' : ''}" 
                    x1="${this.tooltip.point.x}" 
                    y1="0" 
                    x2="${this.tooltip.point.x}" 
                    y2="100" 
                    vector-effect="non-scaling-stroke"
                  />
                ` : ''}
                
                <!-- Render each series -->
                ${series.map((s, seriesIdx) => this.renderSeries(s, seriesPoints[seriesIdx], chartHeight, minValue, paddedRange, seriesIdx, details))}
              </svg>
              
              <!-- Tooltip -->
              ${this.interactive ? html`
                <div 
                  class="chart-tooltip ${this.tooltip.visible ? 'visible' : ''}"
                  style="left: ${this.tooltip.x}%; top: ${this.tooltip.y}%;"
                >
                  <div class="tooltip-series">
                    <span class="tooltip-dot" style="background-color: ${this.tooltip.point.seriesColor || colors.oracle.primary}"></span>
                    <span>${this.tooltip.point.seriesName || 'Value'}</span>
                  </div>
                  <div class="tooltip-value">${this.formatValue(this.tooltip.point.value)}</div>
                  <div class="tooltip-label">${this.tooltip.point.label}</div>
                </div>
              ` : ''}
            </div>
            <div class="x-axis-labels">
              ${labels.map(l => html`<span class="x-label">${l}</span>`)}
            </div>
          </div>
        </div>
        
        <div class="legend">
          ${series.map(s => html`
            <div 
              class="legend-item ${this.hoveredSeries === s.name ? 'active' : ''} ${this.hoveredSeries && this.hoveredSeries !== s.name ? 'dimmed' : ''}"
              @mouseenter=${() => this.hoverSeries(s.name)}
              @mouseleave=${() => this.hoverSeries(null)}
              @click=${() => this.selectSeries(s)}
            >
              <div class="legend-dot" style="background-color: ${s.color}; color: ${s.color};"></div>
              <span>${s.name}</span>
            </div>
          `)}
        </div>
        ${this.renderDetailsPanel(series, labels)}
      </div>
    `;
  }

  private renderDetailsPanel(allSeries: SeriesData[], _labels: string[]) {
    if (!this.detailsData) return html`<div class="details-panel"></div>`;

    const { point, series, customDetails } = this.detailsData;
    const pointIndex = point.index ?? 0;

    const comparisonData = allSeries
      .filter(s => s.name !== series.name)
      .map(s => ({
        name: s.name,
        color: s.color,
        value: s.values[pointIndex] ?? 0
      }));

    const seriesValues = series.values;
    const avg = seriesValues.reduce((a, b) => a + b, 0) / seriesValues.length;
    const max = Math.max(...seriesValues);
    const min = Math.min(...seriesValues);
    const isAboveAvg = point.value > avg;
    const percentOfMax = max > 0 ? (point.value / max) * 100 : 0;
    const hasCustomDetails = !!customDetails && Object.keys(customDetails).length > 0;

    return html`
      <div class="details-panel ${this.showDetails ? 'open' : ''}">
        <div class="details-header">
          <div class="details-title">
            <div class="details-dot" style="background-color: ${series.color};"></div>
            ${series.name} at ${point.label}
          </div>
          <button class="details-close" @click=${this.closeDetails}>×</button>
        </div>
        <div class="details-body">
          ${hasCustomDetails ? html`
            <div class="details-main">
              ${Object.entries(customDetails!).map(([key, value]) => html`
                <div class="detail-item">
                  <span class="detail-label">${this.formatLabel(key)}</span>
                  <span class="detail-value ${typeof value === 'number' ? 'highlight' : 'small'}">
                    ${typeof value === 'number' ? this.formatValue(value) : String(value)}
                  </span>
                </div>
              `)}
            </div>
          ` : html`
            <div class="details-main">
              <div class="detail-item">
                <span class="detail-label">Value</span>
                <span class="detail-value highlight">${this.formatValue(point.value)}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Period</span>
                <span class="detail-value small">${point.label}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Series Average</span>
                <span class="detail-value small">${this.formatValue(avg)}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">vs Average</span>
                <span class="detail-value small" style="color: ${isAboveAvg ? 'var(--semantic-success)' : 'var(--semantic-error)'};">
                  ${isAboveAvg ? '+' : '-'} ${Math.abs(((point.value - avg) / avg) * 100).toFixed(1)}%
                </span>
              </div>
              <div class="detail-item">
                <span class="detail-label">Series Range</span>
                <span class="detail-value small">${this.formatValue(min)} - ${this.formatValue(max)}</span>
              </div>
              <div class="detail-item">
                <span class="detail-label">% of Max</span>
                <span class="detail-value small">${percentOfMax.toFixed(0)}%</span>
              </div>
            </div>
            ${comparisonData.length > 0 ? html`
              <div class="compare-section">
                <div class="compare-title">Other Series at ${point.label}</div>
                <div class="compare-items">
                  ${comparisonData.map(c => html`
                    <div class="compare-item">
                      <div class="compare-dot" style="background-color: ${c.color};"></div>
                      <span class="compare-name">${c.name}:</span>
                      <span class="compare-value">${this.formatValue(c.value)}</span>
                    </div>
                  `)}
                </div>
              </div>
            ` : ''}
          `}
        </div>
      </div>
    `;
  }
  private closeDetails() {
    this.showDetails = false;
    this.selectedPoint = null;
    this.detailsData = null;
  }

  private showTooltip(point: ChartPoint, seriesName: string, seriesColor: string) {
    this.tooltip = {
      x: point.x,
      y: point.y,
      point: { ...point, seriesName, seriesColor },
      visible: true
    };
  }

  private hideTooltip() {
    this.tooltip = { ...this.tooltip, visible: false };
  }

  private handlePointClick(point: ChartPoint, series: SeriesData, pointIndex: number, customDetails?: DetailRecord) {
    const enrichedPoint = { ...point, index: pointIndex, seriesName: series.name, seriesColor: series.color };
    
    // Toggle details panel
    if (this.selectedPoint && 
        this.selectedPoint.x === point.x && 
        this.selectedPoint.y === point.y &&
        this.selectedPoint.seriesName === series.name) {
      this.closeDetails();
    } else {
      this.selectedPoint = enrichedPoint;
      this.detailsData = {
        point: enrichedPoint,
        series: series,
        allSeries: [], // Will be set from render context
        customDetails
      };
      this.showDetails = true;
    }
    
    this.dispatchEvent(new CustomEvent('point-select', {
      bubbles: true,
      composed: true,
      detail: { point: enrichedPoint, series }
    }));
  }

  private hoverSeries(seriesName: string | null) {
    this.hoveredSeries = seriesName;
  }

  private selectSeries(series: SeriesData) {
    this.dispatchEvent(new CustomEvent('series-select', {
      bubbles: true,
      composed: true,
      detail: { series }
    }));
  }

  private formatValue(value: number): string {
    if (Math.abs(value) >= 1000000) {
      return (value / 1000000).toFixed(1) + 'M';
    } else if (Math.abs(value) >= 1000) {
      return (value / 1000).toFixed(1) + 'K';
    }
    return value.toFixed(0);
  }

  private formatLabel(key: string): string {
    return key
      .replace(/([A-Z])/g, ' $1')
      .replace(/[_-]/g, ' ')
      .replace(/\b\w/g, l => l.toUpperCase())
      .trim();
  }

  private renderSeries(series: SeriesData, points: ChartPoint[], chartHeight: number, _minValue: number, _range: number, seriesIdx: number, details: DetailRecord[]) {
    if (points.length === 0) return '';

    const linePath = this.createSmoothPath(points);
    
    // Create area path
    const areaPath = `${linePath} L ${points[points.length - 1].x} ${chartHeight} L ${points[0].x} ${chartHeight} Z`;

    const isSeriesDimmed = this.hoveredSeries && this.hoveredSeries !== series.name;

    return svg`
      <!-- Area fill (if enabled) -->
      ${this.showArea ? svg`
        <path 
          class="data-area ${this.animated ? 'animated' : ''}" 
          d="${areaPath}" 
          fill="${series.color}"
          vector-effect="non-scaling-stroke"
          style="opacity: ${isSeriesDimmed ? '0.05' : ''}"
        />
      ` : ''}
      
      <!-- Line -->
      <path 
        class="data-line ${this.animated ? 'animated' : ''}" 
        d="${linePath}" 
        stroke="${series.color}" 
        stroke-width="${this.strokeWidth}"
        vector-effect="non-scaling-stroke"
        style="animation-delay: ${seriesIdx * 0.2}s; color: ${series.color}; opacity: ${isSeriesDimmed ? '0.3' : '1'};"
      />
      
      <!-- Data points -->
      ${this.showPoints ? points.map((p, i) => svg`
        <circle 
          class="data-point ${this.animated ? 'animated' : ''} ${this.selectedPoint && this.selectedPoint.x === p.x && this.selectedPoint.y === p.y && this.selectedPoint.seriesName === series.name ? 'selected' : ''}" 
          cx="${p.x}" 
          cy="${p.y}" 
          r="${isSeriesDimmed ? '0.5' : '0.8'}"
          fill="${series.color}"
          stroke="#1a1a2e"
          stroke-width="0.3"
          vector-effect="non-scaling-stroke"
          style="animation-delay: ${seriesIdx * 0.2 + 1 + i * 0.1}s; color: ${series.color}; opacity: ${isSeriesDimmed ? '0.4' : '1'};"
          @mouseenter=${() => this.showTooltip(p, series.name, series.color)}
          @mouseleave=${() => this.hideTooltip()}
          @click=${() => this.handlePointClick(p, series, i, details[i])}
        >
        </circle>
      `) : ''}
    `;
  }

  private createSmoothPath(points: ChartPoint[]): string {
    if (points.length < 2) {
      return points.length === 1 ? `M ${points[0].x} ${points[0].y}` : '';
    }

    // Use simple line segments for cleaner look
    return points.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x} ${p.y}`).join(' ');
  }

  private isMapLike(value: any): boolean {
    return !!value
      && typeof value.get === 'function'
      && typeof value.values === 'function'
      && typeof value.forEach === 'function';
  }

  private mapToObject(mapOrValue: any): any {
    if (this.isMapLike(mapOrValue)) {
      const obj: Record<string, any> = {};
      mapOrValue.forEach((value: any, key: string) => {
        obj[key] = this.mapToObject(value);
      });
      return obj;
    }
    return mapOrValue;
  }

  private parseRecordItem(item: any): DetailRecord {
    const record: DetailRecord = {};
    if (!item || typeof item !== 'object') return record;

    if ('valueMap' in item && Array.isArray(item.valueMap)) {
      for (const kv of item.valueMap) {
        if (!kv || !kv.key) continue;
        if (kv.valueString !== undefined) {
          record[kv.key] = kv.valueString;
        } else if (kv.valueNumber !== undefined) {
          record[kv.key] = kv.valueNumber;
        } else if (kv.valueBoolean !== undefined) {
          record[kv.key] = kv.valueBoolean;
        } else if (kv.valueMap !== undefined) {
          record[kv.key] = this.mapToObject(kv.valueMap);
        }
      }
      return record;
    }

    if (this.isMapLike(item)) {
      return this.mapToObject(item);
    }

    return { ...item };
  }

  private parseRecordsFromPath(path: any): DetailRecord[] {
    if (!path || typeof path !== 'string' || !this.processor) return [];
    let rawData = this.processor.getData(this.component, path, this.surfaceId ?? 'default') as any;

    if (this.isMapLike(rawData)) {
      rawData = Array.from(rawData.values());
    }
    if (!Array.isArray(rawData)) return [];

    return rawData.map((item: any) => this.parseRecordItem(item));
  }
}


