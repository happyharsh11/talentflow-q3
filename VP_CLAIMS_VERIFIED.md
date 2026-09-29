# VP Email Claims — Verified / Challenged / Qualified

Source: `CANDIDATE_PACK_PM.md.docx` (assignment document)
Data: `data/raw/*.json` (downloaded from Airtable base `appYePRAI75PMbQNQ`)
Verification script: `scripts/test_vp_claims.py`

---

## CLAIM 1: "Job boards are our biggest channel by a wide margin and they bring in 26.9% of our hires."

### Reproduced from data
- **Candidate sources** (`Candidates` table, `Source` field, n=300):
  - Job Board: **191 (63.7%)** — clearly the largest source of candidates
  - Agency: 35 (11.7%)
  - LinkedIn: 31 (10.3%)
  - Career Site: 31 (10.3%)
  - Referral: 8 (2.7%)
  - Campus: 4 (1.3%)
- **Definite hires** (offers with `Status="Accepted"`, linked back through Application → Candidate): **26 hires total**
  - Job Board hires: **7 / 26 = 26.9%**
  - Referral hires: 7 / 26 = 26.9% (equal share, not "by a wide margin")
  - Career Site: 5 (19.2%)
  - Agency: 4 (15.4%)
  - LinkedIn: 3 (11.5%)

### Challenge / Qualification
- **The number 26.9% is reproducible — but only for hires (accepted offers), not for candidates.**
- The VP says "biggest channel by a wide margin." For hires, Job Board (26.9%) is **tied with Referral (26.9%)** — there is **no wide margin** at the hire level.
- For candidates, Job Board (63.7%) IS a wide margin — but the claim specifies "hires," not candidates.
- **Conclusion: The 26.9% figure is numerically accurate for hires, but the "wide margin" description fails because Referral equals it. The VP likely confused the candidate-share figure (63.7%) with the hire-share figure. Qualify — do not accept unchallenged.**

---

## CLAIM 2: "Our offer acceptance rate is sitting at around 72% and the board is asking about it."

### Reproduced from data
- `Offers` table: **36 records**
  - `Status = "Accepted"`: 26 (72.2%)
  - `Status = "Pending"`: 5 (13.9%)
  - `Status = "Declined"`: 5 (13.9%)
- **Definite outcomes only** (`Accepted` vs `Declined`, excluding `Pending`):
  - 26 / (26 + 5) = **26/31 = 83.9%**
- **If "Pending" is excluded but "Declined" counted as rejected (the only negative outcome present):** 83.9%, not 72%.
- **If "Pending" is treated as non-accepted (i.e., denominator = all offers):** 26/36 = 72.2% — but this treats 5 pending offers as implicit rejections, which is an assumption, not data.

### Problems / Qualifiers
1. **No `Rejected` status exists in the Offers table.** The only non-accepted, non-pending status is `Declined` (5 records). There are **zero true "Rejected" offers**.
2. **5 offers are `Pending` (13.9%).** These have **no definite outcome**. Counting them in the denominator (as rejections) produces 72.2%; excluding them produces **83.9%**.
3. **No duplicate offers** (each application has at most 1 offer).
4. **0 broken references** — all 36 offers link to valid applications.
5. **No contradictory offers** — no application has both `Accepted` and `Declined` offers.

### Challenge / Qualification
- **The 72% figure requires including `Pending` as non-accepted (i.e., treating them as implicit rejections).** With only **definite outcomes** (`Accepted` vs `Declined`), the rate is **83.9%**.
- If the board asks for the rate based on resolved outcomes: **83.9%** is the defensible number.
- If the VP insists on 72%, the implicit assumption is that all 5 pending offers will decline — that is speculative.
- **Conclusion: Reject 72% as a definitive rate. Report 83.9% for resolved offers, and separately disclose 5 pending (13.9%) plus 5 declined (13.9%). Qualify — the number moves depending on how pending is handled.**

---

## Cross-Reference Integrity (verified)
- `Applications` (350) → `Candidate` links: 350 verified, 0 broken
- `Applications` → `Opening` links: 350 verified, 0 broken
- `Applications` → `Recruiter` (People): 350 verified, 0 broken
- `Interviews` (160) → `Application`: 160 verified, 0 broken
- `Interviews` → `Interviewer` (People): 160 verified, 0 broken
- `Offers` (36) → `Application`: 36 verified, 0 broken
- `Job Openings` (24) → `Recruiter` / `Hiring Manager` (People): 24 verified, 0 broken
- `Candidates` → `Applications` reverse: 350 verified, 0 broken

---

## Final Recommendation
1. **Job boards**: Acknowledge 63.7% candidate share and 26.9% hire share (tied with Referral). Challenge the "wide margin" claim at hire level. Qualify.
2. **Offer acceptance**: Report **83.9%** (resolved: 26 accepted / 31 resolved = 26 accepted / 5 declined + 26 accepted). Separately note **5 pending (13.9%)** as unresolved. Reject 72% unless the pending group is explicitly treated as non-accepted — which requires justification.
