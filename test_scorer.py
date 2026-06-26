from backend.loaders.candidate_loader import CandidateLoader
from backend.features.feature_extractor import FeatureExtractor
from backend.ranker.scorer import CandidateScorer

DATASET = "backend/data/raw/candidates.jsonl"

loader_gen = CandidateLoader.load(DATASET)
candidate = next(loader_gen)

features = FeatureExtractor().extract(candidate)
score = CandidateScorer().score(features)

print(f"Candidate: {candidate.candidate_id}")
print(f"Score: {score}")
