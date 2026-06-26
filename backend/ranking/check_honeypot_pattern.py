import json
from collections import defaultdict, Counter
from datetime import datetime

path = "backend/data/raw/candidates.jsonl"
per_candidate_flags = defaultdict(list)

def flag(name, cid):
    per_candidate_flags[cid].append(name)

with open(path) as f:
    for line in f:
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

triple_plus = {cid: tuple(sorted(flags)) for cid, flags in per_candidate_flags.items() if len(flags) >= 3}
pattern_counts = Counter(triple_plus.values())

print(f"Total 3+ anomaly candidates: {len(triple_plus)}")
print("\nDistinct patterns among them:")
for pattern, count in pattern_counts.most_common():
    print(f"  {count}x : {pattern}")

with open("backend/data/raw/honeypot_candidates.txt", "w") as out:
    for cid in sorted(triple_plus.keys()):
        out.write(cid + "\n")
print(f"\nSaved {len(triple_plus)} honeypot candidate IDs to backend/data/raw/honeypot_candidates.txt")
