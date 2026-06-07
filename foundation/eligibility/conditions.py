

def within_distance(student_location, school_location, max_km: float) -> bool:
    # Placeholder for geo-distance check
    return True


def compute_age(dob_iso: str, ref_date: str = None) -> int:
    """Compute age in years from ISO date string (YYYY-MM-DD).

    If ref_date is provided (YYYY-MM-DD) compute relative to that date.
    """
    dob = None
    dob = datetime_from_iso(dob_iso)
    if ref_date:
        ref = datetime_from_iso(ref_date)
    else:
        from datetime import datetime

        ref = datetime.utcnow()
    # naive age compute
    age = ref.year - dob.year - ((ref.month, ref.day) < (dob.month, dob.day))
    return age


def datetime_from_iso(s: str):
    from datetime import datetime

    return datetime.strptime(s, "%Y-%m-%d")
