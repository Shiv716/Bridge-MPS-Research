from __future__ import annotations
"""
Bridge – MPS Provider Universe & Analytics Data
Extended from MPSEnhancer with full analytical framework
"""

from datetime import datetime, timedelta
import random
import math

# ─── Platforms ───────────────────────────────────────────────────────────
PLATFORMS = ["Transact", "Fundment", "Quilter", "Aegon", "abrdn", "Parmenion", "Aviva", "Standard Life"]

# ─── Investment Styles ───────────────────────────────────────────────────
INVESTMENT_STYLES = ["Passive", "Active", "Blended", "ESG/Ethical", "Multi-Manager"]

# ─── Provider Metadata ───────────────────────────────────────────────────
PROVIDERS = {
    "Vanguard": {
        "id": "vanguard",
        "name": "Vanguard",
        "full_name": "Vanguard Asset Management",
        "description": "Global leader in passive index investing, known for low-cost, broadly diversified portfolio solutions.",
        "aum_bn": 42.5,
        "established": 1975,
        "headquarters": "London / Valley Forge, PA",
        "investment_style": "Passive",
        "key_personnel": [
            {"name": "Tim Buckley", "role": "CEO"},
            {"name": "Sean Hagerty", "role": "Managing Director, Europe"},
        ],
        "strengths": [
            "Industry-leading low costs across all risk profiles",
            "Extremely broad diversification through index-tracking approach",
            "Transparent, rules-based methodology with automatic rebalancing",
            "Consistent tracking of benchmarks with minimal tracking error",
        ],
        "considerations": [
            "No tactical flexibility – fully strategic allocation",
            "Limited ESG integration in core LifeStrategy range",
            "Single-manager approach with no external fund selection",
            "Currency exposure largely unhedged in equity allocation",
        ],
        "regulatory_status": "FCA Authorised",
        "website": "https://www.vanguardinvestor.co.uk",
    },
    "7IM": {
        "id": "7im",
        "name": "7IM",
        "full_name": "Seven Investment Management",
        "description": "Multi-asset specialist combining strategic allocation with active fund selection and alternatives exposure.",
        "aum_bn": 18.2,
        "established": 2002,
        "headquarters": "London",
        "investment_style": "Active",
        "key_personnel": [
            {"name": "Dean Sherwood", "role": "CEO"},
            {"name": "Matthew Sheridan", "role": "CIO"},
        ],
        "strengths": [
            "Active asset allocation provides tactical flexibility",
            "Alternatives allocation adds diversification beyond traditional assets",
            "Strong investment team with institutional pedigree",
            "Comprehensive risk management framework with quarterly rebalancing",
        ],
        "considerations": [
            "Higher OCF compared to passive alternatives",
            "Active management introduces manager selection risk",
            "Limited platform availability vs peers",
            "Minimum investment threshold may exclude smaller portfolios",
        ],
        "regulatory_status": "FCA Authorised",
        "website": "https://www.7im.co.uk",
    },
    "Tatton": {
        "id": "tatton",
        "name": "Tatton",
        "full_name": "Tatton Investment Management",
        "description": "Adviser-focused DFM specialising in low-cost passive portfolios with monthly rebalancing and broad platform coverage.",
        "aum_bn": 14.8,
        "established": 2013,
        "headquarters": "London",
        "investment_style": "Passive",
        "key_personnel": [
            {"name": "Lothar Sherwood", "role": "CEO"},
            {"name": "Ricky Chan", "role": "CIO"},
        ],
        "strengths": [
            "Low-cost passive approach with institutional-quality implementation",
            "Monthly rebalancing provides tighter risk management",
            "Excellent platform coverage across major adviser platforms",
            "Strong adviser service model with dedicated support",
        ],
        "considerations": [
            "Relatively newer entrant compared to established managers",
            "Passive-only approach limits tactical positioning",
            "Portfolio construction relies heavily on Vanguard and iShares funds",
            "Limited alternatives exposure across risk profiles",
        ],
        "regulatory_status": "FCA Authorised",
        "website": "https://www.tattonim.com",
    },
    "EQ Investors": {
        "id": "eq",
        "name": "EQ Investors",
        "full_name": "EQ Investors",
        "description": "Specialist ESG/ethical investment manager offering positive impact portfolios for values-aligned investors.",
        "aum_bn": 4.2,
        "established": 2007,
        "headquarters": "London",
        "investment_style": "ESG/Ethical",
        "key_personnel": [
            {"name": "John Spiers", "role": "CEO"},
            {"name": "Damien Lardoux", "role": "Head of Impact Investing"},
        ],
        "strengths": [
            "Deep expertise in ethical and impact investing",
            "Rigorous ESG screening methodology with positive impact focus",
            "Strong narrative for clients with values-driven investment preferences",
            "Differentiated proposition in growing ESG market segment",
        ],
        "considerations": [
            "Higher OCF due to specialist fund selection",
            "Smaller AUM compared to mainstream providers",
            "ESG universe constraints may limit diversification",
            "Limited platform availability restricts access",
        ],
        "regulatory_status": "FCA Authorised",
        "website": "https://www.eqinvestors.co.uk",
    },
    "Parmenion": {
        "id": "parmenion",
        "name": "Parmenion",
        "full_name": "Parmenion Investment Management",
        "description": "Technology-led investment platform and DFM providing risk-graded portfolios with integrated adviser tools.",
        "aum_bn": 9.6,
        "established": 2007,
        "headquarters": "Bristol",
        "investment_style": "Blended",
        "key_personnel": [
            {"name": "Michael Maydon", "role": "Managing Director"},
            {"name": "Martin Sherwood", "role": "CIO"},
        ],
        "strengths": [
            "Integrated technology platform reduces adviser operational burden",
            "Granular risk grading system across 10 risk levels",
            "Low minimum investment threshold (£1,000) supports smaller portfolios",
            "Blended active/passive approach offers cost-effective active management",
        ],
        "considerations": [
            "Primarily available on own platform, limiting choice for multi-platform firms",
            "Transact is only major third-party platform supported",
            "Blended approach may underperform in strongly trending markets",
            "Risk grading system differs from industry-standard ATR scales",
        ],
        "regulatory_status": "FCA Authorised",
        "website": "https://www.parmenion.co.uk",
    },
}

# ─── MPS Universe (expanded from MPSEnhancer) ────────────────────────────
MPS_UNIVERSE = [
    # Vanguard LifeStrategy
    {
        "id": "vanguard-ls-20", "name": "Vanguard LifeStrategy 20% Equity",
        "provider": "Vanguard", "risk_rating": 3, "risk_label": "Cautious",
        "asset_allocation": {"equity": 20, "bonds": 80, "alternatives": 0, "cash": 0},
        "geographic_allocation": {"uk": 18, "north_america": 32, "europe": 22, "asia_pacific": 15, "emerging_markets": 8, "other": 5},
        "ocf": 0.22, "return_1yr": 4.2, "return_3yr": 8.1, "return_5yr": 15.3,
        "return_ytd": 2.1, "return_since_inception": 42.8,
        "volatility": 4.8, "max_drawdown": -8.2, "sharpe_ratio": 0.72,
        "income_yield": 2.1, "rebalancing": "Automatic", "min_investment": 500,
        "platforms": ["Transact", "Fundment", "Quilter", "Aegon", "abrdn"],
        "ethical": False, "decumulation_suitable": True,
        "time_horizons": ["short", "medium", "long"],
        "underlying_funds": [
            {"name": "Vanguard Global Bond Index", "weight": 60, "type": "Bond"},
            {"name": "Vanguard UK Gilt UCITS ETF", "weight": 20, "type": "Bond"},
            {"name": "Vanguard FTSE All-World UCITS ETF", "weight": 15, "type": "Equity"},
            {"name": "Vanguard FTSE 100 UCITS ETF", "weight": 5, "type": "Equity"},
        ],
        "inception_date": "2011-06-23", "benchmark": "20% FTSE All-Share / 80% Bloomberg Barclays Global Aggregate",
    },
    {
        "id": "vanguard-ls-40", "name": "Vanguard LifeStrategy 40% Equity",
        "provider": "Vanguard", "risk_rating": 4, "risk_label": "Cautious-Moderate",
        "asset_allocation": {"equity": 40, "bonds": 60, "alternatives": 0, "cash": 0},
        "geographic_allocation": {"uk": 20, "north_america": 30, "europe": 20, "asia_pacific": 16, "emerging_markets": 9, "other": 5},
        "ocf": 0.22, "return_1yr": 6.1, "return_3yr": 12.4, "return_5yr": 22.8,
        "return_ytd": 3.2, "return_since_inception": 68.4,
        "volatility": 6.8, "max_drawdown": -12.4, "sharpe_ratio": 0.78,
        "income_yield": 1.8, "rebalancing": "Automatic", "min_investment": 500,
        "platforms": ["Transact", "Fundment", "Quilter", "Aegon", "abrdn"],
        "ethical": False, "decumulation_suitable": True,
        "time_horizons": ["medium", "long"],
        "underlying_funds": [
            {"name": "Vanguard Global Bond Index", "weight": 44, "type": "Bond"},
            {"name": "Vanguard UK Gilt UCITS ETF", "weight": 16, "type": "Bond"},
            {"name": "Vanguard FTSE All-World UCITS ETF", "weight": 30, "type": "Equity"},
            {"name": "Vanguard FTSE 100 UCITS ETF", "weight": 10, "type": "Equity"},
        ],
        "inception_date": "2011-06-23", "benchmark": "40% FTSE All-Share / 60% Bloomberg Barclays Global Aggregate",
    },
    {
        "id": "vanguard-ls-60", "name": "Vanguard LifeStrategy 60% Equity",
        "provider": "Vanguard", "risk_rating": 5, "risk_label": "Moderate",
        "asset_allocation": {"equity": 60, "bonds": 40, "alternatives": 0, "cash": 0},
        "geographic_allocation": {"uk": 22, "north_america": 28, "europe": 18, "asia_pacific": 17, "emerging_markets": 10, "other": 5},
        "ocf": 0.22, "return_1yr": 8.4, "return_3yr": 18.2, "return_5yr": 32.5,
        "return_ytd": 4.6, "return_since_inception": 98.2,
        "volatility": 9.8, "max_drawdown": -18.6, "sharpe_ratio": 0.85,
        "income_yield": 1.6, "rebalancing": "Automatic", "min_investment": 500,
        "platforms": ["Transact", "Fundment", "Quilter", "Aegon", "abrdn"],
        "ethical": False, "decumulation_suitable": True,
        "time_horizons": ["medium", "long"],
        "underlying_funds": [
            {"name": "Vanguard FTSE All-World UCITS ETF", "weight": 45, "type": "Equity"},
            {"name": "Vanguard FTSE 100 UCITS ETF", "weight": 15, "type": "Equity"},
            {"name": "Vanguard Global Bond Index", "weight": 28, "type": "Bond"},
            {"name": "Vanguard UK Gilt UCITS ETF", "weight": 12, "type": "Bond"},
        ],
        "inception_date": "2011-06-23", "benchmark": "60% FTSE All-Share / 40% Bloomberg Barclays Global Aggregate",
    },
    {
        "id": "vanguard-ls-80", "name": "Vanguard LifeStrategy 80% Equity",
        "provider": "Vanguard", "risk_rating": 6, "risk_label": "Moderate-Adventurous",
        "asset_allocation": {"equity": 80, "bonds": 20, "alternatives": 0, "cash": 0},
        "geographic_allocation": {"uk": 24, "north_america": 28, "europe": 16, "asia_pacific": 18, "emerging_markets": 10, "other": 4},
        "ocf": 0.22, "return_1yr": 10.2, "return_3yr": 24.6, "return_5yr": 42.1,
        "return_ytd": 5.8, "return_since_inception": 132.6,
        "volatility": 12.4, "max_drawdown": -24.2, "sharpe_ratio": 0.88,
        "income_yield": 1.4, "rebalancing": "Automatic", "min_investment": 500,
        "platforms": ["Transact", "Fundment", "Quilter", "Aegon", "abrdn"],
        "ethical": False, "decumulation_suitable": False,
        "time_horizons": ["long"],
        "underlying_funds": [
            {"name": "Vanguard FTSE All-World UCITS ETF", "weight": 60, "type": "Equity"},
            {"name": "Vanguard FTSE 100 UCITS ETF", "weight": 20, "type": "Equity"},
            {"name": "Vanguard Global Bond Index", "weight": 14, "type": "Bond"},
            {"name": "Vanguard UK Gilt UCITS ETF", "weight": 6, "type": "Bond"},
        ],
        "inception_date": "2011-06-23", "benchmark": "80% FTSE All-Share / 20% Bloomberg Barclays Global Aggregate",
    },
    {
        "id": "vanguard-ls-100", "name": "Vanguard LifeStrategy 100% Equity",
        "provider": "Vanguard", "risk_rating": 7, "risk_label": "Adventurous",
        "asset_allocation": {"equity": 100, "bonds": 0, "alternatives": 0, "cash": 0},
        "geographic_allocation": {"uk": 24, "north_america": 30, "europe": 15, "asia_pacific": 18, "emerging_markets": 10, "other": 3},
        "ocf": 0.22, "return_1yr": 12.4, "return_3yr": 28.6, "return_5yr": 52.1,
        "return_ytd": 7.2, "return_since_inception": 168.4,
        "volatility": 14.2, "max_drawdown": -32.4, "sharpe_ratio": 0.92,
        "income_yield": 1.2, "rebalancing": "Automatic", "min_investment": 500,
        "platforms": ["Transact", "Fundment", "Quilter", "Aegon", "abrdn"],
        "ethical": False, "decumulation_suitable": False,
        "time_horizons": ["long"],
        "underlying_funds": [
            {"name": "Vanguard FTSE All-World UCITS ETF", "weight": 58, "type": "Equity"},
            {"name": "Vanguard FTSE 100 UCITS ETF", "weight": 22, "type": "Equity"},
            {"name": "Vanguard Emerging Markets Stock Index", "weight": 12, "type": "Equity"},
            {"name": "Vanguard FTSE Developed Europe ex-UK", "weight": 8, "type": "Equity"},
        ],
        "inception_date": "2011-06-23", "benchmark": "FTSE All-Share",
    },
    # 7IM
    {
        "id": "7im-cautious", "name": "7IM Moderately Cautious",
        "provider": "7IM", "risk_rating": 4, "risk_label": "Moderately Cautious",
        "asset_allocation": {"equity": 35, "bonds": 55, "alternatives": 10, "cash": 0},
        "geographic_allocation": {"uk": 22, "north_america": 26, "europe": 20, "asia_pacific": 14, "emerging_markets": 8, "other": 10},
        "ocf": 0.54, "return_1yr": 5.8, "return_3yr": 11.2, "return_5yr": 19.8,
        "return_ytd": 2.8, "return_since_inception": 52.4,
        "volatility": 6.2, "max_drawdown": -10.8, "sharpe_ratio": 0.71,
        "income_yield": 2.2, "rebalancing": "Quarterly", "min_investment": 10000,
        "platforms": ["Transact", "Quilter", "Aegon"],
        "ethical": False, "decumulation_suitable": True,
        "time_horizons": ["medium", "long"],
        "underlying_funds": [
            {"name": "7IM UK Equity Value", "weight": 12, "type": "Equity"},
            {"name": "7IM US Equity Value", "weight": 10, "type": "Equity"},
            {"name": "7IM International Equity", "weight": 13, "type": "Equity"},
            {"name": "7IM Sterling Bond", "weight": 35, "type": "Bond"},
            {"name": "7IM Global Bond", "weight": 20, "type": "Bond"},
            {"name": "7IM Alternative Strategies", "weight": 10, "type": "Alternative"},
        ],
        "inception_date": "2014-03-15", "benchmark": "IA Mixed Investment 20-60% Shares",
    },
    {
        "id": "7im-balanced", "name": "7IM Balanced",
        "provider": "7IM", "risk_rating": 5, "risk_label": "Balanced",
        "asset_allocation": {"equity": 55, "bonds": 35, "alternatives": 10, "cash": 0},
        "geographic_allocation": {"uk": 20, "north_america": 28, "europe": 18, "asia_pacific": 16, "emerging_markets": 10, "other": 8},
        "ocf": 0.54, "return_1yr": 7.6, "return_3yr": 16.8, "return_5yr": 28.4,
        "return_ytd": 3.8, "return_since_inception": 72.6,
        "volatility": 9.4, "max_drawdown": -16.2, "sharpe_ratio": 0.79,
        "income_yield": 1.8, "rebalancing": "Quarterly", "min_investment": 10000,
        "platforms": ["Transact", "Quilter", "Aegon"],
        "ethical": False, "decumulation_suitable": True,
        "time_horizons": ["medium", "long"],
        "underlying_funds": [
            {"name": "7IM UK Equity Value", "weight": 18, "type": "Equity"},
            {"name": "7IM US Equity Value", "weight": 15, "type": "Equity"},
            {"name": "7IM International Equity", "weight": 22, "type": "Equity"},
            {"name": "7IM Sterling Bond", "weight": 20, "type": "Bond"},
            {"name": "7IM Global Bond", "weight": 15, "type": "Bond"},
            {"name": "7IM Alternative Strategies", "weight": 10, "type": "Alternative"},
        ],
        "inception_date": "2014-03-15", "benchmark": "IA Mixed Investment 40-85% Shares",
    },
    {
        "id": "7im-adventurous", "name": "7IM Moderately Adventurous",
        "provider": "7IM", "risk_rating": 6, "risk_label": "Moderately Adventurous",
        "asset_allocation": {"equity": 75, "bonds": 15, "alternatives": 10, "cash": 0},
        "geographic_allocation": {"uk": 18, "north_america": 30, "europe": 16, "asia_pacific": 18, "emerging_markets": 12, "other": 6},
        "ocf": 0.54, "return_1yr": 9.8, "return_3yr": 22.4, "return_5yr": 38.6,
        "return_ytd": 5.2, "return_since_inception": 96.8,
        "volatility": 12.8, "max_drawdown": -22.6, "sharpe_ratio": 0.82,
        "income_yield": 1.4, "rebalancing": "Quarterly", "min_investment": 10000,
        "platforms": ["Transact", "Quilter", "Aegon"],
        "ethical": False, "decumulation_suitable": False,
        "time_horizons": ["long"],
        "underlying_funds": [
            {"name": "7IM UK Equity Value", "weight": 22, "type": "Equity"},
            {"name": "7IM US Equity Value", "weight": 20, "type": "Equity"},
            {"name": "7IM International Equity", "weight": 18, "type": "Equity"},
            {"name": "7IM Emerging Markets Equity", "weight": 15, "type": "Equity"},
            {"name": "7IM Sterling Bond", "weight": 10, "type": "Bond"},
            {"name": "7IM Alternative Strategies", "weight": 10, "type": "Alternative"},
            {"name": "7IM Global Bond", "weight": 5, "type": "Bond"},
        ],
        "inception_date": "2014-03-15", "benchmark": "IA Flexible Investment",
    },
    # EQ Investors
    {
        "id": "eq-cautious", "name": "EQ Positive Impact Cautious",
        "provider": "EQ Investors", "risk_rating": 4, "risk_label": "Cautious",
        "asset_allocation": {"equity": 40, "bonds": 55, "alternatives": 5, "cash": 0},
        "geographic_allocation": {"uk": 28, "north_america": 24, "europe": 22, "asia_pacific": 12, "emerging_markets": 8, "other": 6},
        "ocf": 0.68, "return_1yr": 5.2, "return_3yr": 10.8, "return_5yr": 18.6,
        "return_ytd": 2.4, "return_since_inception": 38.2,
        "volatility": 6.8, "max_drawdown": -11.4, "sharpe_ratio": 0.65,
        "income_yield": 1.6, "rebalancing": "Quarterly", "min_investment": 5000,
        "platforms": ["Transact", "Fundment"],
        "ethical": True, "decumulation_suitable": True,
        "time_horizons": ["medium", "long"],
        "underlying_funds": [
            {"name": "Impax Environmental Markets", "weight": 15, "type": "Equity"},
            {"name": "Liontrust Sustainable Future Corporate Bond", "weight": 25, "type": "Bond"},
            {"name": "Rathbone Ethical Bond", "weight": 20, "type": "Bond"},
            {"name": "Stewart Investors Worldwide Sustainability", "weight": 15, "type": "Equity"},
            {"name": "Triodos Pioneer Impact", "weight": 10, "type": "Equity"},
            {"name": "FP WHEB Sustainability", "weight": 10, "type": "Bond"},
            {"name": "Greencoat UK Wind", "weight": 5, "type": "Alternative"},
        ],
        "inception_date": "2017-09-01", "benchmark": "IA Mixed Investment 20-60% Shares (Ethical)",
    },
    {
        "id": "eq-balanced", "name": "EQ Positive Impact Balanced",
        "provider": "EQ Investors", "risk_rating": 5, "risk_label": "Balanced",
        "asset_allocation": {"equity": 60, "bonds": 35, "alternatives": 5, "cash": 0},
        "geographic_allocation": {"uk": 26, "north_america": 26, "europe": 20, "asia_pacific": 14, "emerging_markets": 8, "other": 6},
        "ocf": 0.68, "return_1yr": 7.4, "return_3yr": 15.2, "return_5yr": 26.4,
        "return_ytd": 3.4, "return_since_inception": 54.8,
        "volatility": 10.2, "max_drawdown": -17.8, "sharpe_ratio": 0.72,
        "income_yield": 1.2, "rebalancing": "Quarterly", "min_investment": 5000,
        "platforms": ["Transact", "Fundment"],
        "ethical": True, "decumulation_suitable": True,
        "time_horizons": ["medium", "long"],
        "underlying_funds": [
            {"name": "Impax Environmental Markets", "weight": 20, "type": "Equity"},
            {"name": "Stewart Investors Worldwide Sustainability", "weight": 20, "type": "Equity"},
            {"name": "Liontrust Sustainable Future Corporate Bond", "weight": 18, "type": "Bond"},
            {"name": "Rathbone Ethical Bond", "weight": 12, "type": "Bond"},
            {"name": "Triodos Pioneer Impact", "weight": 10, "type": "Equity"},
            {"name": "Baillie Gifford Positive Change", "weight": 10, "type": "Equity"},
            {"name": "Greencoat UK Wind", "weight": 5, "type": "Alternative"},
            {"name": "FP WHEB Sustainability", "weight": 5, "type": "Bond"},
        ],
        "inception_date": "2017-09-01", "benchmark": "IA Mixed Investment 40-85% Shares (Ethical)",
    },
    {
        "id": "eq-adventurous", "name": "EQ Positive Impact Adventurous",
        "provider": "EQ Investors", "risk_rating": 7, "risk_label": "Adventurous",
        "asset_allocation": {"equity": 90, "bonds": 5, "alternatives": 5, "cash": 0},
        "geographic_allocation": {"uk": 22, "north_america": 28, "europe": 18, "asia_pacific": 16, "emerging_markets": 12, "other": 4},
        "ocf": 0.68, "return_1yr": 10.2, "return_3yr": 21.8, "return_5yr": 42.2,
        "return_ytd": 5.6, "return_since_inception": 82.4,
        "volatility": 15.4, "max_drawdown": -28.6, "sharpe_ratio": 0.78,
        "income_yield": 0.6, "rebalancing": "Quarterly", "min_investment": 5000,
        "platforms": ["Transact", "Fundment"],
        "ethical": True, "decumulation_suitable": False,
        "time_horizons": ["long"],
        "underlying_funds": [
            {"name": "Impax Environmental Markets", "weight": 25, "type": "Equity"},
            {"name": "Baillie Gifford Positive Change", "weight": 22, "type": "Equity"},
            {"name": "Stewart Investors Worldwide Sustainability", "weight": 20, "type": "Equity"},
            {"name": "Triodos Pioneer Impact", "weight": 13, "type": "Equity"},
            {"name": "FP WHEB Sustainability", "weight": 10, "type": "Equity"},
            {"name": "Greencoat UK Wind", "weight": 5, "type": "Alternative"},
            {"name": "Rathbone Ethical Bond", "weight": 5, "type": "Bond"},
        ],
        "inception_date": "2017-09-01", "benchmark": "IA Flexible Investment (Ethical)",
    },
    # Tatton
    {
        "id": "tatton-cautious", "name": "Tatton Passive Cautious",
        "provider": "Tatton", "risk_rating": 3, "risk_label": "Cautious",
        "asset_allocation": {"equity": 25, "bonds": 70, "alternatives": 5, "cash": 0},
        "geographic_allocation": {"uk": 25, "north_america": 24, "europe": 22, "asia_pacific": 14, "emerging_markets": 8, "other": 7},
        "ocf": 0.30, "return_1yr": 4.6, "return_3yr": 9.2, "return_5yr": 16.8,
        "return_ytd": 2.2, "return_since_inception": 28.4,
        "volatility": 5.2, "max_drawdown": -9.4, "sharpe_ratio": 0.74,
        "income_yield": 2.4, "rebalancing": "Monthly", "min_investment": 5000,
        "platforms": ["Transact", "Fundment", "Quilter", "abrdn"],
        "ethical": False, "decumulation_suitable": True,
        "time_horizons": ["short", "medium", "long"],
        "underlying_funds": [
            {"name": "iShares Core UK Gilts UCITS ETF", "weight": 35, "type": "Bond"},
            {"name": "Vanguard Global Bond Index", "weight": 25, "type": "Bond"},
            {"name": "iShares Corp Bond 0-5yr UCITS ETF", "weight": 10, "type": "Bond"},
            {"name": "Vanguard FTSE All-World UCITS ETF", "weight": 18, "type": "Equity"},
            {"name": "iShares UK Property UCITS ETF", "weight": 5, "type": "Alternative"},
            {"name": "Vanguard FTSE 100 UCITS ETF", "weight": 7, "type": "Equity"},
        ],
        "inception_date": "2015-01-12", "benchmark": "ARC Cautious PCI",
    },
    {
        "id": "tatton-balanced", "name": "Tatton Passive Balanced",
        "provider": "Tatton", "risk_rating": 5, "risk_label": "Balanced",
        "asset_allocation": {"equity": 55, "bonds": 40, "alternatives": 5, "cash": 0},
        "geographic_allocation": {"uk": 22, "north_america": 28, "europe": 18, "asia_pacific": 16, "emerging_markets": 10, "other": 6},
        "ocf": 0.30, "return_1yr": 7.8, "return_3yr": 17.4, "return_5yr": 30.2,
        "return_ytd": 4.0, "return_since_inception": 58.6,
        "volatility": 9.6, "max_drawdown": -16.8, "sharpe_ratio": 0.82,
        "income_yield": 1.6, "rebalancing": "Monthly", "min_investment": 5000,
        "platforms": ["Transact", "Fundment", "Quilter", "abrdn"],
        "ethical": False, "decumulation_suitable": True,
        "time_horizons": ["medium", "long"],
        "underlying_funds": [
            {"name": "Vanguard FTSE All-World UCITS ETF", "weight": 35, "type": "Equity"},
            {"name": "Vanguard FTSE 100 UCITS ETF", "weight": 12, "type": "Equity"},
            {"name": "iShares Core UK Gilts UCITS ETF", "weight": 20, "type": "Bond"},
            {"name": "Vanguard Global Bond Index", "weight": 15, "type": "Bond"},
            {"name": "iShares Emerging Markets Equity", "weight": 8, "type": "Equity"},
            {"name": "iShares Corp Bond 0-5yr UCITS ETF", "weight": 5, "type": "Bond"},
            {"name": "iShares UK Property UCITS ETF", "weight": 5, "type": "Alternative"},
        ],
        "inception_date": "2015-01-12", "benchmark": "ARC Balanced Asset PCI",
    },
    {
        "id": "tatton-growth", "name": "Tatton Passive Growth",
        "provider": "Tatton", "risk_rating": 7, "risk_label": "Growth",
        "asset_allocation": {"equity": 85, "bonds": 10, "alternatives": 5, "cash": 0},
        "geographic_allocation": {"uk": 20, "north_america": 30, "europe": 15, "asia_pacific": 18, "emerging_markets": 12, "other": 5},
        "ocf": 0.30, "return_1yr": 11.2, "return_3yr": 26.2, "return_5yr": 48.4,
        "return_ytd": 6.4, "return_since_inception": 102.6,
        "volatility": 14.6, "max_drawdown": -28.2, "sharpe_ratio": 0.88,
        "income_yield": 1.0, "rebalancing": "Monthly", "min_investment": 5000,
        "platforms": ["Transact", "Fundment", "Quilter", "abrdn"],
        "ethical": False, "decumulation_suitable": False,
        "time_horizons": ["long"],
        "underlying_funds": [
            {"name": "Vanguard FTSE All-World UCITS ETF", "weight": 45, "type": "Equity"},
            {"name": "Vanguard S&P 500 UCITS ETF", "weight": 15, "type": "Equity"},
            {"name": "Vanguard FTSE 100 UCITS ETF", "weight": 12, "type": "Equity"},
            {"name": "iShares Emerging Markets Equity", "weight": 13, "type": "Equity"},
            {"name": "iShares Core UK Gilts UCITS ETF", "weight": 6, "type": "Bond"},
            {"name": "Vanguard Global Bond Index", "weight": 4, "type": "Bond"},
            {"name": "iShares UK Property UCITS ETF", "weight": 5, "type": "Alternative"},
        ],
        "inception_date": "2015-01-12", "benchmark": "ARC Equity Risk PCI",
    },
    # Parmenion
    {
        "id": "parmenion-3", "name": "Parmenion Risk Grade 3",
        "provider": "Parmenion", "risk_rating": 3, "risk_label": "Cautious",
        "asset_allocation": {"equity": 30, "bonds": 65, "alternatives": 5, "cash": 0},
        "geographic_allocation": {"uk": 24, "north_america": 22, "europe": 22, "asia_pacific": 14, "emerging_markets": 10, "other": 8},
        "ocf": 0.35, "return_1yr": 4.8, "return_3yr": 9.6, "return_5yr": 17.2,
        "return_ytd": 2.4, "return_since_inception": 32.8,
        "volatility": 5.4, "max_drawdown": -9.8, "sharpe_ratio": 0.72,
        "income_yield": 2.2, "rebalancing": "Quarterly", "min_investment": 1000,
        "platforms": ["Transact", "Parmenion"],
        "ethical": False, "decumulation_suitable": True,
        "time_horizons": ["short", "medium", "long"],
        "underlying_funds": [
            {"name": "L&G UK Index Trust", "weight": 14, "type": "Equity"},
            {"name": "Vanguard Global Bond Index", "weight": 30, "type": "Bond"},
            {"name": "L&G All Stocks Gilt Index Trust", "weight": 20, "type": "Bond"},
            {"name": "HSBC FTSE All-World Index", "weight": 10, "type": "Equity"},
            {"name": "L&G Short Dated Sterling Corp Bond", "weight": 15, "type": "Bond"},
            {"name": "Royal London Short Duration Global", "weight": 6, "type": "Equity"},
            {"name": "iShares UK Property UCITS ETF", "weight": 5, "type": "Alternative"},
        ],
        "inception_date": "2012-06-01", "benchmark": "ARC Cautious PCI",
    },
    {
        "id": "parmenion-5", "name": "Parmenion Risk Grade 5",
        "provider": "Parmenion", "risk_rating": 5, "risk_label": "Balanced",
        "asset_allocation": {"equity": 55, "bonds": 40, "alternatives": 5, "cash": 0},
        "geographic_allocation": {"uk": 22, "north_america": 26, "europe": 20, "asia_pacific": 16, "emerging_markets": 10, "other": 6},
        "ocf": 0.35, "return_1yr": 7.4, "return_3yr": 16.2, "return_5yr": 28.8,
        "return_ytd": 3.6, "return_since_inception": 62.4,
        "volatility": 9.2, "max_drawdown": -16.4, "sharpe_ratio": 0.78,
        "income_yield": 1.6, "rebalancing": "Quarterly", "min_investment": 1000,
        "platforms": ["Transact", "Parmenion"],
        "ethical": False, "decumulation_suitable": True,
        "time_horizons": ["medium", "long"],
        "underlying_funds": [
            {"name": "Vanguard FTSE All-World UCITS ETF", "weight": 28, "type": "Equity"},
            {"name": "L&G UK Index Trust", "weight": 16, "type": "Equity"},
            {"name": "HSBC FTSE All-World Index", "weight": 11, "type": "Equity"},
            {"name": "Vanguard Global Bond Index", "weight": 20, "type": "Bond"},
            {"name": "L&G All Stocks Gilt Index Trust", "weight": 12, "type": "Bond"},
            {"name": "L&G Short Dated Sterling Corp Bond", "weight": 8, "type": "Bond"},
            {"name": "iShares UK Property UCITS ETF", "weight": 5, "type": "Alternative"},
        ],
        "inception_date": "2012-06-01", "benchmark": "ARC Balanced Asset PCI",
    },
    {
        "id": "parmenion-8", "name": "Parmenion Risk Grade 8",
        "provider": "Parmenion", "risk_rating": 8, "risk_label": "Adventurous",
        "asset_allocation": {"equity": 95, "bonds": 0, "alternatives": 5, "cash": 0},
        "geographic_allocation": {"uk": 18, "north_america": 30, "europe": 14, "asia_pacific": 18, "emerging_markets": 14, "other": 6},
        "ocf": 0.35, "return_1yr": 12.8, "return_3yr": 28.4, "return_5yr": 54.2,
        "return_ytd": 7.4, "return_since_inception": 118.6,
        "volatility": 16.2, "max_drawdown": -34.2, "sharpe_ratio": 0.86,
        "income_yield": 0.8, "rebalancing": "Quarterly", "min_investment": 1000,
        "platforms": ["Transact", "Parmenion"],
        "ethical": False, "decumulation_suitable": False,
        "time_horizons": ["long"],
        "underlying_funds": [
            {"name": "Vanguard FTSE All-World UCITS ETF", "weight": 35, "type": "Equity"},
            {"name": "L&G UK Index Trust", "weight": 15, "type": "Equity"},
            {"name": "iShares Emerging Markets Equity", "weight": 15, "type": "Equity"},
            {"name": "HSBC FTSE All-World Index", "weight": 12, "type": "Equity"},
            {"name": "Vanguard S&P 500 UCITS ETF", "weight": 10, "type": "Equity"},
            {"name": "L&G Pacific Index Trust", "weight": 8, "type": "Equity"},
            {"name": "iShares UK Property UCITS ETF", "weight": 5, "type": "Alternative"},
        ],
        "inception_date": "2012-06-01", "benchmark": "ARC Equity Risk PCI",
    },
]


def _generate_performance_history(mps: dict, months: int = 36) -> list[dict]:
    """Generate realistic monthly performance data based on MPS characteristics."""
    random.seed(hash(mps["id"]))
    base_monthly = (1 + mps["return_3yr"] / 100) ** (1/36) - 1
    vol_monthly = mps["volatility"] / 100 / math.sqrt(12)
    
    history = []
    cumulative = 100.0
    now = datetime.now()
    
    for i in range(months, 0, -1):
        date = now - timedelta(days=i * 30)
        monthly_return = random.gauss(base_monthly, vol_monthly)
        cumulative *= (1 + monthly_return)
        history.append({
            "date": date.strftime("%Y-%m-%d"),
            "value": round(cumulative, 2),
            "monthly_return": round(monthly_return * 100, 2),
        })
    
    return history


# ─── Public API ──────────────────────────────────────────────────────────

def get_all_mps() -> list[dict]:
    return MPS_UNIVERSE

def get_providers() -> dict:
    return PROVIDERS

def get_provider(provider_name: str) -> dict | None:
    return PROVIDERS.get(provider_name)

def get_mps_by_provider(provider_name: str) -> list[dict]:
    return [m for m in MPS_UNIVERSE if m["provider"] == provider_name]

def get_mps_by_id(mps_id: str) -> dict | None:
    return next((m for m in MPS_UNIVERSE if m["id"] == mps_id), None)

def get_platforms() -> list[str]:
    return PLATFORMS

def get_investment_styles() -> list[str]:
    return INVESTMENT_STYLES

def get_performance_history(mps_id: str, months: int = 36) -> list[dict]:
    mps = get_mps_by_id(mps_id)
    if not mps:
        return []
    return _generate_performance_history(mps, months)

def filter_mps(
    risk_min: int = 1, risk_max: int = 10,
    platforms: list[str] | None = None,
    providers: list[str] | None = None,
    styles: list[str] | None = None,
    ethical_only: bool = False,
    decumulation: bool = False,
    time_horizon: str | None = None,
    min_investment_limit: float | None = None,
    ocf_max: float | None = None,
) -> list[dict]:
    results = []
    for mps in MPS_UNIVERSE:
        if not (risk_min <= mps["risk_rating"] <= risk_max):
            continue
        if platforms and not any(p in mps["platforms"] for p in platforms):
            continue
        if providers and mps["provider"] not in providers:
            continue
        if ethical_only and not mps["ethical"]:
            continue
        if decumulation and not mps["decumulation_suitable"]:
            continue
        if time_horizon and time_horizon not in mps["time_horizons"]:
            continue
        if min_investment_limit is not None and mps["min_investment"] > min_investment_limit:
            continue
        if ocf_max is not None and mps["ocf"] > ocf_max:
            continue
        results.append(mps)
    return results
