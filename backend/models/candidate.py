from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class Candidate:
    candidate_id: str
    data: dict[str, Any]

    @property
    def profile(self) -> dict:
        return self.data.get("profile", {})

    @property
    def skills(self) -> list:
        return self.data.get("skills", [])

    @property
    def career_history(self) -> list:
        return self.data.get("career_history", [])

    @property
    def education(self) -> list:
        return self.data.get("education", [])

    @property
    def redrob_signals(self) -> dict:
        return self.data.get("redrob_signals", {})
