import json
import sys
from pathlib import Path

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.loaders.candidate_loader import CandidateLoader
from backend.features.feature_extractor import FeatureExtractor
from backend.ranking.scorer import CandidateScorer

JD_PATH = "backend/data/raw/job_description.docx"
TARGETS = {"CAND_0005644", "CAND_0006521"}

def load_jd_text(path):
    from docx import Document
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

jd_text = load_jd_text(JD_PATH)
extractor = FeatureExtractor()
scorer = CandidateScorer()

for candidate in CandidateLoader.load("backend/data/raw/candidates.jsonl"):
    cid = getattr(candidate, "candidate_id")
    if cid in TARGETS:
        features = extractor.extract(candidate)
        score, diagnostics = scorer.score(candidate, features, jd_text=jd_text)
        print(f"=== {cid} ===")
        print(f"Total score: {score}")
        for k, v in diagnostics.items():
            if k not in ("candidate_text", "skill_text"):
                print(f"  {k}: {v}")
        print()
