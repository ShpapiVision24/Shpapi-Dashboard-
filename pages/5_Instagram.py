import streamlit as st
import requests
import os

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
.kpi-label {{ font-size: 0.65rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1.8px; color: {T3}; margin-bottom: 0.65rem; }}
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
.metric-row {{ display: grid; gap: 0.5rem; margin-bottom: 0.75rem; }}
.metric-cell {{ background: rgba(255,255,255,0.03); border-radius: 8px; padding: 0.6rem 0.8rem; }}
.metric-cell-label {{ font-size: 0.58rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1.4px; color: {T3}; margin-bottom: 0.2rem; }}
.metric-cell-value {{ font-size: 0.9rem; font-weight: 700; color: {T1}; }}
.divider {{ border-top: 1px solid {BORDER}; margin: 0.75rem 0; }}
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
  <div style="font-size:0.7rem;font-weight:500;text-transform:uppercase;letter-spacing:2px;color:{T3};margin-top:0.3rem;">Shpapi &nbsp;·&nbsp; Sponsored Posts & Reels</div>
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
@st.cache_data(ttl=1800, show_spinner=False)
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

@st.cache_data(ttl=1800, show_spinner=False)
def fetch_campaign_details():
    r = requests.get(
        f"https://graph.facebook.com/v19.0/{IG_ACCOUNT}/campaigns",
        params={
            "fields": "id,name,status,effective_status,daily_budget,lifetime_budget,start_time,end_time,budget_remaining",
            "limit": 200,
            "access_token": ACCESS_TOKEN,
        },
        timeout=15,
    )
    return {c["id"]: c for c in r.json().get("data", [])}

def act(actions, atype):
    for a in (actions or []):
        if a["action_type"] == atype:
            try: return int(float(a["value"]))
            except: return 0
    return 0

def act_val(action_values, atype):
    for a in (action_values or []):
        if a["action_type"] == atype:
            try: return float(a["value"])
            except: return 0.0
    return 0.0

def fmt_val(v, prefix="", suffix="", zero="—"):
    if v == 0: return zero
    if prefix == "$": return f"${v:,.2f}{suffix}"
    return f"{prefix}{v:,}{suffix}"

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
total_roas      = (total_conv_val / total_spend) if total_spend else 0

st.markdown('<div class="section">Overview</div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi" style="border-top:3px solid {PINK};">
        <div class="kpi-label">Total Spend</div>
        <div class="kpi-value">${total_spend:,.2f}</div>
        <div class="kpi-sub">{sel}</div>
    </div>
    <div class="kpi" style="border-top:3px solid {GREEN};">
        <div class="kpi-label">Reach</div>
        <div class="kpi-value">{total_reach:,}</div>
        <div class="kpi-sub">Unique accounts reached</div>
    </div>
    <div class="kpi" style="border-top:3px solid {BLUE};">
        <div class="kpi-label">Impressions</div>
        <div class="kpi-value">{total_impr:,}</div>
        <div class="kpi-sub">Total views</div>
    </div>
    <div class="kpi" style="border-top:3px solid {YELLOW};">
        <div class="kpi-label">Purchase ROAS</div>
        <div class="kpi-value">{total_roas:.2f}x</div>
        <div class="kpi-sub">${total_conv_val:,.2f} conv. value</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Per-boost breakdown ───────────────────────────────────────────────────────
st.markdown('<div class="section">Boost Breakdown</div>', unsafe_allow_html=True)

for c in sorted(campaigns, key=lambda x: float(x.get("spend", 0)), reverse=True):
    cid     = c.get("campaign_id", "")
    name    = c.get("campaign_name", "Unnamed boost")
    spend   = float(c.get("spend", 0))
    reach   = int(c.get("reach", 0))
    impr    = int(c.get("impressions", 0))
    clicks  = int(c.get("clicks", 0))
    actions = c.get("actions", [])
    avals   = c.get("action_values", [])

    video_views    = act(actions, "video_view")
    purchases      = act(actions, "purchase")
    checkouts      = act(actions, "initiate_checkout")
    adds_to_cart   = act(actions, "add_to_cart")
    content_views  = act(actions, "view_content")
    link_clicks    = act(actions, "link_click")
    conv_value     = act_val(avals, "purchase")
    roas           = (conv_value / spend) if spend and conv_value else 0
    cpp            = (spend / purchases) if purchases else 0
    pct            = (spend / total_spend * 100) if total_spend else 0

    # Campaign metadata
    meta   = camp_meta.get(cid, {})
    status = meta.get("effective_status", meta.get("status", "")).replace("_", " ").title()
    lb     = int(meta.get("lifetime_budget", 0)) / 100
    db     = int(meta.get("daily_budget", 0)) / 100
    budget_str = f"${lb:,.0f} lifetime" if lb else (f"${db:,.0f}/day" if db else "—")

    status_color = GREEN if status in ("Active",) else (YELLOW if "Pending" in status else T3)

    st.markdown(f"""
    <div style="background:{SURFACE};border:1px solid {BORDER};border-radius:14px;
                padding:1.4rem 1.6rem;margin-bottom:1rem;">

      <!-- Header -->
      <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:1rem;">
        <div style="font-size:0.9rem;font-weight:600;color:{T1};max-width:65%;line-height:1.4;">{name}</div>
        <div style="text-align:right;">
          <div style="font-size:1.15rem;font-weight:700;color:{PINK};">${spend:,.2f}</div>
          <div style="font-size:0.68rem;color:{T3};">{pct:.0f}% of total spend</div>
        </div>
      </div>

      <!-- Reach / Impressions / Clicks / Video Views -->
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0.6rem;margin-bottom:1rem;">
        <div style="background:rgba(255,255,255,0.03);border-radius:8px;padding:0.6rem 0.8rem;">
          <div style="font-size:0.58rem;font-weight:600;text-transform:uppercase;letter-spacing:1.4px;color:{T3};margin-bottom:0.2rem;">Reach</div>
          <div style="font-size:0.95rem;font-weight:700;color:{T1};">{fmt_val(reach)}</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);border-radius:8px;padding:0.6rem 0.8rem;">
          <div style="font-size:0.58rem;font-weight:600;text-transform:uppercase;letter-spacing:1.4px;color:{T3};margin-bottom:0.2rem;">Impressions</div>
          <div style="font-size:0.95rem;font-weight:700;color:{T1};">{fmt_val(impr)}</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);border-radius:8px;padding:0.6rem 0.8rem;">
          <div style="font-size:0.58rem;font-weight:600;text-transform:uppercase;letter-spacing:1.4px;color:{T3};margin-bottom:0.2rem;">Link Clicks</div>
          <div style="font-size:0.95rem;font-weight:700;color:{T1};">{fmt_val(link_clicks)}</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);border-radius:8px;padding:0.6rem 0.8rem;">
          <div style="font-size:0.58rem;font-weight:600;text-transform:uppercase;letter-spacing:1.4px;color:{T3};margin-bottom:0.2rem;">Video Views</div>
          <div style="font-size:0.95rem;font-weight:700;color:{T1};">{fmt_val(video_views)}</div>
        </div>
      </div>

      <!-- Goal & Conversions -->
      <div style="font-size:0.58rem;font-weight:600;text-transform:uppercase;letter-spacing:1.8px;color:{T3};margin-bottom:0.5rem;">Goal & Conversions</div>
      <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:0.6rem;margin-bottom:1rem;">
        <div style="background:rgba(255,255,255,0.03);border-radius:8px;padding:0.6rem 0.8rem;">
          <div style="font-size:0.58rem;font-weight:600;text-transform:uppercase;letter-spacing:1.4px;color:{T3};margin-bottom:0.2rem;">Purchases</div>
          <div style="font-size:0.95rem;font-weight:700;color:{T1};">{fmt_val(purchases)}</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);border-radius:8px;padding:0.6rem 0.8rem;">
          <div style="font-size:0.58rem;font-weight:600;text-transform:uppercase;letter-spacing:1.4px;color:{T3};margin-bottom:0.2rem;">Cost / Purchase</div>
          <div style="font-size:0.95rem;font-weight:700;color:{T1};">{"${:,.2f}".format(cpp) if cpp else "—"}</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);border-radius:8px;padding:0.6rem 0.8rem;">
          <div style="font-size:0.58rem;font-weight:600;text-transform:uppercase;letter-spacing:1.4px;color:{T3};margin-bottom:0.2rem;">Conv. Value</div>
          <div style="font-size:0.95rem;font-weight:700;color:{T1};">{"${:,.2f}".format(conv_value) if conv_value else "—"}</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);border-radius:8px;padding:0.6rem 0.8rem;">
          <div style="font-size:0.58rem;font-weight:600;text-transform:uppercase;letter-spacing:1.4px;color:{T3};margin-bottom:0.2rem;">Purchase ROAS</div>
          <div style="font-size:0.95rem;font-weight:700;color:{GREEN if roas >= 1 else T1};">{"{}x".format(round(roas,2)) if roas else "—"}</div>
        </div>
      </div>

      <!-- Funnel -->
      <div style="font-size:0.58rem;font-weight:600;text-transform:uppercase;letter-spacing:1.8px;color:{T3};margin-bottom:0.5rem;">Funnel</div>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0.6rem;margin-bottom:1rem;">
        <div style="background:rgba(255,255,255,0.03);border-radius:8px;padding:0.6rem 0.8rem;">
          <div style="font-size:0.58rem;font-weight:600;text-transform:uppercase;letter-spacing:1.4px;color:{T3};margin-bottom:0.2rem;">Content Views</div>
          <div style="font-size:0.95rem;font-weight:700;color:{T1};">{fmt_val(content_views)}</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);border-radius:8px;padding:0.6rem 0.8rem;">
          <div style="font-size:0.58rem;font-weight:600;text-transform:uppercase;letter-spacing:1.4px;color:{T3};margin-bottom:0.2rem;">Adds to Cart</div>
          <div style="font-size:0.95rem;font-weight:700;color:{T1};">{fmt_val(adds_to_cart)}</div>
        </div>
        <div style="background:rgba(255,255,255,0.03);border-radius:8px;padding:0.6rem 0.8rem;">
          <div style="font-size:0.58rem;font-weight:600;text-transform:uppercase;letter-spacing:1.4px;color:{T3};margin-bottom:0.2rem;">Checkouts</div>
          <div style="font-size:0.95rem;font-weight:700;color:{T1};">{fmt_val(checkouts)}</div>
        </div>
      </div>

      <!-- Details bar -->
      <div style="border-top:1px solid {BORDER};padding-top:0.75rem;display:flex;gap:2rem;flex-wrap:wrap;">
        <div><span style="font-size:0.65rem;color:{T3};">Status &nbsp;</span><span style="font-size:0.72rem;font-weight:600;color:{status_color};">{status or "—"}</span></div>
        <div><span style="font-size:0.65rem;color:{T3};">Budget &nbsp;</span><span style="font-size:0.72rem;font-weight:600;color:{T2};">{budget_str}</span></div>
        <div><span style="font-size:0.65rem;color:{T3};">Placements &nbsp;</span><span style="font-size:0.72rem;font-weight:600;color:{T2};">Instagram & Facebook</span></div>
      </div>

    </div>
    """, unsafe_allow_html=True)
