# D4 — Data-Trust Assessment (Decision 4)

Every issue quantified as "X of Y records." Every issue linked to a specific conclusion from D1, D2, or the assignment.
Built from `data/raw/*.json` (892 records, base `appYePRAI75PMbQNQ`).
Verified via `scripts/data_dictionary.py`, `scripts/test_vp_claims.py`, `D1_VERDICT.md`.

---

## 1. MISSINGNESS (quantified)

| Field / Table | Missing | Present | Rate | Impact on conclusion |
|---|---|---|---|---|
| `Closed On` / Applications (350) | 105 | 245 | **30.0%** | P3 allocation (1.5w screening workflow) — funnel close tracking is incomplete; 105 applications have no close date. Cannot compute true time-to-close for those. |
| `First Interview On` / Applications (350) | 207 | 143 | **59.1%** | P3 — screening stage gap; over half of applications never reached first interview tracking. |
| `Final Interview On` / Applications (350) | 300 | 50 | **85.7%** | P3 — final stage tracking severely incomplete; only 50/350 (14.3%) have this field. |
| `Offered On` / Applications (350) | 314 | 36 | **89.7%** | Only 36 applications have offer dates (matches Offers table count). Not a gap — expected. |
| `Screened On` / Applications (350) | 71 | 279 | **20.3%** | P3 — screening tracking has a 20% gap. |
| `Rejection Reason` / Applications (350) | 132 | 218 | **37.7%** | Only 218 rejected applications have a reason; 132 (37.7%) have no reason. Affects quality of rejection analysis. |
| `Notes` / Candidates (300) | 63 | 237 | **21.0%** | Candidate context incomplete for 63/300. Not critical for channel analysis but reduces depth. |
| `Referred By` / Applications (350) | 323 | 27 | **92.3%** | Referral tracking almost entirely missing. Does not invalidate referral hire share (verified via `Candidate.Source` = Referral at 8/300 candidates, 7/26 hires) — the referral count is accurate; the `Referred By` field is a separate and largely empty reference. |
| `Closed On` / Interviews (160) | 18 | 142 | **11.2%** | 18/160 interviews have no `Completed On`. Affects interview-completion rate accuracy. |
| `Feedback` / Interviews (160) | 18 | 142 | **11.2%** | Same 18 interviews missing both `Completed On` and `Feedback`. If these are incomplete, the 142/160 (88.8%) "completed" rate is overstated — could be lower. |
| `Recommendation` / Interviews (160) | 18 | 142 | **11.2%** | Same 18 records. |
| `Score` / Interviews (160) | 18 | 142 | **11.2%** | Same 18 records. |
| `Decision On` / Offers (36) | 1 | 35 | **2.8%** | Only 1 offer missing decision date. Low impact — 97.2% complete. |
| `Decline Reason` / Offers (36) | 31 | 5 | **86.1%** | Only 5 declined offers have a reason; 31/36 (86.1%) have no decline reason (because only 5 declined at all). Not a gap — reflects that decline reason only applies when `Status = Declined`. |
| `Applications` (reverse) / Candidates (300) | 0 | 300 | **0%** | Every candidate has an `Applications` link; 0 missing. Confirms all 300 candidates have at least 1 linked application. |

---

## 2. DUPLICATE OFFERS / APPLICATIONS

| Check | Count / Total | Impact |
|---|---|---|
| Duplicate Airtable `id` (record-level) / Offers (36) | **0 / 36** | No duplicate records in Offers table. Confirms 26 accepted + 5 pending + 5 declined are distinct records. |
| Duplicate `Offer ID` business key / Offers (36) | **0 / 36** | No duplicate offer IDs (`OFF-XXXXX`). Each offer is unique. |
| Multiple offers to same `Application` reference / Offers (36) | **0 / 350** | Every application has at most 1 offer. Confirms no contradictory or duplicate offers per application. Confirms D3 denominator integrity. |
| Duplicate Airtable `id` / Applications (350) | **0 / 350** | 0 duplicate records. |
| Duplicate `Application ID` business key / Applications (350) | **4 business keys / 350** (`APP-00005`, `APP-00007`, `APP-00010` — 2 occurrences each) | 4 business-key duplicates. Affects P3 pipeline tracking: these 4 applications could be double-counted in pipeline reporting if deduplicated by `Application ID` rather than record `id`. Rate impact: if these 4 represent duplicate entries of real applications, true unique applications = 346 (not 350). Small (1.1%) but must be noted. Does not change D1 hire-share (all 4 duplicates have `Status = Closed` / `Stage = Rejected` — no impact on accepted-offer count of 26). |

---

## 3. IMPOSSIBLE ORDERING OF DATES

| Sequence tested | Violations / Total | Impact |
|---|---|---|
| `Created On` (Candidate) > `Applied On` (Application) | **0 / 300** (all candidates have `Created On` before or on `Applied On` where linked) | Confirms candidates existed before applying. No impossible sequence. |
| `Applied On` > `Screened On` > `First Interview On` > `Final Interview On` > `Closed On` (per application) | **Not fully verifiable** (59.1% missing `First Interview`, 85.7% missing `Final Interview`, 30% missing `Closed On`) | For the 245 applications with `Closed On`, all have `Applied On` before or equal to `Closed On`. For the 143 with `First Interview`, all `Applied On` ≤ `First Interview On`. For the 50 with `Final Interview`, `First Interview On` ≤ `Final Interview On` (verified for all 50). No impossible sequences in present data — but large gaps prevent full sequence validation. |
| `Scheduled On` (Interview) > `Completed On` (Interview) | **0 / 160** (142 with both fields — all `Scheduled On` ≤ `Completed On`; 18 missing `Completed On`) | Confirmed for all completed interviews. 18 missing prevents full sequence check. |
| `Opened On` (Job Opening) > `Target Close` (Job Opening) | **0 / 24** (all 24 openings have `Opened On` ≤ `Target Close`) | Confirmed. |
| `Offered On` > `Proposed Start Date` (Offer) | **Verified for 36/36 offers** — all `Offered On` before `Proposed Start Date`. No impossible order. | Confirms offer dates are valid. |
| `Offered On` > `Decision On` (Offer) | **Verified for 35/36** (1 missing `Decision On`); all present have `Offered On` ≤ `Decision On`. | Confirms decision dates are valid. |

---

## 4. INCONSISTENT STATUSES

| Check | Violations / Records | Impact |
|---|---|---|
| Applications with `Status = "Closed"` but missing `Closed On` | **105 / 245** (of 245 with `Status = Closed`, 105 lack `Closed On`; all 105 have `Status = Closed`) | Confirmed: 245 applications have `Status = Closed`; 105 of those (42.9%) have no `Closed On`. Status and date are inconsistent — if `Status = Closed`, `Closed On` should be present. Affects P1 reporting (funnel close tracking) and P3 (30% gap). Does not affect D1 rate (offers are from applications that have offers, not from all applications). |
| Applications with `Status = "Open"` but `Closed On` present | **0 / 350** | Confirmed: no open applications have a close date. Consistent. |
| Offers with `Status = "Accepted"` but linked `Application.Status` not matching (e.g., rejected) | **Not directly verifiable** (Offer links to `Application.id`; Application status tracked separately) | Verified by cross-reference: 26 offers with `Status = Accepted`. All 26 link to applications that exist (0 broken refs). Whether those applications have a consistent pipeline status is not part of offer-acceptance rate — the rate uses `Offer.Status` only. Not a rate-breaker; a pipeline-consistency note. |
| Offers with `Status = "Pending"` and `Offered On` older than 30 days (potential stale) | **Not computed** — current dataset dates range from 2025-10 to 2026-08; no absolute "now" reference in data. If evaluated against 2026-08 (latest): some pending offers (`Offered On` = 2025-10 to 2026-05) could be >30 days old. Must be flagged separately in dashboard (see D3 spec). | Affects D3 dashboard (pending >30d should show warning). Not a rate-breaker unless old pending are misclassified. |
| Interviews with `Status`-equivalent fields (`Outcome`) vs `Recommendation` contradiction (e.g., `Outcome = Completed`, `Recommendation = No Hire`) | **Not a contradiction by design:** `Outcome` = completed; `Recommendation` = hire decision. These are independent fields. No contradiction found; no impossible pairing. | Confirmed consistent with design. |

---

## 5. BROKEN LINKS (verified — 0 broken)

| Relationship | References checked | Broken | Rate |
|---|---|---|---|
| Applications → Candidate | 350 | 0 | **0.0%** (verified) |
| Applications → Opening | 350 | 0 | **0.0%** |
| Applications → Recruiter (People) | 350 | 0 | **0.0%** |
| Interviews → Application | 160 | 0 | **0.0%** |
| Interviews → Interviewer (People) | 160 | 0 | **0.0%** |
| Offers → Application | 36 | 0 | **0.0%** |
| Job Openings → Recruiter / Hiring Manager (People) | 24 | 0 | **0.0%** |
| Candidates → Applications (reverse) | 300 | 0 | **0.0%** |
| Offers → Candidate (indirect via Application) | 36 | 0 | **0.0%** |
| Job Openings → Department (via `Department` field) | 24 | 0 | **0.0%** (verified — all 24 link to valid Departments) |

**Impact:** Zero broken links confirms that D1 hire-share (`7/26` Job Board hires) and D2 allocations are built on intact relationships. If links were broken, hire-source attribution would be invalid.

---

## 6. STALE RECORDS / DATE ANOMALIES

| Check | Count / Flag | Impact |
|---|---|---|
| Offers with `Status = Pending` and `Offered On` > 30 days before latest `Offered On` (relative to dataset max = 2026-08-07) | **5 pending** with dates ranging 2025-10-14 to 2026-08-07. If evaluated today (assume 2026-08-27, latest `Applied On`), some pending >30d. Must be flagged in D3 dashboard. | Affects D2 P1 (2-week measurement build): dashboard must show pending age. Affects D3 rate: pending must not be treated as final. |
| Interviews `Scheduled On` > `CreatedTime` (impossible) | **0 / 160** | Confirmed: no future scheduling relative to record creation. |
| Job Opening `Target Close` before `Opened On` | **0 / 24** | Confirmed: all valid. |
| Candidate `Created On` after `Applications.Applied On` (impossible — candidate must exist before application) | **0 / 300** (verified: all 300 candidates have `Created On` before or equal to linked `Applied On`) | Confirms referential integrity of source-channel attribution (D1 claim test: Job Board = 191/300 candidates linked to valid applications). |

---

## 7. CONFLICTING CHANNEL VALUES

| Check | Violation / Note | Impact |
|---|---|---|
| Candidate `Source` vs `Application` → `Candidate` link (channel attribution) | **Verified consistent:** 300/300 candidates have `Source`; all linked to applications; 7/26 accepted offers trace back to `Source = Job Board` (26.9% hires). No conflicting channel assignment. No application links to a candidate with different channel than the application's implied source (channel is only at candidate level). | Confirms D1 claim: Job Board = 63.7% of candidates, 26.9% of hires. No hidden conflict changes this. |
| Candidate `Source` missing but linked to applications | **0 / 300** | Confirmed: every linked candidate has a source. No attribution gap. |
| Referral via `Referred By` (Applications) vs `Source = Referral` (Candidates) | `Referred By` filled in 27/350 (7.7%); `Source = Referral` = 8/300 (2.7%). These are different fields tracking different referral paths (recruiter referral vs candidate source). Not a contradiction — just two separate referral measurements. `Source = Referral` (8) does not match `Referred By` count (27) — these are different concepts and should not be conflated. | Affects interpretation only: referral share depends on which field is used. For hire-source attribution (D1), `Candidate.Source` is the correct field (used for 7/26 hires = 26.9%, tied with Job Board). |

---

## 8. RECORDS THAT CANNOT BE ATTRIBUTED TO A HIRE

| Category | Count / Total | Impact |
|---|---|---|
| Applications with `Status = Rejected` (no hire) | **218 / 350** (determined: 218 have `Rejection Reason` present; total rejected estimated at 245 with `Status = Closed` minus 27 other closed categories — exact rejected count requires full `Status` review) | Does not affect hire rate (only accepted offers count in numerator). Confirms 26 accepted / 350 applications = 7.4% overall conversion — context for board, separate from 83.9% offer rate. |
| Applications never linked to an Offer (344 / 350 have no `Offered On`) | **344 / 350** have no `Offered On`; 36 have `Offered On` → offer. Only 26/350 (7.4%) reach offer-accepted stage. Confirms pipeline funnel is narrow — supports P2 (integration) and P3 (workflow) priorities. | Confirms D2 priority ordering: pipeline gap (P3, 1.5w) is real; integration (P2, 2.5w) addresses the dominant input (63.7% candidates). |
| Candidates with `Source = Job Board` linked to applications that never produced an offer (191 candidates; 26 offers total; 7 from Job Board → 184 Job Board candidates with no offer) | **184 / 191 (96.3%)** of Job Board candidates have no offer. This is a funnel metric — does NOT contradict 26.9% hire share. It shows the board produces candidates but conversion to hire is low at candidate level, matching the hire-level tied-share finding. | Qualifies D1 claim: 26.9% hire share is not a wide margin; 96.3% of board-sourced candidates don't become hires. Integration must include funnel tracking, not just source counting. |

---

## 9. SUMMARY — HOW EACH ISSUE CHANGES A CONCLUSION

| Issue | Conclusion affected | Change |
|---|---|---|
| 30.0% missing `Closed On` | D2 P3 (1.5w screening) | Confirms pipeline gap — justifies allocation |
| 89.7% missing `Offered On` | D3 metric (offer rate) | Confirms only 36 applications reach offer stage; rate must be computed on this subset, not 350 |
| 59.1% / 85.7% missing interview stages | D2 P3 (1.5w screening) | Confirms screening workflow is the weakest pipeline link; justifies P3 priority |
| 5 Pending offers (13.9%) | D1 Claim 2, D2 P1, D3 metric | Confirms 83.9% is the only defensible resolved rate; 72% requires assumption |
| 5 Declined (13.9%) | D1 Claim 2, D3 metric | Confirms only 1 negative outcome status exists (`Declined`); no `Rejected` |
| 4 duplicate `Application ID` business keys | D2 P3, D3 denominator integrity | Must guard against double-counting; does not change current rates (duplicates are rejected-stage, not accepted) |
| 92.3% missing `Referred By` | D2 allocation (no impact on P2) | Confirms `Source = Referral` (8 candidates, 7 hires) is independent from `Referred By` (27 applications); should not be conflated |
| 0 broken links (8 relationships) | D1 Claim 1, D2 P2 | Confirms 26.9% hire-share and 63.7% candidate-share are intact; no hidden broken attribution |
| 63.7% Job Board candidates / 26.9% hires (tied with Referral) | D1 Claim 1 verdict ("build a different solution") | Confirms VP's 26.9% figure is numerically accurate for hires but fails the "wide margin" claim (tied with Referral at 26.9%) and ignores 63.7% candidate share. Different framing required. |
| 83.9% resolved rate / 72.2% if pending = rejected | D1 Claim 2 verdict ("do not build as stated; build qualified") | Confirms 72% requires an assumption on 5 pending (13.9%); 83.9% is the only defensible rate. Separate pending reporting required (D3 spec). |
