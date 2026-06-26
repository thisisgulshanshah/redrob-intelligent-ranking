from __future__ import annotations

from typing import Any, Dict, List

from backend.ranking.scorer import _candidate_profile, _candidate_skills, _candidate_history, _candidate_signals, _normalize_text


def _top_skills(candidate: Any, limit: int = 3) -> List[str]:
    skills = _candidate_skills(candidate)
    enriched = []
    for s in skills:
        if not isinstance(s, dict):
            continue
        enriched.append(
            (
                int(s.get("endorsements", 0) or 0),
                int(s.get("duration_months", 0) or 0),
                _normalize_text(s.get("name")),
                _normalize_text(s.get("proficiency")),
            )
        )
    enriched.sort(key=lambda x: (-x[0], -x[1], x[2]))
    return [name for _, _, name, _ in enriched[:limit] if name]


def _history_signals(candidate: Any) -> Dict[str, int]:
    history = _candidate_history(candidate)
    text = " ".join(
        _normalize_text(item.get("description"))
        for item in history
        if isinstance(item, dict)
    )

    terms = {
        "retrieval": 0,
        "ranking": 0,
        "search": 0,
        "recommendation": 0,
        "product": 0,
        "vector": 0,
        "embedding": 0,
        "evaluation": 0,
        "python": 0,
        "open source": 0,
    }
    for term in list(terms.keys()):
        terms[term] = text.count(term)
    return terms


def build_reasoning(candidate: Any, score: float, diagnostics: Dict[str, Any]) -> str:
    profile = _candidate_profile(candidate)
    signals = _candidate_signals(candidate)

    title = profile.get("current_title") or profile.get("headline") or "candidate"
    company = profile.get("current_company") or "their current company"
    years = float(profile.get("years_of_experience", diagnostics.get("experience_years", 0.0)) or 0.0)
    location = profile.get("location", "")
    notice = signals.get("notice_period_days", None)
    open_to_work = bool(signals.get("open_to_work_flag", False))
    response_rate = float(signals.get("recruiter_response_rate", 0.0) or 0.0)
    top_skills = _top_skills(candidate, 3)
    hist = _history_signals(candidate)

    strong_evidence = []
    if hist["ranking"] or hist["retrieval"] or hist["search"] or hist["recommendation"]:
        strong_evidence.append("retrieval/ranking/search work")
    if hist["product"]:
        strong_evidence.append("product-side experience")
    if hist["vector"] or hist["embedding"]:
        strong_evidence.append("vector or embedding systems")
    if hist["evaluation"]:
        strong_evidence.append("evaluation mindset")
    if hist["python"]:
        strong_evidence.append("Python-heavy work")

    evidence_text = ", ".join(strong_evidence) if strong_evidence else "adjacent engineering experience"
    skills_text = ", ".join(top_skills) if top_skills else "limited skill detail"

    if score >= 80:
        lead = f"Strong fit: {years:.1f} years in {title} at {company}, with {evidence_text}."
    elif score >= 65:
        lead = f"Good fit: {years:.1f} years in {title} at {company}, plus {evidence_text}."
    elif score >= 50:
        lead = f"Adjacent fit: {years:.1f} years in {title} at {company}, with some {evidence_text}."
    else:
        lead = f"Weaker fit: {years:.1f} years in {title} at {company}, but the profile leans toward {skills_text} rather than the JD's retrieval and ranking focus."

    concerns = []
    if notice is not None and int(notice) > 60:
        concerns.append(f"{int(notice)}-day notice period")
    if not open_to_work:
        concerns.append("not marked open to work")
    if response_rate < 0.35:
        concerns.append(f"{response_rate:.0%} recruiter response rate")
    if location:
        concerns.append(location)
    if diagnostics.get("honeypot_penalty", 0.0) < 0:
        concerns.append("suspicious profile consistency")

    if concerns:
        tail = f"Main caveat: {', '.join(concerns[:3])}."
    else:
        tail = "No major availability or consistency red flags from the profile."

    if score >= 80:
        second = f"The profile also shows top skills like {skills_text}, and the recent signals are healthy enough to support recruiter follow-up."
    elif score >= 65:
        second = "The strongest evidence comes from the career history rather than the skills list, which is the right shape for this JD."
    elif score >= 50:
        second = "The profile is credible but still looks more adjacent than exact, so it should sit below the obvious search and ranking specialists."
    else:
        second = "The JD wants proven retrieval and ranking depth, and this profile does not yet show enough of that in the work history."

    return f"{lead} {second} {tail}"
