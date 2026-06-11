SELECT table_schema, table_name 
FROM information_schema.tables 
WHERE (table_name LIKE '%cidad%' OR table_name LIKE '%citizen%')
  AND table_schema NOT IN ('pg_catalog', 'information_schema')
ORDER BY table_schema, table_name;
