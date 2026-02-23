

def test_create_dashboard_skeleton():
    # smoke: create payload and assert mapping
    payload = {"name": "d1", "description": "desc", "owner_id": 1, "layout": {}}
    assert payload["name"] == "d1"


def test_update_layout_permission():
    # placeholder to remind permissions must be enforced
    user = {"permissions": ["bi:view"]}
    assert "bi:admin" not in user.get("permissions")
