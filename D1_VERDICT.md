# D1 — Verdict on VP's Two Claims (Decision 1)

Built from `data/raw/*.json` (8 Airtable tables, 892 records, base `appYePRAI75PMbQNQ`).
Method: `scripts/test_vp_claims.py` + manual cross-check of linked records.

---

## CLAIM 1 — Job-board integration ("biggest channel — 26.9% of hires")

**Verdict: BUILD A DIFFERENT SOLUTION.**

| Element | Value |
|---|---|
| **Claim text** | "Job boards are our biggest channel by a wide margin and they bring in 26.9% of our hires." |
| **Decision** | Build a different solution — do **not** build the VP's framing unchallenged. |
| **Deciding metric** | Job-Board share of **definite hires** (accepted offers → candidate source) |
| **Exact calculation** | `Job_Board_accepted_offers / total_accepted_offers` = `7 / 26` = **26.9%**. Cross-checked via `Candidate.Source` → `Application` (Candidate field) → `Offer` (Application field, Status=Accepted). |
| **Confidence** | **HIGH (verified)** for the 26.9% hire-share figure; **MEDIUM** for the "wide margin" interpretation, which fails at hire level. |

**Why not "build it":** The number is reproducible only for hires (26.9%), but at that level Job Board ties with Referral (7/26 each = 26.9%). The "wide margin" claim requires the **candidate** denominator (191/300 = 63.7%), which is a different metric than "hires." Building the VP's solution verbatim builds on a conflated denominator.

**Why not "do not build it":** Job boards ARE the dominant source of candidates (63.7%) and do contribute 26.9% of hires — a real channel. The integration has merit; the framing is wrong.

**Different solution:** Build job-board integration, but benchmark it against **both** metrics separately: (a) candidate-source share (63.7%, dominant) and (b) hire-source share (26.9%, tied with Referral). Report both to the board — don't present 26.9% as a margin over competitors.

---

## CLAIM 2 — Offer acceptance rate ("around 72%")

**Verdict: DO NOT BUILD IT (as stated). Build a qualified, different measurement.**

| Element | Value |
|---|---|
| **Claim text** | "Our offer acceptance rate is sitting at around 72% and the board is asking about it." |
| **Decision** | **Do not build** 72% as a definitive rate. Build a **separate resolved + pending** report instead. |
| **Deciding metric** | Acceptance rate computed from **definite outcomes only** (Accepted vs Declined, excluding Pending) |
| **Exact calculation** | `Accepted / (Accepted + Declined)` = `26 / (26 + 5)` = **83.9%**. If Pending (5) treated as implicit rejections: `26 / 36` = 72.2% — requires unverified assumption. |
| **Confidence** | **HIGH (verified)** that 83.9% is the defensible resolved rate; **LOW (assumption)** for 72% because it depends on treating 5 pending offers as declined. |

**Why not "build it":** 72% is only achievable by counting 5 `Pending` offers as non-accepted. There is **no `Rejected` status** in the Offers table — only `Accepted`, `Pending`, `Declined`. The 72% is not an observed rate; it's a modeled rate with an unverified assumption.

**Why not fully "do not build":** There is real data (26 accepted, 5 declined, 5 pending) and a board question. Ignoring the metric is worse than misreporting — the correct action is report it with the pending group separated.

**Different solution:** Report **83.9% resolved acceptance** (26/31) + separately disclose **13.9% pending (5)** and **13.9% declined (5)**. If the board demands a single figure, present both (83.9% resolved / 72.2% if all pending declined) with the assumption stated explicitly. Do not state 72% without the qualifier.

---

## Cross-Verification Notes (both claims)
- Link integrity: 8 relationship types, **0 broken references** (Applications→Candidate/Opening/Recruiter; Interviews→Application/Interviewer; Offers→Application; Job Openings→Recruiter/Hiring Manager; Candidates→Applications reverse).
- Duplicates: 4 duplicate `Application ID` business keys (APP-00005/07/10, 2 occurrences each); 0 duplicate Airtable `id` values.
- No contradictory offeers (no app has both Accepted + Declined).
- No broken offer-to-application references.
