"""
Bridge – Data Pipeline
Converts provider Excel/CSV files into the JSON format the frontend expects.

Usage:
    python pipeline.py --provider quilter --input ./data/ --output ./output/

The script reads Excel files from the input directory, transforms them into
the D= blob structure, and writes the JSON to the output directory.

To integrate into index.html:
    1. Run this script
    2. Open the generated JSON
    3. Replace the const D={...}; blob in index.html with the new data

Or use --inject flag to automatically inject into an existing index.html:
    python pipeline.py --provider quilter --input ./data/ --inject ./index.html
"""

import openpyxl
import json
import os
import sys
import argparse
from datetime import datetime


# ─── Excel Reader ──────────────────────────────────────────────────────

def read_sheet(path, sheet=None):
    """Read an Excel sheet into a list of dicts."""
    wb = openpyxl.load_workbook(path, data_only=True)
    ws = wb[sheet] if sheet else wb[wb.sheetnames[0]]
    rows = list(ws.iter_rows(values_only=True))
    headers = [str(h) for h in rows[0]]
    data = []
    for row in rows[1:]:
        if all(v is None for v in row):
            continue
        data.append(dict(zip(headers, row)))
    return data


def ser(v):
    """Serialize datetime objects to ISO strings."""
    if isinstance(v, datetime):
        return v.strftime("%Y-%m-%d")
    return v


def clean(rows):
    """Clean a list of dicts, serializing datetimes."""
    return [{k: ser(v) for k, v in r.items()} for r in rows]


# ─── Quilter WealthSelect Managed Active ──────────────────────────────

def build_quilter(input_dir):
    """Build the full data blob from Quilter Excel files."""

    def load(filename, sheet=None):
        path = os.path.join(input_dir, filename)
        if not os.path.exists(path):
            print(f"  ⚠ Missing: {filename}")
            return []
        return read_sheet(path, sheet)

    # Load all files
    cal_all = load("Quilter_WS_Active_-_Calendar_Returns.xlsx")
    trail_all = load("Quilter_WS_Active_-_Trailing_Returns.xlsx")
    hist_aa = load("Quilter_WS_Active_7_Historical_Asset_Allocation.xlsx")
    hist_eq = load("Quilter_WS_Active_7_Historical_Equity_Region.xlsx")
    hist_fi = load("Quilter_WS_Active_7_Historical_Fixed_Income.xlsx")
    holdings = load("Quilter_WS_Active_Current_Holdings.xlsx")
    eq_exp = load("Quilter_WS_Active_Current_Equity___Fixed_Income_Exposure.xlsx", "Equity")
    fi_exp = load("Quilter_WS_Active_Current_Equity___Fixed_Income_Exposure.xlsx", "Fixed Income")

    # Separate Quilter rows from EAA benchmarks
    cal = [r for r in cal_all if r["Model"].startswith("Quilter")]
    trail = [r for r in trail_all if r["Model"].startswith("Quilter")]
    benchmarks_trail = [r for r in trail_all if r["Model"].startswith("EAA")]
    benchmarks_cal = [r for r in cal_all if r["Model"].startswith("EAA")]

    eq_abs = [r for r in eq_exp if r.get("Type") == "Absolute"]
    fi_abs = [r for r in fi_exp if r.get("Type") == "Absolute"]

    # Cost data (from the Cost tab in the product)
    cost_data = {
        "3":  {"dfm": 0.15, "underlying": 0.45, "all_in": 0.60},
        "4":  {"dfm": 0.15, "underlying": 0.52, "all_in": 0.67},
        "5":  {"dfm": 0.15, "underlying": 0.58, "all_in": 0.73},
        "6":  {"dfm": 0.15, "underlying": 0.63, "all_in": 0.78},
        "7":  {"dfm": 0.15, "underlying": 0.66, "all_in": 0.81},
        "8":  {"dfm": 0.15, "underlying": 0.68, "all_in": 0.83},
        "9":  {"dfm": 0.15, "underlying": 0.66, "all_in": 0.81},
        "10": {"dfm": 0.15, "underlying": 0.64, "all_in": 0.79},
    }

    platforms = [
        "AJ Bell Investcentre", "Fidelity Adviser Solutions", "M&G Wealth",
        "Morningstar Wealth", "Parmenion", "Quilter", "Transact"
    ]

    # Provider metadata
    provider = {
        "id": "quilter",
        "name": "Quilter Investors",
        "full_name": "Quilter WealthSelect Managed Active",
        "description": "Quilter WealthSelect Managed Active is an actively managed MPS range offering 8 risk-graded portfolios (3-10) with broad multi-asset diversification across equity, fixed income, alternatives and cash. Managed by Quilter Investors with a DFM fee of 0.15% across all models.",
        "aum_bn": 25.4,
        "established": 2014,
        "headquarters": "London",
        "investment_style": "Active",
        "key_personnel": [
            {"name": "Quilter Investors", "role": "Multi-Asset Investment Management"}
        ],
        "strengths": [
            "Broad range of 8 risk-graded portfolios covering risk levels 3 to 10",
            "Competitive DFM fee of 0.15% across all models",
            "Wide platform availability across 7 major UK adviser platforms",
            "Comprehensive quarterly rebalancing with documented rationale",
            "Mapped to multiple risk rating providers (Dynamic Planner, Synaptic, EV, Finametrica)"
        ],
        "considerations": [
            "All-in costs increase with risk level (0.60% to 0.83%)",
            "Active approach introduces manager selection risk",
            "No unitised fund equivalents available",
            "Alternatives allocation has varied significantly over time"
        ],
        "regulatory_status": "FCA Authorised",
        "website": "https://www.quilter.com",
    }

    # Build MPS models
    models = []
    for t in trail:
        name = t["Model"]
        num = name.replace("Quilter WealthSelect Active Managed ", "")

        # Asset allocation from exposure sheets
        eq_total = sum((r.get(f"Portfolio {num}") or 0) for r in eq_abs)
        fi_total = sum((r.get(f"Portfolio {num}") or 0) for r in fi_abs)

        # Alt + cash from holdings
        port_holdings = [h for h in holdings if h["Model"] == f"Managed Active Portfolio {num}"]
        alt_total = sum((h.get("Portfolio Weighting (%)") or 0) for h in port_holdings if h.get("Asset Class") == "Alternative")
        cash_total = sum((h.get("Portfolio Weighting (%)") or 0) for h in port_holdings if h.get("Asset Class") == "Cash")

        # Calendar returns for this model
        cal_row = next((c for c in cal if c["Model"] == name), {})
        costs = cost_data.get(num, {"dfm": 0.15, "underlying": 0.60, "all_in": 0.75})

        # Geographic allocation from equity exposure
        geo = {}
        for r in eq_abs:
            region = r.get("Sub Asset Class", "")
            val = r.get(f"Portfolio {num}") or 0
            if val > 0:
                geo[region.lower().replace(" ", "_")] = round(val, 2)

        # Fixed income breakdown
        fi_breakdown = {}
        for r in fi_abs:
            sub = r.get("Sub Asset Class", "")
            val = r.get(f"Portfolio {num}") or 0
            if val > 0:
                fi_breakdown[sub.lower().replace(" ", "_")] = round(val, 2)

        # Underlying fund holdings
        uf = []
        for h in sorted(port_holdings, key=lambda x: x.get("Portfolio Weighting (%)") or 0, reverse=True):
            uf.append({
                "name": h.get("Name", ""),
                "isin": h.get("ISIN", ""),
                "weight": round(h.get("Portfolio Weighting (%)") or 0, 2),
                "type": h.get("Asset Class", ""),
                "sub_type": h.get("Sub Asset Class", "")
            })

        # Calendar returns dict
        calendar = {}
        for k, v in cal_row.items():
            if k != "Model" and v is not None:
                calendar[str(k)] = v

        risk = int(num)
        model = {
            "id": f"quilter-ws-active-{num}",
            "name": name,
            "provider": "Quilter Investors",
            "risk_rating": risk,
            "risk_label": f"Risk {num}",
            "asset_allocation": {
                "equity": round(eq_total, 1),
                "bonds": round(fi_total, 1),
                "alternatives": round(alt_total, 1),
                "cash": round(cash_total, 1)
            },
            "geographic_allocation": geo,
            "fixed_income_breakdown": fi_breakdown,
            "ocf": costs["all_in"],
            "cost_breakdown": costs,
            "return_1yr": t.get("1Y"),
            "return_3yr": t.get("3Y"),
            "return_5yr": t.get("5Y"),
            "return_10yr": t.get("10Y"),
            "return_ytd": t.get("YTD"),
            "return_1m": t.get("1M"),
            "return_3m": t.get("3M"),
            "return_6m": t.get("6M"),
            "calendar_returns": calendar,
            "trailing_returns": {k: v for k, v in t.items() if k != "Model"},
            "rebalancing": "Quarterly",
            "min_investment": 0,
            "platforms": platforms,
            "ethical": False,
            "decumulation_suitable": risk <= 5,
            "time_horizons": (
                ["short", "medium", "long"] if risk <= 4
                else ["medium", "long"] if risk <= 6
                else ["long"]
            ),
            "underlying_funds": uf,
            "inception_date": "2014-02-24",
        }
        models.append(model)

    # Assemble final output
    output = {
        "mps": models,
        "providers": {"Quilter Investors": provider},
        "platforms": platforms,
        "styles": ["Active"],
        "insights": [],
        "performance": {},
        "historical": {
            "portfolio_7": {
                "asset_allocation": clean(hist_aa),
                "equity_region": clean(hist_eq),
                "fixed_income": clean(hist_fi),
            }
        },
        "benchmarks": {
            "trailing": clean(benchmarks_trail),
            "calendar": clean(benchmarks_cal),
        },
        "cost_table": [{"model": m["name"], **m["cost_breakdown"]} for m in models],
    }

    return output, models


# ─── Inject into index.html ──────────────────────────────────────────

def inject_into_html(data, html_path, output_path=None):
    """Replace the const D={...}; blob in index.html with new data."""
    with open(html_path, "r") as f:
        html = f.read()

    # Find and replace the data blob
    start_marker = "const D="
    end_marker = ";\n"

    start_idx = html.index(start_marker)
    # Find the semicolon+newline after the JSON blob
    # The blob is a single line of JSON, so find the next ;\n after start
    json_start = start_idx + len(start_marker)
    # Find matching end - the JSON is one line so look for ;\n
    search_from = json_start
    depth = 0
    for i in range(search_from, len(html)):
        if html[i] == "{":
            depth += 1
        elif html[i] == "}":
            depth -= 1
            if depth == 0:
                end_idx = i + 1
                break

    old_blob = html[start_idx:end_idx + 1]  # includes the ;
    new_blob = f"const D={json.dumps(data, default=str)};"

    html = html[:start_idx] + new_blob + html[end_idx + 1:]

    out = output_path or html_path
    with open(out, "w") as f:
        f.write(html)

    print(f"✓ Injected into {out}")
    print(f"  Old blob: {len(old_blob)} chars")
    print(f"  New blob: {len(new_blob)} chars")


# ─── CLI ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Bridge Data Pipeline")
    parser.add_argument("--provider", default="quilter", help="Provider name (default: quilter)")
    parser.add_argument("--input", default="./data/", help="Input directory with Excel files")
    parser.add_argument("--output", default="./output/", help="Output directory for JSON")
    parser.add_argument("--inject", default=None, help="Path to index.html to inject data into")
    args = parser.parse_args()

    print(f"Bridge Data Pipeline")
    print(f"Provider: {args.provider}")
    print(f"Input: {args.input}")
    print()

    if args.provider == "quilter":
        data, models = build_quilter(args.input)
    else:
        print(f"Unknown provider: {args.provider}")
        print("Supported: quilter")
        sys.exit(1)

    # Print summary
    print(f"\n{'='*50}")
    print(f"SUMMARY")
    print(f"{'='*50}")
    print(f"Portfolios: {len(models)}")
    for m in models:
        aa = m["asset_allocation"]
        print(f"  {m['name']}")
        print(f"    Eq {aa['equity']}% | FI {aa['bonds']}% | Alt {aa['alternatives']}% | Cash {aa['cash']}%")
        print(f"    OCF {m['ocf']}% | 1Y {m['return_1yr']}% | 3Y {m['return_3yr']}% | 5Y {m['return_5yr']}%")
    hist = data.get("historical", {}).get("portfolio_7", {})
    print(f"Historical AA points: {len(hist.get('asset_allocation', []))}")
    print(f"Historical Equity points: {len(hist.get('equity_region', []))}")
    print(f"Historical FI points: {len(hist.get('fixed_income', []))}")
    print(f"Total fund holdings: {sum(len(m['underlying_funds']) for m in models)}")
    print(f"Benchmark rows: {len(data.get('benchmarks', {}).get('trailing', []))}")

    # Write JSON
    os.makedirs(args.output, exist_ok=True)
    json_path = os.path.join(args.output, f"{args.provider}_data.json")
    with open(json_path, "w") as f:
        json.dump(data, f, indent=2, default=str)
    print(f"\n✓ JSON saved to {json_path}")

    # Inject if requested
    if args.inject:
        inject_into_html(data, args.inject)

    print("\nDone.")


if __name__ == "__main__":
    main()
