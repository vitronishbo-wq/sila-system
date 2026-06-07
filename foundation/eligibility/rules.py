import datetime
from typing import Any

from foundation.policies import policy_engine

from .conditions import compute_age


class HasAvailableVacancyRule:
    def evaluate(self, context: dict[str, Any]) -> tuple[bool, str]:
        # Expect context to include 'institution_capacity' or 'vacancies'
        cap = context.get("institution_capacity")
        vacancies = context.get("vacancies")
        if cap is not None:
            try:
                available = int(cap.get("available", 0))
            except Exception:
                available = 0
            if available <= 0:
                return False, "no_vacancy"
            return True, "vacancy_available"

        if vacancies is not None:
            try:
                if int(vacancies) <= 0:
                    return False, "no_vacancy"
            except Exception:
                return False, "no_vacancy"
            return True, "vacancy_available"

        return False, "vacancy_info_missing"


class WithinTransferDistanceRule:
    def evaluate(self, context: dict[str, Any]) -> tuple[bool, str]:
        max_distance = policy_engine.get_policy("MAX_TRANSFER_DISTANCE")
        if max_distance is None:
            return True, "distance_policy_missing"

        distance_km = context.get("distance_km")
        if distance_km is None:
            return True, "distance_unknown"
        try:
            if float(distance_km) > float(max_distance):
                return False, "distance_exceeded"
            return True, "distance_within_limit"
        except Exception:
            return False, "distance_parse_error"


class NoPendingDebtRule:
    def evaluate(self, context: dict[str, Any]) -> tuple[bool, str]:
        # Expect 'debts' as list of dicts with 'amount'
        max_debt = policy_engine.get_policy("MAX_PENDING_DEBT")
        if max_debt is None:
            return True, "debt_policy_missing"

        debts = context.get("debts") or []
        total = 0
        for d in debts:
            try:
                total += float(d.get("amount", 0))
            except Exception:
                total += 0
        if total > float(max_debt):
            return False, "pending_debt"
        return True, "no_debt"


class ValidAcademicStatusRule:
    def evaluate(self, context: dict[str, Any]) -> tuple[bool, str]:
        sanctions = context.get("sanctions") or []
        if len(sanctions) > 0:
            return False, "sanctioned"
        return True, "valid_status"


class CompatibleAgeRule:
    def evaluate(self, context: dict[str, Any]) -> tuple[bool, str]:
        dob = context.get("date_of_birth")
        target_class = str(context.get("target_class")) if context.get("target_class") is not None else None
        if not dob:
            return False, "age_unknown"
        try:
            age = compute_age(dob)
        except Exception:
            return False, "age_parse_error"

        compatibility = policy_engine.get_policy("GRADE_COMPATIBILITY")
        if not isinstance(compatibility, dict):
            return True, "grade_compatibility_policy_missing"

        if target_class and target_class in compatibility:
            min_age, max_age = compatibility[target_class]
            if age < min_age or age > max_age:
                return False, "age_incompatible"
            return True, "age_compatible"

        return True, "age_unknown_class_allowed"


class TransferWindowRule:
    def _parse_date(self, value: Any) -> datetime.date | None:
        if value is None:
            return None
        if isinstance(value, datetime.date):
            return value
        try:
            return datetime.datetime.strptime(str(value), "%Y-%m-%d").date()
        except (TypeError, ValueError):
            return None

    def _select_window_config(self, config: Any, context: dict[str, Any]) -> Any:
        if not isinstance(config, dict):
            return config

        region = context.get("region") or context.get("region_code")
        semester = context.get("semester")

        if region and isinstance(config.get("regions"), dict):
            region_config = config["regions"].get(str(region))
            if region_config is not None:
                if semester and isinstance(region_config.get("semesters"), dict):
                    semester_config = region_config["semesters"].get(str(semester))
                    if semester_config is not None:
                        return semester_config
                return region_config

        if semester and isinstance(config.get("semesters"), dict):
            semester_config = config["semesters"].get(str(semester))
            if semester_config is not None:
                return semester_config

        return config

    def _evaluate_window_value(self, config: Any) -> tuple[bool, str]:
        if isinstance(config, bool):
            return bool(config), "within_window" if config else "transfer_window_closed"
        if not isinstance(config, dict):
            return True, "within_window"

        if not bool(config.get("enabled", True)):
            return False, "transfer_window_closed"

        start_date = self._parse_date(config.get("start_date"))
        end_date = self._parse_date(config.get("end_date"))
        today = datetime.date.today()

        if start_date is not None and today < start_date:
            return False, "transfer_window_not_started"
        if end_date is not None and today > end_date:
            return False, "transfer_window_expired"

        return True, "within_window"

    def evaluate(self, context: dict[str, Any]) -> tuple[bool, str]:
        if context.get("transfer_closed"):
            return False, "transfer_window_closed"

        transfer_windows = policy_engine.get_policy("TRANSFER_WINDOWS")
        if not isinstance(transfer_windows, dict):
            transfer_windows = {"default": True}

        academic_year = str(context.get("academic_year")) if context.get("academic_year") is not None else "default"
        if academic_year in transfer_windows:
            year_config = transfer_windows[academic_year]
            return self._evaluate_window_value(self._select_window_config(year_config, context))

        return self._evaluate_window_value(self._select_window_config(transfer_windows.get("default", True), context))
