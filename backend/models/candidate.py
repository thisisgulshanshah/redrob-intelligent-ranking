from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class Candidate:
    candidate_id: str
    data: dict[str, Any]

    @property
    def profile(self) -> dict:
        value = self.data.get("profile", {})
        return value if isinstance(value, dict) else {}

    @property
    def skills(self) -> list:
        value = self.data.get("skills", [])
        return value if isinstance(value, list) else []

    @property
    def career_history(self) -> list:
        value = self.data.get("career_history", [])
        return value if isinstance(value, list) else []

    @property
    def education(self) -> list:
        value = self.data.get("education", [])
        return value if isinstance(value, list) else []

    @property
    def redrob_signals(self) -> dict:
        value = self.data.get("redrob_signals", {})
        return value if isinstance(value, dict) else {}
