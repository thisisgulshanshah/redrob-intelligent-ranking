import re
from dataclasses import dataclass


@dataclass
class JobRequirements:
    min_experience: float
    max_experience: float

    required_skills: list[str]
    preferred_skills: list[str]

    avoid_service_only: bool

    prefer_product: bool

    max_notice_days: int

    require_ranking_background: bool

    require_open_source: bool

    require_python: bool


class JDParser:

    def parse(self, text: str) -> JobRequirements:

        text = text.lower()

        required = [
            "python",
            "embeddings",
            "retrieval",
            "vector",
            "ranking",
            "evaluation",
        ]

        preferred = [
            "lora",
            "qlora",
            "peft",
            "learning-to-rank",
            "marketplace",
            "hr-tech",
            "opensource",
        ]

        exp = re.search(r"(\d+)\s*[-–]\s*(\d+)\s*years", text)

        if exp:
            mn = float(exp.group(1))
            mx = float(exp.group(2))
        else:
            mn = 0
            mx = 100

        return JobRequirements(
            min_experience=mn,
            max_experience=mx,
            required_skills=required,
            preferred_skills=preferred,
            avoid_service_only=True,
            prefer_product=True,
            max_notice_days=30,
            require_ranking_background=True,
            require_open_source=True,
            require_python=True,
        )
