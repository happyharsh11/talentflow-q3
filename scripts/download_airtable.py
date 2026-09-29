#!/usr/bin/env python3
"""
Download all records from Airtable TalentFlow base.
Uses requests (matches user snippet) with pagination, retries, rate limiting.
Reads AIRTABLE_TOKEN and AIRTABLE_BASE_ID from .env, writes raw JSON under data/raw.
"""
import os
import json
import time
from pathlib import Path
import requests
from dotenv import load_dotenv

load_dotenv()

token = os.environ["AIRTABLE_TOKEN"]
base_id = os.environ["AIRTABLE_BASE_ID"]

tables = [
    "Departments", "People", "Job Openings", "Candidates",
    "Applications", "Interviews", "Offers", "Findings"
]

headers = {"Authorization": f"Bearer {token}"}
out_dir = Path("data/raw")
out_dir.mkdir(parents=True, exist_ok=True)

REQUEST_DELAY = 0.25  # ~4 req/s, well under 5 req/s limit
MAX_RETRIES = 5

def fetch_table(table_name: str) -> list:
    records = []
    params = {"pageSize": 100}
    url = f"https://api.airtable.com/v0/{base_id}/{table_name.replace(' ', '%20')}"
    retries = 0
    while True:
        try:
            resp = requests.get(url, headers=headers, params=params, timeout=30)
            if resp.status_code == 429:
                print(f"  [{table_name}] Rate limited (429), backing off 30s...")
                time.sleep(30)
                retries = 0
                continue
            resp.raise_for_status()
            payload = resp.json()
            records.extend(payload.get("records", []))
            if "offset" not in payload:
                break
            params["offset"] = payload["offset"]
            retries = 0
            time.sleep(REQUEST_DELAY)
        except requests.exceptions.RequestException as e:
            retries += 1
            if retries > MAX_RETRIES:
                raise
            wait = min(30, 2 ** retries)
            print(f"  [{table_name}] Request error ({e}), retry {retries}/{MAX_RETRIES} in {wait}s...")
            time.sleep(wait)
    return records

def main():
    print(f"Base: {base_id} | Tables: {len(tables)}")
    total = 0
    for t in tables:
        print(f"Fetching {t}...")
        records = fetch_table(t)
        out_path = out_dir / f"{t}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
        print(f"  {len(records)} records -> {out_path}")
        total += len(records)
        time.sleep(REQUEST_DELAY)
    print(f"Done. Total: {total} records in data/raw/")

if __name__ == "__main__":
    main()
