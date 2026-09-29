# D5 — Quarter Roadmap Memo (6 Engineer-Weeks)

Lead decision: Build **offer measurement (2w)** → **job-board integration with dual-metric reporting (2.5w)** → **application-stage tracking (1.5w)**. Do not build 72% as definitive; do not build findings module (0 records); do not build "clear hire leader" framing (Job Board = Referral at 26.9% hires).

---

## WHAT TO BUILD (3 initiatives, 6 weeks)

| # | Initiative | Weeks | Why (evidence) |
|---|---|---|---|
| P1 | Offer-acceptance measurement + reporting | 2 | 83.9% resolved rate (`26/31` Accepted/Declined); 5 `Pending` (13.9%) must be shown separately; board asking; 0 broken offer links (D4) |
| P2 | Job-board integration — dual metric (candidate + hire share) | 2.5 | Job Board = 63.7% of 300 candidates (191/300) AND 26.9% of 26 hires (tied with Referral at 7/26) — build integration, reject "wide margin" claim |
| P3 | Application-stage / screening workflow | 1.5 | 30% missing `Closed On` (105/350); 59.1% missing `First Interview` (207/350); 4 duplicate `Application ID` business keys (`APP-00005/07/10`) |

---

## VP CLAIM VERDICTS (D1 / D3)

- **Claim 1 (26.9% job-board hires):** REPRODUCED — `7/26` = 26.9% of accepted offers. QUALIFIED — ties Referral (`7/26`); 63.7% of candidates, not hires. **Verdict: build different framing (dual-metric).**
- **Claim 2 (~72% acceptance):** REJECTED as definitive. Definite outcomes (`Accepted` vs `Declined`): `26/31` = **83.9%**. 72.2% only if 5 `Pending` treated as rejected (assumption, not observation). **Verdict: build qualified rate (83.9% + pending shown separately; D3 spec).**

---

## MAIN METRIC (P1 / dashboard spec from D3)

- **Numerator:** offers `Status = "Accepted"`, `Offered On` present, `Application` link valid, `Offer ID` unique.
- **Denominator:** same cohort with `Status` in (`Accepted`, `Declined`). `Pending` excluded — never silent.
- **Rate:** 83.9% (26/31) on current cohort. Pending: 5 (13.9%). Declined: 5 (13.9%).
- **Cohort date:** `Offered On`. Window: configurable (default 365d).
- **Quality flags (verified):** 0 broken links (8 relationships); 0 duplicate `Offer ID`; 0 duplicate record `id`; 0 missing `Status`; 0 missing `Offered On`.

---

## MAJOR CAVEAT

- **Pending offers (5/36 = 13.9%) must stay out of denominator.** No `Rejected` status exists in Offers table — only `Accepted`, `Pending`, `Declined`. Claiming 72% requires an unverified assumption on 5 pending records. Report 83.9% + separate pending line.
- **Findings table = 0 records.** Defer findings / audit module (would consume 6w with no feed). Build only if data arrives.
- **4 duplicate `Application ID` business keys** (`APP-00005/07/10`, 2 occurrences each) — guard needed in P3 pipeline; does not break D1 hire-share (all duplicates = rejected stage).

---

## NEXT DATA CHECK (before P1 deploys)

1. Confirm `Offers.Status` has not acquired a new value (e.g., `Rejected`) since download.
2. Confirm 5 `Pending` offers have not changed to `Accepted` or `Declined`.
3. Confirm 0 new broken links added (re-run `scripts/test_vp_claims.py` join check).
4. Confirm P3 duplicate-guard detects any new `APP-XXXXX` duplicates before pipeline deploys.

---

## DETAILED CALCULATIONS
→ See `VP_CLAIMS_VERIFIED.md` (D1), `D2_ALLOCATION.md` (weeks + priority), `D3_METRIC_SPEC.md` (numerator/denominator/cohort), `D4_TRUST.md` (missingness/duplicates/broken/sequence/stale/conflict counts with exact fractions).
