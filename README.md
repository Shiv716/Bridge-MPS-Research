<p align="center">
  <img src="https://img.shields.io/badge/Bridge-MPS%20Research%20%26%20Oversight-2563eb?style=for-the-badge&labelColor=0a0f1a" alt="Bridge">
</p>

<p align="center">
  <strong>Independent research infrastructure for the UK Model Portfolio Service market.</strong>
</p>

<p align="center">
  <a href="#the-problem">Problem</a> · <a href="#what-bridge-does">Product</a> · <a href="#live-demo">Demo</a> · <a href="#mps-universe">Data</a> · <a href="#roadmap">Roadmap</a> · <a href="#license">License</a>
</p>

---

## Overview

Bridge is a B2B SaaS platform for UK financial adviser firms that outsource client investments to Model Portfolio Service (MPS) providers.

The UK MPS market is approximately **£150bn in assets** and continues to grow. Adviser firms need independent, specialist oversight of these portfolios, Bridge provides that in a structured, scalable format.

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

Bridge exists to close this gap — delivering institutional-grade analytical depth through software.

---

## What Bridge Does

The platform consists of three core modules:

### MPS Selection

Allows adviser firms to filter the full universe of MPS solutions available on the platform. Users can filter by:

| Filter | Options |
|---|---|
| Platform | Transact, Fundment, Quilter, Aegon, abrdn, Parmenion, Aviva, Standard Life |
| Provider | Vanguard, 7IM, Tatton, EQ Investors, Parmenion |
| Risk Profile | 1–10 scale |
| ESG / Ethical | Yes / No |

The goal is to let advisers quickly narrow the universe to relevant solutions before deeper analysis.

### MPS Analysis

Structured analytical dashboards for each approved MPS provider. Each provider contains multiple analysis views covering:

- **Performance** — 36-month history, 1yr/3yr/5yr returns, YTD, since inception
- **Asset Allocation** — equity, bonds, alternatives, cash breakdowns with interactive charts
- **Geographic Allocation** — regional exposure across UK, North America, Europe, Asia Pacific, Emerging Markets
- **Risk Metrics** — volatility, max drawdown, Sharpe ratio, risk vs return positioning
- **Cost Analysis** — OCF comparison across providers and peer group
- **Underlying Holdings** — fund-level breakdown with weights and asset types
- **Peer Comparison** — side-by-side analysis against same-risk-rated portfolios
- **Strengths & Considerations** — structured qualitative assessment of each provider
- **Key Personnel** — investment team leadership
- **Portfolio Details** — rebalancing frequency, minimum investment, benchmarks, time horizons, platform availability

### Insights

A dedicated research section containing:

- **Weekly market commentary** — how market developments affect MPS portfolios
- **Regulatory analysis** — Consumer Duty guidance, FCA requirements for MPS oversight
- **Thematic research** — passive vs active frameworks, rebalancing approaches, cost analysis
- **Investment views** — broader market context for adviser communications

This content supports advisers internally, in client communications, and as documentation for regulatory oversight.

---

## Live Demo

Open `index.html` in any browser. No server, no dependencies, no setup.

The platform runs entirely client-side as a single static file.

---

## MPS Universe

**17 portfolios** across **5 providers** covering **8 UK adviser platforms**.

| Provider | Portfolios | Style | OCF | Platforms |
|---|---|---|---|---|
| Vanguard LifeStrategy | 5 (20%–100% Equity) | Passive | 0.22% | Transact, Fundment, Quilter, Aegon, abrdn |
| 7IM | 3 (Cautious–Adventurous) | Active | 0.54% | Transact, Quilter, Aegon |
| Tatton | 3 (Cautious–Growth) | Passive | 0.30% | Transact, Fundment, Quilter, abrdn |
| EQ Investors | 3 (Cautious–Adventurous) | ESG / Ethical | 0.68% | Transact, Fundment |
| Parmenion | 3 (Grade 3–8) | Blended | 0.35% | Transact, Parmenion |

> **Note:** All data in this MVP is illustrative. Production deployment will connect to live provider data feeds.

---

## Target Market

**Primary:** UK financial adviser firms that outsource to MPS providers — particularly centralised investment proposition (CIP) teams and oversight / governance committees.

**Future segments:**
- UK adviser firms using Multi Asset Funds (MAFs)
- UK adviser firms managing investments in-house
- Asset managers and distribution teams

---

## Commercial Model

- Subscription-based with firm-wide licensing
- Tiered pricing based on adviser count
- Clear regulatory tailwinds driving demand (Consumer Duty, FCA oversight expectations)
- Positioned as independent research infrastructure, governance support tool, and client outcome enhancer

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Vanilla JavaScript SPA |
| Visualisation | Chart.js 4.x |
| Typography | DM Sans + Fraunces (Google Fonts) |
| Hosting | Any static hosting (GitHub Pages, Netlify, Cloudflare Pages) |

**Architecture:** Single `index.html` file with embedded data. Zero dependencies, zero build step, zero backend.

For production scale, the architecture expands to:

```
bridge/
├── frontend/          → React / Next.js dashboard
├── backend/           → FastAPI (Python) API layer
│   ├── mps_data.py    → Provider universe, filtering, analytics
│   ├── insights.py    → Content management
│   └── main.py        → API endpoints
├── database/          → PostgreSQL (provider data, user accounts)
└── infrastructure/    → Auth, multi-tenancy, automated ingestion
```

A working FastAPI backend implementation is included in the `backend/` directory of the full repository.

---

## Roadmap

### Phase 2 — Strengthen & Scale

- [ ] Rebuild on production stack (React + FastAPI + PostgreSQL)
- [ ] Automated data ingestion from MPS providers (replacing manual/static data)
- [ ] Improved dashboard UX and navigation
- [ ] User authentication and firm-level multi-tenancy
- [ ] Subscription alerts for provider changes and updates
- [ ] Downloadable PDF reports for regulatory compliance

### Phase 3 — Expansion & Advanced Features

- [ ] AI-enhanced commentary — "explain this chart", AI-generated provider summaries
- [ ] AI-assisted regulatory reports (customisable Consumer Duty reports)
- [ ] Integrated messaging (adviser ↔ Bridge, adviser ↔ MPS provider)
- [ ] Portfolio change analysis — tracking allocation shifts over time
- [ ] Expanded provider universe (full UK MPS market coverage)
- [ ] Client-facing commentary generation tools
- [ ] Structured MPS dataset as a standalone data product

---

## Deployment

This MVP is a single static file. Deploy anywhere:

**GitHub Pages**
1. Push `index.html` and `README.md` to a repository
2. Settings → Pages → Source → Deploy from branch → `main` → `/ (root)`
3. Live at `https://username.github.io/repo-name`

**Netlify**
1. Go to [app.netlify.com/drop](https://app.netlify.com/drop)
2. Drag and drop the `index.html` file
3. Live instantly

**Cloudflare Pages / Vercel**
1. Connect repository
2. Deploy — no build settings needed

---

## Repository Structure

```
├── index.html          # Complete working platform (standalone, no backend)
├── README.md           # This file
└── LICENSE             # MIT License
```

---

## Disclaimer

This platform is for research and information purposes only and does not constitute financial advice. All data shown in this MVP is illustrative and simulated. Adviser firms retain full responsibility for suitability assessments and investment decisions. Performance data should not be relied upon for investment decisions.

---

## License

[MIT](LICENSE)
