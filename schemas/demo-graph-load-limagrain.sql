-- Reset and load LIMAGRAIN Vegetable Seeds relational schema, demo data, then create the Oracle property graph.
-- Usage:
--   @schemas/demo-graph-load-limagrain.sql

PROMPT === Loading LIMAGRAIN relational demo schema and data ===
@schemas/demo-load-limagrain.sql

PROMPT === Creating LIMAGRAIN property graph ===
@schemas/demo-graph-limagrain.sql

PROMPT === Smoke check: LIMAGRAIN property graph exists ===
SELECT COUNT(*) AS graph_count
FROM user_property_graphs
WHERE graph_name = UPPER('limagrain_operations');

PROMPT === LIMAGRAIN graph load complete ===
