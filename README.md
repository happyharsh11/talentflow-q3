# TalentFlow Airtable Data Download

Downloads all records from the TalentFlow Airtable base (8 tables) and saves raw JSON to `data/raw/`.

## Quick Start (Unix / macOS / WSL)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/download_airtable.py
```

## Quick Start (Windows PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts\download_airtable.py
```

## Quick Start (Windows CMD)

```cmd
python -m venv .venv
call .venv\Scripts\activate.bat
pip install -r requirements.txt
python scripts\download_airtable.py
```

## One-liner (if .venv already exists)

```bash
# Unix
source .venv/bin/activate && python scripts/download_airtable.py

# Windows PowerShell
.\.venv\Scripts\Activate.ps1; python scripts\download_airtable.py

# Windows CMD
call .venv\Scripts\activate.bat && python scripts\download_airtable.py
```

## What It Does

- Reads `AIRTABLE_TOKEN` and `AIRTABLE_BASE_ID` from `.env`
- Authenticates with **Bearer token** header: `Authorization: Bearer <token>`
- Fetches all 8 tables: Departments, People, Job Openings, Candidates, Applications, Interviews, Offers, Findings
- Handles **pagination** via `offset` token (100 records per page)
- Respects **rate limit** (5 req/s) with 0.25s delay between requests
- **Retries** on transient errors (exponential backoff, max 5 retries)
- **429 handling**: waits 30s on rate-limit response
- Saves raw JSON to `data/raw/{Table Name}.json`
- **Read-only** — no write operations to Airtable

## Output

```
data/raw/
├── Departments.json       (8 records)
├── People.json           (14 records)
├── Job Openings.json     (24 records)
├── Candidates.json       (300 records)
├── Applications.json     (350 records)
├── Interviews.json       (160 records)
├── Offers.json           (36 records)
└── Findings.json         (0 records)
```

Total: ~892 records

## Configuration

- `REQUEST_DELAY = 0.25` seconds (adjust if needed)
- `MAX_RETRIES = 5`
- `REQUEST_TIMEOUT = 30` seconds
- `pageSize = 100` (Airtable max)

## Files

| File | Description |
|------|-------------|
| `scripts/download_airtable.py` | Main script (uses `requests`) |
| `scripts/download_airtable_stdlib.py` | Zero-dependency version (stdlib only) |
| `requirements.txt` | Python dependencies |
| `.env` | Credentials (not committed) |
| `data/raw/*.json` | Downloaded raw data |