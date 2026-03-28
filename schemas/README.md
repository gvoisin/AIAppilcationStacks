# Demo Oracle Schema for Terrena and LIMAGRAIN Vegetable Seeds Scenarios

This folder contains a self-contained Oracle demo schema plus two demo datasets built from the application sample questions and agent scenarios.

The goal of these files is to give the chat and agent modules a realistic relational model for questions about filieres, logistics, quality, traceability, brands, sites, campaigns, and operational risks.

## Available demo scenarios

### 1. Terrena demo scenario

The original dataset is Terrena-oriented and supports cooperative agriculture, poultry, wines, grandes cultures, semences, logistics, quality, and traceability use cases.

Main files:

- `demo-data-terrena.sql`
- `demo-queries-terrena.sql`
- `demo-load-terrena.sql`
- `demo-load.sql` (legacy alias for Terrena loader)
- `demo-graph-terrena.sql`
- `demo-graph-load-terrena.sql`
- `demo-graph-load.sql` (legacy alias for Terrena graph loader)

### 2. LIMAGRAIN Vegetable Seeds demo scenario

The second dataset is centered on LIMAGRAIN Vegetable Seeds and its vegetable seed business activities, including selection, production, processing, quality, distribution, export compliance, and launch execution.

Main files:

- `demo-data-limagrain.sql`
- `demo-queries-limagrain.sql`
- `demo-load-limagrain.sql`
- `demo-graph-limagrain.sql`
- `demo-graph-load-limagrain.sql`

This dataset uses official LIMAGRAIN Vegetable Seeds business-line context and official brand references such as HM.CLAUSE, Hazera, Vilmorin-Mikado, and Vilmorin, adapted into synthetic demo operational data.

## Shared schema files

- `demo-schema.sql`  
  Creates the Oracle tables for the demo domain.

- `demo-drop.sql`  
  Drops the demo tables in foreign-key-safe order.

- `demo-truncate.sql`  
  Truncates all rows from the shared demo tables in foreign-key-safe order while keeping the schema in place.

## Terrena-specific files

- `demo-data-terrena.sql`  
  Inserts sample data covering the Terrena sample questions.

- `demo-queries-terrena.sql`  
  Contains example Oracle queries mapped to the Terrena sample chat questions and agent scenarios.

- `demo-load-terrena.sql`  
  Resets and reloads the Terrena relational demo dataset, then runs smoke checks.

- `demo-load.sql`  
  Legacy alias that also loads the Terrena relational demo dataset for backward compatibility.

- `demo-graph-terrena.sql`  
  Creates the Oracle property graph `terrena_operations` on top of the relational demo tables.

- `demo-graph-load-terrena.sql`  
  Loads the Terrena relational demo dataset and then creates the `terrena_operations` property graph.

- `demo-graph-load.sql`  
  Legacy alias that also loads the Terrena graph workflow for backward compatibility.

## LIMAGRAIN-specific files

- `demo-data-limagrain.sql`  
  Inserts LIMAGRAIN Vegetable Seeds sample data in French for the vegetable-seeds scenario.

- `demo-queries-limagrain.sql`  
  Contains example Oracle queries mapped to the LIMAGRAIN Vegetable Seeds sample questions and agent scenarios.

- `demo-load-limagrain.sql`  
  Resets and reloads the LIMAGRAIN Vegetable Seeds relational demo dataset, then runs LIMAGRAIN-specific smoke checks.

- `demo-graph-limagrain.sql`  
  Creates the Oracle property graph `limagrain_operations` on top of the relational demo tables.

- `demo-graph-load-limagrain.sql`  
  Loads the LIMAGRAIN relational demo dataset and then creates the `limagrain_operations` property graph.

## Domain Model Overview

The shared schema supports these main entities:

- `territories` — operational territories and regions
- `filieres` — business chains or operational streams
- `brands` — brands or business portfolios
- `campaigns` — campaign periods and seasonal business cycles
- `sites` — operational sites such as hubs, production sites, processing centers, and quality centers
- `brand_filieres` — mapping between brands and filieres
- `brand_sites` — mapping between brands and sites
- `operational_alerts` — alerts for sanitary, logistics, traceability, service-level, capacity, and supply-chain issues
- `alert_brand_impacts` — which brands are impacted by which alerts
- `logistics_flows` — major logistics routes with service-level and backlog metrics
- `lots` — production, shipping, or trial lots used for quality and traceability scenarios
- `quality_issues` — quality incidents that may need escalation
- `traceability_checks` — detailed traceability indicators and compliance signals
- `reference_documents` — supporting procedures, guides, checklists, and notes
- `action_plans` — prioritized response actions for operational follow-up

## Why this schema exists

The application needs structured data behind chat questions and agent scenarios. The shared schema was designed so those questions can be answered directly from relational data while allowing different demo customers to reuse the same tables.

### Terrena sample prompts

Examples include:

- "Quels incidents pourraient impacter Pere Dodu cette semaine ?"
- "Y a t il un risque pour les expeditions Ackerman ?"
- "Quels sujets doivent etre remontes a un responsable qualite pour Douce France ?"

### LIMAGRAIN Vegetable Seeds sample prompts

Examples include:

- "Quels territoires menacent HM.CLAUSE ou Hazera ?"
- "Y a t il un risque pour les expeditions Vilmorin-Mikado vers l APAC ?"
- "Quels sujets doivent etre remontes a un responsable qualite pour HM.CLAUSE ?"
- "Resume les impacts sur la filiere de processing et qualite des semences potageres en Europe du Sud."
- "Genere un tableau de priorisation des actions pour proteger le niveau de service Hazera sur 72 heures."

## Load and Reset Workflow

### Recommended: full reset and reload for Terrena

From SQLcl or SQL*Plus, run:

```sql
@schemas/demo-load-terrena.sql
```

This script will:

1. Drop existing demo tables if they exist
2. Recreate the schema
3. Insert the Terrena sample data
4. Commit the data
5. Run smoke-test queries

### Recommended: full reset and reload for LIMAGRAIN Vegetable Seeds

From SQLcl or SQL*Plus, run:

```sql
@schemas/demo-load-limagrain.sql
```

This script will:

1. Drop existing demo tables if they exist
2. Recreate the schema
3. Insert the LIMAGRAIN Vegetable Seeds sample data
4. Commit the data
5. Run LIMAGRAIN-specific smoke-test queries

### Fast data reset without dropping tables

If you want to empty the current demo dataset but keep the schema and constraints in place, run:

```sql
@schemas/demo-truncate.sql
```

This script truncates all shared demo tables in foreign-key-safe order. After that, you can reload either scenario with `demo-load-terrena.sql` or `demo-load-limagrain.sql`.

### Property graph setup for Terrena

If you want the NL2Graph / PGQL path to work for the Terrena scenario, you must also create the Oracle property graph:

```sql
@schemas/demo-graph-load-terrena.sql
```

This script will:

1. Run the Terrena relational demo load
2. Create the `terrena_operations` property graph
3. Check `user_property_graphs` for graph existence

You can also create only the graph after the relational tables and Terrena data already exist:

```sql
@schemas/demo-graph-terrena.sql
```

### Property graph setup for LIMAGRAIN Vegetable Seeds

If you want the NL2Graph / PGQL path to work for the LIMAGRAIN scenario, create the LIMAGRAIN property graph:

```sql
@schemas/demo-graph-load-limagrain.sql
```

This script will:

1. Run the LIMAGRAIN relational demo load
2. Create the `limagrain_operations` property graph
3. Check `user_property_graphs` for graph existence

You can also create only the graph after the relational tables and LIMAGRAIN data already exist:

```sql
@schemas/demo-graph-limagrain.sql
```

### Manual load order for Terrena

```sql
@schemas/demo-drop.sql
@schemas/demo-schema.sql
@schemas/demo-data-terrena.sql
@schemas/demo-queries-terrena.sql
@schemas/demo-graph-terrena.sql
```

### Manual load order for LIMAGRAIN Vegetable Seeds

```sql
@schemas/demo-drop.sql
@schemas/demo-schema.sql
@schemas/demo-data-limagrain.sql
@schemas/demo-queries-limagrain.sql
@schemas/demo-graph-limagrain.sql
```

## Smoke Checks

### In `demo-load-terrena.sql`

The Terrena relational loader includes a few quick checks:

- row counts for the main tables
- top priority operational alerts
- Ackerman traceability-risk records

### In `demo-load-limagrain.sql`

The LIMAGRAIN relational loader includes a few quick checks:

- row counts for the main tables
- top priority operational alerts
- Vilmorin-Mikado export traceability-risk records
- HM.CLAUSE quality issue records

The graph loaders add existence checks for `terrena_operations` and `limagrain_operations` in `user_property_graphs`.

These are intended as quick confirmation that the dataset loaded correctly and supports the expected business scenarios.

## Query Mapping

- `demo-queries-terrena.sql` maps the Terrena sample prompts to concrete SQL examples.
- `demo-queries-limagrain.sql` maps the LIMAGRAIN Vegetable Seeds sample prompts to concrete SQL examples.

## Notes on Oracle Compatibility

The scripts were written for Oracle-style SQL and use patterns such as:

- `VARCHAR2`
- `NUMBER`
- `DATE 'YYYY-MM-DD'`
- `FETCH FIRST N ROWS ONLY`
- `LISTAGG`
- `NVL`
- identity columns via `GENERATED BY DEFAULT AS IDENTITY`

The seed data was normalized to avoid depending on special character handling where possible.

## Scope and Intent

This is a demo schema, not a production model. It is intentionally compact and optimized for:

- sample-question coverage
- readability
- ease of reset and reload
- dashboard and NL2SQL demonstration value

If the application later needs stricter production semantics, this schema should be treated as a functional prototype rather than a final enterprise data model.
