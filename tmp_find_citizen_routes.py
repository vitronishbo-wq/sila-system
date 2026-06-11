import json, sys
d = json.load(sys.stdin)
for p in d["paths"]:
    if "citizen" in p.lower() and ("/" in p and len(p.split("/")) < 5):
        methods = list(d["paths"][p].keys())
        print(f"{' '.join(m.upper() for m in methods)} {p}")
