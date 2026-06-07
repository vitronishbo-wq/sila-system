def register_default_policies() -> None:
    """Register the supported domain policy defaults.

    These values are the canonical policy definitions used by the eligibility
    rule engine and can be overridden at runtime by loading a different policy
    set.
    """
    from .engine import policy_engine

    policy_engine.register_policy(
        "MAX_TRANSFER_DISTANCE",
        50,
        description="Maximum distance in kilometers allowed for a transfer request.",
    )

    policy_engine.register_policy(
        "MAX_PENDING_DEBT",
        0,
        description="Maximum amount of pending debt allowed for a transfer request.",
    )

    policy_engine.register_policy(
        "TRANSFER_WINDOWS",
        {
            "default": True,
            "2026": {
                "enabled": True,
                "start_date": "2026-03-01",
                "end_date": "2026-05-31",
                "semesters": {
                    "1": {
                        "enabled": True,
                        "start_date": "2026-03-01",
                        "end_date": "2026-04-15",
                    },
                    "2": {
                        "enabled": True,
                        "start_date": "2026-09-01",
                        "end_date": "2026-10-15",
                    },
                },
                "regions": {
                    "north": {
                        "enabled": True,
                        "start_date": "2026-03-01",
                        "end_date": "2026-05-31",
                        "semesters": {
                            "1": {
                                "enabled": True,
                                "start_date": "2026-03-01",
                                "end_date": "2026-04-15",
                            }
                        },
                    },
                    "south": {
                        "enabled": False,
                        "start_date": "2026-03-01",
                        "end_date": "2026-05-31",
                    },
                },
            },
            "2027": {
                "enabled": True,
                "start_date": "2027-03-01",
                "end_date": "2027-05-31",
            },
            "2028": {
                "enabled": True,
                "start_date": "2028-03-01",
                "end_date": "2028-05-31",
            },
            "2029": {
                "enabled": True,
                "start_date": "2029-03-01",
                "end_date": "2029-05-31",
            },
            "2030": {
                "enabled": True,
                "start_date": "2030-03-01",
                "end_date": "2030-05-31",
            },
        },
        description=(
            "Open transfer windows by academic year or default rule. "
            "Windows may be boolean or period objects with start and end dates."
        ),
    )

    policy_engine.register_policy(
        "GRADE_COMPATIBILITY",
        {
            "1": (6, 7),
            "2": (7, 8),
            "3": (8, 9),
            "4": (9, 10),
            "5": (10, 11),
            "6": (11, 12),
            "7": (12, 13),
            "8": (13, 14),
            "9": (14, 14),
            "10": (15, 15),
            "11": (16, 16),
            "12": (17, 18),
        },
        description="Allowed age ranges per class for transfer eligibility.",
    )


register_default_policies()
