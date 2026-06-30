from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from math import log1p
from typing import Any, Dict, List, Sequence, Tuple


PRODUCT_COMPANIES = {
    "google", "microsoft", "amazon", "meta", "apple", "netflix", "uber", "ola",
    "swiggy", "zomato", "razorpay", "pied piper", "acme corp", "hooli", "globex inc",
    "wayve", "bytedance", "spotify", "airbnb", "stripe", "shopify",
}

SERVICE_COMPANIES = {
    "tcs", "infosys", "wipro", "accenture", "capgemini", "cognizant", "mindtree",
    "ltimindtree", "hcl", "tech mahindra", "deloitte", "pwc", "ey", "kpmg",
}

RETRIEVAL_TERMS = {
    "retrieval", "ranking", "recommendation", "search", "vector", "embedding",
    "embeddings", "faiss", "qdrant", "milvus", "weaviate", "pinecone",
    "elasticsearch", "opensearch", "bm25", "ndcg", "mrr", "map", "learning to rank",
    "ltr", "sentence-transformers", "bge", "e5", "rag", "llm", "fine-tuning",
}

TECH_TERMS = {
    "python", "sql", "spark", "airflow", "dbt", "kafka", "postgres", "postgresql",
    "snowflake", "bigquery", "aws", "gcp", "azure", "kubeflow", "mlops", "pytorch",
    "tensorflow", "hugging face", "transformers", "fastapi", "docker", "kubernetes",
}

LOCATION_BONUS = {
    "pune": 3.5,
    "noida": 3.5,
    "hyderabad": 2.0,
    "mumbai": 2.0,
    "delhi": 2.0,
    "ncr": 2.0,
    "bengaluru": 1.5,
    "bangalore": 1.5,
}



ENGINEERING_TITLES = {
    "ai specialist", "ai research engineer", "data scientist", "ml engineer",
    "computer vision engineer", "nlp engineer", "ai engineer", "machine learning engineer",
    "recommendation systems", "applied ml engineer", "mlops engineer",
    "ml infrastructure engineer", "deep learning engineer", "research scientist",
    "applied scientist", "search engineer", "ranking engineer", "relevance",
    "information retrieval", "personalization engineer",
    "ai platform engineer", "genai engineer", "llm engineer", "nlp scientist",
    "computer vision scientist", "knowledge graph engineer", "ai infrastructure engineer",
    "ml research engineer",
}

# Off-domain titles only. Generic titles (Software Engineer, Data Engineer, Backend
# Engineer, Analytics Engineer) deliberately excluded — too ambiguous to penalize on
# title alone; career_history/skills/jd_fit scoring decides those cases instead.
NEGATIVE_TITLES = {
    "business analyst", "mechanical engineer", "marketing manager", "project manager",
    "hr manager", "operations manager", "accountant", "content writer", "civil engineer",
    "customer support", "graphic designer", "sales executive", "devops engineer",
    "cloud engineer", "full stack developer", ".net developer", "java developer",
    "frontend engineer", "qa engineer", "mobile developer", "recruiter", "teacher",
    "lecturer", "finance manager", "legal counsel", "supply chain manager",
    "logistics manager", "procurement manager", "product manager", "ui designer",
    "ux designer", "network engineer", "system administrator", "database administrator",
    "site reliability engineer", "solutions architect", "technical writer", "scrum master",
    "quality analyst", "embedded engineer", "hardware engineer", "electrical engineer",
    "sales engineer", "customer success manager", "social media manager", "seo specialist",
    "financial analyst", "investment banker",
}

import re as _re

_SYNONYM_MAP = [
    (_re.compile(r"\(ml\)"), "ml engineer"), (_re.compile(r"\(ai\)"), "ai engineer"),
    (_re.compile(r"\bmachine learning\b"), "ml"), (_re.compile(r"\bnatural language processing\b"), "nlp"),
    (_re.compile(r"\bartificial intelligence\b"), "ai"), (_re.compile(r"\brecommender\b"), "recommendation"),
    (_re.compile(r"\bcv engineer\b"), "computer vision engineer"),
    (_re.compile(r"\bsearch relevance\b"), "relevance"), (_re.compile(r"\binfo retrieval\b"), "information retrieval"),
    (_re.compile(r"\bgenerative ai\b"), "genai"), (_re.compile(r"\blarge language model\b"), "llm"),
]

def _normalize_for_title_match(title: str) -> str:
    t = title.lower().strip()
    for pattern, canonical in _SYNONYM_MAP:
        t = pattern.sub(canonical, t)
    return t


def _normalize_text(value: Any) -> str:
    return str(value or "").strip().lower()


def _candidate_profile(candidate: Any) -> Dict[str, Any]:
    if hasattr(candidate, "profile"):
        prof = getattr(candidate, "profile") or {}
        if isinstance(prof, dict):
            return prof

    data = getattr(candidate, "data", None)
    if isinstance(data, dict):
        prof = data.get("profile", {})
        if isinstance(prof, dict):
            return prof

    raw = getattr(candidate, "raw_data", None)
    if isinstance(raw, dict):
        prof = raw.get("profile", {})
        if isinstance(prof, dict):
            return prof

    return {}


def _candidate_skills(candidate: Any) -> List[Dict[str, Any]]:
    if hasattr(candidate, "skills"):
        skills = getattr(candidate, "skills") or []
        if isinstance(skills, list):
            return skills

    data = getattr(candidate, "data", None)
    if isinstance(data, dict):
        skills = data.get("skills", [])
        if isinstance(skills, list):
            return skills

    raw = getattr(candidate, "raw_data", None)
    if isinstance(raw, dict):
        skills = raw.get("skills", [])
        if isinstance(skills, list):
            return skills

    return []


def _candidate_history(candidate: Any) -> List[Dict[str, Any]]:
    if hasattr(candidate, "career_history"):
        history = getattr(candidate, "career_history") or []
        if isinstance(history, list):
            return history

    data = getattr(candidate, "data", None)
    if isinstance(data, dict):
        history = data.get("career_history", [])
        if isinstance(history, list):
            return history

    raw = getattr(candidate, "raw_data", None)
    if isinstance(raw, dict):
        history = raw.get("career_history", [])
        if isinstance(history, list):
            return history

    return []


def _candidate_education(candidate: Any) -> List[Dict[str, Any]]:
    if hasattr(candidate, "education"):
        education = getattr(candidate, "education") or []
        if isinstance(education, list):
            return education

    data = getattr(candidate, "data", None)
    if isinstance(data, dict):
        education = data.get("education", [])
        if isinstance(education, list):
            return education

    raw = getattr(candidate, "raw_data", None)
    if isinstance(raw, dict):
        education = raw.get("education", [])
        if isinstance(education, list):
            return education

    return []


def _candidate_signals(candidate: Any) -> Dict[str, Any]:
    if hasattr(candidate, "redrob_signals"):
        signals = getattr(candidate, "redrob_signals") or {}
        if isinstance(signals, dict):
            return signals

    data = getattr(candidate, "data", None)
    if isinstance(data, dict):
        signals = data.get("redrob_signals", {})
        if isinstance(signals, dict):
            return signals

    raw = getattr(candidate, "raw_data", None)
    if isinstance(raw, dict):
        signals = raw.get("redrob_signals", {})
        if isinstance(signals, dict):
            return signals

    return {}


def _history_text(candidate: Any) -> str:
    profile = _candidate_profile(candidate)
    chunks = [
        _normalize_text(profile.get("headline")),
        _normalize_text(profile.get("summary")),
        _normalize_text(profile.get("current_title")),
        _normalize_text(profile.get("current_company")),
    ]
    for item in _candidate_history(candidate):
        if not isinstance(item, dict):
            continue
        chunks.extend(
            [
                _normalize_text(item.get("company")),
                _normalize_text(item.get("title")),
                _normalize_text(item.get("industry")),
                _normalize_text(item.get("description")),
            ]
        )
    return " ".join(chunks)


def _skill_text(candidate: Any) -> str:
    texts = []
    for s in _candidate_skills(candidate):
        if not isinstance(s, dict):
            continue
        texts.append(_normalize_text(s.get("name")))
    return " ".join(texts)


def _days_since(date_str: Any, today: date | None = None) -> int | None:
    if not date_str:
        return None
    try:
        dt = datetime.strptime(str(date_str), "%Y-%m-%d").date()
    except ValueError:
        return None
    today = today or date.today()
    return max(0, (today - dt).days)


def _company_bucket(company: str) -> str:
    c = _normalize_text(company)
    if c in PRODUCT_COMPANIES:
        return "product"
    if c in SERVICE_COMPANIES:
        return "service"
    return "unknown"


@dataclass
class ScoreBreakdown:
    experience: float = 0.0
    career: float = 0.0
    skills: float = 0.0
    behavior: float = 0.0
    location: float = 0.0
    education: float = 0.0
    jd_fit: float = 0.0
    honeypot_penalty: float = 0.0

    def total(self) -> float:
        return self.experience + self.career + self.skills + self.behavior + self.location + self.education + self.jd_fit + self.honeypot_penalty


class CandidateScorer:
    def score(self, candidate: Any, features: Dict[str, Any], jd_text: str = "") -> Tuple[float, Dict[str, Any]]:
        profile = _candidate_profile(candidate)
        signals = _candidate_signals(candidate)
        history = _candidate_history(candidate)
        education = _candidate_education(candidate)
        skills = _candidate_skills(candidate)

        breakdown = ScoreBreakdown()

        experience = float(features.get("experience", profile.get("years_of_experience", 0.0)) or 0.0)
        breakdown.experience = self._experience_score(experience)

        breakdown.career = self._career_score(candidate, profile, history)
        breakdown.skills = self._skills_score(skills)
        breakdown.behavior = self._behavior_score(signals)
        breakdown.location = self._location_score(profile, signals)
        breakdown.education = self._education_score(education)
        breakdown.jd_fit = self._jd_fit_score(candidate, profile, history, skills, jd_text)
        breakdown.honeypot_penalty = self._honeypot_penalty(candidate, profile, history, skills, signals, experience)

        total = breakdown.total()
        total = max(0.0, total)
        total = round(total, 6)

        diagnostics = {
            "experience": breakdown.experience,
            "career": breakdown.career,
            "skills": breakdown.skills,
            "behavior": breakdown.behavior,
            "location": breakdown.location,
            "education": breakdown.education,
            "jd_fit": breakdown.jd_fit,
            "honeypot_penalty": breakdown.honeypot_penalty,
            "experience_years": experience,
            "candidate_text": _history_text(candidate),
            "skill_text": _skill_text(candidate),
            "signals": signals,
        }
        return total, diagnostics

    def _experience_score(self, years: float) -> float:
        if 5.0 <= years <= 9.0:
            return 20.0
        if 4.0 <= years < 5.0 or 9.0 < years <= 10.0:
            return 16.0
        if 3.0 <= years < 4.0 or 10.0 < years <= 12.0:
            return 12.0
        if years < 3.0:
            return max(0.0, 10.0 - (3.0 - years) * 2.5)
        return max(0.0, 12.0 - (years - 10.0) * 1.5)

    def _career_score(self, candidate: Any, profile: Dict[str, Any], history: Sequence[Dict[str, Any]]) -> float:
        text = _history_text(candidate)
        score = 0.0

        companies = []
        product_evidence = 0
        retrieval_evidence = 0
        engineering_evidence = 0

        for item in history:
            if not isinstance(item, dict):
                continue
            company = _normalize_text(item.get("company"))
            title = _normalize_text(item.get("title"))
            desc = _normalize_text(item.get("description"))
            industry = _normalize_text(item.get("industry"))
            companies.append(company)

            bucket = _company_bucket(company)
            if bucket == "product":
                score += 4.0
            elif bucket == "service":
                score += 0.5

            for term in ("product", "user", "users", "feature", "shipping", "launched", "launch", "experiment", "a/b", "revenue"):
                if term in desc:
                    product_evidence += 1
            for term in RETRIEVAL_TERMS:
                if term in desc or term in title:
                    retrieval_evidence += 1
            for term in ("production", "deployed", "monitoring", "evaluation", "offline", "benchmark", "scale", "real-time", "search"):
                if term in desc:
                    engineering_evidence += 1

        if companies and all(_company_bucket(c) == "service" for c in companies):
            score -= 6.0

        if retrieval_evidence:
            score += min(18.0, retrieval_evidence * 3.0)

        if product_evidence:
            score += min(10.0, product_evidence * 1.5)

        if engineering_evidence:
            score += min(8.0, engineering_evidence * 1.0)

        current_title = _normalize_for_title_match(profile.get("current_title") or "")
        if any(term in current_title for term in ENGINEERING_TITLES):
            score += 6.0

        if any(term in current_title for term in NEGATIVE_TITLES):
            score -= 8.0
            score = min(score, 5.0)

        return max(-10.0, min(30.0, score))

    def _skills_score(self, skills: Sequence[Dict[str, Any]]) -> float:
        score = 0.0
        relevant_hits = 0
        generic_hits = 0

        for skill in skills:
            if not isinstance(skill, dict):
                continue
            name = _normalize_text(skill.get("name"))
            prof = _normalize_text(skill.get("proficiency"))
            endorsements = int(skill.get("endorsements", 0) or 0)
            duration = int(skill.get("duration_months", 0) or 0)

            prof_mult = {
                "beginner": 0.35,
                "intermediate": 0.7,
                "advanced": 1.0,
                "expert": 1.15,
            }.get(prof, 0.5)

            evidence = 0.0
            if any(term == name or term in name for term in RETRIEVAL_TERMS):
                evidence += 3.0
                relevant_hits += 1
            if any(term == name or term in name for term in TECH_TERMS):
                evidence += 1.0
                generic_hits += 1

            evidence += min(2.0, endorsements / 20.0)
            evidence += min(1.5, duration / 24.0)
            evidence *= prof_mult

            score += evidence

        if relevant_hits == 0 and generic_hits > 8:
            score += 1.5

        return max(0.0, min(18.0, score))

    def _behavior_score(self, signals: Dict[str, Any]) -> float:
        score = 0.0

        if signals.get("open_to_work_flag"):
            score += 3.5

        response_rate = float(signals.get("recruiter_response_rate", 0.0) or 0.0)
        score += min(5.0, response_rate * 8.0)

        interview_rate = float(signals.get("interview_completion_rate", 0.0) or 0.0)
        score += min(3.0, interview_rate * 4.0)

        profile_completeness = float(signals.get("profile_completeness_score", 0.0) or 0.0)
        score += min(3.0, profile_completeness / 35.0)

        github_score = float(signals.get("github_activity_score", -1) or -1)
        if github_score >= 0:
            score += min(4.0, github_score / 20.0)

        notice = int(signals.get("notice_period_days", 180) or 180)
        if notice <= 30:
            score += 4.0
        elif notice <= 60:
            score += 2.0
        elif notice <= 90:
            score += 1.0
        else:
            score -= 2.0

        last_active = _days_since(signals.get("last_active_date"))
        if last_active is not None:
            if last_active <= 30:
                score += 5.0
            elif last_active <= 90:
                score += 3.0
            elif last_active <= 180:
                score += 1.0
            else:
                score -= 6.0

        if bool(signals.get("verified_email")):
            score += 0.8
        if bool(signals.get("verified_phone")):
            score += 0.8
        if bool(signals.get("linkedin_connected")):
            score += 0.8

        saved = int(signals.get("saved_by_recruiters_30d", 0) or 0)
        search_appearances = int(signals.get("search_appearance_30d", 0) or 0)
        score += min(2.0, log1p(saved) / 2.0)
        score += min(1.5, log1p(search_appearances) / 4.0)

        return max(-10.0, min(16.0, score))

    def _location_score(self, profile: Dict[str, Any], signals: Dict[str, Any]) -> float:
        location = _normalize_text(profile.get("location"))
        country = _normalize_text(profile.get("country"))
        willing = bool(signals.get("willing_to_relocate", False))

        score = 0.0
        for key, bonus in LOCATION_BONUS.items():
            if key in location:
                score += bonus

        if country == "india" and score == 0.0:
            score += 1.0

        if country and country != "india" and not willing:
            score -= 4.0
        elif country and country != "india" and willing:
            score -= 1.0

        return max(-4.0, min(4.0, score))

    def _education_score(self, education: Sequence[Dict[str, Any]]) -> float:
        score = 0.0
        for item in education:
            if not isinstance(item, dict):
                continue
            tier = _normalize_text(item.get("tier"))
            if tier == "tier_1":
                score += 4.0
            elif tier == "tier_2":
                score += 3.0
            elif tier == "tier_3":
                score += 1.0
        return max(0.0, min(6.0, score))

    def _jd_fit_score(
        self,
        candidate: Any,
        profile: Dict[str, Any],
        history: Sequence[Dict[str, Any]],
        skills: Sequence[Dict[str, Any]],
        jd_text: str,
    ) -> float:
        text = (jd_text or "").lower()
        if not text:
            text = ""

        evidence = _history_text(candidate)

        score = 0.0

        jd_core_terms = [
            "retrieval", "ranking", "search", "embedding", "embeddings", "vector",
            "llm", "fine-tuning", "evaluation", "ndcg", "mrr", "map", "python",
        ]
        jd_pref_terms = [
            "product", "product company", "open source", "hr-tech", "marketplace",
            "hybrid", "pune", "noida", "relocation", "offline", "a/b",
        ]

        core_hits = sum(1 for term in jd_core_terms if term in evidence)
        pref_hits = sum(1 for term in jd_pref_terms if term in evidence)

        score += min(12.0, core_hits * 2.5)
        score += min(5.0, pref_hits * 1.0)

        # Give only a tiny boost for skills keywords, since the JD says skills-only matching is a trap.
        skill_blob = _skill_text(candidate)
        skill_hits = sum(1 for term in ("retrieval", "ranking", "search", "embedding", "python", "faiss", "qdrant", "milvus", "elasticsearch", "opensearch") if term in skill_blob)
        score += min(4.0, skill_hits * 0.5)

        current_company = _normalize_text(profile.get("current_company"))
        if current_company in PRODUCT_COMPANIES:
            score += 2.0

        return max(0.0, min(18.0, score))

    def _honeypot_penalty(
        self,
        candidate: Any,
        profile: Dict[str, Any],
        history: Sequence[Dict[str, Any]],
        skills: Sequence[Dict[str, Any]],
        signals: Dict[str, Any],
        declared_experience_years: float,
    ) -> float:
        total_history_months = 0
        for item in history:
            if not isinstance(item, dict):
                continue
            total_history_months += int(item.get("duration_months", 0) or 0)

        total_history_years = total_history_months / 12.0
        expert_skills = 0
        advanced_skills = 0
        short_high_level_skills = 0

        for skill in skills:
            if not isinstance(skill, dict):
                continue
            prof = _normalize_text(skill.get("proficiency"))
            duration = int(skill.get("duration_months", 0) or 0)

            if prof == "expert":
                expert_skills += 1
            if prof == "advanced":
                advanced_skills += 1
            if prof in {"advanced", "expert"} and duration <= 3:
                short_high_level_skills += 1

        penalty = 0.0

        if declared_experience_years >= 5.0 and total_history_years > 0:
            if declared_experience_years > total_history_years + 2.5:
                penalty += 35.0

        if expert_skills >= 5 and short_high_level_skills >= 3:
            penalty += 30.0

        profile_completeness = float(signals.get("profile_completeness_score", 0.0) or 0.0)
        if profile_completeness < 25.0 and (expert_skills + advanced_skills) >= 6:
            penalty += 20.0

        last_active = _days_since(signals.get("last_active_date"))
        response_rate = float(signals.get("recruiter_response_rate", 0.0) or 0.0)
        if last_active is not None and last_active > 180 and response_rate < 0.1:
            penalty += 20.0

        current_title = _normalize_text(profile.get("current_title"))
        current_company = _normalize_text(profile.get("current_company"))
        if current_title and any(t in current_title for t in NEGATIVE_TITLES):
            if all(_company_bucket(item.get("company", "")) == "service" for item in history if isinstance(item, dict)) and not any(term in _history_text(candidate) for term in RETRIEVAL_TERMS):
                penalty += 12.0

        return -min(80.0, penalty)
