import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os
from datetime import date, timedelta

ASSETS    = os.path.join(os.path.dirname(__file__), "..", "assets")
LOGO_CROP = os.path.join(ASSETS, "logo_cropped.png")
BG = "#0a1628"; SURFACE = "#0e1f3c"; BORDER = "rgba(255,255,255,0.08)"
T1 = "#ffffff"; T2 = "rgba(255,255,255,0.65)"; T3 = "rgba(255,255,255,0.38)"; BLUE = "#3b82f6"

st.set_page_config(page_title="Shpapi · Google Ads", layout="wide", initial_sidebar_state="collapsed")

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
.kpi-grid {{ display: grid; grid-template-columns: repeat(4,1fr); gap: 1rem; margin-bottom: 1.5rem; }}
.kpi {{ background: {SURFACE}; border: 1px solid {BORDER}; border-radius: 12px; padding: 1.4rem 1.6rem 1.3rem; }}
.kpi-label {{ font-size: 0.65rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1.8px; color: {T3}; margin-bottom: 0.65rem; }}
.kpi-value {{ font-size: 2rem; font-weight: 700; color: #ffffff; letter-spacing: -1px; line-height: 1; }}
.kpi-sub {{ font-size: 0.72rem; color: {T3}; margin-top: 0.4rem; }}
.section {{ font-size: 0.62rem; font-weight: 600; text-transform: uppercase; letter-spacing: 2.5px; color: {T3}; margin: 0 0 0.9rem 0; display: flex; align-items: center; gap: 1rem; }}
.section::after {{ content: ''; flex: 1; height: 1px; background: {BORDER}; }}
.surface {{ background: {SURFACE}; border: 1px solid {BORDER}; border-radius: 12px; padding: 1.4rem 1.4rem 0.6rem; margin-bottom: 1rem; }}
.stButton > button {{
    background: transparent !important; border: none !important; box-shadow: none !important;
    outline: none !important; color: {T2} !important; font-weight: 600 !important;
    font-size: 0.78rem !important; padding: 0.35rem 0.85rem !important;
    min-height: 0 !important; width: auto !important; border-radius: 6px !important;
}}
.stButton > button:hover {{ background: rgba(37,99,235,0.08) !important; color: {BLUE} !important; border: none !important; }}
div[data-testid="stPageLink"] {{ border: none !important; background: none !important; box-shadow: none !important; padding: 0 !important; margin: 0 !important; padding-top: 1rem !important; }}
a[data-testid="stPageLink-NavLink"] {{
    color: {T2} !important; font-weight: 500 !important; font-size: 0.70rem !important;
    text-decoration: none !important; padding: 0.3rem 0.75rem !important;
    border-radius: 6px !important; background: transparent !important;
    border: none !important; display: inline-block !important;
}}
a[data-testid="stPageLink-NavLink"]:hover {{ background: rgba(59,130,246,0.15) !important; color: {BLUE} !important; }}
a[data-testid="stPageLink-NavLink"] svg {{ display: none !important; }}
</style>
""", unsafe_allow_html=True)

# ── Nav ──────────────────────────────────────────────────────────────────────
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
    st.markdown(f'<div style="padding-top:1.1rem;"><span style="padding:0.35rem 0.9rem;border-radius:6px;font-size:0.8rem;font-weight:700;color:{BLUE};background:rgba(59,130,246,0.18);white-space:nowrap;">Google Ads</span></div>', unsafe_allow_html=True)
with _c_qb:
    st.page_link("pages/4_QuickBooks.py", label="QuickBooks")
with _c_ig:
    st.page_link("pages/5_Instagram.py", label="Instagram")
st.markdown(f'<div style="border-top:1px solid {BORDER};margin:0.5rem 0 1.8rem;"></div>', unsafe_allow_html=True)

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="padding-bottom:1.4rem;border-bottom:1px solid {BORDER};margin-bottom:2rem;">
  <div style="font-size:0.62rem;font-weight:600;text-transform:uppercase;letter-spacing:2.5px;color:{T3};">
    Google Ads &nbsp;·&nbsp; Campaign Performance
  </div>
</div>
""", unsafe_allow_html=True)

# ── Date range ────────────────────────────────────────────────────────────────
col_l, col_r = st.columns([3, 1])
with col_r:
    preset = st.selectbox("Date range", ["Last 30 days", "Last 7 days", "Last 90 days", "This month", "All time"], label_visibility="collapsed")

today = date.today()
if preset == "Last 7 days":
    start_date = today - timedelta(days=7)
elif preset == "Last 90 days":
    start_date = today - timedelta(days=90)
elif preset == "This month":
    start_date = today.replace(day=1)
elif preset == "All time":
    start_date = date(2020, 1, 1)
else:
    start_date = today - timedelta(days=30)
end_date = today - timedelta(days=1)

# ── Google Ads data fetch ─────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_google_ads_data(start_str, end_str):
    try:
        from google.ads.googleads.client import GoogleAdsClient
        from google.ads.googleads.errors import GoogleAdsException

        cfg = st.secrets["google_ads"]
        config = {
            "developer_token": cfg["developer_token"],
            "client_id": cfg["client_id"],
            "client_secret": cfg["client_secret"],
            "refresh_token": cfg["refresh_token"],
            "login_customer_id": cfg["client_customer_id"].replace("-", ""),
            "use_proto_plus": True,
        }
        client = GoogleAdsClient.load_from_dict(config)
        ga_service = client.get_service("GoogleAdsService")
        customer_id = cfg["client_customer_id"].replace("-", "")

        query = f"""
            SELECT
                campaign.name,
                campaign.status,
                metrics.impressions,
                metrics.clicks,
                metrics.cost_micros,
                metrics.conversions,
                metrics.ctr,
                metrics.average_cpc,
                segments.date
            FROM campaign
            WHERE segments.date BETWEEN '{start_str}' AND '{end_str}'
              AND campaign.status != 'REMOVED'
            ORDER BY metrics.cost_micros DESC
        """

        response = ga_service.search(customer_id=customer_id, query=query)
        rows = []
        for row in response:
            rows.append({
                "Campaign": row.campaign.name,
                "Status": row.campaign.status.name,
                "Date": row.segments.date,
                "Impressions": row.metrics.impressions,
                "Clicks": row.metrics.clicks,
                "Cost": row.metrics.cost_micros / 1_000_000,
                "Conversions": row.metrics.conversions,
                "CTR": row.metrics.ctr * 100,
                "Avg CPC": row.metrics.average_cpc / 1_000_000,
            })
        return pd.DataFrame(rows), None
    except Exception as e:
        return None, str(e)


with st.spinner("Loading Google Ads data…"):
    df, error = fetch_google_ads_data(start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"))

if error:
    needs_basic = "developer token" in error.lower() or "test" in error.lower() or "authorization" in error.lower()
    if needs_basic:
        st.markdown(f"""
        <div style="background:rgba(59,130,246,0.08);border:1px solid rgba(59,130,246,0.25);border-radius:12px;padding:2rem;text-align:center;margin-top:2rem;">
            <div style="font-size:1.1rem;font-weight:700;color:{T1};margin-bottom:0.6rem;">Basic API Access Required</div>
            <div style="font-size:0.85rem;color:{T2};max-width:500px;margin:0 auto 1.2rem;">
                Your developer token currently has <strong>Test Account</strong> access, which cannot read real campaign data.
                Apply for <strong>Basic Access</strong> in the Google Ads API Center to unlock this page.
            </div>
            <div style="font-size:0.75rem;color:{T3};">
                Go to your Manager Account → Admin → API Center → Apply for Basic Access
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error(f"Google Ads API error: {error}")
    st.stop()

if df is None or df.empty:
    st.markdown(f'<div style="text-align:center;padding:4rem;color:{T3};font-size:0.9rem;">No campaign data found for the selected period.</div>', unsafe_allow_html=True)
    st.stop()

# ── Aggregate KPIs ────────────────────────────────────────────────────────────
total_spend       = df["Cost"].sum()
total_clicks      = int(df["Clicks"].sum())
total_impressions = int(df["Impressions"].sum())
total_conversions = df["Conversions"].sum()
avg_ctr           = (total_clicks / total_impressions * 100) if total_impressions else 0
avg_cpc           = (total_spend / total_clicks) if total_clicks else 0

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi">
    <div class="kpi-label">Total Spend</div>
    <div class="kpi-value">${total_spend:,.2f}</div>
  </div>
  <div class="kpi">
    <div class="kpi-label">Clicks</div>
    <div class="kpi-value">{total_clicks:,}</div>
  </div>
  <div class="kpi">
    <div class="kpi-label">Impressions</div>
    <div class="kpi-value">{total_impressions:,}</div>
  </div>
  <div class="kpi">
    <div class="kpi-label">Conversions</div>
    <div class="kpi-value">{total_conversions:,.1f}</div>
  </div>
</div>
<div class="kpi-grid">
  <div class="kpi">
    <div class="kpi-label">Avg CTR</div>
    <div class="kpi-value">{avg_ctr:.2f}%</div>
  </div>
  <div class="kpi">
    <div class="kpi-label">Avg CPC</div>
    <div class="kpi-value">${avg_cpc:.2f}</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Spend over time chart ─────────────────────────────────────────────────────
st.markdown('<div class="section">Spend Over Time</div>', unsafe_allow_html=True)
daily = df.groupby("Date")["Cost"].sum().reset_index().sort_values("Date")

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=daily["Date"], y=daily["Cost"],
    mode="lines", fill="tozeroy",
    line=dict(color=BLUE, width=2),
    fillcolor="rgba(59,130,246,0.1)",
    hovertemplate="$%{y:,.2f}<extra></extra>",
))
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    margin=dict(l=0, r=0, t=10, b=0), height=220,
    xaxis=dict(showgrid=False, color=T3, tickfont=dict(size=11)),
    yaxis=dict(showgrid=True, gridcolor=BORDER, color=T3, tickprefix="$", tickfont=dict(size=11)),
)
st.plotly_chart(fig, use_container_width=True)

# ── Campaign breakdown ────────────────────────────────────────────────────────
st.markdown('<div class="section">Campaign Breakdown</div>', unsafe_allow_html=True)
camp = (df.groupby(["Campaign", "Status"])
          .agg(Impressions=("Impressions","sum"), Clicks=("Clicks","sum"),
               Cost=("Cost","sum"), Conversions=("Conversions","sum"))
          .reset_index()
          .sort_values("Cost", ascending=False))
camp["CTR"]     = (camp["Clicks"] / camp["Impressions"] * 100).fillna(0)
camp["Avg CPC"] = (camp["Cost"] / camp["Clicks"]).fillna(0)
camp["Cost"]    = camp["Cost"].map("${:,.2f}".format)
camp["Avg CPC"] = camp["Avg CPC"].map("${:,.2f}".format)
camp["CTR"]     = camp["CTR"].map("{:.2f}%".format)
camp["Impressions"] = camp["Impressions"].map("{:,}".format)
camp["Clicks"]      = camp["Clicks"].map("{:,}".format)
camp["Conversions"] = camp["Conversions"].map("{:.1f}".format)

st.dataframe(camp, use_container_width=True, hide_index=True)
