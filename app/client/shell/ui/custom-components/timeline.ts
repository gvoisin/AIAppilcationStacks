import { html, css } from "lit";
import { property, customElement, state } from "lit/decorators.js";
import { Root } from "@a2ui/lit/ui";
import { colors } from "../../theme/design-tokens.js";
import { ItemSelectEvent } from "./detail-modal.js";

interface TimelineEvent {
  date: string;
  title: string;
  description?: string;
  category?: string;
  color?: string;
  details?: Record<string, any>;
}

@customElement('timeline-component')
export class TimelineComponent extends Root {
  @property({ attribute: false }) accessor dataPath: any = "";
  @property({ attribute: false }) accessor expandable: boolean = true;

  @state() accessor expandedItems: Set<number> = new Set();

  static styles = [
    ...Root.styles,
    css`
      :host {
        display: block;
        background: var(--surface-primary);
        border-radius: var(--radius-lg);
        box-shadow: var(--shadow-lg);
        padding: var(--space-md);
        margin: var(--space-xs);
        overflow-y: auto;
        max-height: 600px;
      }

      .timeline {
        position: relative;
        padding-left: 30px;
      }

      .timeline::before {
        content: '';
        position: absolute;
        left: 15px;
        top: 0;
        bottom: 0;
        width: 2px;
        background: var(--border-secondary);
      }

      .timeline-item {
        position: relative;
        margin-bottom: 30px;
        padding-left: 20px;
      }

      .timeline-item::before {
        content: '';
        position: absolute;
        left: -25px;
        top: 8px;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        background: var(--color-success);
        border: 2px solid var(--surface-primary);
        box-shadow: 0 0 0 2px var(--border-secondary);
      }

      .timeline-content {
        background: var(--surface-secondary);
        border-radius: var(--radius-sm);
        padding: var(--space-sm);
        box-shadow: var(--shadow-sm);
      }

      .timeline-date {
        font-size: 12px;
        color: var(--text-secondary);
        margin-bottom: 4px;
        font-weight: var(--font-weight-medium);
      }

      .timeline-title {
        font-size: 16px;
        font-weight: var(--font-weight-semibold);
        color: var(--text-primary);
        margin-bottom: 4px;
      }

      .timeline-description {
        font-size: 14px;
        color: var(--text-secondary);
        line-height: 1.4;
      }

      .timeline-category {
        display: inline-block;
        padding: 2px 8px;
        border-radius: var(--radius-xl);
        font-size: 11px;
        font-weight: var(--font-weight-medium);
        margin-top: 8px;
        background: var(--surface-primary);
        color: var(--text-secondary);
      }

      .empty-state {
        text-align: center;
        color: var(--text-muted);
        padding: 40px;
        font-style: italic;
      }

      .timeline-item.custom-color::before {
        background: var(--event-color, var(--color-success));
      }

      /* Expandable styles */
      .timeline-content.expandable {
        cursor: pointer;
        transition: all var(--transition-normal);
      }

      .timeline-content.expandable:hover {
        background: var(--surface-elevated);
        transform: translateX(4px);
      }

      .timeline-header {
        display: flex;
        align-items: flex-start;
        justify-content: space-between;
        gap: var(--space-sm);
      }

      .timeline-header-content {
        flex: 1;
      }

      .expand-toggle {
        color: var(--text-secondary);
        font-size: 12px;
        padding: 4px;
        transition: transform var(--transition-normal);
        flex-shrink: 0;
      }

      .expand-toggle.expanded {
        transform: rotate(90deg);
      }

      .timeline-expanded-details {
        max-height: 0;
        overflow: hidden;
        opacity: 0;
        transition: max-height 0.3s ease, opacity 0.2s ease, margin 0.3s ease;
      }

      .timeline-expanded-details.open {
        max-height: 300px;
        opacity: 1;
        margin-top: var(--space-sm);
        padding-top: var(--space-sm);
        border-top: 1px dashed var(--border-subtle);
      }

      .timeline-detail-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
        gap: var(--space-sm);
      }

      .timeline-detail-item {
        display: flex;
        flex-direction: column;
        gap: 2px;
      }

      .timeline-detail-label {
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: var(--text-muted);
        font-weight: var(--font-weight-semibold);
      }

      .timeline-detail-value {
        font-size: 13px;
        color: var(--text-primary);
      }

      .timeline-actions {
        display: flex;
        gap: var(--space-sm);
        margin-top: var(--space-sm);
      }

      .timeline-action-btn {
        padding: 6px 12px;
        font-size: 11px;
        border-radius: var(--radius-sm);
        background: var(--surface-primary);
        border: 1px solid var(--border-primary);
        color: var(--text-secondary);
        cursor: pointer;
        transition: all var(--transition-normal);
      }

      .timeline-action-btn:hover {
        background: var(--oracle-primary);
        color: var(--surface-primary);
        border-color: var(--oracle-primary);
      }
    `,
  ];

  render() {
    const events = this.getEvents();

    if (events.length === 0) {
      return html`
        <div class="empty-state">
          No timeline data available
        </div>
      `;
    }

    return html`
      <div class="timeline">
        ${events.map((event, index) => this.renderTimelineItem(event, index))}
      </div>
    `;
  }

  private getEvents(): TimelineEvent[] {
    let events: TimelineEvent[] = [];

    if (this.dataPath && typeof this.dataPath === 'string') {
      if (this.processor) {
        let data = this.processor.getData(this.component, this.dataPath, this.surfaceId ?? 'default') as any;

        if (data instanceof Map) {
          data = Array.from(data.values());
        }

        if (Array.isArray(data)) {
          events = data.map((item: any) => {
            let eventData: any = {};

            if (item instanceof Map) {
              // Handle A2UI Map structure: Map('date' -> '2023-01-15', 'title' -> 'Project Start', ...)
              for (const [key, value] of item.entries()) {
                if (key === 'date') eventData.date = value;
                if (key === 'title') eventData.title = value;
                if (key === 'description') eventData.description = value;
                if (key === 'category') eventData.category = value;
              }
            } else if (typeof item === 'object' && item.valueMap && Array.isArray(item.valueMap)) {
              // Handle A2UI structure: {valueMap: [{key: 'date', valueString: ...}, ...]}
              item.valueMap.forEach((entry: any) => {
                if (entry.key === 'date' && entry.valueString) eventData.date = entry.valueString;
                if (entry.key === 'title' && entry.valueString) eventData.title = entry.valueString;
                if (entry.key === 'description' && entry.valueString) eventData.description = entry.valueString;
                if (entry.key === 'category' && entry.valueString) eventData.category = entry.valueString;
              });
            }

            if (eventData.date) {
              return {
                date: eventData.date,
                title: eventData.title || 'Event',
                description: eventData.description || '',
                category: eventData.category || 'Event',
                color: colors.semantic.success
              };
            }
            return null;
          }).filter(Boolean) as TimelineEvent[];
        }
      }
    }

    events.sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());

    return events;
  }

  private renderTimelineItem(event: TimelineEvent, index: number) {
    const formattedDate = this.formatDate(event.date);
    const isExpanded = this.expandedItems.has(index);

    return html`
      <div class="timeline-item" style="--event-color: ${event.color}">
        <div 
          class="timeline-content ${this.expandable ? 'expandable' : ''}"
          @click=${() => this.toggleExpand(index, event)}
        >
          <div class="timeline-header">
            <div class="timeline-header-content">
              <div class="timeline-date">${formattedDate}</div>
              <div class="timeline-title">${event.title}</div>
            </div>
            ${this.expandable ? html`
              <span class="expand-toggle ${isExpanded ? 'expanded' : ''}">▶</span>
            ` : ''}
          </div>
          ${event.description ? html`<div class="timeline-description">${event.description}</div>` : ''}
          ${event.category ? html`<div class="timeline-category">${event.category}</div>` : ''}
          
          ${this.expandable ? html`
            <div class="timeline-expanded-details ${isExpanded ? 'open' : ''}">
              <div class="timeline-detail-grid">
                <div class="timeline-detail-item">
                  <span class="timeline-detail-label">Full Date</span>
                  <span class="timeline-detail-value">${this.formatFullDate(event.date)}</span>
                </div>
                <div class="timeline-detail-item">
                  <span class="timeline-detail-label">Category</span>
                  <span class="timeline-detail-value">${event.category || 'General'}</span>
                </div>
                ${event.details ? Object.entries(event.details).map(([key, value]) => html`
                  <div class="timeline-detail-item">
                    <span class="timeline-detail-label">${this.formatLabel(key)}</span>
                    <span class="timeline-detail-value">${value}</span>
                  </div>
                `) : ''}
              </div>
              <div class="timeline-actions">
                <button class="timeline-action-btn" @click=${(e: Event) => this.handleAction(e, 'view', event)}>View Details</button>
                <button class="timeline-action-btn" @click=${(e: Event) => this.handleAction(e, 'edit', event)}>Edit</button>
              </div>
            </div>
          ` : ''}
        </div>
      </div>
    `;
  }

  private toggleExpand(index: number, event: TimelineEvent) {
    if (!this.expandable) return;
    
    if (this.expandedItems.has(index)) {
      this.expandedItems.delete(index);
    } else {
      this.expandedItems.add(index);
    }
    this.requestUpdate();
    
    // Dispatch selection event
    this.dispatchEvent(new ItemSelectEvent(event, index));
  }

  private handleAction(e: Event, action: string, event: TimelineEvent) {
    e.stopPropagation();
    this.dispatchEvent(new CustomEvent('timeline-action', {
      bubbles: true,
      composed: true,
      detail: { action, event }
    }));
  }

  private formatLabel(key: string): string {
    return key
      .replace(/([A-Z])/g, ' $1')
      .replace(/[_-]/g, ' ')
      .replace(/\b\w/g, l => l.toUpperCase())
      .trim();
  }

  private formatFullDate(dateString: string): string {
    try {
      const date = new Date(dateString);
      if (isNaN(date.getTime())) return dateString;
      return date.toLocaleString(undefined, {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      });
    } catch {
      return dateString;
    }
  }

  private formatDate(dateString: string): string {
    try {
      const date = new Date(dateString);
      if (isNaN(date.getTime())) {
        return dateString;
      }

      const options: Intl.DateTimeFormatOptions = {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      };

      return date.toLocaleDateString(undefined, options);
    } catch {
      return dateString;
    }
  }
}