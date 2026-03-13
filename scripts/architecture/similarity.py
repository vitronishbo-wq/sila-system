"""Module similarity heuristics for architecture overlap analysis."""

from __future__ import annotations

import itertools
import re
from collections import Counter

try:
    from .scanner import ModuleScan
except ImportError:
    from scanner import ModuleScan  # type: ignore

TOKEN_RE = re.compile(r"[a-zA-Z0-9]+")
CAMEL_RE = re.compile(r"[A-Z]?[a-z]+|[A-Z]+(?=[A-Z]|$)|\d+")

SYNONYMS = {
    "estatistica": "statistics",
    "statistics": "statistics",
    "financas": "finance",
    "taxpayer": "taxation",
    "impostos": "taxation",
    "saude": "health",
    "primaria": "primary",
    "identidade": "identity",
    "registo": "registry",
    "portos": "ports",
    "logistica": "logistics",
    "transportes": "transport",
    "defesa": "defense",
    "consumidor": "consumer",
}

MERGE_SEEDS = {
    tuple(sorted(("estatistica", "statistics"))),
    tuple(sorted(("financas", "financas_publicas"))),
    tuple(sorted(("financas", "financas_impostos"))),
    tuple(sorted(("financas_impostos", "taxpayer"))),
    tuple(sorted(("saude", "saude_primaria"))),
    tuple(sorted(("transportes_logistica", "portos_logistica"))),
    tuple(sorted(("identidade_civil", "identity"))),
}


def _norm(token: str) -> str:
    key = token.lower().strip("_")
    return SYNONYMS.get(key, key)


def _tokenize_text(text: str) -> set[str]:
    tokens: set[str] = set()
    for part in text.split("_"):
        if not part:
            continue
        for camel in CAMEL_RE.findall(part):
            for token in TOKEN_RE.findall(camel):
                normalized = _norm(token)
                if normalized:
                    tokens.add(normalized)
    return tokens


def _jaccard(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def _top_concepts(scan: ModuleScan, limit: int = 35) -> set[str]:
    concepts = Counter(_norm(token) for token in scan.concept_tokens if token)
    return {token for token, _ in concepts.most_common(limit)}


def _entity_tokens(scan: ModuleScan) -> set[str]:
    out: set[str] = set()
    for item in scan.entities:
        out |= _tokenize_text(item)
    return out


def _repository_tokens(scan: ModuleScan) -> set[str]:
    out: set[str] = set()
    for item in scan.repositories:
        out |= _tokenize_text(item)
    return out


def compute_similarity_candidates(scans: dict[str, ModuleScan], min_score: float = 0.60) -> list[dict]:
    module_names = sorted(scans.keys())
    results: list[dict] = []

    for left_name, right_name in itertools.combinations(module_names, 2):
        left = scans[left_name]
        right = scans[right_name]

        name_similarity = _jaccard(_tokenize_text(left_name), _tokenize_text(right_name))
        concept_similarity = _jaccard(_top_concepts(left), _top_concepts(right))
        entity_similarity = _jaccard(_entity_tokens(left), _entity_tokens(right))
        repository_similarity = _jaccard(_repository_tokens(left), _repository_tokens(right))

        cross_imports = left.imports_out.get(right_name, 0) + right.imports_out.get(left_name, 0)
        coupling_bonus = min(0.10, cross_imports * 0.02)

        score = (
            0.35 * name_similarity
            + 0.35 * concept_similarity
            + 0.15 * entity_similarity
            + 0.15 * repository_similarity
            + coupling_bonus
        )
        seed_bonus = 0.0
        if tuple(sorted((left_name, right_name))) in MERGE_SEEDS:
            seed_bonus = 0.35
            score += seed_bonus

        if score < min_score:
            continue

        if score >= 0.85:
            suggestion = "merge modules"
        elif score >= 0.70:
            suggestion = "create bounded context"
        else:
            suggestion = "review boundary"

        results.append(
            {
                "left": left_name,
                "right": right_name,
                "similarity_score": round(min(score, 1.0), 2),
                "name_similarity": round(name_similarity, 2),
                "concept_similarity": round(concept_similarity, 2),
                "entity_similarity": round(entity_similarity, 2),
                "repository_similarity": round(repository_similarity, 2),
                "cross_imports": cross_imports,
                "seed_bonus": round(seed_bonus, 2),
                "suggestion": suggestion,
            }
        )

    return sorted(results, key=lambda item: (-item["similarity_score"], item["left"], item["right"]))
