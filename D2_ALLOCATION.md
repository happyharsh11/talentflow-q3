# D2 — 6 Engineer-Week Allocation (Decision 2)

Context: 6 engineer-weeks = 6 weeks of 1 engineer, or 3 engineers × 2 weeks, etc. Allocation picks 3 initiatives in priority order with evidence from `data/raw/*.json` and `VP_CLAIMS_VERIFIED.md`.

---

## PRIORITY ORDER & ALLOCATION

| Priority | Initiative | Weeks | Evidence |
|---|---|---|---|
| **P1** | Offer-acceptance measurement & reporting | **2** | Definite-rate 83.9% vs claimed 72%; 5 Pending (13.9%) unreported; board actively asking. High-stakes, quick win. |
| **P2** | Job-board integration (qualified — dual-metric) | **2.5** | 63.7% of candidates (191/300) from Job Board vs 26.9% of hires; tied with Referral at hire level. Real channel, wrong framing. Build integration but report both metrics. |
| **P3** | Application-stage / screening workflow | **1.5** | 350 applications; 30% missing `Closed On`; 59% missing `First Interview On`; 85.7% missing `Final Interview On`. Funnel gaps = productivity loss. |
| **—** | **Total** | **6** | — |

---

## P1 — Offer-Acceptance Measurement & Reporting (2 weeks)

**What:** Build the resolved + pending reporting pipeline for offers; expose 83.9% (resolved) vs 72.2% (if pending treated as declined); separate `Pending` (5), `Declined` (5), `Accepted` (26).

**Evidence (from `Offers.json`, n=36):**
- Status distribution: Accepted=26, Pending=5, Declined=5. **Zero `Rejected`** status exists.
- 5/36 (13.9%) have no definite outcome — these cannot be counted as either accepted or rejected.
- All 36 offers link correctly to applications; 0 broken references; 0 duplicates; 0 contradictions.
- The VP's 72% only works if pending = rejected (assumption). Building this removes the assumption from board reporting.

**Risk if skipped:** Board continues on unverified 72% figure; no visibility into 13.9% pending; future offer decisions made on incomplete data.

**Why 2 weeks:** Reporting pipeline + dashboard widget + validation rules (flag missing Status, flag offers >30 days Pending, flag duplicate offers — none currently exist but pipeline should detect them).

---

## P2 — Job-Board Integration (2.5 weeks)

**What:** Integrate job-board feed; report source metrics separately — candidate-share (63.7%) and hire-share (26.9%, tied with Referral at 7/26).

**Evidence (from `Candidates.json` + `Applications.json` + `Offers.json`):**
- Job Board = 191/300 candidates (63.7%) — dominant.
- Job Board = 7/26 accepted-offer hires (26.9%) — tied with Referral (7/26).
- No "wide margin" at hire level; integration must not claim one.
- 24 job openings span 8 departments; 350 applications show board-sourced candidates enter at ~1.27 applications per opening on average — meaningful pipeline.

**Risk if skipped:** Largest candidate channel unmonitored; board's 26.9% figure has no operational backing; can't distinguish board quality from referral quality at hire level.

**Why 2.5 weeks:** API integration + dual-metric reporting (candidate vs hire) + quality tracking (offer-accept rate by source). Extra 0.5 week accounts for dual-metric design (not single denominator).

---

## P3 — Application / Screening Workflow (1.5 weeks)

**What:** Close funnel gaps: 30% missing `Closed On`; 59% missing `First Interview On`; 85.7% missing `Final Interview On`; 20.3% missing `Screened On`.

**Evidence (from `Applications.json`, n=350):**
- `Applied On` = 100% filled; `Status` = 100%; `Stage` = 100%; `Candidate` = 100%; `Opening` = 100%.
- Pipeline stages drop sharply: `Screened On` 79.7% → `First Interview` 40.9% → `Final Interview` 14.3% → `Closed On` 70%.
- This is not data-loss — it's a process gap. Candidates reach applications but stages aren't recorded.
- 4 duplicate `Application ID` business keys (APP-00005/07/10) — pipeline needs idempotency.

**Risk if skipped:** No visibility into screening velocity; stage-level conversion impossible; duplicate application IDs could cause double-counting in any pipeline metric.

**Why 1.5 weeks:** Workflow automation (stage tracking, close-date enforcement) + duplicate-ID guard + basic funnel reporting. Smaller than others because data already exists — just needs capture discipline.

---

## THREE THINGS NOT TO BUILD (with evidence / risk)

### NOT TO BUILD — "Universal 72% offer-acceptance banner" (P1-adjacent, rejected)
- **Evidence:** 72% requires assuming 5 `Pending` = declined (no `Rejected` status exists). Definite rate = 83.9%.
- **Risk:** Reporting 72% without qualifier repeats VP's unverified assumption; board makes decisions on speculative denominator.
- **Alternative:** Build qualified report (83.9% / 72.2% with assumption stated).

### NOT TO BUILD — "Job-board is the clear hire leader" (P2-adjacent, rejected framing)
- **Evidence:** Job Board = 26.9% of hires — tied with Referral (7/26 each). "Wide margin" only holds at candidate level (63.7%).
- **Risk:** Building this claim into product messaging overstates board's hire contribution; referral channel under-credited (equally strong at hire level).
- **Alternative:** Build dual-metric reporting (candidate 63.7% / hire 26.9%).

### NOT TO BUILD — "Full findings / audit module" (P3-adjacent, deferred)
- **Evidence:** `Findings` table = 0 records. `Findings` is listed in assignment but empty in data.
- **Risk:** Building audit module without findings data = empty feature; 6 weeks consumed with no incoming feed; opportunity cost = skip actual pipeline gaps (P3).
- **Alternative:** Defer findings module until data exists; allocate 1.5 weeks to pipeline gaps instead.

---

## Summary Table

| # | Initiative | Weeks | Verdict Type | Key Evidence |
|---|---|---|---|---|
| 1 | Offer measurement | 2 | Build (qualified) | 83.9% vs 72%; 5 Pending unreported; 0 broken refs |
| 2 | Job-board integration | 2.5 | Build (different framing) | 63.7% candidates, 26.9% hires (tied); 191/300 candidates |
| 3 | Screening workflow | 1.5 | Build | 30-86% stage gaps; 4 duplicate app IDs |
| — | 72% banner | — | Don't build | Assumes Pending = declined; no `Rejected` status |
| — | "Clear hire leader" | — | Don't build framing | Tied with Referral at 26.9% |
| — | Findings module | — | Don't build now | 0 records; empty feed |

**Total: 6 weeks, 3 initiatives, 3 rejections with evidence-backed alternatives.**
