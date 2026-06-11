import json, sys
d = json.load(sys.stdin)
paths = list(d.get('paths', {}).keys())
print(f'Total paths: {len(paths)}')
cats = set()
for p in paths:
    parts = p.split('/')
    if len(parts) >= 5:
        prefix = '/'.join(parts[1:5])
        cats.add(prefix)
for c in sorted(cats):
    print(f'  /{c}')
