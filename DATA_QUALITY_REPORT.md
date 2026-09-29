# Data Dictionary & Quality Report — TalentFlow Airtable

Generated: 2026-09-28
Script: `scripts/data_dictionary.py`
Data source: `data/raw/*.json` (downloaded from base `appYePRAI75PMbQNQ`)

## Record Counts
| Table | Records |
|-------|---------|
| Applications | 350 |
| Candidates | 300 |
| Job Openings | 24 |
| Interviews | 160 |
| Offers | 36 |
| People | 14 |
| Departments | 8 |
| Findings | 0 |
| **Total** | **892** |

## Field Inventory (per table — count and null rate)
- See `scripts/data_dictionary.py` output; all fields documented with type samples.
- Key linked fields: `Candidate`, `Opening`, `Recruiter` (Applications); `Application`, `Interviewer` (Interviews); `Application` (Offers); `Applications`, `Department`, `Recruiter`, `Hiring Manager` (Job Openings); `Applications` (Candidates).

## Cross-Table Join Verification (8 relationships)
All links verified — **0 broken references**:
1. Applications → Candidate (350/350 OK)
2. Applications → Opening (350/350 OK)
3. Applications → Recruiter / People (350/350 OK)
4. Interviews → Application (160/160 OK)
5. Interviews → Interviewer / People (160/160 OK)
6. Offers → Application (36/36 OK)
7. Job Openings → Recruiter / People (24/24 OK)
8. Job Openings → Hiring Manager / People (24/24 OK)
9. Candidates → Applications (reverse link, 350/350 OK)

## Data Quality Flags
- **Duplicates**: 4 duplicate `Application ID` values (`APP-00005`, `APP-00007`, `APP-00010` — 2 occurrences each). No duplicate Airtable `id` (record-level) values.
- **Null rates** (high): `Referred By` 92.3% (Applications); `Offered On` / `Offers` 89.7%; `Notes` 21% (Candidates); `Closing Date`-related fields ~30-85%.
- **Invalid values**: 4 Candidates with `Expected CTC < Current CTC`. Zero negative bonuses. Zero salary-band inversions. Zero interview scores outside 1-5.
- **Dates**: Ranges verified; no future anomalies (>2030) detected.

## Read-Only Access Confirmed
The script performs no writes. All data comes from the Airtable REST API (`GET /v0/{base_id}/{table}` with `Authorization: Bearer {token}` header) and paginates via the `offset` token.
