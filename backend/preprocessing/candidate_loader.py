
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Candidate:
    candidate_id: str

    name: Optional[str] = None
    headline: Optional[str] = None
    location: Optional[str] = None
    country: Optional[str] = None

    experience_years: float = 0.0
    current_title: Optional[str] = None
    current_company: Optional[str] = None

    career_history: List[Dict[str, Any]] = field(default_factory=list)
    education: List[Dict[str, Any]] = field(default_factory=list)
    skills: List[Dict[str, Any]] = field(default_factory=list)
    certifications: List[Dict[str, Any]] = field(default_factory=list)
    languages: List[Dict[str, Any]] = field(default_factory=list)

    redrob_signals: Dict[str, Any] = field(default_factory=dict)
    raw_data: Dict[str, Any] = field(default_factory=dict)
