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
sel    = st.selectbox("Date range", list(DATE_PRESETS.keys()), index=1, label_visibility="collapsed")
preset = DATE_PRESETS[sel]

@st.cache_data(ttl=1800, show_spinner=False)
def fetch_campaigns(preset):
    rows, url = [], f"https://graph.facebook.com/v19.0/{IG_ACCOUNT}/insights"
    params = {
        "fields": "campaign_name,spend,reach,impressions,actions,clicks",
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

def get_engagements(actions):
    types = {"post_engagement", "link_click", "page_engagement",
             "onsite_conversion.post_save", "video_view", "post_reaction", "comment"}
    return sum(int(float(a["value"])) for a in actions if a["action_type"] in types)

with st.spinner("Loading Instagram data..."):
    campaigns = fetch_campaigns(preset)

if not campaigns:
    st.info("No boost data found for this period.")
    st.stop()

total_spend = sum(float(c.get("spend", 0)) for c in campaigns)
total_reach = sum(int(c.get("reach", 0)) for c in campaigns)
total_impr  = sum(int(c.get("impressions", 0)) for c in campaigns)
total_eng   = sum(get_engagements(c.get("actions", [])) for c in campaigns)

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
    <div class="kpi" style="border-top:3px solid #f59e0b;">
        <div class="kpi-label">Engagements</div>
        <div class="kpi-value">{total_eng:,}</div>
        <div class="kpi-sub">Likes, comments, saves, clicks</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section">Boost Breakdown</div>', unsafe_allow_html=True)

for c in sorted(campaigns, key=lambda x: float(x.get("spend", 0)), reverse=True):
    spend = float(c.get("spend", 0))
    reach = int(c.get("reach", 0))
    impr  = int(c.get("impressions", 0))
    eng   = get_engagements(c.get("actions", []))
    name  = c.get("campaign_name", "Unnamed boost")
    pct   = (spend / total_spend * 100) if total_spend else 0
    cpe   = (spend / eng) if eng else 0

    st.markdown(f"""
    <div style="background:{SURFACE};border:1px solid {BORDER};border-radius:12px;
                padding:1.2rem 1.5rem;margin-bottom:0.6rem;">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.9rem;">
            <div style="font-size:0.85rem;font-weight:600;color:{T1};max-width:65%;line-height:1.4;">{name}</div>
            <div style="text-align:right;">
                <div style="font-size:1.1rem;font-weight:700;color:{PINK};">${spend:,.2f}</div>
                <div style="font-size:0.68rem;color:{T3};">{pct:.0f}% of total spend</div>
            </div>
        </div>
        <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1rem;">
            <div>
                <div style="font-size:0.58rem;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;color:{T3};margin-bottom:0.2rem;">Reach</div>
                <div style="font-size:0.95rem;font-weight:700;color:{T1};">{reach:,}</div>
            </div>
            <div>
                <div style="font-size:0.58rem;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;color:{T3};margin-bottom:0.2rem;">Impressions</div>
                <div style="font-size:0.95rem;font-weight:700;color:{T1};">{impr:,}</div>
            </div>
            <div>
                <div style="font-size:0.58rem;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;color:{T3};margin-bottom:0.2rem;">Engagements</div>
                <div style="font-size:0.95rem;font-weight:700;color:{T1};">{eng:,}</div>
            </div>
            <div>
                <div style="font-size:0.58rem;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;color:{T3};margin-bottom:0.2rem;">Cost / Engagement</div>
                <div style="font-size:0.95rem;font-weight:700;color:{T1};">${cpe:.2f}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
