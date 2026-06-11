SELECT id::text || '|' || name || '|' || type FROM locations WHERE type='province' ORDER BY name;
