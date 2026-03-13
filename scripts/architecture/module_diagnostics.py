from pathlib import Path

BASE = Path("apps/backend/app/modules")
REPORT = Path("modules_report.md")

results = []

module_roots: list[Path] = []
for manifest in BASE.rglob("module.yaml"):
    module = manifest.parent
    rel = module.relative_to(BASE)
    # Ignore macro root folders and system noise.
    if len(rel.parts) < 2:
        continue
    if any(part.startswith("__") for part in rel.parts):
        continue
    module_roots.append(module)

for module in sorted(set(module_roots), key=lambda p: p.as_posix()):
    rel = module.relative_to(BASE)
    name = ".".join(rel.parts)

    models = (module / "domain").is_dir()
    services = (module / "application").is_dir()
    router = (module / "api/router.py").is_file()
    health = (module / "api/health.py").is_file()
    infra = (module / "infrastructure").is_dir()

    score = sum([
        models,
        services,
        router,
        health,
        infra
    ])

    results.append({
        "name": name,
        "models": models,
        "services": services,
        "router": router,
        "health": health,
        "infra": infra,
        "score": score * 20
    })

with open(REPORT, "w", encoding="utf-8") as f:

    f.write("# SILA MODULE MATURITY REPORT\n\n")
    f.write(f"Total modules analyzed: {len(results)}\n\n")

    for r in sorted(results, key=lambda x: x["score"]):

        f.write(f"## {r['name']}\n")

        f.write(f"- models: {'✓' if r['models'] else '✗'}\n")
        f.write(f"- services: {'✓' if r['services'] else '✗'}\n")
        f.write(f"- router: {'✓' if r['router'] else '✗'}\n")
        f.write(f"- health: {'✓' if r['health'] else '✗'}\n")
        f.write(f"- infrastructure: {'✓' if r['infra'] else '✗'}\n")

        f.write(f"\n**score:** {r['score']}%\n")
        f.write(f"score: {r['score']}%\n\n")

    f.write("## CRITICAL (<40%)\n\n")
    critical = [r for r in sorted(results, key=lambda x: x["score"]) if r["score"] < 40]
    if not critical:
        f.write("- none\n")
    else:
        for r in critical:
            f.write(f"- {r['name']} -> {r['score']}%\n")

    f.write("\n## ECONOMY FOCUS\n\n")
    economy = [r for r in sorted(results, key=lambda x: (x["score"], x["name"])) if r["name"].startswith("economy.")]
    if not economy:
        f.write("- none\n")
    else:
        for r in economy:
            f.write(f"- {r['name']}: {r['score']}%\n")

print("Report generated -> modules_report.md")
