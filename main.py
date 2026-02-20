from __future__ import annotations
"""
Bridge – API Server
B2B SaaS platform for UK financial adviser firms
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from typing import Optional
import os
from dotenv import load_dotenv
load_dotenv()

from mps_data import (
    get_all_mps, get_providers, get_provider, get_mps_by_provider,
    get_mps_by_id, get_platforms, get_investment_styles,
    get_performance_history, filter_mps, get_historical, get_benchmarks,
    get_cost_table,
)
from insights import (
    get_all_insights, get_insight_by_id, get_insights_by_category,
    get_insight_categories, search_insights,
)

app = FastAPI(
    title="Bridge",
    description="Independent MPS research & oversight platform for UK financial advisers",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


def safe_avg(values):
    """Average that handles None values."""
    clean = [v for v in values if v is not None]
    return round(sum(clean) / len(clean), 2) if clean else 0


# ─── Selection Module ──────────────────────────────────────────────────

@app.get("/api/selection/filters")
async def get_filter_options():
    all_mps = get_all_mps()
    risk_ratings = sorted(set(m["risk_rating"] for m in all_mps))
    providers = sorted(set(m["provider"] for m in all_mps))
    # Collect unique fund selection styles from provider data
    all_providers = get_providers()
    styles = sorted(set(p.get("investment_style", "") for p in all_providers.values() if p.get("investment_style")))
    # Collect unique risk rating providers
    rrp = set()
    for prov in all_providers.values():
        for r in prov.get("risk_rating_providers", []):
            rrp.add(r)
    return {
        "platforms": get_platforms(),
        "providers": providers,
        "investment_styles": styles,
        "risk_ratings": risk_ratings,
        "risk_range": {"min": min(risk_ratings), "max": max(risk_ratings)} if risk_ratings else {},
        "risk_rating_providers": sorted(rrp),
    }


@app.get("/api/selection/mps")
async def search_mps(
    risk_min: int = Query(1, ge=1, le=10),
    risk_max: int = Query(10, ge=1, le=10),
    platforms: Optional[str] = None,
    providers: Optional[str] = None,
    ethical_only: bool = False,
    decumulation: bool = False,
    time_horizon: Optional[str] = None,
    max_ocf: Optional[float] = None,
):
    platform_list = platforms.split(",") if platforms else None
    provider_list = providers.split(",") if providers else None

    results = filter_mps(
        risk_min=risk_min, risk_max=risk_max,
        platforms=platform_list, providers=provider_list,
        ethical_only=ethical_only, decumulation=decumulation,
        time_horizon=time_horizon, ocf_max=max_ocf,
    )
    return {"count": len(results), "mps": results}


# ─── Analysis Module ───────────────────────────────────────────────────

@app.get("/api/providers")
async def list_providers():
    providers = get_providers()
    result = []
    for name, data in providers.items():
        portfolios = get_mps_by_provider(name)
        result.append({
            **data,
            "portfolio_count": len(portfolios),
            "risk_range": f"{min(p['risk_rating'] for p in portfolios)}-{max(p['risk_rating'] for p in portfolios)}" if portfolios else "N/A",
            "ocf_range": f"{min(p['ocf'] for p in portfolios):.2f}-{max(p['ocf'] for p in portfolios):.2f}" if portfolios else "N/A",
        })
    return {"providers": result}


@app.get("/api/providers/{provider_id}")
async def get_provider_detail(provider_id: str):
    provider = None
    for name, data in get_providers().items():
        if data["id"] == provider_id:
            provider = data
            break

    if not provider:
        raise HTTPException(404, "Provider not found")

    portfolios = get_mps_by_provider(provider["name"])

    return {
        "provider": provider,
        "portfolios": portfolios,
        "analytics": {
            "avg_ocf": safe_avg([p["ocf"] for p in portfolios]),
            "avg_return_1yr": safe_avg([p.get("return_1yr") for p in portfolios]),
            "avg_return_3yr": safe_avg([p.get("return_3yr") for p in portfolios]),
            "avg_return_5yr": safe_avg([p.get("return_5yr") for p in portfolios]),
            "platform_count": len(set(p for port in portfolios for p in port.get("platforms", []))),
        },
    }
@app.get("/api/mps/{mps_id}")
async def get_mps_detail(mps_id: str):
    mps = get_mps_by_id(mps_id)
    if not mps:
        raise HTTPException(404, "MPS not found")

    provider = get_provider(mps["provider"])
    history = get_performance_history(mps_id, months=36)

    peers = [m for m in get_all_mps()
             if m["risk_rating"] == mps["risk_rating"] and m["id"] != mps_id]

    return {
        "mps": mps,
        "provider": provider,
        "performance_history": history,
        "peer_comparison": {
            "count": len(peers),
            "peers": peers,
            "avg_ocf": safe_avg([p["ocf"] for p in peers]),
            "avg_return_1yr": safe_avg([p.get("return_1yr") for p in peers]),
            "avg_return_3yr": safe_avg([p.get("return_3yr") for p in peers]),
        },
    }


@app.get("/api/mps/{mps_id}/performance")
async def get_mps_performance(mps_id: str, months: int = Query(36, ge=6, le=60)):
    mps = get_mps_by_id(mps_id)
    if not mps:
        raise HTTPException(404, "MPS not found")
    return {"mps_id": mps_id, "history": get_performance_history(mps_id, months)}


@app.get("/api/compare")
async def compare_mps(ids: str = Query(..., description="Comma-separated MPS IDs")):
    id_list = [i.strip() for i in ids.split(",")]
    results = [get_mps_by_id(i) for i in id_list if get_mps_by_id(i)]

    if not results:
        raise HTTPException(404, "No valid MPS found")

    return {
        "count": len(results),
        "mps": results,
    }


# ─── Historical & Benchmarks ──────────────────────────────────────────

@app.get("/api/historical/{key}")
async def get_historical_data(key: str):
    data = get_historical(key)
    if not data:
        raise HTTPException(404, "Historical data not found")
    return data


@app.get("/api/benchmarks")
async def get_benchmark_data():
    return get_benchmarks()


@app.get("/api/costs")
async def get_costs():
    return {"costs": get_cost_table()}


# ─── Insights Module ──────────────────────────────────────────────────

@app.get("/api/insights")
async def list_insights(
    category: Optional[str] = None,
    search: Optional[str] = None,
):
    if search:
        results = search_insights(search)
    elif category:
        results = get_insights_by_category(category)
    else:
        results = get_all_insights()

    return {
        "count": len(results),
        "insights": results,
        "categories": get_insight_categories(),
    }


@app.get("/api/insights/{insight_id}")
async def get_insight_detail(insight_id: str):
    insight = get_insight_by_id(insight_id)
    if not insight:
        raise HTTPException(404, "Insight not found")
    return {"insight": insight}


# ─── Dashboard ─────────────────────────────────────────────────────────

@app.get("/api/dashboard")
async def get_dashboard():
    all_mps = get_all_mps()
    providers = get_providers()
    insights = get_all_insights()

    return {
        "stats": {
            "total_mps": len(all_mps),
            "total_providers": len(providers),
            "total_platforms": len(get_platforms()),
            "latest_insights": len(insights),
            "market_aum_bn": sum(p.get("aum_bn", 0) for p in providers.values()),
        },
        "recent_insights": insights[:3],
        "provider_overview": [
            {
                "name": name,
                "aum_bn": data.get("aum_bn", 0),
                "style": data.get("investment_style", ""),
                "portfolio_count": len(get_mps_by_provider(name)),
            }
            for name, data in providers.items()
        ],
        "risk_distribution": {
            str(r): len([m for m in all_mps if m["risk_rating"] == r])
            for r in sorted(set(m["risk_rating"] for m in all_mps))
        },
    }


@app.get("/api/health")
async def health():
    return {"status": "healthy", "version": "1.0.0", "platform": "Bridge"}


# ─── Feedback ──────────────────────────────────────────────────────────


FEEDBACK_EMAIL = os.environ.get("FEEDBACK_EMAIL", "")
SMTP_HOST = os.environ.get("SMTP_HOST", "")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASS = os.environ.get("SMTP_PASS", "")

@app.post("/api/feedback")
async def submit_feedback(body: dict):
    subject = body.get("subject", "").strip()
    message = body.get("message", "").strip()
    if not subject or not message:
        raise HTTPException(400, "Subject and message are required")

    # If SMTP is configured, send email
    if SMTP_HOST and SMTP_USER:
        import smtplib
        from email.mime.text import MIMEText
        try:
            msg = MIMEText(message, "plain")
            msg["Subject"] = f"[Bridge Feedback] {subject}"
            msg["From"] = SMTP_USER
            msg["To"] = FEEDBACK_EMAIL
            with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
                server.starttls()
                server.login(SMTP_USER, SMTP_PASS)
                server.send_message(msg)
        except Exception as e:
            print(f"SMTP error: {e}")
            raise HTTPException(500, "Failed to send email. Please try again later.")
    else:
        # Log to console if SMTP not configured
        print(f"\n--- FEEDBACK ---")
        print(f"Subject: {subject}")
        print(f"Message: {message}")
        print(f"(Configure SMTP_HOST, SMTP_USER, SMTP_PASS env vars to send via email)")
        print(f"----------------\n")

    return {"status": "ok", "message": "Feedback received"}


# ─── Consumer Duty Export ────────────────────────────────────────────

@app.post("/api/export/consumer-duty")
async def export_consumer_duty(data: dict):
    """Generate a formatted .docx Consumer Duty Oversight Report."""
    from docx import Document
    from docx.shared import Inches, Pt, Cm, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT
    import io

    doc = Document()

    # Page margins
    for section in doc.sections:
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.5)

    # Styles
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(11)
    style.font.color.rgb = RGBColor(0x1A, 0x1F, 0x2E)
    style.paragraph_format.space_after = Pt(6)
    style.paragraph_format.line_spacing = 1.15

    # Title
    title = doc.add_heading("Consumer Duty Oversight Report", level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    for run in title.runs:
        run.font.size = Pt(22)
        run.font.color.rgb = RGBColor(0x1A, 0x1F, 0x2E)

    doc.add_paragraph("")

    # Report Details table
    details = data.get("details", {})
    if details:
        detail_heading = doc.add_heading("Report Details", level=2)
        for run in detail_heading.runs:
            run.font.color.rgb = RGBColor(0x25, 0x63, 0xEB)
            run.font.size = Pt(14)

        table = doc.add_table(rows=0, cols=2)
        table.style = "Light Grid Accent 1"
        table.alignment = WD_TABLE_ALIGNMENT.LEFT

        for key, val in details.items():
            row = table.add_row()
            cell_key = row.cells[0]
            cell_val = row.cells[1]
            cell_key.text = key
            cell_val.text = val
            for paragraph in cell_key.paragraphs:
                for run in paragraph.runs:
                    run.font.bold = True
                    run.font.size = Pt(10.5)
            for paragraph in cell_val.paragraphs:
                for run in paragraph.runs:
                    run.font.size = Pt(10.5)

        doc.add_paragraph("")

    # Content sections
    sections = data.get("sections", [])
    for sec in sections:
        sec_title = sec.get("title", "")
        sec_content = sec.get("content", "")

        heading = doc.add_heading(sec_title, level=2)
        for run in heading.runs:
            run.font.color.rgb = RGBColor(0x25, 0x63, 0xEB)
            run.font.size = Pt(14)

        # Split content into paragraphs
        for para_text in sec_content.split("\n"):
            para_text = para_text.strip()
            if para_text:
                p = doc.add_paragraph(para_text)
                p.paragraph_format.space_after = Pt(4)

        doc.add_paragraph("")

    # Footer
    doc.add_paragraph("")
    footer_line = doc.add_paragraph()
    footer_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = footer_line.add_run("Generated by Bridge – Independent MPS Research & Oversight")
    run.font.size = Pt(9)
    run.font.color.rgb = RGBColor(0x6B, 0x72, 0x80)
    run.font.italic = True

    # Save to buffer
    buffer = io.BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    from fastapi.responses import StreamingResponse
    return StreamingResponse(
        buffer,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": "attachment; filename=Consumer_Duty_Oversight_Report.docx"},
    )


# ─── Serve Frontend ───────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    html_path = os.path.join(os.path.dirname(__file__), "index.html")
    if os.path.exists(html_path):
        with open(html_path, "r") as f:
            return f.read()
    return "<h1>Bridge</h1><p>Frontend not found. See <a href='/docs'>/docs</a></p>"


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
