# Bridge – MPS Research & Oversight

Independent research platform for UK financial adviser firms that outsource to Model Portfolio Service (MPS) providers.

---

## Quick Start

```bash
pip install -r requirements.txt
python pipeline.py --provider quilter --input ./data/ --output ./
python main.py
```

Open **http://localhost:8000**

---

## How It Works

```
Excel files → pipeline.py → quilter_data.json → mps_data.py → main.py (API) → index.html (frontend)
```

**Three steps:**

1. **Pipeline** reads provider Excel files from `data/`, transforms them into a structured JSON file (`quilter_data.json`)
2. **Backend** (`main.py`) auto-loads every `*_data.json` file and serves it through a REST API
3. **Frontend** (`index.html`) fetches from the API and renders the dashboard

---

## Project Structure

```
├── main.py              → FastAPI server (API + serves frontend)
├── mps_data.py          → Data layer (reads *_data.json files)
├── insights.py          → Research content (manually maintained)
├── pipeline.py          → Excel → JSON data converter
├── index.html           → Frontend SPA
├── requirements.txt     → Python dependencies
├── quilter_data.json    → Generated provider data (do not edit manually)
└── data/                → Source Excel files per provider
```

---

## Modules

**Dashboard** — Aggregate stats, provider overview, risk distribution, latest insights.

**MPS Selection** — Filter the full portfolio universe by platform, provider, risk rating (3–10), and ESG preference.

**MPS Analysis** — Per-provider dashboards with asset allocation charts, portfolio range tables, strengths & considerations, key personnel. Individual portfolio pages with performance history, geographic breakdown, underlying fund holdings, and peer comparison.

**Insights** — Market commentary, regulatory analysis, and thematic research.

---

## Current Data

**Quilter WealthSelect Managed Active** — 8 risk-graded portfolios (3–10), real data from provider Excel exports:

| Data | Source |
|---|---|
| Trailing returns (1M–10Y) | `Quilter_WS_Active_-_Trailing_Returns.xlsx` |
| Calendar year returns (2016–2025) | `Quilter_WS_Active_-_Calendar_Returns.xlsx` |
| Current holdings (281 funds) | `Quilter_WS_Active_Current_Holdings.xlsx` |
| Equity & FI exposure by region | `Quilter_WS_Active_Current_Equity_+_Fixed_Income_Exposure.xlsx` |
| Historical asset allocation (2015–2025) | `Quilter_WS_Active_7_Historical_Asset_Allocation.xlsx` |
| Historical equity regions | `Quilter_WS_Active_7_Historical_Equity_Region.xlsx` |
| Historical fixed income | `Quilter_WS_Active_7_Historical_Fixed_Income.xlsx` |
| Cost breakdown (DFM + underlying) | Hardcoded from provider cost tab |

---

## Adding a New Provider

1. Place their Excel files in `data/`
2. Add a `build_newprovider()` function in `pipeline.py`
3. Run: `python pipeline.py --provider newprovider --input ./data/ --output ./`
4. Restart server — backend picks up the new `*_data.json` automatically

No changes needed to `main.py`, `mps_data.py`, or `index.html`.

---

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /api/dashboard` | Overview stats and provider summary |
| `GET /api/selection/filters` | Available filter options |
| `GET /api/selection/mps` | Filter MPS universe (query params) |
| `GET /api/providers` | All providers with metadata |
| `GET /api/providers/{id}` | Provider detail with portfolios |
| `GET /api/mps/{id}` | Portfolio detail with performance and peers |
| `GET /api/insights` | Research articles (filterable) |
| `GET /api/historical/{key}` | Historical allocation data |
| `GET /api/benchmarks` | EAA benchmark returns |
| `GET /api/costs` | Cost breakdown table |

---

## Tech Stack

| Component | Technology |
|---|---|
| Backend | FastAPI (Python) |
| Frontend | Vanilla JS SPA + Chart.js |
| Data Pipeline | openpyxl (Excel parsing) |
| Data Format | JSON (generated, not hardcoded) |

---

## License

MIT
