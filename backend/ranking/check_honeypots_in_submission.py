import csv

with open("backend/data/raw/honeypot_candidates.txt") as f:
    honeypots = set(line.strip() for line in f)

with open("submissions/submission.csv") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

flagged_in_submission = [r for r in rows if r["candidate_id"] in honeypots]

print(f"Total rows in submission: {len(rows)}")
print(f"Honeypots found in submission: {len(flagged_in_submission)}")
print(f"Honeypot rate: {len(flagged_in_submission)/len(rows)*100:.1f}%  (disqualified if > 10%)")

if flagged_in_submission:
    print("\nFlagged rows:")
    for r in flagged_in_submission:
        print(f"  {r['candidate_id']} rank={r['rank']} score={r['score']}")
