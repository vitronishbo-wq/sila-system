import json, sys
d = json.load(sys.stdin)
for p in d["paths"]:
    if "escola" in p.lower() or "turma" in p.lower() or "inscric" in p.lower() or "fuc" in p.lower() or "matricula" in p.lower() or "boletim" in p.lower() or "certificado" in p.lower():
        print(p)
print("---TOTAL:", len(d["paths"]))
