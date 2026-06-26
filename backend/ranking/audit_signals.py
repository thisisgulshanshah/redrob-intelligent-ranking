import json
from collections import Counter, defaultdict
from datetime import datetime

path = "backend/data/raw/candidates.jsonl"
anomaly_counts = Counter()
per_candidate_flags = defaultdict(list)
total = 0

def flag(name, cid):
    anomaly_counts[name] += 1
    per_candidate_flags[cid].append(name)

with open(path) as f:
    for line in f:
        total += 1
        c = json.loads(line)
        cid = c.get("candidate_id", "UNKNOWN")
        sig = c.get("redrob_signals", {})

        try:
            signup = datetime.fromisoformat(sig.get("signup_date", "").replace("Z",""))
            last_active = datetime.fromisoformat(sig.get("last_active_date", "").replace("Z",""))
            if last_active < signup:
                flag("last_active_before_signup", cid)
        except Exception:
            flag("bad_date_format", cid)

        rrr = sig.get("recruiter_response_rate")
        if rrr is not None and not (0.0 <= rrr <= 1.0):
            flag("response_rate_out_of_range", cid)

        icr = sig.get("interview_completion_rate")
        if icr is not None and not (0.0 <= icr <= 1.0):
            flag("interview_completion_out_of_range", cid)

        oar = sig.get("offer_acceptance_rate")
        if oar is not None and not (-1 <= oar <= 1.0):
            flag("offer_acceptance_out_of_range", cid)

        if oar is not None and oar > 0 and icr == 0:
            flag("accepted_offer_but_zero_interviews", cid)

        gh = sig.get("github_activity_score")
        if gh is not None and not (-1 <= gh <= 100):
            flag("github_score_out_of_range", cid)

        npd = sig.get("notice_period_days")
        if npd is not None and not (0 <= npd <= 180):
            flag("notice_period_out_of_range", cid)

        pcs = sig.get("profile_completeness_score")
        if pcs is not None and not (0 <= pcs <= 100):
            flag("profile_completeness_out_of_range", cid)

        sal_min = sig.get("expected_salary_range_inr_lpa", {}).get("min")
        sal_max = sig.get("expected_salary_range_inr_lpa", {}).get("max")
        if sal_min is not None and sal_max is not None and sal_min > sal_max:
            flag("salary_min_greater_than_max", cid)

        if rrr is not None and rrr > 0.9 and sig.get("avg_response_time_hours", 0) > 500:
            flag("high_response_rate_but_slow_response", cid)

        if not sig.get("verified_email") and not sig.get("verified_phone") and not sig.get("linkedin_connected"):
            if sig.get("endorsements_received", 0) > 50 or sig.get("connection_count", 0) > 200:
                flag("unverified_but_high_social_proof", cid)

print(f"Total candidates scanned: {total}\n")
print("Anomaly counts:")
for name, count in anomaly_counts.most_common():
    print(f"  {name}: {count}")

multi_flagged = {cid: flags for cid, flags in per_candidate_flags.items() if len(flags) >= 2}
print(f"\nCandidates with 2+ anomalies: {len(multi_flagged)}")
triple_flagged = {cid: flags for cid, flags in per_candidate_flags.items() if len(flags) >= 3}
print(f"Candidates with 3+ anomalies: {len(triple_flagged)}")

print("\nSample of 3+ anomaly candidates:")
for cid, flags in list(triple_flagged.items())[:10]:
    print(f"  {cid}: {flags}")
