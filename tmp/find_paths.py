import json
d = json.load(open('/tmp/openapi.json'))
for p in sorted(d['paths'].keys()):
    if any(k in p for k in ['educacao', 'workflow', 'familia', 'assistencia', 'matricula', 'nascimento']):
        methods = list(d['paths'][p].keys())
        print(f'{p}  [{",".join(methods)}]')
