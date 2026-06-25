from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

ROOT = Path(__file__).resolve().parents[2]

DATA_DIR = ROOT / "data"
RAW_DATA = DATA_DIR / "raw"
EMBEDDING_DIR = DATA_DIR / "embeddings"

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "BAAI/bge-large-en-v1.5"
)

TOP_K = int(os.getenv("TOP_K", 50))
RERANK_TOP_K = int(os.getenv("RERANK_TOP_K", 10))


