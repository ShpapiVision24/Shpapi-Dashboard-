import streamlit as st
import requests
import pandas as pd
import json
import io
import os
from datetime import date, timedelta

try:
    from fpdf import FPDF
    FPDF_OK = True
except ImportError:
    FPDF_OK = False

ASSETS    = os.path.join(os.path.dirname(__file__), "..", "assets")
LOGO_CROP = os.path.join(ASSETS, "logo_cropped.png")

BG      = "#0a1628"
SURFACE = "#0e1f3c"
BORDER  = "rgba(255,255,255,0.08)"
T1      = "#ffffff"
T2      = "rgba(255,255,255,0.65)"
T3      = "rgba(255,255,255,0.38)"
BLUE    = "#3b82f6"
GREEN   = "#22c55e"
ORANGE  = "#f59e0b"
PURPLE  = "#a855f7"
PINK    = "#ec4899"

META_ACCOUNT = "act_8429913163714900"

st.set_page_config(page_title="Shpapi · Reports", layout="wide", initial_sidebar_state="collapsed")

from auth import check_password
if not check_password():
    st.stop()

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
*, *::before, *::after {{ font-family: 'Inter', sans-serif !important; box-sizing: border-box; }}
html, body, .stApp {{ background: {BG} !important; color: {T1}; }}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding: 1.5rem 3rem 4rem 3rem !important; max-width: 100% !important; }}
section[data-testid="stSidebar"] {{ display: none !important; }}
[data-testid="stSidebarNav"], [data-testid="stSidebarNavItems"],
div[data-testid="stPageNavContainer"], nav[data-testid="stSidebarNav"] {{ display: none !important; }}
::-webkit-scrollbar {{ width: 6px; background: transparent; }}
::-webkit-scrollbar-thumb {{ background: rgba(255,255,255,0.15); border-radius: 3px; }}
.kpi-grid {{ display: grid; grid-template-columns: repeat(4,1fr); gap: 1rem; margin-bottom: 1rem; }}
.kpi {{ background: {SURFACE}; border: 1px solid {BORDER}; border-radius: 12px; padding: 1.4rem 1.6rem 1.3rem; }}
.kpi-label {{ font-size: 0.65rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1.8px; color: {T3}; margin-bottom: 0.65rem; }}
.kpi-value {{ font-size: 2rem; font-weight: 700; color: #ffffff; letter-spacing: -1px; line-height: 1; }}
.kpi-sub {{ font-size: 0.72rem; color: {T2}; margin-top: 0.4rem; }}
.section {{ font-size: 0.62rem; font-weight: 600; text-transform: uppercase; letter-spacing: 2.5px; color: {T3}; margin: 2rem 0 0.9rem 0; display: flex; align-items: center; gap: 1rem; }}
.section::after {{ content: ''; flex: 1; height: 1px; background: {BORDER}; }}
.stButton > button {{
    background: transparent !important; border: none !important; box-shadow: none !important;
    outline: none !important; color: {T2} !important; font-weight: 600 !important;
    font-size: 0.78rem !important; padding: 0.35rem 0.85rem !important;
    min-height: 0 !important; width: auto !important; border-radius: 6px !important;
}}
.stButton > button:hover {{ background: rgba(37,99,235,0.08) !important; color: {BLUE} !important; border: none !important; }}
div[data-testid="stPageLink"] {{ border: none !important; background: none !important; box-shadow: none !important; padding: 0 !important; margin: 0 !important; padding-top: 1rem !important; }}
a[data-testid="stPageLink-NavLink"] {{ color: {T2} !important; font-weight: 500 !important; font-size: 0.70rem !important; text-decoration: none !important; padding: 0.3rem 0.75rem !important; border-radius: 6px !important; background: transparent !important; border: none !important; display: inline-block !important; }}
a[data-testid="stPageLink-NavLink"]:hover {{ background: rgba(59,130,246,0.15) !important; color: {BLUE} !important; }}
a[data-testid="stPageLink-NavLink"] svg {{ display: none !important; }}
button[kind="primaryFormSubmit"], button[kind="primary"] {{ background: {BLUE} !important; border: none !important; border-radius: 8px !important; color: #fff !important; font-weight: 700 !important; font-size: 0.85rem !important; }}
</style>
""", unsafe_allow_html=True)

# ── Nav ───────────────────────────────────────────────────────────────────────
_c_logo, _c_h, _c_m, _c_s, _c_g, _c_qb, _c_ig, _c_rp, _ = st.columns([1.5, 1, 1, 1, 1.2, 1.3, 1.0, 1.0, 0.6])
with _c_logo:
    if os.path.exists(LOGO_CROP):
        st.image(LOGO_CROP, width=90)
with _c_h:
    st.page_link("app.py", label="Home")
with _c_m:
    st.page_link("pages/1_Meta_Ads.py", label="Meta Ads")
with _c_s:
    st.page_link("pages/2_Shopify.py", label="Shopify")
with _c_g:
    st.page_link("pages/3_Google_Ads.py", label="Google Ads")
with _c_qb:
    st.page_link("pages/4_QuickBooks.py", label="QuickBooks")
with _c_ig:
    st.page_link("pages/5_Instagram.py", label="Instagram")
with _c_rp:
    st.markdown(f'<div style="padding-top:1.1rem;"><span style="padding:0.35rem 0.9rem;border-radius:6px;font-size:0.8rem;font-weight:700;color:{PURPLE};background:rgba(168,85,247,0.18);white-space:nowrap;">Reports</span></div>', unsafe_allow_html=True)
st.markdown(f'<div style="border-top:1px solid {BORDER};margin:0.5rem 0 2rem;"></div>', unsafe_allow_html=True)

st.markdown(f"""
<div style="margin-bottom:2rem;">
  <div style="font-size:1.4rem;font-weight:700;color:{T1};letter-spacing:-0.5px;">Business Report</div>
  <div style="font-size:0.7rem;font-weight:500;text-transform:uppercase;letter-spacing:2px;color:{T3};margin-top:0.3rem;">Shpapi &nbsp;·&nbsp; Analytics &amp; AI Business Analysis</div>
</div>
""", unsafe_allow_html=True)

# ── Period selector ───────────────────────────────────────────────────────────
today    = date.today()
cur_q    = (today.month - 1) // 3 + 1
q_labels = ["Q1  (Jan – Mar)", "Q2  (Apr – Jun)", "Q3  (Jul – Sep)", "Q4  (Oct – Dec)"]

sc1, sc2, sc3, _ = st.columns([1.1, 1, 1.4, 2.5])
with sc1:
    period_type = st.selectbox("Period", ["All Time", "By Quarter"], index=0, label_visibility="collapsed")
with sc2:
    sel_year = st.selectbox("Year", [2026, 2025, 2024], index=0,
                            label_visibility="collapsed",
                            disabled=(period_type == "All Time"))
with sc3:
    sel_q_label = st.selectbox("Quarter", q_labels, index=cur_q - 1,
                               label_visibility="collapsed",
                               disabled=(period_type == "All Time"))

all_time = (period_type == "All Time")

if all_time:
    start_str = "2020-01-01"
    end_str   = today.strftime("%Y-%m-%d")
    q_short   = "All Time"
    period_label = f"All available data through {today.strftime('%B %d, %Y')}"
else:
    q_idx  = q_labels.index(sel_q_label)
    q_num  = q_idx + 1
    _QR    = {1: (1,1,3,31), 2: (4,1,6,30), 3: (7,1,9,30), 4: (10,1,12,31)}
    sm, sd, em, ed = _QR[q_num]
    q_start  = date(sel_year, sm, sd)
    q_end    = min(date(sel_year, em, ed), today)
    start_str = q_start.strftime("%Y-%m-%d")
    end_str   = q_end.strftime("%Y-%m-%d")
    q_short   = f"Q{q_num} {sel_year}"
    period_label = f"{q_start.strftime('%B %d, %Y')} → {q_end.strftime('%B %d, %Y')}"

st.markdown(f'<div style="font-size:0.75rem;color:{T3};margin:-0.5rem 0 1.5rem;">{period_label}</div>', unsafe_allow_html=True)

# ── Secrets ───────────────────────────────────────────────────────────────────
ACCESS_TOKEN    = st.secrets.get("META_ACCESS_TOKEN", "")
SHOPIFY_TOKEN   = st.secrets.get("SHOPIFY_TOKEN", "")
SHOP_URL        = st.secrets.get("SHOP_URL", "")
SH_HEADERS      = {"X-Shopify-Access-Token": SHOPIFY_TOKEN, "Content-Type": "application/json"}

# ── Fetch functions ───────────────────────────────────────────────────────────
def _meta_fetch(params_extra):
    if not ACCESS_TOKEN:
        return [], None
    try:
        rows, url = [], f"https://graph.facebook.com/v19.0/{META_ACCOUNT}/insights"
        params = {
            "fields": "campaign_name,spend,reach,impressions,clicks,actions,action_values",
            "level": "campaign",
            "limit": 100,
            "access_token": ACCESS_TOKEN,
            **params_extra,
        }
        while url:
            r    = requests.get(url, params=params, timeout=15)
            data = r.json()
            if "error" in data:
                return [], data["error"].get("message", "Meta API error")
            rows.extend(data.get("data", []))
            url    = data.get("paging", {}).get("next")
            params = {}
        return rows, None
    except Exception as e:
        return [], str(e)

@st.cache_data(ttl=300, show_spinner=False)
def fetch_meta_alltime():
    return _meta_fetch({"date_preset": "maximum"})

@st.cache_data(ttl=300, show_spinner=False)
def fetch_meta_q(start_str, end_str):
    return _meta_fetch({"time_range": json.dumps({"since": start_str, "until": end_str})})

@st.cache_data(ttl=300, show_spinner=False)
def fetch_google_q(start_str, end_str):
    try:
        from google.ads.googleads.client import GoogleAdsClient
        cfg = st.secrets["google_ads"]
        config = {
            "developer_token": cfg["developer_token"],
            "client_id": cfg["client_id"],
            "client_secret": cfg["client_secret"],
            "refresh_token": cfg["refresh_token"],
            "login_customer_id": cfg["client_customer_id"].replace("-", ""),
            "use_proto_plus": True,
        }
        client     = GoogleAdsClient.load_from_dict(config)
        ga_service = client.get_service("GoogleAdsService")
        customer_id = cfg["client_customer_id"].replace("-", "")
        query = f"""
            SELECT campaign.name, metrics.impressions, metrics.clicks,
                   metrics.cost_micros, metrics.conversions
            FROM campaign
            WHERE segments.date BETWEEN '{start_str}' AND '{end_str}'
              AND campaign.status != 'REMOVED'
        """
        rows = []
        for row in ga_service.search(customer_id=customer_id, query=query):
            rows.append({
                "Campaign":    row.campaign.name,
                "Impressions": row.metrics.impressions,
                "Clicks":      row.metrics.clicks,
                "Cost":        row.metrics.cost_micros / 1_000_000,
                "Conversions": row.metrics.conversions,
            })
        return pd.DataFrame(rows) if rows else pd.DataFrame(), None
    except Exception as e:
        return pd.DataFrame(), str(e)

@st.cache_data(ttl=300, show_spinner=False)
def fetch_shopify_q(start_str, end_str):
    if not SHOPIFY_TOKEN or not SHOP_URL:
        return [], None
    try:
        orders, url = [], f"{SHOP_URL}/admin/api/2024-01/orders.json"
        params = {
            "status": "any", "limit": 250,
            "fields": "id,created_at,total_price,financial_status,line_items",
            "created_at_min": f"{start_str}T00:00:00Z",
            "created_at_max": f"{end_str}T23:59:59Z",
        }
        while url:
            r    = requests.get(url, headers=SH_HEADERS, params=params, timeout=20)
            data = r.json()
            orders.extend(data.get("orders", []))
            link = r.headers.get("Link", "")
            if 'rel="next"' in link:
                parts     = [p.strip() for p in link.split(",")]
                next_part = next((p for p in parts if 'rel="next"' in p), None)
                url       = next_part.split(";")[0].strip().strip("<>") if next_part else None
                params    = {}
            else:
                url = None
        return orders, None
    except Exception as e:
        return [], str(e)

# ── Load data ─────────────────────────────────────────────────────────────────
with st.spinner("Loading data for all platforms…"):
    if all_time:
        meta_rows, meta_err = fetch_meta_alltime()
    else:
        meta_rows, meta_err = fetch_meta_q(start_str, end_str)
    google_df,   google_err = fetch_google_q(start_str, end_str)
    shopify_raw, sh_err     = fetch_shopify_q(start_str, end_str)

# ── Compute metrics ───────────────────────────────────────────────────────────
paid_orders = [o for o in shopify_raw if o.get("financial_status") == "paid"]
sh_revenue  = sum(float(o.get("total_price", 0)) for o in paid_orders)
sh_orders   = len(paid_orders)
sh_aov      = sh_revenue / sh_orders if sh_orders else 0

def _act(actions, atype):
    return sum(int(float(a["value"])) for a in (actions or []) if a.get("action_type") == atype)

meta_spend       = sum(float(r.get("spend", 0)) for r in meta_rows)
meta_reach       = sum(int(r.get("reach", 0)) for r in meta_rows)
meta_impressions = sum(int(r.get("impressions", 0)) for r in meta_rows)
meta_clicks      = sum(int(r.get("clicks", 0)) for r in meta_rows)
meta_purchases   = sum(_act(r.get("actions", []), "purchase") for r in meta_rows)
meta_conv_val    = sum(
    sum(float(a["value"]) for a in (r.get("action_values") or []) if a.get("action_type") == "purchase")
    for r in meta_rows
)

g_ok          = google_df is not None and not google_df.empty
g_spend       = float(google_df["Cost"].sum())        if g_ok else 0.0
g_clicks      = int(google_df["Clicks"].sum())        if g_ok else 0
g_impressions = int(google_df["Impressions"].sum())   if g_ok else 0
g_conversions = float(google_df["Conversions"].sum()) if g_ok else 0.0

total_ad_spend = meta_spend + g_spend
roas           = sh_revenue / total_ad_spend if total_ad_spend else 0.0
meta_roas      = meta_conv_val / meta_spend if meta_spend else 0.0

# ── KPI grid ──────────────────────────────────────────────────────────────────
st.markdown(f'<div class="section">{q_short} &nbsp;·&nbsp; Cross-Platform Summary</div>', unsafe_allow_html=True)

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi" style="border-top:3px solid {GREEN};">
    <div class="kpi-label">Shopify Revenue</div>
    <div class="kpi-value">${sh_revenue:,.2f}</div>
    <div class="kpi-sub">{sh_orders} paid orders &nbsp;·&nbsp; AOV ${sh_aov:,.2f}</div>
  </div>
  <div class="kpi" style="border-top:3px solid {ORANGE};">
    <div class="kpi-label">Total Ad Spend</div>
    <div class="kpi-value">${total_ad_spend:,.2f}</div>
    <div class="kpi-sub">Meta ${meta_spend:,.2f} &nbsp;·&nbsp; Google ${g_spend:,.2f}</div>
  </div>
  <div class="kpi" style="border-top:3px solid {BLUE};">
    <div class="kpi-label">Overall ROAS</div>
    <div class="kpi-value">{roas:.2f}x</div>
    <div class="kpi-sub">Revenue per $1 of ad spend</div>
  </div>
  <div class="kpi" style="border-top:3px solid {PURPLE};">
    <div class="kpi-label">Combined Reach</div>
    <div class="kpi-value">{(meta_reach + g_impressions):,}</div>
    <div class="kpi-sub">Meta unique reach + Google impressions</div>
  </div>
</div>
<div class="kpi-grid">
  <div class="kpi">
    <div class="kpi-label">Meta Impressions</div>
    <div class="kpi-value">{meta_impressions:,}</div>
    <div class="kpi-sub">Unique reach: {meta_reach:,}</div>
  </div>
  <div class="kpi">
    <div class="kpi-label">Meta Link Clicks</div>
    <div class="kpi-value">{meta_clicks:,}</div>
    <div class="kpi-sub">Purchases: {meta_purchases} &nbsp;·&nbsp; ROAS {meta_roas:.2f}x</div>
  </div>
  <div class="kpi">
    <div class="kpi-label">Google Clicks</div>
    <div class="kpi-value">{g_clicks:,}</div>
    <div class="kpi-sub">Impressions: {g_impressions:,}</div>
  </div>
  <div class="kpi">
    <div class="kpi-label">Google Conversions</div>
    <div class="kpi-value">{g_conversions:.1f}</div>
    <div class="kpi-sub">CPC: ${(g_spend/g_clicks if g_clicks else 0):.2f}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# Platform warnings
for label, err in [("Shopify", sh_err), ("Meta Ads", meta_err), ("Google Ads", google_err)]:
    if err and "test" not in str(err).lower() and "basic" not in str(err).lower():
        st.warning(f"{label}: {err}")

# ── AI Summary ────────────────────────────────────────────────────────────────
st.markdown(f'<div class="section">AI Business Analysis</div>', unsafe_allow_html=True)

ss_key = f"ai_{q_short.replace(' ','_')}"

if st.button("Generate Full Business Analysis", type="primary"):
    api_key = st.secrets.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        st.error("Add ANTHROPIC_API_KEY to your Streamlit secrets to enable AI summaries.")
    else:
        ctx = f"""Business: Shpapi — sunglasses and clothing brand.
Quarter: {q_short}  ({q_start.strftime('%b %d')} – {q_end.strftime('%b %d, %Y')})

SHOPIFY:
  Revenue: ${sh_revenue:,.2f}
  Paid Orders: {sh_orders}
  Average Order Value: ${sh_aov:,.2f}

META ADS (Instagram / Facebook Boosts):
  Ad Spend: ${meta_spend:,.2f}
  Unique Reach: {meta_reach:,}
  Impressions: {meta_impressions:,}
  Link Clicks: {meta_clicks:,}
  Attributed Purchases: {meta_purchases}
  Attributed Revenue: ${meta_conv_val:,.2f}
  Meta ROAS: {meta_roas:.2f}x

GOOGLE ADS:
  Ad Spend: ${g_spend:,.2f}
  Impressions: {g_impressions:,}
  Clicks: {g_clicks:,}
  Conversions: {g_conversions:.1f}
  Avg CPC: ${(g_spend/g_clicks if g_clicks else 0):.2f}

COMBINED:
  Total Ad Spend: ${total_ad_spend:,.2f}
  Blended ROAS: {roas:.2f}x"""

        with st.spinner("Generating AI summary…"):
            try:
                import anthropic as _ant
                client = _ant.Anthropic(api_key=api_key)
                msg = client.messages.create(
                    model="claude-sonnet-5",
                    max_tokens=3500,
                    messages=[{
                        "role": "user",
                        "content": f"""You are a seasoned brand strategist and growth advisor for Shpapi — a sunglasses and clothing brand. You know this brand deeply: it sells lifestyle products, competes on aesthetics and identity, and relies on paid social (Meta/Instagram) and Google Ads to drive Shopify revenue.

Here is the data for {q_short}:
{ctx}

Write a comprehensive, honest, and strategic business report. This is NOT a data dump — it's a real narrative about where the business stands and what the founder needs to do. Write it like a trusted advisor speaking directly to the founder, not a consultant writing a corporate report.

Use exactly these seven sections with ## headers:

## Where We Are Right Now
3-4 sentences giving a clear, honest picture of the business's current state. Go beyond the numbers — what does this data tell you about the brand's momentum, trajectory, and market position? Is the brand gaining ground, holding steady, or losing traction? What's the single most important thing to understand about this quarter?

## What's Working
3-4 bullet points on genuine strengths. For each one, cite the specific number AND explain what it actually means for the business (not just that it's a good number, but why it matters strategically). If a metric is strong, say what's driving it.

## What Needs to Improve
4-5 bullet points on real problems, gaps, or inefficiencies. Be direct and specific. For each issue, name the metric, diagnose why it's likely happening, and explain what's at stake if it doesn't get fixed. Don't soften criticism.

## Next Steps (30–60 Days)
5 concrete, time-bound actions the founder should take in the next 30-60 days. Each should be specific enough to act on immediately — not "improve your ads" but "test 3 new creative hooks on Instagram Stories targeting 25-34 female fashion buyers, with a $10/day budget per variation for 7 days." Rank by urgency.

## Ideas & Solutions
This is the most important section. Give 5-6 creative, specific ideas tailored to a fashion/sunglasses brand at this stage. Think across: creative strategy, audience targeting, product bundling, email/retention, seasonal campaigns, influencer/UGC, landing page CRO, or anything else relevant. Each idea should explain what to do, why it fits Shpapi specifically, and what outcome to expect. Be creative — don't just repeat the obvious.

## Improvement Plan
3 structural improvements to how the business runs its marketing and analytics. These are bigger-picture changes (e.g., attribution setup, creative testing cadence, budget allocation framework, retention vs. acquisition balance). Explain the current problem and the specific fix.

## Next Quarter Priority
1 bold paragraph: the single most important thing Shpapi should focus on next quarter and why. Make a clear recommendation. Don't hedge.

Tone: Direct. Confident. Like a smart friend who happens to be a great strategist. No filler. No corporate speak. Use the actual numbers throughout to back every claim."""
                    }],
                )
                st.session_state[ss_key] = msg.content[0].text
            except Exception as e:
                st.error(f"AI generation failed: {e}")

if ss_key in st.session_state:
    ai_text = st.session_state[ss_key]

    st.markdown(f"""
    <style>
    .report-body h2 {{
        font-size: 0.78rem !important; font-weight: 700 !important;
        text-transform: uppercase !important; letter-spacing: 2px !important;
        color: {BLUE} !important; margin: 1.8rem 0 0.6rem !important;
        border-bottom: 1px solid rgba(59,130,246,0.2); padding-bottom: 0.4rem;
    }}
    .report-body p {{ font-size: 0.88rem !important; color: rgba(255,255,255,0.82) !important; line-height: 1.75 !important; margin: 0 0 0.6rem !important; }}
    .report-body ul {{ margin: 0.4rem 0 0.8rem 1.2rem !important; padding: 0 !important; }}
    .report-body li {{ font-size: 0.86rem !important; color: rgba(255,255,255,0.78) !important; line-height: 1.7 !important; margin-bottom: 0.5rem !important; }}
    .report-body strong {{ color: #ffffff !important; font-weight: 700 !important; }}
    </style>
    <div class="report-body" style="background:{SURFACE};border:1px solid {BORDER};border-radius:14px;padding:2rem 2.5rem;">
    """, unsafe_allow_html=True)

    st.markdown(ai_text)
    st.markdown("</div>", unsafe_allow_html=True)

    # ── PDF Export ─────────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)

    if not FPDF_OK:
        st.info("PDF export requires `fpdf2`. It will be available after the next deploy.")
    else:
        def _build_pdf():
            pdf = FPDF()
            pdf.add_page()
            pdf.set_margins(18, 18, 18)
            pdf.set_auto_page_break(auto=True, margin=22)

            # ── Header bar ─────────────────────────────────────────────────────
            pdf.set_fill_color(10, 22, 40)
            pdf.rect(0, 0, 210, 40, "F")
            pdf.set_font("Helvetica", "B", 22)
            pdf.set_text_color(255, 255, 255)
            pdf.set_xy(0, 9)
            pdf.cell(210, 10, "SHPAPI", align="C")
            pdf.set_font("Helvetica", "", 8)
            pdf.set_text_color(150, 165, 190)
            pdf.set_xy(0, 22)
            pdf.cell(210, 6,
                     f"Business Analytics Report  —  {q_short}  —  "
                     f"{q_start.strftime('%b %d, %Y')} to {q_end.strftime('%b %d, %Y')}",
                     align="C")
            pdf.set_y(48)

            # ── KPI boxes ─────────────────────────────────────────────────────
            def _section(title):
                pdf.set_font("Helvetica", "B", 9)
                pdf.set_text_color(80, 100, 140)
                pdf.cell(0, 6, title, ln=True)
                pdf.set_draw_color(59, 130, 246)
                pdf.line(18, pdf.get_y(), 192, pdf.get_y())
                pdf.ln(4)

            def _kpi_box(x, y, w, h, label, value, sub, rgb):
                pdf.set_fill_color(14, 31, 60)
                pdf.set_draw_color(30, 50, 80)
                pdf.rect(x, y, w, h, "FD")
                pdf.set_fill_color(*rgb)
                pdf.rect(x, y, w, 1.5, "F")
                pdf.set_font("Helvetica", "", 6)
                pdf.set_text_color(120, 140, 170)
                pdf.set_xy(x + 3, y + 4)
                pdf.cell(w - 6, 4, label.upper())
                pdf.set_font("Helvetica", "B", 13)
                pdf.set_text_color(255, 255, 255)
                pdf.set_xy(x + 3, y + 9)
                pdf.cell(w - 6, 7, value)
                if sub:
                    pdf.set_font("Helvetica", "", 6)
                    pdf.set_text_color(120, 140, 170)
                    pdf.set_xy(x + 3, y + 18)
                    pdf.cell(w - 6, 4, sub)

            _section("CROSS-PLATFORM SUMMARY")

            cw, gap = 82, 9
            x1, x2 = 18, 18 + cw + gap
            rh, rg  = 28, 5
            y0 = pdf.get_y()

            _kpi_box(x1, y0,           cw, rh, "Shopify Revenue",  f"${sh_revenue:,.2f}",       f"{sh_orders} orders · AOV ${sh_aov:.2f}", (34, 197, 94))
            _kpi_box(x2, y0,           cw, rh, "Total Ad Spend",   f"${total_ad_spend:,.2f}",   f"Meta ${meta_spend:.2f} · Google ${g_spend:.2f}", (245, 158, 11))
            _kpi_box(x1, y0+rh+rg,     cw, rh, "Blended ROAS",     f"{roas:.2f}x",              "Revenue per $1 of ad spend", (59, 130, 246))
            _kpi_box(x2, y0+rh+rg,     cw, rh, "Combined Reach",   f"{(meta_reach+g_impressions):,}", "Meta reach + Google impressions", (168, 85, 247))

            pdf.set_y(y0 + 2*(rh+rg) + 8)

            # Second row of detail boxes
            tw = 172 / 4 - 3
            detail = [
                ("Meta Impressions",  f"{meta_impressions:,}",   f"Reach {meta_reach:,}",        (236, 72, 153)),
                ("Meta Clicks",       f"{meta_clicks:,}",         f"Purchases {meta_purchases}",  (236, 72, 153)),
                ("Google Clicks",     f"{g_clicks:,}",            f"Impr. {g_impressions:,}",     (59, 130, 246)),
                ("Google Conv.",      f"{g_conversions:.1f}",     f"CPC ${(g_spend/g_clicks if g_clicks else 0):.2f}", (59, 130, 246)),
            ]
            dx = 18
            for label, val, sub, rgb in detail:
                _kpi_box(dx, pdf.get_y(), tw, 24, label, val, sub, rgb)
                dx += tw + 4
            pdf.set_y(pdf.get_y() + 32)

            # ── AI Analysis ────────────────────────────────────────────────────
            pdf.ln(3)
            _section("STRATEGIC BUSINESS ANALYSIS")

            import re as _re
            for line in ai_text.split("\n"):
                stripped = line.strip()
                if not stripped:
                    pdf.ln(1.5)
                    continue
                if stripped.startswith("## "):
                    pdf.ln(3)
                    pdf.set_fill_color(14, 28, 58)
                    pdf.set_draw_color(20, 40, 80)
                    pdf.rect(18, pdf.get_y(), 174, 8, "FD")
                    pdf.set_font("Helvetica", "B", 8)
                    pdf.set_text_color(59, 130, 246)
                    pdf.set_x(21)
                    pdf.cell(168, 8, stripped[3:].upper())
                    pdf.ln(10)
                elif stripped.startswith(("- ", "* ", "• ")):
                    content = _re.sub(r'\*\*(.+?)\*\*', r'\1', stripped[2:])
                    pdf.set_font("Helvetica", "", 8.5)
                    pdf.set_text_color(35, 52, 75)
                    pdf.set_x(22)
                    pdf.cell(4, 5, chr(149))
                    pdf.set_x(27)
                    pdf.multi_cell(163, 5, content)
                    pdf.ln(0.5)
                else:
                    content = _re.sub(r'\*\*(.+?)\*\*', r'\1', stripped)
                    pdf.set_font("Helvetica", "", 8.5)
                    pdf.set_text_color(35, 52, 75)
                    pdf.multi_cell(174, 5, content)
                    pdf.ln(0.5)

            # ── Footer ─────────────────────────────────────────────────────────
            pdf.set_y(-18)
            pdf.set_font("Helvetica", "", 7)
            pdf.set_text_color(130, 145, 165)
            pdf.cell(0, 5,
                     f"Generated by Shpapi Vision Dashboard  ·  {date.today().strftime('%B %d, %Y')}",
                     align="C")

            return bytes(pdf.output())

        pdf_bytes = _build_pdf()
        st.download_button(
            label="Download PDF Report",
            data=pdf_bytes,
            file_name=f"shpapi_report_{q_short.lower().replace(' ','_')}.pdf",
            mime="application/pdf",
            type="primary",
        )
