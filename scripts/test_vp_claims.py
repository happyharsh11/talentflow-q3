#!/usr/bin/env python3
"""
Test VP's two claims with actual data, not the email.
Claim 1: Job boards = 26.9% of hires (source/channel)
Claim 2: Offer acceptance = ~72% (definite outcomes only)
"""
import json
from pathlib import Path
from collections import Counter

def load(table):
    with open(Path("data/raw")/f"{table}.json", encoding="utf-8") as f:
        return json.load(f)

apps = load("Applications")
cands = load("Candidates")
offers = load("Offers")
interviews = load("Interviews")
job_openings = load("Job Openings")

print("="*70)
print("CLAIM 1 TEST: 'Job boards are our biggest channel — 26.9% of hires'")
print("="*70)

# Candidate source distribution (available field "Source")
cand_sources = Counter(r["fields"].get("Source") for r in cands if r.get("fields",{}).get("Source"))
print("\n--- Candidate source counts (n=300) ---")
for s,n in cand_sources.most_common():
    print(f"  {s}: {n} ({n/300*100:.1f}%)")

# Job Board % of candidates = 191/300 = 63.7% — much bigger than 26.9%, but these aren't hires
job_board_cands = cand_sources.get("Job Board", 0)
print(f"\nJob Board candidates: {job_board_cands}/300 = {job_board_cands/300*100:.1f}%")

# Hires must be defined: applications that produced an Accepted Offer, OR applications that are Closed/Accepted
# Offers with Status="Accepted" = definite hires (offer accepted)
acc_offers = [o for o in offers if o.get("fields",{}).get("Status") == "Accepted"]
print(f"\n--- Definite hires via Accepted Offers (n={len(acc_offers)}) ---")
# Link accepted offers back to applications, then to candidates, then to source
acc_app_ids = set()
for o in acc_offers:
    app_refs = o.get("fields",{}).get("Application", [])
    for ref in app_refs:
        acc_app_ids.add(ref)
print(f"Applications with Accepted Offer: {len(acc_app_ids)}")

# Map those application record IDs to candidates
app_to_cand = {}
for a in apps:
    cand_refs = a.get("fields",{}).get("Candidate", [])
    if cand_refs:
        app_to_cand[a["id"]] = cand_refs[0]

# Find candidate sources for accepted-offer apps
accepted_sources = Counter()
for app_id in acc_app_ids:
    cand_ref = app_to_cand.get(app_id)
    if cand_ref:
        for c in cands:
            if c["id"] == cand_ref:
                src = c.get("fields",{}).get("Source")
                if src:
                    accepted_sources[src] += 1
                break

print("\n--- Source breakdown of accepted-offer hires ---")
total_acc = sum(accepted_sources.values())
for s,n in accepted_sources.most_common():
    print(f"  {s}: {n} ({n/total_acc*100:.1f}% of {total_acc})")

if total_acc > 0:
    jb_share_acc = accepted_sources.get("Job Board", 0)/total_acc*100
    print(f"\n*** Job Board share of DEFITE hires (accepted offers) = {jb_share_acc:.1f}% (not 26.9%) ***")
    # If claim was candidates, not hires
    print(f"*** Job Board share of CANDIDATES = {job_board_cands/300*100:.1f}% (not 26.9%) ***")

# Check if any source is 26.9% of anything
print("\n--- Does 26.9% match any category? ---")
for s,n in cand_sources.most_common():
    pct = n/300*100
    if abs(pct - 26.9) < 1.0:
        print(f"  CLOSE: {s} = {pct:.1f}%")

print("\n" + "="*70)
print("CLAIM 2 TEST: 'Offer acceptance rate ~72%'")
print("="*70)

# Offers: statuses
offer_statuses = Counter(o.get("fields",{}).get("Status") for o in offers)
print(f"\n--- Offer status counts (n={len(offers)}) ---")
for s,n in offer_statuses.most_common():
    print(f"  {s}: {n} ({n/len(offers)*100:.1f}%)")

accepted = offer_statuses.get("Accepted", 0)
rejected = offer_statuses.get("Rejected", 0)
pending = offer_statuses.get("Pending", 0)

# Definite outcomes only = Accepted + Rejected (not Pending, not missing)
# Also check for withdrawn/declined — look for "Withdrawn" or "Declined" etc.
other = sum(v for k,v in offer_statuses.items() if k not in ("Accepted","Rejected","Pending"))
print(f"\nDefinite outcomes: Accepted={accepted}, Rejected={rejected}")
print(f"Pending={pending}, Other={other}")

definite_total = accepted + rejected
if definite_total > 0:
    rate = accepted / definite_total * 100
    print(f"\n*** Acceptance rate from DEFINITE outcomes only = {accepted}/{definite_total} = {rate:.1f}% ***")
    # Note if close to 72%
    print(f"*** Distance from claimed 72%: {abs(rate - 72):.1f} pts ***")

# Separate reporting for non-definite / contradictory / duplicate
print("\n--- Non-definite / problematic offers ---")
# Check for duplicate Application references in offers (same app has multiple offers?)
app_refs = Counter()
for o in offers:
    for ref in o.get("fields",{}).get("Application", []):
        app_refs[ref] += 1
dup_apps = {k:v for k,v in app_refs.items() if v > 1}
print(f"Offers linked to same Application (duplicate offers): {len(dup_apps)} applications")
if dup_apps:
    for k,v in list(dup_apps.items())[:3]: print(f"    App {k}: {v} offers")

# Check for missing Status
missing_status = sum(1 for o in offers if not o.get("fields",{}).get("Status"))
print(f"Offers with missing Status: {missing_status}")

# Pending offers
pending_offers = [o for o in offers if o.get("fields",{}).get("Status") == "Pending"]
print(f"Pending offers (not a definite outcome): {len(pending_offers)}")

# Check contradictory: Application references that don't exist in applications table
app_ids_set = {a["id"] for a in apps}
broken_offer_apps = []
for o in offers:
    for ref in o.get("fields",{}).get("Application", []):
        if ref and ref not in app_ids_set:
            broken_offer_apps.append(ref)
print(f"Offers with broken Application reference (missing app): {len(broken_offer_apps)}")

# Withdrawn / Declined — check for other statuses
other_statuses = {k for k in offer_statuses if k not in ("Accepted","Rejected","Pending")}
if other_statuses:
    for s in other_statuses:
        n = offer_statuses[s]
        print(f"  Status '{s}': {n} (potential withdrawn/declined/missing category)")

# Also check for applications that have both Accepted and Rejected offers (contradiction)
app_offer_statuses = {}
for o in offers:
    for ref in o.get("fields",{}).get("Application", []):
        status = o.get("fields",{}).get("Status")
        app_offer_statuses.setdefault(ref, set()).add(status)

contradictory_apps = [ref for ref, statuses in app_offer_statuses.items() if len(statuses) > 1 and "Accepted" in statuses and "Rejected" in statuses]
print(f"\nApplications with contradictory offers (both Accepted + Rejected): {len(contradictory_apps)}")
if contradictory_apps:
    print(f"  Example app IDs: {contradictory_apps[:3]}")

print("\n" + "="*70)
print("CONCLUSION")
print("="*70)
print(f"Claim 1 (26.9% job-board hires): Job Board = {jb_share_acc:.1f}% of accepted-offer hires; {job_board_cands/300*100:.1f}% of candidates. 26.9% does NOT match either. Reject or qualify.")
if total_acc > 0:
    print(f"Claim 2 (72% acceptance): {accepted}/{definite_total} = {rate:.1f}%. Distance to 72% = {abs(rate-72):.1f} pts.")
else:
    print("Claim 2: No accepted offers found — cannot compute.")
