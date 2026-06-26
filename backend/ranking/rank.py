from __future__ import annotations

import argparse
import csv
import heapq
import sys
from pathlib import Path
from typing import List, Tuple

if __package__ in {None, ""}:
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from backend.features.feature_extractor import FeatureExtractor
from backend.loaders.candidate_loader import CandidateLoader
from backend.ranking.reasoning import build_reasoning
from backend.ranking.scorer import CandidateScorer
from backend.ranking.honeypot import is_honeypot


def _invert_candidate_id(candidate_id: str) -> str:
    return "".join(chr(255 - ord(ch)) for ch in candidate_id)


def _load_jd_text(jd_path: str | Path) -> str:
    path = Path(jd_path)
    if not path.exists():
        return ""

    suffix = path.suffix.lower()
    if suffix in {".txt", ".md"}:
        return path.read_text(encoding="utf-8")

    if suffix == ".docx":
        try:
            from docx import Document
        except Exception as exc:
            raise RuntimeError(
                "python-docx is required to read .docx job descriptions. "
                "Install it with: pip install python-docx"
            ) from exc

        doc = Document(str(path))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

    return path.read_text(encoding="utf-8", errors="ignore")


def _top_100_stream(candidates_path: str, jd_text: str) -> List[Tuple[float, str, str]]:
    extractor = FeatureExtractor()
    scorer = CandidateScorer()

    heap: List[Tuple[float, str, str, str]] = []

    skipped_honeypots = 0
    for idx, candidate in enumerate(CandidateLoader.load(candidates_path), start=1):
        if is_honeypot(candidate):
            skipped_honeypots += 1
            continue
        features = extractor.extract(candidate)
        score, diagnostics = scorer.score(candidate, features, jd_text=jd_text)
        reasoning = build_reasoning(candidate, score, diagnostics)

        candidate_id = getattr(candidate, "candidate_id")
        item = (float(score), _invert_candidate_id(candidate_id), candidate_id, reasoning)

        if len(heap) < 100:
            heapq.heappush(heap, item)
        else:
            if item > heap[0]:
                heapq.heapreplace(heap, item)

        if idx % 10000 == 0:
            print(f"Scored {idx} candidates...", file=sys.stderr)

    print(f"Skipped {skipped_honeypots} honeypot candidates.", file=sys.stderr)
    ranked = sorted(heap, key=lambda x: (-x[0], x[2]))
    return [(score, candidate_id, reasoning) for score, _, candidate_id, reasoning in ranked]


def write_submission(rows: List[Tuple[float, str, str]], out_path: str | Path) -> None:
    path = Path(out_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if len(rows) != 100:
        raise ValueError(f"Expected 100 rows, got {len(rows)}")

    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["candidate_id", "rank", "score", "reasoning"])
        for rank, (score, candidate_id, reasoning) in enumerate(rows, start=1):
            writer.writerow([candidate_id, rank, f"{score:.6f}", reasoning])


def main() -> None:
    parser = argparse.ArgumentParser(description="Redrob top-100 candidate ranker")
    parser.add_argument("--candidates", required=True)
    parser.add_argument("--jd", required=True)
    parser.add_argument("--out", default="submissions/submission.csv")
    args = parser.parse_args()

    jd_text = _load_jd_text(args.jd)
    rows = _top_100_stream(args.candidates, jd_text)
    write_submission(rows, args.out)

    print(f"Wrote {len(rows)} rows to {args.out}")


if __name__ == "__main__":
    main()
