import gzip
import json
from pathlib import Path
from typing import Generator

from backend.models.candidate import Candidate


class CandidateLoader:

    @staticmethod
    def load(path: str | Path) -> Generator[Candidate, None, None]:

        path = Path(path)

        opener = gzip.open if path.suffix == ".gz" else open

        with opener(path, "rt", encoding="utf-8") as f:
            for line in f:

                line = line.strip()

                if not line:
                    continue

                obj = json.loads(line)

                yield Candidate(
                    candidate_id=obj["candidate_id"],
                    data=obj,
                )