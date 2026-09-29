# D3 — Offer-Acceptance Metric Spec

Based on D1 (definite outcomes = 83.9%, 5 pending) and D2 (P1 = 2-week measurement build).

---

## DEFINITION (numerator / denominator / cohort)

| Element | Definition |
|---|---|
| **Numerator** | Offers with `Status = "Accepted"` and all validity checks passed (see below). |
| **Denominator** | Offers with a **final decision** (`Status = "Accepted"` OR `Status = "Declined"`). **Pending excluded.** |
| **Cohort date** | `Offered On` (date offer was made). Window: offers where `Offered On` falls within the selected reporting period (default rolling 12 months or fixed quarter). |
| **Time window** | Configurable (default: last 365 days from query date; also supports quarterly / half / custom). Cohort bounded by `Offered On`, not by `CreatedTime`. |

---

## COHORT & FILTER RULES

### Cohort date (source of truth: `Offered On`)
- Pull from `Offers` fields: `Offered On` (string YYYY-MM-DD).
- Window: `Offered On >= window_start` AND `Offered On <= window_end`.
- If `Offered On` missing on an offer record: **exclude from all rate calculations** (do not count in numerator, denominator, or unknown); include in separate "missing-date" quality bucket.
- If `Offered On` present but `Status` missing: **exclude from rate**; include in "missing-status" bucket.

### Deduplication rules (before computing rate)
- **Record-level:** `id` is Airtable record ID (already unique per download — verified 0 duplicates in `Offers.json`).
- **Business-key:** `Offer ID` (e.g., `OFF-00021`). If duplicate `Offer ID` found with different `id`: flag duplicate; include only first in rate; exclude rest from rate but include in quality bucket.
- **Candidate-level:** one candidate can have multiple applications, but at offer stage each application should have at most 1 offer (verified: 0 apps with >1 offer). If >1 offer to same `Application` reference: flag; include first `Accepted` if exists; exclude others from rate (duplicate-offer bucket).
- **Multiple offers to same candidate different applications:** allowed; treat each offer independently (numerator / denominator count independently per offer record).

---

## RESCINDED / EXPIRED / WITHDRAWN / PENDING

| Condition | Treatment in rate | Treatment in dashboard |
|---|---|---|
| **Accepted** | Count in numerator + denominator | Confirmed accepted |
| **Declined** (only negative status present) | Count in denominator only (not numerator) | Confirmed declined |
| **Pending** (5 records, 13.9%) | **Excluded from denominator** (not final decision) | Shown as **"Pending / Unknown"** count and % of cohort |
| **Rescinded / Withdrawn / Expired** (not present in data, but spec must handle) | If status = withdrawn/expired: treat as **final negative** (denominator only, like Declined) — because decision is final, not pending. If unknown whether rescinded: treat as unknown. | Listed separately or under "Unknown / Non-final" |
| **Missing Status** (0 in current data, guard needed) | **Excluded from rate** | Shown in "Data quality / Missing status" with count |
| **Missing `Offered On`** | **Excluded from rate** | Shown in quality bucket |

---

## MULTIPLE OFFERS TO ONE CANDIDATE

- If same `Candidate` (via `Application` → `Candidate`) has 2 offers:
  - Both count independently in numerator / denominator (each is a separate offer decision).
  - If one `Accepted`, one `Declined`: rate reflects both outcomes (2 in denominator, 1 in numerator = 50% for that candidate's offer pair).
  - Dashboard should optionally show **offer-level** (default) and **candidate-level** (alternate) rate.

---

## DASHBOARD DISPLAY WHEN DATA IS INCOMPLETE

Never silently treat unknown / pending / missing as rejected. Dashboard shows all three panels:

```
Rate (resolvec):  83.9%  =  26 Accepted  /  31 Final (26 + 5 Declined)
                  [confidence: HIGH — all 31 have Status + Offered On]

Pending / Unknown: 5  (13.9% of 36 total in cohort)
                  [Status = Pending; Offered On present; decision not final]

Data Quality Flags (current cohort):
  • Missing Status: 0
  • Missing Offered On: 0
  • Duplicate Offer IDs: 0
  • Multiple offers per app: 0
  • Broken Application links: 0
  • Pending older than 30d: count shown (if any exceed threshold)
```

If larger cohort (e.g., 12 months) has more missing / pending:
- Rate is computed on **resolvable subset only**.
- A separate line reads: `Rate = X% (based on N of M offers with final status; M-N = unknown / pending / missing)`.
- Never compute `26 / 36 = 72%` without a visible "5 pending not included" note.

---

## EXACT CALCULATION METHOD (machine-readable)

```python
def offer_acceptance_rate(offers_in_window):
    # 1. Filter by Offered On in window
    cohort = [o for o in offers_in_window if o.get("Offered_On")]
    
    # 2. Deduplicate by Offer ID (first wins; rest to quality bucket)
    seen_ids = {}
    for o in cohort:
        offer_id = o.get("Offer_ID")
        if offer_id in seen_ids:
            quality["duplicate_offer_id"] += 1
            continue
        seen_ids[offer_id] = o
    
    # 3. Deduplicate by Application reference (max 1 per app; flag >1)
    # (Verified 0 cases in current data — guard needed)
    
    # 4. Final-decision filter
    final = [o for o in seen_ids.values()
             if o.get("Status") in ("Accepted", "Declined")]
    
    # 5. Count
    num = sum(1 for o in final if o.get("Status") == "Accepted")
    den = len(final)
    
    # 6. Unknown / pending separate
    pending = [o for o in cohort
               if o.get("Status") == "Pending" and o.get("Offered_On")]
    missing_status = [o for o in cohort if o.get("Status") is None]
    
    rate = num / den if den > 0 else None
    
    return {
        "rate": rate,
        "numerator": num,
        "denominator": den,
        "pending": len(pending),
        "missing_status": len(missing_status),
        "quality_flags": {...},
        "assumption_note": "Pending excluded from denominator (not a final decision)."
    }
```

---

## DATA QUALITY GUARDRAILS (current cohort verified)
- `Offered On`: 36/36 present
- `Status`: 36/36 present (Accepted/Declined/Pending — 0 missing)
- `Application`: 36/36 link to valid `Applications.id`
- `Offer ID`: 36 unique business keys (0 duplicates)
- `id`: 36 unique record IDs (0 duplicates)
- `Status = Declined`: 5 — only negative outcome present; no `Rejected` status exists
- `Status = Pending`: 5 — must stay out of rate denominator

---

## CONFIDENCE STATEMENT FOR DASHBOARD
- **Verified:** 83.9% on 31 final-decision offers (26 accepted / 5 declined).
- **Assumption:** 5 pending not counted as declined; 72.2% only if that assumption is adopted and stated.
- **Incomplete:** 0 offers missing date/status/reference; 5 pending = 13.9% of cohort must be shown separately.
