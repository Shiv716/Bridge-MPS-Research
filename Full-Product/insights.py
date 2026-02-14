from __future__ import annotations
"""
Bridge – Insights & Market Commentary Module
Weekly commentary, thought pieces, thematic analysis
"""

from datetime import datetime, timedelta

INSIGHTS = [
    {
        "id": "insight-001",
        "title": "Q4 2025 MPS Market Review: Navigating Rate Uncertainty",
        "category": "Market Commentary",
        "date": "2026-01-10",
        "author": "Bridge Research",
        "summary": "An analysis of how UK MPS providers positioned portfolios through Q4 2025 amid shifting rate expectations and geopolitical uncertainty.",
        "content": """The final quarter of 2025 presented UK Model Portfolio Service providers with a complex environment. The Bank of England's decision to hold rates steady in November, following two consecutive cuts earlier in the year, forced a recalibration of duration positioning across bond allocations.

**Key Observations Across the MPS Universe:**

Passive providers such as Vanguard and Tatton maintained their strategic allocations with minimal deviation, which is consistent with their rules-based approaches. The automatic rebalancing mechanisms in Vanguard's LifeStrategy range resulted in modest equity trimming as markets reached new highs in October before pulling back in December.

Active managers showed more tactical flexibility. 7IM notably reduced duration in their bond allocations during October, a move that proved well-timed as gilt yields moved higher into year-end. Their alternatives allocation also contributed positively, providing ballast during the November equity volatility.

EQ Investors' Positive Impact range experienced stronger-than-average inflows, reflecting the continued adviser appetite for ESG-aligned solutions. Performance was mixed relative to mainstream peers, with the ethical universe constraint creating some headwind in the energy-heavy Q4 environment.

Parmenion's blended approach navigated the quarter effectively, with the active overlay adding approximately 20-30bps relative to a pure passive implementation at equivalent risk levels.

**Implications for Adviser Oversight:**

The quarter highlighted the importance of understanding how different MPS providers respond to market stress. For adviser firms conducting oversight, the key questions are: (1) Did the portfolio behave as expected given its stated risk profile? (2) Were any tactical changes communicated effectively? (3) Does the cost remain justified relative to the approach?

These are the exact questions Bridge is designed to help advisers answer systematically.""",
        "tags": ["quarterly-review", "rates", "mps-performance", "consumer-duty"],
        "read_time_minutes": 6,
    },
    {
        "id": "insight-002",
        "title": "Consumer Duty One Year On: What Advisers Need to Know for MPS Oversight",
        "category": "Regulatory",
        "date": "2026-01-24",
        "summary": "Practical guidance on how Consumer Duty requirements affect MPS selection and ongoing monitoring obligations for adviser firms.",
        "author": "Bridge Research",
        "content": """Consumer Duty has been in force for over a year, and the FCA's supervisory approach is becoming clearer. For adviser firms that outsource to MPS providers, the regulatory expectations around selection and ongoing monitoring continue to crystallise.

**The Core Requirements:**

The Products and Services outcome requires adviser firms to demonstrate that the MPS solutions they recommend deliver fair value relative to the target market. This means advisers cannot simply defer to the provider's own assessment – independent oversight is expected.

The Price and Value outcome necessitates regular review of total cost to the client, including the MPS OCF, platform charges, and adviser fees. Firms should be able to articulate why the combined cost represents fair value for each client segment.

The Consumer Understanding outcome means that communications about MPS holdings should be clear and not misleading. Advisers should be able to explain in plain language why a particular MPS was selected and how it is performing relative to expectations.

**Practical Steps for Firms:**

1. Document your MPS selection criteria and the rationale for each approved provider
2. Establish a regular monitoring cadence (quarterly is becoming the expected standard)
3. Record oversight activities and any actions taken as a result
4. Ensure your monitoring goes beyond performance – consider cost, risk positioning, and suitability alignment
5. Be prepared to evidence that you have considered alternatives and can justify why your approved list remains appropriate

Bridge provides the infrastructure to systematically address each of these requirements.""",
        "tags": ["consumer-duty", "regulation", "fca", "compliance", "oversight"],
        "read_time_minutes": 5,
    },
    {
        "id": "insight-003",
        "title": "Passive vs Active MPS: A Framework for Adviser Decision-Making",
        "category": "Thematic Analysis",
        "date": "2026-02-03",
        "summary": "A structured comparison of passive and active MPS approaches to help advisers select the right solution for different client segments.",
        "author": "Bridge Research",
        "content": """The passive vs active debate in MPS selection is often oversimplified. Rather than a binary choice, advisers should consider which approach best serves different client segments and how each aligns with their firm's investment proposition.

**The Passive Case:**

Providers like Vanguard and Tatton offer compelling passive MPS solutions with clear advantages: low cost (OCFs typically 0.22-0.30%), transparent methodology, minimal tracking error, and consistent risk exposure. For clients where cost sensitivity is paramount or where the adviser's primary value-add lies outside investment selection, passive MPS can be highly appropriate.

Tatton's monthly rebalancing provides tighter risk management than Vanguard's automatic approach, which may be relevant for clients near risk boundaries.

**The Active Case:**

7IM and to some extent Parmenion's blended approach offer tactical flexibility that passive solutions cannot. The ability to adjust duration, increase alternatives exposure, or tilt geographic allocation can add value in volatile markets – but this must be weighed against higher costs (OCFs of 0.35-0.54%).

Active MPS also introduces manager selection risk and the possibility of underperformance relative to simpler passive alternatives.

**The ESG Dimension:**

EQ Investors occupies a distinct position. For clients with genuine ethical preferences, the specialist ESG expertise may justify the higher OCF (0.68%). The key question is whether the ESG constraint is a client preference or an adviser assumption.

**A Practical Framework:**

Consider three dimensions when selecting MPS approach:
- **Client cost sensitivity**: High sensitivity → passive bias
- **Client risk profile**: Higher risk tolerance → active may add more value through alternatives and tactical positioning
- **Client values alignment**: Strong ESG preference → specialist providers

The most effective adviser firms often maintain a panel that includes both passive and active options, matching the approach to the client segment.""",
        "tags": ["passive-vs-active", "mps-selection", "investment-style", "cost-analysis"],
        "read_time_minutes": 7,
    },
    {
        "id": "insight-004",
        "title": "Weekly Market Update: 10th February 2026",
        "category": "Weekly Commentary",
        "date": "2026-02-10",
        "summary": "Key market developments affecting MPS portfolios this week, including UK GDP data and US earnings season.",
        "author": "Bridge Research",
        "content": """**Markets This Week:**

UK equities edged higher over the week, with the FTSE 100 gaining 0.8% to close at 8,420. Domestically-focused mid-caps outperformed, with the FTSE 250 advancing 1.2% following better-than-expected preliminary Q4 GDP data suggesting the UK economy grew 0.3% in the final quarter of 2025.

Global equities were mixed. The S&P 500 was broadly flat as strong US tech earnings were offset by renewed inflation concerns following a higher-than-expected CPI print. European equities benefited from ECB rate cut expectations, with the Euro Stoxx 50 gaining 0.6%.

In fixed income, UK gilt yields moved marginally lower, with the 10-year falling to 4.18%. Corporate credit spreads remained tight, supporting investment-grade bond allocations across MPS portfolios.

**MPS Portfolio Implications:**

- Higher equity allocations benefited from the positive UK equity backdrop
- Bond-heavy cautious portfolios saw modest gains from the gilt yield decline
- Sterling strengthened slightly, creating a modest headwind for unhedged international equity exposure
- Alternatives allocations provided stable returns in an otherwise choppy week

**Looking Ahead:**

Next week brings UK employment data (Tuesday) and the Bank of England's February Monetary Policy Report (Thursday). Markets are pricing approximately a 40% probability of a rate cut at the March meeting, which could have implications for both gilt yields and sterling.""",
        "tags": ["weekly-update", "markets", "uk-economy", "bonds", "equities"],
        "read_time_minutes": 4,
    },
    {
        "id": "insight-005",
        "title": "Understanding MPS Rebalancing: Why Frequency and Method Matter",
        "category": "Thematic Analysis",
        "date": "2026-02-07",
        "summary": "A deep dive into how different MPS providers approach portfolio rebalancing and why this matters for risk management and client outcomes.",
        "author": "Bridge Research",
        "content": """Rebalancing is one of the most underappreciated aspects of MPS oversight. Different providers use fundamentally different approaches, and this has real implications for portfolio risk, return, and cost.

**Rebalancing Approaches Across the MPS Universe:**

**Vanguard (Automatic/Continuous):** The LifeStrategy range uses a threshold-based approach. When allocations drift beyond set tolerance bands, the portfolio automatically rebalances. This is efficient and low-cost but can result in periods where the portfolio sits slightly off its target allocation.

**Tatton (Monthly):** The most frequent scheduled rebalancer in our universe. Monthly rebalancing provides tighter risk control, ensuring the portfolio remains close to its target allocation. However, more frequent trading can generate additional transaction costs, albeit small in a passive context.

**7IM & EQ Investors (Quarterly):** Quarterly rebalancing represents a balance between risk management and cost efficiency. It allows some natural drift between rebalancing dates, which can be beneficial in trending markets but may result in brief periods of elevated risk.

**Parmenion (Quarterly):** Similar to 7IM, but with the added dimension that the active overlay can adjust tactical positioning between formal rebalancing dates.

**Why This Matters for Oversight:**

For adviser firms monitoring MPS portfolios, understanding the rebalancing approach helps explain short-term performance deviations. A portfolio that rebalances monthly will behave differently from one that rebalances quarterly, even if their target allocations are identical.

Key questions for oversight:
- Is the rebalancing frequency appropriate for the risk profile?
- Are rebalancing costs transparent and included in the OCF?
- Does the provider communicate when significant rebalancing activity has occurred?
- How does the rebalancing approach interact with the provider's broader investment philosophy?""",
        "tags": ["rebalancing", "risk-management", "portfolio-construction", "oversight"],
        "read_time_minutes": 5,
    },
]


def get_all_insights() -> list[dict]:
    return sorted(INSIGHTS, key=lambda x: x["date"], reverse=True)

def get_insight_by_id(insight_id: str) -> dict | None:
    return next((i for i in INSIGHTS if i["id"] == insight_id), None)

def get_insights_by_category(category: str) -> list[dict]:
    return sorted(
        [i for i in INSIGHTS if i["category"].lower() == category.lower()],
        key=lambda x: x["date"], reverse=True
    )

def get_insight_categories() -> list[str]:
    return list(set(i["category"] for i in INSIGHTS))

def search_insights(query: str) -> list[dict]:
    query_lower = query.lower()
    results = []
    for insight in INSIGHTS:
        if (query_lower in insight["title"].lower() or
            query_lower in insight["summary"].lower() or
            any(query_lower in tag for tag in insight["tags"])):
            results.append(insight)
    return sorted(results, key=lambda x: x["date"], reverse=True)
