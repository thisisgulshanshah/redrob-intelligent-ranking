from collections import Counter

from backend.models.candidate import Candidate

PRODUCT_COMPANIES = {
    "Google",
    "Microsoft",
    "Amazon",
    "Meta",
    "Apple",
    "Netflix",
    "Uber",
    "Ola",
    "Swiggy",
    "Zomato",
    "Razorpay",
    "Pied Piper",
    "Acme Corp",
    "Hooli",
    "Globex Inc",
}


SERVICE_COMPANIES = {
    "TCS",
    "Infosys",
    "Wipro",
    "Accenture",
    "Capgemini",
    "Cognizant",
    "Mindtree",
}


class FeatureExtractor:

    def extract(self, candidate: Candidate) -> dict:

        profile = candidate.profile
        skills = candidate.skills
        history = candidate.career_history
        education = candidate.education
        signals = candidate.redrob_signals

        skill_names = [x["name"].lower() for x in skills]

        companies = [x["company"] for x in history]

        features = {}

        # ---------- profile ----------

        features["experience"] = profile.get(
            "years_of_experience",
            0,
        )

        features["headline"] = profile.get(
            "headline",
            "",
        ).lower()

        features["summary"] = profile.get(
            "summary",
            "",
        ).lower()

        # ---------- skills ----------

        features["skills"] = skill_names

        features["skill_count"] = len(skill_names)

        # ---------- companies ----------

        features["product_company_count"] = sum(
            company in PRODUCT_COMPANIES for company in companies
        )

        features["service_company_count"] = sum(
            company in SERVICE_COMPANIES for company in companies
        )

        # ---------- education ----------

        tiers = Counter(e.get("tier", "") for e in education)

        features["tier2_degree"] = tiers["tier_2"]

        features["tier1_degree"] = tiers["tier_1"]

        # ---------- signals ----------

        features["open_to_work"] = signals.get(
            "open_to_work_flag",
            False,
        )

        features["response_rate"] = signals.get(
            "recruiter_response_rate",
            0,
        )

        features["github_score"] = signals.get(
            "github_activity_score",
            -1,
        )

        features["profile_score"] = signals.get(
            "profile_completeness_score",
            0,
        )

        features["notice_period"] = signals.get(
            "notice_period_days",
            180,
        )

        features["interview_completion"] = signals.get(
            "interview_completion_rate",
            0,
        )

        return features
