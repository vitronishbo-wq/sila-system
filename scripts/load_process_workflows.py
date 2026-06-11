#!/usr/bin/env python3
"""
Loader script: import workflow_definition.json files from
`apps/backend/app/processes/*/workflow_definition.json` and persist them
using the governance workflow repository.

Run with: `python scripts/load_process_workflows.py`
"""

import asyncio
import glob
import json
import os
import sys
from pathlib import Path

_REPO_ROOT = str(Path(__file__).resolve().parent.parent)
_BACKEND = str(Path(_REPO_ROOT) / "apps" / "backend")
for _p in (_REPO_ROOT, _BACKEND):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from apps.backend.app.core.db import db
from apps.backend.app.modules.governance.workflow.infrastructure.repositories.workflow_repository import (
    WorkflowRepository,
)
from apps.backend.app.modules.governance.workflow.domain.models.workflow_definition import (
    WorkflowDefinition,
)
from apps.backend.app.modules.governance.workflow.domain.models.workflow_state import (
    WorkflowState,
)
from apps.backend.app.modules.governance.workflow.domain.models.workflow_transition import (
    WorkflowTransition,
)


async def load_definition(path: str):
    data = json.loads(Path(path).read_text())
    async with db.transaction() as session:
        repo = WorkflowRepository(session)
        definition = WorkflowDefinition(
            code=data["code"],
            name=data.get("name", data.get("code")),
            entity_type=data.get("entity_type", "service_request"),
            description=data.get("description"),
            timeout_hours=data.get("timeout_hours"),
        )
        saved_def = await repo.save_definition(definition)

        # save states
        states_map: dict[str, WorkflowState] = {}
        for s in data.get("states", []):
            state = WorkflowState(
                workflow_id=saved_def.id,
                code=s["code"],
                name=s.get("name", s["code"]),
                is_initial=s.get("is_initial", False),
                is_final=s.get("is_final", False),
                is_auto_forward=s.get("is_auto_forward", False),
                timeout_hours=s.get("timeout_hours"),
                form_schema=s.get("form_schema"),
                metadata=s.get("metadata", {}),
            )
            saved_state = await repo.save_state(state)
            states_map[s["code"]] = saved_state

        # save transitions
        for t in data.get("transitions", []):
            from_state = states_map[t["from"]]
            to_state = states_map[t["to"]]
            transition = WorkflowTransition(
                workflow_id=saved_def.id,
                from_state_id=from_state.id,
                to_state_id=to_state.id,
                code=t["code"],
                name=t.get("name", t["code"]),
                pre_actions=t.get("pre_actions", {}),
                post_actions=t.get("post_actions", {}),
                condition_expression=t.get("condition_expression"),
            )
            await repo.save_transition(transition)


async def main():
    files = glob.glob("apps/backend/app/processes/*/workflow_definition.json")
    if not files:
        print("No workflow_definition.json files found under apps/backend/app/processes/")
        return
    for p in files:
        print("Loading:", p)
        try:
            await load_definition(p)
            print("Loaded", p)
        except Exception as e:
            print("Failed to load", p, e)


if __name__ == "__main__":
    asyncio.run(main())
