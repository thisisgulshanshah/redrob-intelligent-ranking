from backend.loaders.candidate_loader import CandidateLoader

DATASET = "backend/data/raw/candidates.jsonl"

for i, candidate in enumerate(CandidateLoader.load(DATASET)):

    print(candidate.candidate_id)
    print(candidate.profile["headline"])
    print(candidate.profile["years_of_experience"])
    print("-" * 50)

    if i == 4:
        break
