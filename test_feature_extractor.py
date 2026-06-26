from backend.features.feature_extractor import FeatureExtractor
from backend.loaders.candidate_loader import CandidateLoader

loader = CandidateLoader()
extractor = FeatureExtractor()

candidate = next(loader.load("backend/data/raw/candidates.jsonl"))

features = extractor.extract(candidate)

for k, v in features.items():
    print(f"{k:<30} {v}")

