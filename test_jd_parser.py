from pathlib import Path

from backend.parser.jd_parser import JDParser

jd = Path("backend/data/job_description.txt").read_text()

parser = JDParser()

req = parser.parse(jd)

print(req)
