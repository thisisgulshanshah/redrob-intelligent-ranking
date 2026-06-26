from __future__ import annotations
from datetime import datetime


def is_honeypot(candidate) -> bool:
    """Hard rule derived from dataset audit: candidates matching ALL three
    conditions below are deliberately constructed honeypots (71 found in
    100k dataset, 100% consistent pattern, zero false positives observed)."""
    sig = getattr(candidate, "redrob_signals", None) or {}
    if not sig:
        return False

    flags = 0

    try:
        signup = datetime.fromisoformat(str(sig.get("signup_date", "")).replace("Z", ""))
        last_active = datetime.fromisoformat(str(sig.get("last_active_date", "")).replace("Z", ""))
        if last_active < signup:
            flags += 1
    except Exception:
        pass

    sal = sig.get("expected_salary_range_inr_lpa", {}) or {}
    sal_min = sal.get("min")
    sal_max = sal.get("max")
    if sal_min is not None and sal_max is not None and sal_min > sal_max:
        flags += 1

    unverified = (
        not sig.get("verified_email")
        and not sig.get("verified_phone")
        and not sig.get("linkedin_connected")
    )
    high_social_proof = (
        sig.get("endorsements_received", 0) > 50
        or sig.get("connection_count", 0) > 200
    )
    if unverified and high_social_proof:
        flags += 1

    return flags >= 3
