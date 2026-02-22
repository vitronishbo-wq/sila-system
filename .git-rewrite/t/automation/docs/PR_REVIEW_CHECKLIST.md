PR Review Checklist for feature/admin-bootstrap

Purpose: Ensure reviewers validate safety, tests, and deploy-readiness before merging.

- [ ] Confirm scope: changes limited to admin bootstrap automation, force-delete helper,
      and tests.
- [ ] Security checks:
  - [ ] `scripts/force_delete_users.py` contains `check_safety()` guard and host-check
        (localhost/127.0.0.1).
  - [ ] `--dry-run` option present and tested.
  - [ ] No secrets or credentials added to the repo.
- [ ] Tests:
  - [ ] `tests/test_force_delete_users.py` passes locally and in CI.
  - [ ] Unit tests cover critical safety logic.
- [ ] Operational safety:
  - [ ] Backup-on-delete implemented (JSON backup file creation confirmed).
  - [ ] Automation script (`scripts/auto_create_admin.sh`) requires interactive
        confirmation for `--force`.
- [ ] Documentation:
  - [ ] `scripts/AUTO_CREATE_ADMIN.md` reviewed for clarity and correctness.
  - [ ] Makefile target `create-admin-force` documented.
- [ ] Rollback plan:
  - [ ] Reviewer confirms how to restore users from the generated JSON backup if needed.
- [ ] Merge readiness:
  - [ ] No failing tests in CI.
  - [ ] Suggested reviewers assigned.
