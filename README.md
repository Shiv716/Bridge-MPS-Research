# Bridge

**Independent MPS Research & Oversight Platform**

Bridge is a B2B SaaS platform for UK financial adviser firms that outsource client investments to Model Portfolio Service (MPS) providers. It provides independent, specialist investment research and oversight in a structured, scalable format, enabling adviser firms to save time, improve portfolio selection and monitoring quality, and satisfy Consumer Duty and regulatory requirements.

---

## The Problem

UK financial advisers increasingly outsource client investments to MPS providers. However:

- Independent, high-quality research on MPS solutions is limited
- Oversight processes are time-consuming and inconsistent
- Consumer Duty increases scrutiny around both selection and ongoing monitoring
- Advisers often rely on provider-produced material or basic data comparisons
- There is no standardised, specialist oversight layer available at scale

Bridge exists to provide institutional-grade analytical depth, delivered through software.

---

## What Bridge Does

### Module A — MPS Selection

Filter the universe of MPS solutions by platform, provider, risk profile, investment style, ESG preference, and cost. Allows advisers to quickly narrow the universe to solutions relevant for their firm before deeper analysis.

**17 portfolios** across **5 providers** on **8 UK adviser platforms**.

### Module B — MPS Analysis

Structured analytical dashboards for each approved MPS provider, including:

- Interactive performance charts (36-month history)
- Asset allocation and geographic breakdowns
- Risk vs return scatter analysis
- Underlying fund holdings and weightings
- Peer comparison against same-risk portfolios
- Strengths and considerations for each provider
- Key personnel
- Cost analysis (OCF comparison)
- Portfolio details (rebalancing frequency, minimum investment, benchmarks)

### Module C — Insights

Research content for adviser firms:

- Weekly market commentary
- Regulatory analysis (Consumer Duty, FCA guidance)
- Thematic research (passive vs active, rebalancing approaches)
- Filterable by category

---

## MPS Universe

| Provider | Portfolios | Style | OCF | Platforms |
|---|---|---|---|---|
| Vanguard LifeStrategy | 5 | Passive | 0.22% | Transact, Fundment, Quilter, Aegon, abrdn |
| 7IM | 3 | Active | 0.54% | Transact, Quilter, Aegon |
| Tatton | 3 | Passive | 0.30% | Transact, Fundment, Quilter, abrdn |
| EQ Investors | 3 | ESG/Ethical | 0.68% | Transact, Fundment |
| Parmenion | 3 | Blended | 0.35% | Transact, Parmenion |

---

## Target Users

**Primary:** UK financial adviser firms that outsource to MPS providers, particularly centralised investment proposition teams and oversight/governance committees.

**Future:** Firms using Multi Asset Funds, firms managing investments in-house, asset managers and distribution teams.

---

## Commercial Model

- Subscription-based, firm-wide licence
- Tiered pricing based on adviser count
- Positioned as independent research infrastructure, governance support, and a client outcome enhancer

---

## Technology

Single-page application. No backend or database required. All data is embedded and the platform runs entirely in the browser.

- Vanilla JavaScript
- Chart.js for interactive visualisations
- DM Sans + Fraunces typography

---

## Running Locally

Open `index.html` in any browser. That's it.

---

## Deployment

This is a single static HTML file. Deploy anywhere:

- **GitHub Pages** — push to repo, enable Pages in settings
- **Netlify** — drag and drop at app.netlify.com/drop
- **Cloudflare Pages** — connect repo
- **Any static hosting** — just serve the file

---

## Roadmap

This MVP validates the analytical framework and three-module structure. Future development includes:

- Automated data ingestion from MPS providers (replacing static data)
- User authentication and firm-level multi-tenancy
- Subscription alerts for provider updates
- AI-enhanced commentary and interaction
- Downloadable PDF reports for regulatory compliance
- Integrated messaging between advisers, Bridge, and MPS providers
- Portfolio change analysis and tracking over time
- Expanded provider universe

---

## Disclaimer

This platform is for research and information purposes only. It does not constitute financial advice. All data shown is illustrative. Adviser firms retain full responsibility for suitability assessments and investment decisions. Performance data is simulated and should not be relied upon for investment decisions.

---

## License

Copyright © 2026. All rights reserved.

This software and its contents are proprietary. No part of this codebase, data, or analytical framework may be reproduced, distributed, or used without explicit written permission.
