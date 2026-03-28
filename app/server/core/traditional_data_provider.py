"""Jeux de donnees statiques pour la demonstration traditionnelle LIMAGRAIN Vegetable Seeds."""

ALERT_DATA = {
    "outages": [
        {
            "location": "Clermont-Ferrand, coordination portefeuille",
            "start_time": "2026-03-18T05:30:00Z",
            "estimated_restoration": "2026-03-18T16:00:00Z",
            "affected_customers": 2100,
            "cause": "Pression capacitaire retardant la coordination de lots de semences potageres pour la campagne de printemps",
            "crew_assigned": "Cellule logistique portefeuille - 6 coordinateurs",
            "priority": "Critique - saturation des capacites de preparation avant midi",
            "notes": "Reaffectation de 14 expeditions et ouverture d un flux de debord temporaire.",
            "status": "Ouverte",
            "severity": "Elevee"
        },
        {
            "location": "Murcia, production semences EMEA",
            "start_time": "2026-03-18T07:10:00Z",
            "estimated_restoration": "2026-03-19T12:00:00Z",
            "affected_customers": 86000,
            "cause": "Renforcement preventif des controles qualite sur des lots strategiques alimentant HM.CLAUSE et Hazera",
            "crew_assigned": "Equipe qualite semences HM.CLAUSE - 4 responsables terrain",
            "priority": "Critique - maintien des expeditions sous controle renforce",
            "notes": "Audit qualite en cours, mouvements de lots traces unite par unite.",
            "status": "En analyse",
            "severity": "Critique"
        },
        {
            "location": "Valencia, essais et selection",
            "start_time": "2026-03-17T13:45:00Z",
            "estimated_restoration": "2026-03-18T10:00:00Z",
            "affected_customers": 42,
            "cause": "Retard transporteur sur une tournee d echantillons varietaux et de semences certifiees",
            "crew_assigned": "Coordination essais varietaux - 3 gestionnaires",
            "priority": "Haute - fenetre agronomique courte sur le secteur",
            "notes": "Lots reroutes depuis un depot regional avec priorisation des programmes les plus exposes.",
            "status": "Ouverte",
            "severity": "Moyenne"
        },
        {
            "location": "Woodland, processing semences",
            "start_time": "2026-03-19T01:00:00Z",
            "estimated_restoration": "2026-03-19T05:30:00Z",
            "affected_customers": 18,
            "cause": "Maintenance planifiee sur une ligne de processing de lots destines aux lancements APAC",
            "crew_assigned": "Maintenance industrielle - 5 techniciens",
            "priority": "Planifiee - impact limite grace au stock tampon",
            "notes": "Les distributeurs prioritaires ont ete notifies la veille et les volumes ont ete lisses sur deux vagues.",
            "status": "Planifiee",
            "severity": "Faible"
        },
        {
            "location": "Bangkok, hub export APAC",
            "start_time": "2026-03-17T09:20:00Z",
            "estimated_restoration": "2026-03-17T17:00:00Z",
            "affected_customers": 125,
            "cause": "Anomalie de tracabilite sur un lot Vilmorin-Mikado destine a l export",
            "crew_assigned": "Qualite export Vilmorin-Mikado - 2 analystes",
            "priority": "Elevee - verification documentaire avant expedition",
            "notes": "Controle documentaire termine, lot Vilmorin-Mikado debloque et expedition reprogrammee le jour meme.",
            "status": "Resolue",
            "severity": "Moyenne"
        },
        {
            "location": "Chappes, centre qualite",
            "start_time": "2026-03-18T04:40:00Z",
            "estimated_restoration": "2026-03-18T11:30:00Z",
            "affected_customers": 27,
            "cause": "Deviation de flux documentaire sur des dossiers de liberation avec impact potentiel sur Limagrain Vegetable Seeds",
            "crew_assigned": "Pilotage qualite documentaire - 2 ordonnanceurs",
            "priority": "Haute - maintien de la conformite export",
            "notes": "Deux dossiers ont ete reroutes vers la cellule centrale et la conformite est restee maitrisee.",
            "status": "Sous surveillance",
            "severity": "Moyenne"
        }
    ],
    "total_outages": 6,
    "total_affected": 88312
}

OPERATIONS_DATA = {
    "consumption": {
        "total_mwh": 0,
        "by_source": {
            "renewable": 0,
            "fossil": 0,
            "nuclear": 0
        }
    },
    "production": {
        "total_mwh": 128400,
        "by_type": {
            "solar": 128400,
            "wind": 624000,
            "hydro": 18200,
            "coal": 96.4,
            "natural_gas": 99.2,
            "nuclear": 18
        }
    },
    "efficiency_metrics": {
        "grid_efficiency": 96.4,
        "renewable_percentage": 99.2
    },
    "kpi_details": {
        "total_production": {
            "trend": "volumes de semences potageres en hausse sur 4 semaines",
            "forecast": "132000 unites logistiques attendues sur la prochaine periode",
            "breakdown": "Tomate: 28%, Poivron: 18%, Carotte: 16%, Melon: 14%, Laitue: 12%, Autres: 12%"
        },
        "renewable": {
            "trend": "les alertes ouvertes baissent depuis la mise en place des plans de contournement",
            "forecast": "retour a 4 alertes ouvertes si la capacite reste stable",
            "breakdown": "Critique: 1, Elevee: 1, Moyenne: 3, Faible: 1"
        },
        "fossil": {
            "trend": "le nombre de sites et lots touches diminue grace aux reroutages",
            "forecast": "moins de 150 lots ou expeditions impactes d ici 24h",
            "breakdown": "HM.CLAUSE, Hazera, Vilmorin-Mikado et Limagrain Vegetable Seeds"
        },
        "nuclear": {
            "trend": "la conformite tracabilite reste au dessus de l objectif interne",
            "forecast": "99.4% attendus le mois prochain",
            "breakdown": "Lots conformes au premier passage: 97%, apres correction: 2.2%"
        },
        "grid_efficiency": {
            "trend": "service logistique superieur a la cible de 95%",
            "forecast": "96.8% prevus le mois prochain",
            "factors": "planification de tournees, stock tampon et coordination filieres"
        }
    }
}

SECTOR_DATA = {
    "industries": [
        {
            "name": "Selection varietale",
            "production_index": 108.4,
            "employment": 6400,
            "growth_rate": 4.2,
            "key_metrics": {
                "output_value": 1.3,
                "efficiency_score": 88.0
            }
        },
        {
            "name": "Semences potageres",
            "production_index": 112.9,
            "employment": 1850,
            "growth_rate": 8.9,
            "key_metrics": {
                "output_value": 0.9,
                "efficiency_score": 94.0
            }
        },
        {
            "name": "Production semences",
            "production_index": 104.7,
            "employment": 2100,
            "growth_rate": 5.4,
            "key_metrics": {
                "output_value": 1.1,
                "efficiency_score": 92.0
            }
        },
        {
            "name": "Processing et qualite",
            "production_index": 110.3,
            "employment": 1560,
            "growth_rate": 6.8,
            "key_metrics": {
                "output_value": 1.0,
                "efficiency_score": 95.0
            }
        },
        {
            "name": "Distribution export",
            "production_index": 106.2,
            "employment": 1450,
            "growth_rate": 6.1,
            "key_metrics": {
                "output_value": 0.8,
                "efficiency_score": 90.0
            }
        },
        {
            "name": "Support marques",
            "production_index": 109.8,
            "employment": 980,
            "growth_rate": 5.1,
            "key_metrics": {
                "output_value": 0.5,
                "efficiency_score": 93.0
            }
        }
    ],
    "overall_metrics": {
        "total_employment": 14340,
        "average_growth": 6.1,
        "top_performing_industry": "Processing et qualite"
    }
}


async def get_traditional_outage_data():
    """Retourne les alertes operationnelles de demonstration."""
    import json
    return json.loads(json.dumps(ALERT_DATA))


async def get_traditional_energy_data():
    """Retourne les indicateurs operationnels de demonstration."""
    import json
    return json.loads(json.dumps(OPERATIONS_DATA))


async def get_traditional_industry_data():
    """Retourne les indicateurs par filiere de demonstration."""
    import json
    return json.loads(json.dumps(SECTOR_DATA))
