from __future__ import annotations
import csv
import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.loaders.candidate_loader import CandidateLoader
from backend.features.feature_extractor import FeatureExtractor
from backend.ranking.honeypot import is_honeypot

SUBMISSION_PATH = "submissions/submission.csv"
CANDIDATES_PATH = "backend/data/raw/candidates.jsonl"
TOP_N = 20

def load_submission_top_n(path, n):
    with open(path) as f:
        rows = list(csv.DictReader(f))
    return rows[:n]

def main():
    top_rows = load_submission_top_n(SUBMISSION_PATH, TOP_N)
    wanted_ids = {r["candidate_id"] for r in top_rows}
    rank_lookup = {r["candidate_id"]: r for r in top_rows}

    extractor = FeatureExtractor()
    found = {}

    for candidate in CandidateLoader.load(CANDIDATES_PATH):
        cid = getattr(candidate, "candidate_id")
        if cid in wanted_ids:
            found[cid] = candidate
        if len(found) == len(wanted_ids):
            break

    print(f"{'Rank':<5} {'Candidate ID':<15} {'Score':<8} {'Title':<35} {'Company':<20} {'Exp':<5} {'Honeypot'}")
    print("-" * 110)

    for cid in sorted(found, key=lambda c: int(rank_lookup[c]["rank"])):
        candidate = found[cid]
        row = rank_lookup[cid]
        profile = getattr(candidate, "profile", {}) or {}
        features = extractor.extract(candidate)

        title = str(profile.get("current_title", "?"))[:34]
        company = str(profile.get("current_company", "?"))[:19]
        exp = features.get("experience", "?")
        honeypot_flag = is_honeypot(candidate)

        print(f"{row['rank']:<5} {cid:<15} {row['score']:<8} {title:<35} {company:<20} {exp:<5} {honeypot_flag}")

    print("\n--- Detailed view ---\n")
    for cid in sorted(found, key=lambda c: int(rank_lookup[c]["rank"])):
        candidate = found[cid]
        row = rank_lookup[cid]
        profile = getattr(candidate, "profile", {}) or {}
        skills = getattr(candidate, "skills", None) or []
        if isinstance(skills, list):
            skill_names = []
            for s in skills[:6]:
                if isinstance(s, dict):
                    skill_names.append(str(s.get("name") or s.get("skill") or s))
                else:
                    skill_names.append(str(s))
            skills_display = ", ".join(skill_names)
        else:
            skills_display = str(skills)

        print(f"Rank {row['rank']} | {cid} | Score {row['score']}")
        print(f"  Title: {profile.get('current_title', '?')} @ {profile.get('current_company', '?')}")
        print(f"  Location: {profile.get('location', '?')}")
        print(f"  Top skills: {skills_display}")
        print(f"  Reasoning: {row['reasoning']}")
        print()

if __name__ == "__main__":
    main()
