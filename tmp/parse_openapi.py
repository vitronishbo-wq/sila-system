import json
d = json.load(open('/tmp/openapi.json'))
paths = list(d.get('paths', {}).keys())
cats = set()
for p in paths:
    parts = p.split('/')
    if len(parts) >= 4:
        prefix = '/'.join(parts[1:4])
        cats.add(prefix)
for c in sorted(cats):
    print('  ' + c)
print()
print('Total paths:', len(paths))
