import streamlit as st
import requests
import os
from datetime import datetime, timezone

ASSETS    = os.path.join(os.path.dirname(__file__), "..", "assets")
LOGO_CROP = os.path.join(ASSETS, "logo_cropped.png")

ACCESS_TOKEN = st.secrets["META_ACCESS_TOKEN"]
IG_ACCOUNT   = "act_8429913163714900"

BG      = "#0a1628"
SURFACE = "#0e1f3c"
BORDER  = "rgba(255,255,255,0.08)"
T1      = "#ffffff"
T2      = "rgba(255,255,255,0.65)"
T3      = "rgba(255,255,255,0.38)"
BLUE    = "#3b82f6"
GREEN   = "#22c55e"
PINK    = "#ec4899"
YELLOW  = "#f59e0b"

st.set_page_config(page_title="Shpapi · Instagram", layout="wide", initial_sidebar_state="collapsed")

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
.kpi-grid {{ display: grid; grid-template-columns: repeat(4,1fr); gap: 1rem; margin-bottom: 2rem; }}
.kpi {{ background: {SURFACE}; border: 1px solid {BORDER}; border-radius: 12px; padding: 1.4rem 1.6rem 1.3rem; }}
.kpi-label {{ font-size: 0.65rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1.8px; color: {T3}; margin-bottom: 0.65rem; position: relative; }}
.tip {{ display: inline-block; cursor: help; color: rgba(255,255,255,0.25); font-size: 0.6rem; margin-left: 4px; vertical-align: middle; position: relative; }}
.tip .tiptext {{ visibility: hidden; opacity: 0; width: 210px; background: #1a2f50; color: rgba(255,255,255,0.85); font-size: 0.7rem; font-weight: 400; line-height: 1.45; text-align: left; border-radius: 8px; padding: 8px 10px; border: 1px solid rgba(255,255,255,0.1); position: absolute; z-index: 9999; bottom: 140%; left: 50%; transform: translateX(-50%); transition: opacity 0.15s; pointer-events: none; text-transform: none; letter-spacing: 0; }}
.tip:hover .tiptext {{ visibility: visible; opacity: 1; }}
.kpi-value {{ font-size: 2rem; font-weight: 700; color: #ffffff; letter-spacing: -1px; line-height: 1; }}
.kpi-sub {{ font-size: 0.72rem; color: {T2}; margin-top: 0.4rem; }}
.section {{ font-size: 0.62rem; font-weight: 600; text-transform: uppercase; letter-spacing: 2.5px; color: {T3}; margin: 0 0 0.9rem 0; display: flex; align-items: center; gap: 1rem; }}
.section::after {{ content: ''; flex: 1; height: 1px; background: {BORDER}; }}
.stButton > button {{
    background: transparent !important; border: none !important; box-shadow: none !important;
    outline: none !important; color: {T2} !important; font-weight: 600 !important;
    font-size: 0.78rem !important; padding: 0.35rem 0.85rem !important;
    min-height: 0 !important; width: auto !important; border-radius: 6px !important;
}}
.stButton > button:hover {{ background: rgba(37,99,235,0.08) !important; color: {BLUE} !important; border: none !important; }}
div[data-testid="stPageLink"] {{ border: none !important; background: none !important; box-shadow: none !important; padding: 0 !important; margin: 0 !important; padding-top: 1rem !important; }}
a[data-testid="stPageLink-NavLink"] {{ color: {T2} !important; font-weight: 600 !important; font-size: 0.70rem !important; text-decoration: none !important; padding: 0.25rem 0.65rem !important; border-radius: 6px !important; background: transparent !important; border: none !important; display: inline-block !important; }}
a[data-testid="stPageLink-NavLink"]:hover {{ background: rgba(59,130,246,0.15) !important; color: {BLUE} !important; }}
a[data-testid="stPageLink-NavLink"] svg {{ display: none !important; }}
[data-testid="stMetric"] {{ background: rgba(255,255,255,0.03); border-radius: 8px; padding: 0.6rem 0.8rem !important; }}
[data-testid="stMetricLabel"] p {{ font-size: 0.6rem !important; font-weight: 600 !important; text-transform: uppercase !important; letter-spacing: 1.4px !important; color: {T3} !important; }}
[data-testid="stMetricValue"] {{ font-size: 0.95rem !important; font-weight: 700 !important; color: {T1} !important; }}
[data-testid="stMetricDelta"] {{ display: none !important; }}
[data-testid="stVerticalBlockBorderWrapper"] {{ background: {SURFACE} !important; border: 1px solid {BORDER} !important; border-radius: 14px !important; }}
[data-testid="stVerticalBlockBorderWrapper"] > div {{ padding: 1rem 1.2rem !important; }}
</style>
""", unsafe_allow_html=True)

# ── Nav ───────────────────────────────────────────────────────────────────────
_c_logo, _c_h, _c_m, _c_s, _c_g, _c_qb, _c_ig, _ = st.columns([1.5, 1, 1, 1, 1.2, 1.3, 1.2, 1.8])
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
    st.markdown(f'<div style="padding-top:1.1rem;"><span style="padding:0.35rem 0.9rem;border-radius:6px;font-size:0.8rem;font-weight:700;color:{PINK};background:rgba(236,72,153,0.18);white-space:nowrap;">Instagram</span></div>', unsafe_allow_html=True)
st.markdown(f'<div style="border-top:1px solid {BORDER};margin:0.5rem 0 2rem;"></div>', unsafe_allow_html=True)

st.markdown(f"""
<div style="margin-bottom:2rem;">
  <div style="font-size:1.4rem;font-weight:700;color:{T1};letter-spacing:-0.5px;">Instagram Boosts</div>
  <div style="font-size:0.7rem;font-weight:500;text-transform:uppercase;letter-spacing:2px;color:{T3};margin-top:0.3rem;">Shpapi &nbsp;·&nbsp; Sponsored Posts &amp; Reels</div>
</div>
""", unsafe_allow_html=True)

DATE_PRESETS = {
    "Last 7 days":  "last_7d",
    "Last 30 days": "last_30d",
    "Last 90 days": "last_90d",
    "All time":     "maximum",
}
sel    = st.selectbox("Date range", list(DATE_PRESETS.keys()), index=3, label_visibility="collapsed")
preset = DATE_PRESETS[sel]

# ── Data fetching ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=300, show_spinner=False)
def fetch_insights(preset):
    rows, url = [], f"https://graph.facebook.com/v19.0/{IG_ACCOUNT}/insights"
    params = {
        "fields": "campaign_id,campaign_name,spend,reach,impressions,actions,action_values,clicks,video_play_actions",
        "level": "campaign",
        "date_preset": preset,
        "limit": 100,
        "access_token": ACCESS_TOKEN,
    }
    while url:
        r    = requests.get(url, params=params, timeout=15)
        data = r.json()
        rows.extend(data.get("data", []))
        url    = data.get("paging", {}).get("next")
        params = {}
    return rows

@st.cache_data(ttl=300, show_spinner=False)
def fetch_campaign_details():
    r = requests.get(
        f"https://graph.facebook.com/v19.0/{IG_ACCOUNT}/campaigns",
        params={
            "fields": "id,name,effective_status,daily_budget,lifetime_budget,start_time,end_time,stop_time",
            "limit": 200,
            "access_token": ACCESS_TOKEN,
        },
        timeout=15,
    )
    return {c["id"]: c for c in r.json().get("data", [])}

def act(actions, atype):
    for a in (actions or []):
        if a.get("action_type") == atype:
            try: return int(float(a["value"]))
            except: pass
    return 0

def act_val(action_values, atype):
    for a in (action_values or []):
        if a.get("action_type") == atype:
            try: return float(a["value"])
            except: pass
    return 0.0

METRIC_HELP = {
    "Reach":         "How many unique people saw your ad. Each person is counted once no matter how many times they saw it.",
    "Impressions":   "Total times your ad appeared on someone's screen. One person seeing it 5 times counts as 5 impressions.",
    "Link Clicks":   "How many times someone clicked the link in your ad to visit your website or product page.",
    "Video Views":   "How many times your video was watched for at least 3 seconds.",
    "Purchases":     "Number of sales that happened after someone saw or clicked your ad.",
    "Cost/Purchase": "Average amount you spent on ads to get one sale. Lower is better.",
    "Conv. Value":   "Total revenue from purchases that came through your ad.",
    "Purchase ROAS": "Return on Ad Spend — for every $1 you spent, how many dollars came back in sales. 2x means you earned $2 for every $1 spent.",
    "Content Views": "How many times people visited your product page after seeing your ad.",
    "Adds to Cart":  "How many people added a product to their cart after seeing your ad.",
    "Checkouts":     "How many people started the checkout process after seeing your ad.",
    "Total Spend":   "Total money spent on this campaign.",
    "CTR":           "Click-Through Rate — percentage of people who saw your ad and clicked on it. Higher is better.",
    "Avg CPC":       "Average Cost Per Click — how much you paid on average for each click.",
    "Conversions":   "Total number of purchases or desired actions completed after seeing your ad.",
}

def fmt_date(iso_str):
    if not iso_str:
        return ""
    try:
        return datetime.fromisoformat(iso_str.replace("Z", "+00:00")).strftime("%b %d, %Y")
    except:
        return iso_str[:10]

with st.spinner("Loading Instagram data..."):
    campaigns  = fetch_insights(preset)
    camp_meta  = fetch_campaign_details()

if not campaigns:
    st.info("No boost data found for this period.")
    st.stop()

# ── Summary KPIs ──────────────────────────────────────────────────────────────
total_spend     = sum(float(c.get("spend", 0)) for c in campaigns)
total_reach     = sum(int(c.get("reach", 0)) for c in campaigns)
total_impr      = sum(int(c.get("impressions", 0)) for c in campaigns)
total_purchases = sum(act(c.get("actions", []), "purchase") for c in campaigns)
total_conv_val  = sum(act_val(c.get("action_values", []), "purchase") for c in campaigns)
total_roas      = round(total_conv_val / total_spend, 2) if total_spend else 0

st.markdown('<div class="section">Overview</div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi" style="border-top:3px solid {PINK};">
        <div class="kpi-label">Total Spend <span class="tip">ⓘ<span class="tiptext">Total money spent on all boosts during the selected time period.</span></span></div>
        <div class="kpi-value">${total_spend:,.2f}</div>
        <div class="kpi-sub">{sel}</div>
    </div>
    <div class="kpi" style="border-top:3px solid {GREEN};">
        <div class="kpi-label">Reach <span class="tip">ⓘ<span class="tiptext">How many unique people saw your ads. Each person is counted once, no matter how many times they saw it.</span></span></div>
        <div class="kpi-value">{total_reach:,}</div>
        <div class="kpi-sub">Unique accounts reached</div>
    </div>
    <div class="kpi" style="border-top:3px solid {BLUE};">
        <div class="kpi-label">Impressions <span class="tip">ⓘ<span class="tiptext">Total times your ads appeared on screen. One person seeing it 5 times counts as 5 impressions.</span></span></div>
        <div class="kpi-value">{total_impr:,}</div>
        <div class="kpi-sub">Total views</div>
    </div>
    <div class="kpi" style="border-top:3px solid {YELLOW};">
        <div class="kpi-label">Purchase ROAS <span class="tip">ⓘ<span class="tiptext">Return on Ad Spend — for every $1 you spent on ads, how many dollars came back in sales. 2x means you earned $2 for every $1 spent.</span></span></div>
        <div class="kpi-value">{total_roas}x</div>
        <div class="kpi-sub">${total_conv_val:,.2f} conv. value</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Per-boost breakdown ───────────────────────────────────────────────────────
st.markdown('<div class="section">Boost Breakdown</div>', unsafe_allow_html=True)

for c in sorted(campaigns, key=lambda x: camp_meta.get(x.get("campaign_id", ""), {}).get("created_time", ""), reverse=True):
    cid     = c.get("campaign_id", "")
    name    = c.get("campaign_name", "Unnamed boost")
    spend   = float(c.get("spend", 0))
    reach   = int(c.get("reach", 0))
    impr    = int(c.get("impressions", 0))
    actions = c.get("actions", [])
    avals   = c.get("action_values", [])

    video_views   = act(actions, "video_view")
    purchases     = act(actions, "purchase")
    checkouts     = act(actions, "initiate_checkout")
    adds_to_cart  = act(actions, "add_to_cart")
    content_views = act(actions, "view_content")
    link_clicks   = act(actions, "link_click")
    conv_value    = act_val(avals, "purchase")
    roas          = round(conv_value / spend, 2) if spend and conv_value else 0
    cpp           = round(spend / purchases, 2) if purchases else 0
    pct           = round(spend / total_spend * 100) if total_spend else 0

    meta      = camp_meta.get(cid, {})
    effective = meta.get("effective_status", "")
    end_time_str = meta.get("end_time", "") or meta.get("stop_time", "")
    now = datetime.now(timezone.utc)
    if effective == "ACTIVE":
        ended = False
        if end_time_str:
            try:
                ended = datetime.fromisoformat(end_time_str.replace("Z", "+00:00")) <= now
            except:
                pass
        lb_check = int(meta.get("lifetime_budget", 0)) / 100
        if not ended and lb_check > 0 and spend >= lb_check * 0.98:
            ended = True
        status = "Ended" if ended else "Active"
    elif effective == "PAUSED":
        status = "Paused"
    elif effective in ("DELETED", "ARCHIVED"):
        status = "Ended"
    else:
        status = effective.replace("_", " ").title()

    lb        = int(meta.get("lifetime_budget", 0)) / 100
    db        = int(meta.get("daily_budget", 0)) / 100
    budget_str = f"${lb:,.0f} lifetime" if lb else (f"${db:,.0f}/day" if db else "")
    date_str  = fmt_date(meta.get("start_time", ""))

    status_color = GREEN if status == "Active" else (YELLOW if "Pending" in status or "Review" in status else T3)

    with st.container(border=True):
        # ── Header ────────────────────────────────────────────────────────────
        hcol1, hcol2 = st.columns([4, 1])
        with hcol1:
            st.markdown(f'<div style="font-size:0.9rem;font-weight:600;color:{T1};line-height:1.4;margin-bottom:0.2rem;">{name}</div>', unsafe_allow_html=True)
            meta_parts = []
            if date_str:     meta_parts.append(f"Created {date_str}")
            if status:       meta_parts.append(f'<span style="color:{status_color};font-weight:600;">{status}</span>')
            if budget_str:   meta_parts.append(f"Budget: {budget_str}")
            if pct:          meta_parts.append(f"{pct}% of total spend")
            if meta_parts:
                st.markdown(f'<div style="font-size:0.72rem;color:{T3};">{" &nbsp;·&nbsp; ".join(meta_parts)}</div>', unsafe_allow_html=True)
        with hcol2:
            st.markdown(f'<div style="text-align:right;font-size:1.15rem;font-weight:700;color:{PINK};padding-top:0.2rem;">${spend:,.2f}</div>', unsafe_allow_html=True)

        st.markdown(f'<div style="border-top:1px solid {BORDER};margin:0.75rem 0 0.6rem;"></div>', unsafe_allow_html=True)

        # ── Reach / Impressions / Clicks / Video (only non-zero) ──────────────
        row1 = [(label, val) for label, val in [
            ("Reach", f"{reach:,}" if reach else None),
            ("Impressions", f"{impr:,}" if impr else None),
            ("Link Clicks", f"{link_clicks:,}" if link_clicks else None),
            ("Video Views", f"{video_views:,}" if video_views else None),
        ] if val is not None]

        if row1:
            cols = st.columns(len(row1))
            for col, (label, val) in zip(cols, row1):
                with col:
                    st.metric(label, val, help=METRIC_HELP.get(label))

        # ── Goal & Conversions (only if any data) ─────────────────────────────
        row2 = [(label, val) for label, val in [
            ("Purchases", f"{purchases:,}" if purchases else None),
            ("Cost/Purchase", f"${cpp:,.2f}" if cpp else None),
            ("Conv. Value", f"${conv_value:,.2f}" if conv_value else None),
            ("Purchase ROAS", f"{roas}x" if roas else None),
        ] if val is not None]

        if row2:
            st.markdown(f'<div style="font-size:0.6rem;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;color:{T3};margin:0.6rem 0 0.3rem;">Goal &amp; Conversions</div>', unsafe_allow_html=True)
            cols = st.columns(len(row2))
            for col, (label, val) in zip(cols, row2):
                with col:
                    st.metric(label, val, help=METRIC_HELP.get(label))

        # ── Funnel (only if any data) ─────────────────────────────────────────
        row3 = [(label, val) for label, val in [
            ("Content Views", f"{content_views:,}" if content_views else None),
            ("Adds to Cart", f"{adds_to_cart:,}" if adds_to_cart else None),
            ("Checkouts", f"{checkouts:,}" if checkouts else None),
        ] if val is not None]

        if row3:
            st.markdown(f'<div style="font-size:0.6rem;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;color:{T3};margin:0.6rem 0 0.3rem;">Funnel</div>', unsafe_allow_html=True)
            cols = st.columns(len(row3))
            for col, (label, val) in zip(cols, row3):
                with col:
                    st.metric(label, val, help=METRIC_HELP.get(label))
