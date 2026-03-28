-- Reset and load Terrena demo relational schema, demo data, then create the Oracle property graph.
-- Usage:
--   @schemas/demo-graph-load-terrena.sql

PROMPT === Loading relational demo schema and data ===
@schemas/demo-load.sql

PROMPT === Creating Terrena property graph ===
@schemas/demo-graph-terrena.sql

PROMPT === Smoke check: Terrena property graph exists ===
SELECT COUNT(*) AS graph_count
FROM user_property_graphs
WHERE graph_name = UPPER('terrena_operations');

PROMPT === Graph load complete ===
