def sanitation_coverage(total_households: int, households_covered: int) -> float:
    if total_households == 0:
        return 0
    return round((households_covered / total_households) * 100, 2)
