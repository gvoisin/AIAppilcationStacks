import { LitElement, html, css } from "lit"
import { customElement, property, state } from "lit/decorators.js"
import { v0_8 } from "@a2ui/lit";
import "./stat_bar.js"
import { registerShellComponents } from "../ui/custom-components/register-components.js";
import { outageConfig } from "../configs/outage_config.js"
import { designTokensCSS, buttonStyles, colors, radius } from "../theme/design-tokens.js"
import { ItemSelectEvent, KpiClickEvent } from "../ui/custom-components/detail-modal.js";

registerShellComponents();

// #region Component
@customElement("static-module")
export class StaticModule extends LitElement {
  @property({ type: String }) accessor currentTab = 'summary';
  @property({ attribute: false }) accessor component: any = this;
  
  @state() accessor selectedItem: any = null;
  @state() accessor showNotification = false;
  @state() accessor notificationMessage = '';

  private processor = v0_8.Data.createSignalA2uiMessageProcessor();

  // #region Data Loading
  connectedCallback() {
    super.connectedCallback();
    this.initializeData();
  }

  private async initializeData() {
    try {
      const response = await fetch('http://localhost:10002/traditional');
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const messages: v0_8.Types.ServerToClientMessage[] = await response.json();
      this.processor.processMessages(messages);
    } catch (error) {
      console.error('Echec du chargement des alertes operationnelles depuis le serveur :', error);
      // Fall back to local data if the server is unavailable.
      this.initializeStaticData();
    }
  }

  private async fetchData(endpoint: string) {
    try {
      const response = await fetch(`http://localhost:10002${endpoint}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const messages: v0_8.Types.ServerToClientMessage[] = await response.json();
      this.processor.processMessages(messages);
      this.requestUpdate();
    } catch (error) {
      console.error(`Failed to fetch data from ${endpoint}:`, error);
    }
  }

  private async loadEnergyTrends() {
    await this.fetchData('/traditional/trends');
  }

  private async loadTimeline() {
    await this.fetchData('/traditional/timeline');
  }

  private async loadIndustryData() {
    await this.fetchData('/traditional/industry');
  }

  private hasEnergyTrends(): boolean {
    return !!this.processor.getData(this.component, "/trends/energyTrend");
  }

  private hasTimeline(): boolean {
    return !!this.processor.getData(this.component, "/timeline/timelineEvents");
  }

  private hasIndustry(): boolean {
    return !!this.processor.getData(this.component, "/industry/industryTable");
  }
  // #endregion Data Loading

  // #region Static Fallback Data
  private initializeStaticData() {
    const messages: v0_8.Types.ServerToClientMessage[] = [
      {
        dataModelUpdate: {
          surfaceId: 'default',
          path: '/',
          contents: [
            {
              key: 'energyKPIs',
              valueMap: [
                { key: '0', valueMap: [
                  { key: 'label', valueString: 'Coordination portefeuille semences potageres' },
                  { key: 'value', valueNumber: 128400 },
                  { key: 'unit', valueString: 't' },
                  { key: 'change', valueNumber: 6.2 },
                  { key: 'changeLabel', valueString: 'vs periode precedente' },
                  { key: 'icon', valueString: '🌾' },
                  { key: 'colorTheme', valueString: 'cyan' },
                  { key: 'trend', valueString: 'hausse des volumes de semences potageres sur tomate, poivron et carotte' },
                  { key: 'forecast', valueString: '132000 unites logistiques attendues sur la prochaine periode' },
                  { key: 'breakdown', valueString: 'Tomate: 28%, Poivron: 18%, Carotte: 16%, Melon: 14%, Laitue: 12%, Autres: 12%' }
                ]},
                { key: '1', valueMap: [
                  { key: 'label', valueString: 'Alertes ouvertes' },
                  { key: 'value', valueNumber: 3 },
                  { key: 'unit', valueString: '' },
                  { key: 'change', valueNumber: -14 },
                  { key: 'changeLabel', valueString: 'vs hier' },
                  { key: 'icon', valueString: '🚜' },
                  { key: 'colorTheme', valueString: 'coral' },
                  { key: 'trend', valueString: 'baisse des alertes grace aux plans de contournement' },
                  { key: 'breakdown', valueString: 'Critique: 1, Elevee: 1, Moyenne: 1' }
                ]},
                { key: '2', valueMap: [
                  { key: 'label', valueString: 'Service logistique' },
                  { key: 'value', valueNumber: 96.4 },
                  { key: 'unit', valueString: '%' },
                  { key: 'change', valueNumber: 1.1 },
                  { key: 'changeLabel', valueString: 'vs objectif' },
                  { key: 'icon', valueString: '📦' },
                  { key: 'colorTheme', valueString: 'teal' },
                  { key: 'trend', valueString: 'niveau OTIF superieur a la cible interne' },
                  { key: 'factors', valueString: 'planification transport, sites tampons et coordination filieres' }
                ]},
                { key: '3', valueMap: [
                  { key: 'label', valueString: 'Conformite marques et tracabilite' },
                  { key: 'value', valueNumber: 99.2 },
                  { key: 'unit', valueString: '%' },
                  { key: 'change', valueNumber: 0.4 },
                  { key: 'changeLabel', valueString: 'vs mois dernier' },
                  { key: 'icon', valueString: '🔎' },
                  { key: 'colorTheme', valueString: 'green' },
                  { key: 'trend', valueString: 'conformite elevee sur les lots HM.CLAUSE, Hazera et Vilmorin-Mikado' },
                  { key: 'forecast', valueString: '99.4% vises le mois prochain' },
                  { key: 'breakdown', valueString: 'Premier passage: 97%, apres correction: 2.2%' }
                ]}
              ]
            },
            {
              key: 'outageSummary',
              valueMap: [
                { key: '0', valueNumber: 2 },
                { key: '1', valueNumber: 1 },
                { key: '2', valueNumber: 1 },
                { key: '3', valueNumber: 1 },
                { key: '4', valueNumber: 1 }
              ]
            },
            {
              key: 'outageSummaryLabels',
              valueMap: [
                { key: '0', valueString: 'Ouverte' },
                { key: '1', valueString: 'En analyse' },
                { key: '2', valueString: 'Resolue' },
                { key: '3', valueString: 'Planifiee' },
                { key: '4', valueString: 'Sous surveillance' }
              ]
            },
            {
              key: 'outageSummaryDetails',
              valueMap: [
                { key: '0', valueMap: [
                  { key: 'status', valueString: 'Ouverte' },
                  { key: 'customersAffected', valueNumber: 2142 },
                  { key: 'severityBreakdown', valueString: 'Elevee: 1, Moyenne: 1' },
                  { key: 'topAreas', valueString: 'Clermont-Ferrand, Valencia' },
                  { key: 'mainCauses', valueString: 'Retards de portefeuille, retard transporteur' },
                  { key: 'priority', valueString: 'Mobilisation immediate sur les flux amont' }
                ]},
                { key: '1', valueMap: [
                  { key: 'status', valueString: 'En analyse' },
                  { key: 'customersAffected', valueNumber: 86000 },
                  { key: 'severityBreakdown', valueString: 'Critique: 1' },
                  { key: 'topAreas', valueString: 'Site de production EMEA' },
                  { key: 'mainCauses', valueString: 'Renforcement qualite preventif' },
                  { key: 'estimatedResolution', valueString: 'Audit terrain et qualite en cours' }
                ]},
                { key: '2', valueMap: [
                  { key: 'status', valueString: 'Resolue' },
                  { key: 'customersRestored', valueNumber: 125 },
                  { key: 'resolutionRate', valueString: 'Flux documentaires remis au nominal' },
                  { key: 'topAreas', valueString: 'Bangkok' },
                  { key: 'mainCauses', valueString: 'Anomalie de tracabilite' },
                  { key: 'avgResolutionTime', valueString: '7 h 40 en moyenne' }
                ]},
                { key: '3', valueMap: [
                  { key: 'status', valueString: 'Planifiee' },
                  { key: 'plannedCustomers', valueNumber: 18 },
                  { key: 'scheduledWindow', valueString: 'Cette nuit 01:00 - 05:30' },
                  { key: 'topAreas', valueString: 'Woodland' },
                  { key: 'maintenanceType', valueString: 'Maintenance preventive sur une ligne de processing de lots export' },
                  { key: 'notificationSent', valueString: 'Oui - enseignes prevenues' }
                ]},
                { key: '4', valueMap: [
                  { key: 'status', valueString: 'Sous surveillance' },
                  { key: 'customersWatched', valueNumber: 27 },
                  { key: 'monitoringLevel', valueString: 'Controle documentaire et reroutage' },
                  { key: 'topAreas', valueString: 'Chappes' },
                  { key: 'lastChecked', valueString: 'Mise a jour il y a 12 minutes' },
                  { key: 'alertThreshold', valueString: 'Escalade automatique si ecart documentaire ou retard' }
                ]}
              ]
            },
            {
              key: 'outageTable',
              valueMap: [
                { key: '0', valueMap: [
                  { key: 'id', valueString: 'ALT-001' },
                  { key: 'location', valueString: 'Clermont-Ferrand, coordination portefeuille' },
                  { key: 'status', valueString: 'Ouverte' },
                  { key: 'severity', valueString: 'Elevee' },
                  { key: 'startTime', valueString: '2026-03-18T05:30:00Z' },
                  { key: 'estimatedRestoration', valueString: '2026-03-18T16:00:00Z' },
                  { key: 'affectedCustomers', valueNumber: 2100 }
                ]},
                { key: '1', valueMap: [
                  { key: 'id', valueString: 'ALT-002' },
                  { key: 'location', valueString: 'Murcia, production semences EMEA' },
                  { key: 'status', valueString: 'En analyse' },
                  { key: 'severity', valueString: 'Critique' },
                  { key: 'startTime', valueString: '2026-03-18T07:10:00Z' },
                  { key: 'estimatedRestoration', valueString: '2026-03-19T12:00:00Z' },
                  { key: 'affectedCustomers', valueNumber: 86000 }
                ]},
                { key: '2', valueMap: [
                  { key: 'id', valueString: 'ALT-003' },
                  { key: 'location', valueString: 'Valencia, essais et selection' },
                  { key: 'status', valueString: 'Ouverte' },
                  { key: 'severity', valueString: 'Moyenne' },
                  { key: 'startTime', valueString: '2026-03-17T13:45:00Z' },
                  { key: 'estimatedRestoration', valueString: '2026-03-18T10:00:00Z' },
                  { key: 'affectedCustomers', valueNumber: 42 }
                ]},
                { key: '3', valueMap: [
                  { key: 'id', valueString: 'ALT-004' },
                  { key: 'location', valueString: 'Woodland, processing semences' },
                  { key: 'status', valueString: 'Planifiee' },
                  { key: 'severity', valueString: 'Faible' },
                  { key: 'startTime', valueString: '2026-03-19T01:00:00Z' },
                  { key: 'estimatedRestoration', valueString: '2026-03-19T05:30:00Z' },
                  { key: 'affectedCustomers', valueNumber: 18 }
                ]},
                { key: '4', valueMap: [
                  { key: 'id', valueString: 'ALT-005' },
                  { key: 'location', valueString: 'Bangkok, hub export APAC' },
                  { key: 'status', valueString: 'Resolue' },
                  { key: 'severity', valueString: 'Moyenne' },
                  { key: 'startTime', valueString: '2026-03-17T09:20:00Z' },
                  { key: 'estimatedRestoration', valueString: '2026-03-17T17:00:00Z' },
                  { key: 'affectedCustomers', valueNumber: 125 }
                ]},
                { key: '5', valueMap: [
                  { key: 'id', valueString: 'ALT-006' },
                  { key: 'location', valueString: 'Chappes' },
                  { key: 'status', valueString: 'Sous surveillance' },
                  { key: 'severity', valueString: 'Moyenne' },
                  { key: 'startTime', valueString: '2026-03-18T04:40:00Z' },
                  { key: 'estimatedRestoration', valueString: '2026-03-18T11:30:00Z' },
                  { key: 'affectedCustomers', valueNumber: 27 }
                ]}
              ]
            },
            {
              key: 'timeline',
              valueMap: [
                { key: 'timelineEvents', valueMap: [
                  { key: '0', valueMap: [
                    { key: 'date', valueString: '2026-03-18T05:30:00Z' },
                    { key: 'title', valueString: 'Retard de coordination portefeuille semences sur le hub principal' },
                    { key: 'description', valueString: 'La saturation des capacites ralentit la preparation de plusieurs lots critiques' },
                    { key: 'status', valueString: 'Ouverte' },
                    { key: 'affectedArea', valueString: 'Clermont-Ferrand et coordination centrale' },
                    { key: 'assignedTeam', valueString: 'Cellule logistique Ouest' }
                  ]},
                  { key: '1', valueMap: [
                    { key: 'date', valueString: '2026-03-18T07:10:00Z' },
                    { key: 'title', valueString: 'Controle qualite renforce pour HM.CLAUSE sur un site de production' },
                    { key: 'description', valueString: 'Trois lots strategiques passent sous protocole de controle renforce' },
                    { key: 'status', valueString: 'En analyse' },
                    { key: 'affectedArea', valueString: 'Site de production EMEA' },
                    { key: 'assignedTeam', valueString: 'Equipe qualite semences HM.CLAUSE' }
                  ]},
                  { key: '2', valueMap: [
                    { key: 'date', valueString: '2026-03-17T13:45:00Z' },
                    { key: 'title', valueString: 'Retard tournee semences' },
                    { key: 'description', valueString: 'Une tournee varietale est reroutee depuis un depot regional' },
                    { key: 'status', valueString: 'Ouverte' },
                    { key: 'affectedArea', valueString: 'Valencia, essais et selection' },
                    { key: 'assignedTeam', valueString: 'ADV semences' }
                  ]},
                  { key: '3', valueMap: [
                    { key: 'date', valueString: '2026-03-17T17:00:00Z' },
                    { key: 'title', valueString: 'Blocage export Vilmorin-Mikado leve' },
                    { key: 'description', valueString: 'Le lot Vilmorin-Mikado est conforme apres verification documentaire' },
                    { key: 'status', valueString: 'Resolue' },
                    { key: 'resolution', valueString: 'Traceabilite revalidee et expedition relancee' },
                    { key: 'duration', valueString: '7 h 40' }
                  ]}
                ]},
                { key: 'timelineEventDetails', valueMap: [
                  { key: '0', valueMap: [{ key: 'status', valueString: 'Ouverte' }, { key: 'affectedArea', valueString: 'Clermont-Ferrand et coordination centrale' }, { key: 'assignedTeam', valueString: 'Cellule logistique Ouest' }]},
                  { key: '1', valueMap: [{ key: 'status', valueString: 'En analyse' }, { key: 'affectedArea', valueString: 'Site de production EMEA' }, { key: 'assignedTeam', valueString: 'Equipe qualite semences HM.CLAUSE' }]},
                  { key: '2', valueMap: [{ key: 'status', valueString: 'Ouverte' }, { key: 'affectedArea', valueString: 'Valencia, essais et selection' }, { key: 'assignedTeam', valueString: 'ADV semences' }]},
                  { key: '3', valueMap: [{ key: 'status', valueString: 'Resolue' }, { key: 'resolution', valueString: 'Traceabilite revalidee et expedition relancee' }, { key: 'duration', valueString: '7 h 40' }]}
                ]}
              ]
            },
            {
              key: 'mapMarkers',
              valueMap: [
                { key: '0', valueMap: [
                  { key: 'name', valueString: 'Clermont-Ferrand, coordination portefeuille' },
                  { key: 'latitude', valueNumber: 47.3656 },
                  { key: 'longitude', valueNumber: -1.1772 },
                  { key: 'description', valueString: 'Ouverte - retard de coordination portefeuille' },
                  { key: 'status', valueString: 'Ouverte' },
                  { key: 'severity', valueString: 'Elevee' },
                  { key: 'affectedCustomers', valueNumber: 2100 },
                  { key: 'crew', valueString: 'Cellule logistique Ouest' }
                ]},
                { key: '1', valueMap: [
                  { key: 'name', valueString: 'Murcia, production semences EMEA' },
                  { key: 'latitude', valueNumber: 46.67 },
                  { key: 'longitude', valueNumber: -1.43 },
                  { key: 'description', valueString: 'En analyse - protocole qualite renforce' },
                  { key: 'status', valueString: 'En analyse' },
                  { key: 'severity', valueString: 'Critique' },
                  { key: 'affectedCustomers', valueNumber: 86000 },
                  { key: 'crew', valueString: 'Equipe qualite semences HM.CLAUSE' }
                ]},
                { key: '2', valueMap: [
                  { key: 'name', valueString: 'Woodland, processing semences' },
                  { key: 'latitude', valueNumber: 47.0594 },
                  { key: 'longitude', valueNumber: -0.879 },
                  { key: 'description', valueString: 'Planifiee - maintenance processing' },
                  { key: 'status', valueString: 'Planifiee' },
                  { key: 'severity', valueString: 'Faible' },
                  { key: 'affectedCustomers', valueNumber: 18 },
                  { key: 'crew', valueString: 'Maintenance industrielle' }
                ]},
                { key: '3', valueMap: [
                  { key: 'name', valueString: 'Bangkok, hub export APAC' },
                  { key: 'latitude', valueNumber: 47.2597 },
                  { key: 'longitude', valueNumber: -0.0781 },
                  { key: 'description', valueString: 'Resolue - tracabilite lot export' },
                  { key: 'status', valueString: 'Resolue' },
                  { key: 'severity', valueString: 'Moyenne' },
                  { key: 'affectedCustomers', valueNumber: 125 },
                  { key: 'crew', valueString: 'Qualite export Vilmorin-Mikado' }
                ]},
                { key: '4', valueMap: [
                  { key: 'name', valueString: 'Chappes' },
                  { key: 'latitude', valueNumber: 47.2184 },
                  { key: 'longitude', valueNumber: -1.5536 },
                  { key: 'description', valueString: 'Sous surveillance - reroutage documentaire export' },
                  { key: 'status', valueString: 'Sous surveillance' },
                  { key: 'severity', valueString: 'Moyenne' },
                  { key: 'affectedCustomers', valueNumber: 27 },
                  { key: 'crew', valueString: 'Pilotage qualite documentaire' }
                ]}
              ]
            },
            {
              key: 'trends',
              valueMap: [
                { key: 'energyTrend', valueMap: [
                  { key: '0', valueMap: [
                    { key: 'name', valueString: 'Coordination portefeuille semences potageres' },
                    { key: 'color', valueString: '#D4A017' },
                    { key: 'values', valueMap: [
                      { key: '0', valueNumber: 82 }, { key: '1', valueNumber: 88 }, { key: '2', valueNumber: 95 }, { key: '3', valueNumber: 101 },
                      { key: '4', valueNumber: 110 }, { key: '5', valueNumber: 124 }, { key: '6', valueNumber: 138 }, { key: '7', valueNumber: 132 },
                      { key: '8', valueNumber: 118 }, { key: '9', valueNumber: 109 }, { key: '10', valueNumber: 97 }, { key: '11', valueNumber: 90 }
                    ]}
                  ]},
                  { key: '1', valueMap: [
                    { key: 'name', valueString: 'Distribution export' },
                    { key: 'color', valueString: '#4ECDC4' },
                    { key: 'values', valueMap: [
                      { key: '0', valueNumber: 96 }, { key: '1', valueNumber: 94 }, { key: '2', valueNumber: 98 }, { key: '3', valueNumber: 102 },
                      { key: '4', valueNumber: 106 }, { key: '5', valueNumber: 108 }, { key: '6', valueNumber: 111 }, { key: '7', valueNumber: 109 },
                      { key: '8', valueNumber: 107 }, { key: '9', valueNumber: 104 }, { key: '10', valueNumber: 101 }, { key: '11', valueNumber: 99 }
                    ]}
                  ]},
                  { key: '2', valueMap: [
                    { key: 'name', valueString: 'Production HM.CLAUSE / Hazera' },
                    { key: 'color', valueString: '#FF7F50' },
                    { key: 'values', valueMap: [
                      { key: '0', valueNumber: 90 }, { key: '1', valueNumber: 91 }, { key: '2', valueNumber: 93 }, { key: '3', valueNumber: 95 },
                      { key: '4', valueNumber: 99 }, { key: '5', valueNumber: 104 }, { key: '6', valueNumber: 108 }, { key: '7', valueNumber: 107 },
                      { key: '8', valueNumber: 105 }, { key: '9', valueNumber: 103 }, { key: '10', valueNumber: 101 }, { key: '11', valueNumber: 98 }
                    ]}
                  ]},
                  { key: '3', valueMap: [
                    { key: 'name', valueString: 'Commandes semences et filieres marqueses' },
                    { key: 'color', valueString: '#2E8B57' },
                    { key: 'values', valueMap: [
                      { key: '0', valueNumber: 72 }, { key: '1', valueNumber: 78 }, { key: '2', valueNumber: 89 }, { key: '3', valueNumber: 98 },
                      { key: '4', valueNumber: 104 }, { key: '5', valueNumber: 99 }, { key: '6', valueNumber: 86 }, { key: '7', valueNumber: 79 },
                      { key: '8', valueNumber: 84 }, { key: '9', valueNumber: 96 }, { key: '10', valueNumber: 108 }, { key: '11', valueNumber: 115 }
                    ]}
                  ]}
                ]},
                { key: 'energyTrendLabels', valueMap: [
                  { key: '0', valueString: 'Jan' }, { key: '1', valueString: 'Fev' }, { key: '2', valueString: 'Mar' }, { key: '3', valueString: 'Avr' },
                  { key: '4', valueString: 'Mai' }, { key: '5', valueString: 'Jun' }, { key: '6', valueString: 'Jul' }, { key: '7', valueString: 'Aou' },
                  { key: '8', valueString: 'Sep' }, { key: '9', valueString: 'Oct' }, { key: '10', valueString: 'Nov' }, { key: '11', valueString: 'Dec' }
                ]},
                { key: 'energyTrendDetails', valueMap: [
                  { key: '0', valueMap: [{ key: 'period', valueString: 'Janvier' }, { key: 'trend', valueString: 'Suivi des stocks hivernaux et preparation des semis' }, { key: 'forecast', valueString: 'Legere hausse des commandes de semences' }]},
                  { key: '1', valueMap: [{ key: 'period', valueString: 'Fevrier' }, { key: 'trend', valueString: 'Acceleration des travaux de printemps' }, { key: 'forecast', valueString: 'Hausse des besoins logistiques attendue' }]},
                  { key: '2', valueMap: [{ key: 'period', valueString: 'Mars' }, { key: 'trend', valueString: 'Montee en charge des interventions agronomiques' }, { key: 'forecast', valueString: 'Volumes semences au dessus du plan' }]},
                  { key: '3', valueMap: [{ key: 'period', valueString: 'Avril' }, { key: 'trend', valueString: 'Arbitrage capacitaire entre selection et processing' }, { key: 'forecast', valueString: 'Reequilibrage des flux de lots strategiques' }]},
                  { key: '4', valueMap: [{ key: 'period', valueString: 'Mai' }, { key: 'trend', valueString: 'Preparation des campagnes de lancement et des plans de stockage' }, { key: 'forecast', valueString: 'Pic d activite logistique a anticiper' }]},
                  { key: '5', valueMap: [{ key: 'period', valueString: 'Juin' }, { key: 'trend', valueString: 'Demarrage des lots ete et du processing' }, { key: 'forecast', valueString: 'Forte tension sur les capacites de traitement' }]},
                  { key: '6', valueMap: [{ key: 'period', valueString: 'Juillet' }, { key: 'trend', valueString: 'Pic de processing et de preparation export' }, { key: 'forecast', valueString: 'Maintien d un niveau eleve attendu' }]},
                  { key: '7', valueMap: [{ key: 'period', valueString: 'Aout' }, { key: 'trend', valueString: 'Lissage post-pic et tri qualite' }, { key: 'forecast', valueString: 'Repli progressif des flux' }]},
                  { key: '8', valueMap: [{ key: 'period', valueString: 'Septembre' }, { key: 'trend', valueString: 'Relance des plans de distribution export' }, { key: 'forecast', valueString: 'Hausse des commandes filieres elevage' }]},
                  { key: '9', valueMap: [{ key: 'period', valueString: 'Octobre' }, { key: 'trend', valueString: 'Stabilisation des flux et plans commerciaux' }, { key: 'forecast', valueString: 'Activite soutenue sur HM.CLAUSE, Hazera et Vilmorin-Mikado' }]},
                  { key: '10', valueMap: [{ key: 'period', valueString: 'Novembre' }, { key: 'trend', valueString: 'Preparation des campagnes d hiver' }, { key: 'forecast', valueString: 'Remontee des besoins varietaux et commerciaux' }]},
                  { key: '11', valueMap: [{ key: 'period', valueString: 'Decembre' }, { key: 'trend', valueString: 'Consolidation annuelle et projections' }, { key: 'forecast', valueString: 'Redemarrage progressif en janvier' }]}
                ]}
              ]
            },
            {
              key: 'industry',
              valueMap: [
                { key: 'industryTable', valueMap: [
                  { key: '0', valueMap: [
                    { key: 'name', valueString: 'Selection varietale' },
                    { key: 'productionIndex', valueNumber: 108.4 },
                    { key: 'employment', valueNumber: 6400 },
                    { key: 'growthRate', valueNumber: 4.2 },
                    { key: 'outputValue', valueNumber: 1.3 },
                    { key: 'efficiencyScore', valueNumber: 88 }
                  ]},
                  { key: '1', valueMap: [
                    { key: 'name', valueString: 'Semences' },
                    { key: 'productionIndex', valueNumber: 104.9 },
                    { key: 'employment', valueNumber: 850 },
                    { key: 'growthRate', valueNumber: 8.9 },
                    { key: 'outputValue', valueNumber: 0.4 },
                    { key: 'efficiencyScore', valueNumber: 91 }
                  ]},
                  { key: '2', valueMap: [
                    { key: 'name', valueString: 'Production semences' },
                    { key: 'productionIndex', valueNumber: 101.7 },
                    { key: 'employment', valueNumber: 2100 },
                    { key: 'growthRate', valueNumber: 3.4 },
                    { key: 'outputValue', valueNumber: 0.9 },
                    { key: 'efficiencyScore', valueNumber: 94 }
                  ]},
                  { key: '3', valueMap: [
                    { key: 'name', valueString: 'Processing et qualite' },
                    { key: 'productionIndex', valueNumber: 112.3 },
                    { key: 'employment', valueNumber: 3100 },
                    { key: 'growthRate', valueNumber: 6.8 },
                    { key: 'outputValue', valueNumber: 1.7 },
                    { key: 'efficiencyScore', valueNumber: 84 }
                  ]}
                ]}
              ]
            }
          ]
        }
      }
    ];

    this.processor.processMessages(messages);
  }
  // #endregion Static Fallback Data

  // #region Styles
  static styles = css`
    ${designTokensCSS}
    ${buttonStyles}

    :host {
      display: block;
      flex: 1 1 0;
      min-width: 0;
      overflow: hidden;
      background: var(--module-traditional-bg);
      border-radius: var(--radius-xl);
      padding: var(--space-sm);
      color: var(--text-primary);
    }

    .tabs {
      display: flex;
      gap: var(--space-xs);
      margin-bottom: var(--space-md);
      border-bottom: 1px solid var(--border-secondary);
    }

    .tabs .btn-tab.active {
      color: var(--color-error);
      border-bottom-color: var(--color-error);
    }

    .tabs .btn-tab:hover {
      background: var(--module-traditional-active);
    }

    .tab-content {
      display: flex;
      flex-direction: column;
      gap: var(--space-md);
    }

    .chart-section {
      background: var(--surface-secondary);
      border-radius: var(--radius-md);
      padding: var(--space-md);
    }

    .table-section {
      background: var(--surface-secondary);
      border-radius: var(--radius-md);
      padding: var(--space-md);
      overflow-x: auto;
    }

    .timeline-section {
      background: var(--surface-secondary);
      border-radius: var(--radius-md);
      padding: var(--space-md);
    }

    .map-section {
      background: var(--surface-secondary);
      border-radius: var(--radius-md);
      padding: var(--space-md);
      display: flex;
      flex-direction: column;
      gap: var(--space-md);
    }

    .map-description {
      font-size: var(--font-size-sm);
      line-height: var(--line-height-normal);
      color: var(--text-secondary);
    }

    .section-title {
      font-size: var(--font-size-lg);
      font-weight: var(--font-weight-bold);
      margin-bottom: var(--space-md);
      color: var(--text-primary);
    }

    .action-buttons {
      display: flex;
      gap: var(--space-sm);
      margin: var(--space-md) 0;
      justify-content: center;
      flex-wrap: wrap;
    }

    .notification {
      position: fixed;
      bottom: 20px;
      right: 20px;
      background: var(--surface-tertiary);
      color: var(--text-primary);
      padding: var(--space-md) var(--space-lg);
      border-radius: var(--radius-md);
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
      z-index: 1000;
      animation: slideIn 0.3s ease-out;
      border-left: 4px solid var(--color-primary);
    }

    @keyframes slideIn {
      from {
        transform: translateX(100%);
        opacity: 0;
      }
      to {
        transform: translateX(0);
        opacity: 1;
      }
    }

    .notification-close {
      margin-left: var(--space-md);
      cursor: pointer;
      opacity: 0.7;
    }

    .notification-close:hover {
      opacity: 1;
    }

    .bar-chart-section {
      background: var(--surface-secondary);
      border-radius: var(--radius-md);
      padding: var(--space-md);
    }
  `
  // #endregion Styles

  // #region Render
  render() {
    return html`
      <stat-bar .title=${"Application traditionnelle LIMAGRAIN Vegetable Seeds"} .time=${""} .tokens=${""} .configUrl=${"/outage_config"} .configType=${"traditional"} .configData=${outageConfig}></stat-bar>
      <div class="tabs">
        <button class="btn btn-tab ${this.currentTab === 'summary' ? 'active' : ''}" @click=${() => this.switchTab('summary')}>
          Synthese operationnelle
        </button>
        <button class="btn btn-tab ${this.currentTab === 'details' ? 'active' : ''}" @click=${() => this.switchTab('details')}>
          Details des alertes
        </button>
        <button class="btn btn-tab ${this.currentTab === 'map' ? 'active' : ''}" @click=${() => this.switchTab('map')}>
          Carte des alertes
        </button>
      </div>
      <div class="tab-content">
        ${this.renderTabContent()}
      </div>
      ${this.renderNotification()}
    `
  }
  // #endregion Render

  // #region Notifications
  private renderNotification() {
    if (!this.showNotification) return null;
    return html`
      <div class="notification">
        ${this.notificationMessage}
        <span class="notification-close" @click=${this.closeNotification}>✕</span>
      </div>
    `;
  }

  private showNotify(message: string) {
    this.notificationMessage = message;
    this.showNotification = true;
    setTimeout(() => {
      this.showNotification = false;
    }, 4000);
  }

  private closeNotification() {
    this.showNotification = false;
  }
  // #endregion Notifications

  // #region Interaction Handlers
  // Interaction handlers
  private handleItemSelect(e: CustomEvent) {
    const detail = e.detail;
    this.selectedItem = detail.item;
    this.showNotify(`Selection : ${detail.item?.id || detail.item?.label || 'element'}`);
  }

  private handleKpiClick(e: CustomEvent) {
    const detail = e.detail;
    this.showNotify(`Indicateur : ${detail.label} = ${detail.value}`);
  }

  private handleBarSelect(e: CustomEvent) {
    const { label, value, percentage } = e.detail;
    this.showNotify(`Statut selectionne : ${label} - ${value} (${percentage}%)`);
  }

  private handlePointSelect(e: CustomEvent) {
    const { series, index, value, label } = e.detail;
    this.showNotify(`Point selectionne : ${series} en ${label} = ${value}`);
  }

  private handleMarkerSelect(e: CustomEvent) {
    const marker = e.detail.marker;
    this.showNotify(`Territoire : ${marker.name} - ${marker.status || 'Voir le detail'}`);
  }

  private handleTimelineAction(e: CustomEvent) {
    const { action, item } = e.detail;
    this.showNotify(`${action} sur : ${item.title}`);
  }
  // #endregion Interaction Handlers

  // #region Tab Rendering
  private switchTab(tab: string) {
    this.currentTab = tab;
  }

  private renderTabContent() {
    switch (this.currentTab) {
      case 'summary':
        return this.renderSummaryTab();
      case 'details':
        return this.renderDetailsTab();
      case 'map':
        return this.renderMapTab();
      default:
        return this.renderSummaryTab();
    }
  }

  private renderSummaryTab() {
    return html`
      <div class="chart-section">
        <div class="section-title">Indicateurs operations et filieres</div>
        <kpi-card-group 
          .dataPath=${"/energyKPIs"} 
          .title=${"Indicateurs semences potageres"} 
          .processor=${this.processor} 
          .component=${this}
          clickable
          @kpi-click=${this.handleKpiClick}
        ></kpi-card-group>
      </div>
      <div class="bar-chart-section">
        <div class="section-title">Repartition des alertes par statut</div>
        <bar-graph
          .dataPath=${"/outageSummary"}
          .labelPath=${"/outageSummaryLabels"}
          .detailsPath=${"/outageSummaryDetails"}
          .title=${"Alertes par statut"}
          .processor=${this.processor}
          .component=${this}
          interactive
          colorful
          @bar-select=${this.handleBarSelect}
        ></bar-graph>
      </div>
      <div class="chart-section">
        <div class="section-title">Tendances des campagnes et filieres</div>
        <line-graph 
          .seriesPath=${"/trends/energyTrend"} 
          .labelPath=${"/trends/energyTrendLabels"} 
          .detailsPath=${"/trends/energyTrendDetails"}
          .title=${"Tendances mensuelles par activite"} 
          .processor=${this.processor} 
          .component=${this}
          interactive
          showPoints
          @point-select=${this.handlePointSelect}
        ></line-graph>
        ${!this.hasEnergyTrends() ? html`<button @click=${this.loadEnergyTrends} class="btn btn-outline-traditional">Charger les tendances</button>` : ''}
      </div>
    `;
  }

  private renderDetailsTab() {
    return html`
      <div class="table-section">
        <div class="section-title">Alertes operationnelles par territoire</div>
        <data-table
          .dataPath=${"/outageTable"}
          .detailsPath=${"/outageTableDetails"}
          .title=${"Details des alertes"}
          .columns=${[
            {header: "ID alerte", field: "id", type: "string"},
            {header: "Territoire", field: "location", type: "string"},
            {header: "Statut", field: "status", type: "status"},
            {header: "Priorite", field: "severity", type: "severity"},
            {header: "Ouverture", field: "startTime", type: "date"},
            {header: "Retour au nominal", field: "estimatedRestoration", type: "date"},
            {header: "Impact", field: "affectedCustomers", type: "number"}
          ]}
          .processor=${this.processor}
          .component=${this}
          expandable
          showDetailPanel
          @item-select=${this.handleItemSelect}
        ></data-table>
      </div>
      <div class="timeline-section">
        <div class="section-title">Chronologie des alertes et actions</div>
        <timeline-component 
          .dataPath=${"/timeline/timelineEvents"} 
          .detailsPath=${"/timeline/timelineEventDetails"}
          .processor=${this.processor} 
          .component=${this}
          expandable
          @timeline-action=${this.handleTimelineAction}
        ></timeline-component>
        ${!this.hasTimeline() ? html`<button @click=${this.loadTimeline} class="btn btn-outline-traditional">Charger la chronologie</button>` : ''}
      </div>
      <div class="table-section">
        <div class="section-title">Performance des filieres</div>
        <data-table
          .dataPath=${"/industry/industryTable"}
          .detailsPath=${"/industry/industryTableDetails"}
          .title=${"Indicateurs filieres"}
          .columns=${[
            {header: "Filiere", field: "name", type: "string"},
            {header: "Indice activite", field: "productionIndex", type: "number"},
            {header: "Exploitations / emplois", field: "employment", type: "number"},
            {header: "Croissance", field: "growthRate", type: "number"},
            {header: "Valeur", field: "outputValue", type: "number"},
            {header: "Score maitrise", field: "efficiencyScore", type: "number"}
          ]}
          .processor=${this.processor}
          .component=${this}
          expandable
        ></data-table>
        ${!this.hasIndustry() ? html`<button @click=${this.loadIndustryData} class="btn btn-outline-traditional">Charger les filieres</button>` : ''}
      </div>
    `;
  }

  private renderMapTab() {
    return html`
      <div class="map-section">
        <div class="section-title">Localisation des alertes</div>
        <map-component 
          .dataPath=${"/mapMarkers"} 
          .centerLat=${47.35} 
          .centerLng=${-1.1} 
          .zoom=${8} 
          .processor=${this.processor} 
          .component=${this}
          interactive
          showInfoPanel
          @marker-select=${this.handleMarkerSelect}
        ></map-component>
        <div class="map-description">
          <p>Cette carte presente les alertes operationnelles LIMAGRAIN Vegetable Seeds. Cliquez sur un marqueur pour afficher le contexte metier, les impacts et l equipe mobilisee.</p>
          <p>Les couleurs representent le niveau de priorite : <strong style="color: #FF6B6B;">Rouge = critique / elevee</strong>, <strong style="color: #FFB347;">Orange = moyenne</strong>, <strong style="color: #4ECDC4;">Vert = resolue ou maitrisee</strong></p>
        </div>
      </div>
    `;
  }
  // #endregion Tab Rendering


}
// #endregion Component

// #region Element Registration
declare global {
  interface HTMLElementTagNameMap {
    "static-module": StaticModule
  }
}
// #endregion Element Registration
