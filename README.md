<p align="center">
  <img src="https://img.shields.io/badge/Bridge-MPS%20Research%20%26%20Oversight-2563eb?style=for-the-badge&labelColor=0a0f1a" alt="Bridge">
</p>

<p align="center">
  <strong>Independent research infrastructure for the UK Model Portfolio Service market.</strong>
</p>

<p align="center">
  <a href="#the-problem">Problem</a> · <a href="#what-bridge-does">Product</a> · <a href="#data-pipeline">Pipeline</a> · <a href="#quick-start">Quick Start</a> · <a href="#deployment">Deployment</a> · <a href="#roadmap">Roadmap</a>
</p>

---

## Overview

Bridge is a B2B SaaS platform for UK financial adviser firms that outsource client investments to Model Portfolio Service (MPS) providers.

The UK MPS market is approximately **£150bn in assets** and continues to grow. Adviser firms need independent, specialist oversight of these portfolios — Bridge provides that in a structured, scalable format.

Bridge enables adviser firms to:

- **Save time** on MPS selection and ongoing monitoring
- **Improve quality** of portfolio oversight with institutional-grade analytics
- **Satisfy Consumer Duty** and FCA regulatory requirements
- **Demonstrate to clients** that specialist, independent oversight is in place
- **Improve client outcomes** through better-informed portfolio decisions

---

## The Problem

UK financial advisers increasingly outsource client investments to MPS providers. However:

- Independent, high-quality research on MPS solutions is **limited**
- Oversight processes are **time-consuming and inconsistent**
- Consumer Duty increases scrutiny around both **selection and ongoing monitoring**
- Advisers often rely on **provider-produced material** or basic data comparisons
- There is **no standardised, specialist oversight layer** available at scale

Bridge exists to close this gap, delivering institutional-grade analytical depth through software.

---

## What Bridge Does

### MPS Analysis

Structured analytical dashboards for each approved MPS provider, organised into 8 tabs:

| Tab | Content |
|---|---|
| **Overview** | Provider details, model range (inception, management fee), risk rating providers, platform availability |
| **Investment Process** | Investment team, strategic & tactical asset allocation, fund selection, rebalancing approach |
| **Current Exposure** | Per-portfolio holdings (fund name, ISIN, weighting, asset class, sub asset class), equity & fixed income exposure cross-portfolio |
| **Historical Exposure** | Stacked area charts — asset allocation, equity region, fixed income breakdown over time |
| **Performance** | Calendar year returns (2016–2025), trailing returns (1M–10Y), risk vs return scatter |
| **Cost** | DFM fee, underlying fund cost, all-in cost per model |
| **Adviser Support** | Onboarding & training, ongoing portfolio communication |
| **Quarterly Review** | Asset allocation changes, fund selection changes |

### MPS Selection

Filter the full MPS universe by:

| Filter | Description |
|---|---|
| Platform | Filter by adviser platform availability |
| Provider | Filter by MPS provider |
| Fund Selection | Active, Passive, or Blended approach |
| Risk Rating Provider | Dynamic Planner, Synaptic, EV, Finametrica |
| Risk Range | Minimum and maximum risk level (1–10) |

### Insights

Weekly market commentary, regulatory analysis (Consumer Duty, FCA guidance), and thematic research pieces supporting adviser oversight and client communications.

---

## Current Data

**Quilter WealthSelect Managed Active** — 8 risk-graded portfolios (3–10), sourced from provider Excel exports:

| Data | Source File |
|---|---|
| Trailing returns (1M–10Y) | `Quilter_WS_Active_-_Trailing_Returns.xlsx` |
| Calendar year returns (2016–2025) | `Quilter_WS_Active_-_Calendar_Returns.xlsx` |
| Current holdings (281 funds) | `Quilter_WS_Active_Current_Holdings.xlsx` |
| Equity & FI exposure by region | `Quilter_WS_Active_Current_Equity_+_Fixed_Income_Exposure.xlsx` |
| Historical asset allocation (2015–2025) | `Quilter_WS_Active_7_Historical_Asset_Allocation.xlsx` |
| Historical equity regions | `Quilter_WS_Active_7_Historical_Equity_Region.xlsx` |
| Historical fixed income | `Quilter_WS_Active_7_Historical_Fixed_Income.xlsx` |
| Cost breakdown (DFM + underlying) | Provider cost tab |

---

## Data Pipeline

Provider Excel files are transformed into frontend-ready JSON via an automated pipeline:

```
Excel files → pipeline.py → quilter_data.json → mps_data.py → main.py (API) → index.html
```

**Adding a new provider:**

1. Place their Excel files in `data/`
2. Add a `build_newprovider()` function in `pipeline.py`
3. Run: `python pipeline.py --provider newprovider --input ./data/ --output ./`
4. Restart server — backend auto-loads every `*_data.json` file

No changes needed to `main.py`, `mps_data.py`, or `index.html`.

---

## Quick Start

```bash
pip install -r requirements.txt
python pipeline.py --provider quilter --input ./data/ --output ./
python main.py
```

Open **http://localhost:8000**

---

## Project Structure

```
├── main.py              → FastAPI server (API + serves frontend)
├── mps_data.py          → Data layer (auto-loads *_data.json files)
├── insights.py          → Research content
├── pipeline.py          → Excel → JSON data converter
├── index.html           → Frontend SPA
├── requirements.txt     → Python dependencies
├── quilter_data.json    → Generated provider data
└── data/                → Source Excel files per provider
```

---

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /api/dashboard` | Overview stats and provider summary |
| `GET /api/selection/filters` | Available filter options |
| `GET /api/selection/mps` | Filter MPS universe (query params) |
| `GET /api/providers` | All providers with metadata |
| `GET /api/providers/{id}` | Provider detail with portfolios |
| `GET /api/historical/{key}` | Historical allocation data |
| `GET /api/benchmarks` | EAA benchmark returns |
| `GET /api/costs` | Cost breakdown table |
| `GET /api/insights` | Research articles (filterable) |
| `POST /api/feedback` | Submit feedback (email via SMTP) |

---

## Tech Stack

| Component | Technology |
|---|---|
| Backend | FastAPI (Python) |
| Frontend | Vanilla JS SPA + Chart.js |
| Data Pipeline | openpyxl (Excel parsing) |
| Data Format | JSON (generated from Excel, not hardcoded) |

---

## Deployment

### Render (Recommended)

1. Push to GitHub
2. Go to [render.com](https://render.com) → New → Web Service
3. Connect repo, select branch
4. **Build command:** `pip install -r requirements.txt`
5. **Start command:** `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Add SMTP environment variables for feedback email (optional)
7. Deploy

### Local

```bash
pip install -r requirements.txt
python main.py
```

---

## Target Market

**Primary:** UK financial adviser firms that outsource to MPS providers — particularly centralised investment proposition (CIP) teams and oversight / governance committees.

**Future segments:** Adviser firms using Multi Asset Funds, firms managing investments in-house, asset managers and distribution teams.

---

## Commercial Model

- Subscription-based with firm-wide licensing
- Tiered pricing based on adviser count
- Clear regulatory tailwinds driving demand (Consumer Duty, FCA oversight expectations)
- Positioned as independent research infrastructure, governance support tool, and client outcome enhancer

---

## Roadmap

### Phase 2 — Strengthen & Scale

- [ ] Automated data ingestion from MPS providers
- [ ] User authentication and firm-level multi-tenancy
- [ ] PostgreSQL database (replacing JSON files)
- [ ] Subscription alerts for provider changes
- [ ] Downloadable PDF reports for regulatory compliance

### Phase 3 — Expansion & Advanced Features

- [ ] AI-enhanced commentary and provider summaries
- [ ] AI-assisted Consumer Duty regulatory reports
- [ ] Portfolio change analysis — tracking allocation shifts over time
- [ ] Expanded provider universe (full UK MPS market coverage)
- [ ] Client-facing commentary generation tools
- [ ] Structured MPS dataset as a standalone data product

---

## Disclaimer

This platform is for research and information purposes only and does not constitute financial advice. Adviser firms retain full responsibility for suitability assessments and investment decisions.

---

## License

[MIT](LICENSE)
