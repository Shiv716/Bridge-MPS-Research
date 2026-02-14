# Bridge – MPS Research & Oversight Platform

B2B SaaS platform for UK financial adviser firms that outsource client investments to Model Portfolio Service (MPS) providers. Provides independent, specialist investment research and oversight in a structured, scalable format.

## Quick Start

```bash
cd backend
pip install -r ../requirements.txt
python main.py
```

Open http://localhost:8000

## Architecture

```
bridge/
├── backend/
│   ├── main.py          # FastAPI server with all API endpoints
│   ├── mps_data.py      # MPS universe, provider data, filtering, performance
│   └── insights.py      # Market commentary, regulatory updates, analysis
├── frontend/
│   └── index.html       # Complete SPA (vanilla JS + Chart.js)
├── requirements.txt
└── README.md
```

## Modules

### A. MPS Selection
Filter the universe of MPS solutions by platform, provider, risk profile, investment style, ESG preference, and cost.

### B. MPS Analysis
Structured analytical dashboards per provider with:
- Interactive performance charts
- Asset allocation and geographic breakdowns
- Peer comparison tables
- Underlying fund analysis
- Strengths and considerations
- Risk vs return scatter plots
- Key personnel

### C. Insights
Market commentary, regulatory updates, and thematic analysis:
- Weekly market updates
- Consumer Duty guidance
- Passive vs active frameworks
- Rebalancing analysis

## API Endpoints

| Endpoint | Description |
|---|---|
| `GET /api/dashboard` | Overview stats, provider summary, risk distribution |
| `GET /api/selection/filters` | Available filter options |
| `GET /api/selection/mps` | Filter MPS universe (query params) |
| `GET /api/providers` | All providers with metadata |
| `GET /api/providers/{id}` | Provider detail with portfolios & analytics |
| `GET /api/mps/{id}` | MPS detail with performance history & peers |
| `GET /api/mps/{id}/performance` | Performance time series |
| `GET /api/compare?ids=a,b,c` | Side-by-side MPS comparison |
| `GET /api/insights` | All insights (filterable) |
| `GET /api/insights/{id}` | Full insight article |

## MPS Universe

| Provider | Portfolios | Style | OCF Range | Platforms |
|---|---|---|---|---|
| Vanguard LifeStrategy | 5 | Passive | 0.22% | Transact, Fundment, Quilter, Aegon, abrdn |
| 7IM | 3 | Active | 0.54% | Transact, Quilter, Aegon |
| Tatton | 3 | Passive | 0.30% | Transact, Fundment, Quilter, abrdn |
| EQ Investors | 3 | ESG/Ethical | 0.68% | Transact, Fundment |
| Parmenion | 3 | Blended | 0.35% | Transact, Parmenion |

## Built With

- **Backend**: FastAPI + Python
- **Frontend**: Vanilla JS SPA + Chart.js
- **Data**: Extended from MPSEnhancer scoring/data models
- **Fonts**: DM Sans + Fraunces

## Reused from MPSEnhancer

- MPS universe data structure and provider portfolio definitions
- Suitability scoring engine concepts (risk match, objective match, cost scoring)
- Platform/wrapper filtering logic
- FCA compliance awareness in data model design
