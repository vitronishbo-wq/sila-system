import json
d = json.load(open('/tmp/openapi.json'))
paths = [p for p in d['paths'] if 'search' in p and 'health' in p]
for p in paths:
    print(p, list(d['paths'][p].keys()))
