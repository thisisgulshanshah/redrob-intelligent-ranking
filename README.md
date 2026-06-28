# Redrob Intelligent Candidate Ranking — Purvanchal AI

Team: Purvanchal AI (Gulshan Kumar Shah, Prince Chaudhary)

## Setup
## Reproduce submission
Runtime: well under 5 min, CPU only, no network calls, 16GB RAM.

## Approach
Rule-based scorer combining experience-years fit, career-history evidence (retrieval/ranking keywords from actual job descriptions, not just skills list), product-vs-service company detection, skills relevance (proficiency + endorsement weighted), behavioral signals (recruiter response, notice period, recency), location, education tier. Hard honeypot filter excludes dataset-confirmed honeypots (3+ stacked impossible signal contradictions). Title-based guard caps non-AI roles even when summary text has AI buzzwords.

## Validate
