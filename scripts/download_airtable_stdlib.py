#!/usr/bin/env python3
"""
Download all records from Airtable TalentFlow base using only standard libraries.
Saves raw JSON to data/raw/{table}.json
"""
import os
import json
import time
import sys
from pathlib import Path
from urllib import request, error, parse

def load_dotenv():
    """Load environment variables from .env file."""
    env_path = Path('.env')
    if env_path.is_file():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                key, value = line.split('=', 1)
                os.environ[key] = value.strip('"').strip("'")

load_dotenv()

token = os.environ["AIRTABLE_TOKEN"]
base_id = os.environ["AIRTABLE_BASE_ID"]

tables = [
    "Departments",
    "People",
    "Job Openings",
    "Candidates",
    "Applications",
    "Interviews",
    "Offers",
    "Findings"
]

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}
out_dir = Path("data/raw")
out_dir.mkdir(parents=True, exist_ok=True)

# Rate limiting: 5 req/s = 0.2s between requests
# Plus 30s backoff on 429
REQUEST_DELAY = 0.25  # slightly conservative
MAX_RETRIES = 5

def fetch_all_records(table_name: str) -> list:
    """Fetch all records from a table with pagination and retries."""
    records = []
    params = {"pageSize": 100}
    # Build initial URL without offset; encode table name for URL
    encoded_table = parse.quote(table_name, safe='')
    base_url = f"https://api.airtable.com/v0/{base_id}/{encoded_table}"
    
    retries = 0
    while True:
        # Build URL with parameters
        if params:
            query = '&'.join([f"{k}={parse.quote(str(v), safe='')}" for k, v in params.items()])
            url = f"{base_url}?{query}"
        else:
            url = base_url
        
        req = request.Request(url, headers=headers)
        
        try:
            response = request.urlopen(req, timeout=30)
            # If we get here, status is 200
            data = json.load(response)
            records.extend(data.get("records", []))
            
            if "offset" not in data:
                break
            
            params["offset"] = data["offset"]
            retries = 0  # reset on success
            time.sleep(REQUEST_DELAY)
            
        except error.HTTPError as e:
            if e.code == 429:
                # Rate limited - wait 30 seconds and retry
                wait_time = 30
                print(f"  [{table_name}] Rate limited (429), waiting {wait_time}s...")
                time.sleep(wait_time)
                retries = 0  # reset retries after rate limit
                continue
            else:
                # Other HTTP errors
                retries += 1
                if retries > MAX_RETRIES:
                    print(f"  [{table_name}] Failed after {MAX_RETRIES} retries: {e}")
                    raise
                wait = 2 ** retries  # exponential backoff
                print(f"  [{table_name}] HTTP error {e.code}, retry {retries}/{MAX_RETRIES} in {wait}s...")
                time.sleep(wait)
        except error.URLError as e:
            retries += 1
            if retries > MAX_RETRIES:
                print(f"  [{table_name}] Failed after {MAX_RETRIES} retries: {e}")
                raise
            wait = 2 ** retries  # exponential backoff
            print(f"  [{table_name}] URL error ({e.reason}), retry {retries}/{MAX_RETRIES} in {wait}s...")
            time.sleep(wait)
        except Exception as e:
            retries += 1
            if retries > MAX_RETRIES:
                print(f"  [{table_name}] Failed after {MAX_RETRIES} retries: {e}")
                raise
            wait = 2 ** retries  # exponential backoff
            print(f"  [{table_name}] Unexpected error ({e}), retry {retries}/{MAX_RETRIES} in {wait}s...")
            time.sleep(wait)
    
    return records

def main():
    print(f"Downloading from base: {base_id}")
    print(f"Tables: {', '.join(tables)}")
    print(f"Output: {out_dir.absolute()}")
    print()
    
    total_records = 0
    for table in tables:
        print(f"Fetching {table}...")
        records = fetch_all_records(table)
        out_file = out_dir / f"{table}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
        print(f"  Saved {len(records)} records to {out_file}")
        total_records += len(records)
        time.sleep(REQUEST_DELAY)
    
    print(f"\nDone. Total records: {total_records}")

if __name__ == "__main__":
    main()