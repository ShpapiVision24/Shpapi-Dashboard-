import streamlit as st
import requests
import os
from datetime import timedelta
from PIL import Image
import numpy as np

ASSETS    = os.path.join(os.path.dirname(__file__), "assets")
LOGO_SRC  = os.path.join(ASSETS, "logo.png")
LOGO_CROP = os.path.join(ASSETS, "logo_cropped.png")

def prepare_logo(src, dst):
    if os.path.exists(dst):
        return
    raw  = Image.open(src).convert("RGBA")
    arr  = np.array(raw, dtype=np.uint8)
    alpha = arr[:, :, 3]
    mask  = alpha > 10
    if not mask.any():
        raw.save(dst); return
    rows = np.any(mask, axis=1)
    cols = np.any(mask, axis=0)
    r0, r1 = np.where(rows)[0][[0, -1]]
    c0, c1 = np.where(cols)[0][[0, -1]]
    pad = 20
    cropped = arr[max(0,r0-pad):min(arr.shape[0],r1+pad+1),
                  max(0,c0-pad):min(arr.shape[1],c1+pad+1)]
    Image.fromarray(cropped).save(dst)

if os.path.exists(LOGO_SRC):
    prepare_logo(LOGO_SRC, LOGO_CROP)

BG      = "#0a1628"
SURFACE = "#0e1f3c"
BORDER  = "rgba(255,255,255,0.08)"
T1      = "#ffffff"
T2      = "rgba(255,255,255,0.65)"
T3      = "rgba(255,255,255,0.38)"
BLUE    = "#3b82f6"

ACCESS_TOKEN     = st.secrets["META_ACCESS_TOKEN"]
AD_ACCOUNT_ID    = st.secrets["AD_ACCOUNT_ID"]
SHOPIFY_TOKEN    = st.secrets["SHOPIFY_TOKEN"]
SHOP_URL         = st.secrets["SHOP_URL"]
SHOPIFY_HEADERS  = {"X-Shopify-Access-Token": SHOPIFY_TOKEN}

st.set_page_config(page_title="Shpapi · Home", layout="wide", initial_sidebar_state="collapsed")

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
.stButton > button {{
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    outline: none !important;
    color: {T2} !important;
    font-weight: 600 !important;
    font-size: 0.78rem !important;
    padding: 0.35rem 0.85rem !important;
    min-height: 0 !important;
    width: auto !important;
    border-radius: 6px !important;
}}
.stButton > button:hover {{
    background: rgba(37,99,235,0.08) !important;
    color: {BLUE} !important;
    border: none !important;
}}
.platform-card {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 2rem;
    height: 100%;
    min-height: 320px;
    display: flex;
    flex-direction: column;
}}
.platform-title {{
    font-size: 0.65rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: {T3};
    margin-bottom: 1.5rem;
}}
.platform-metric-label {{
    font-size: 0.6rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: {T3};
    margin-bottom: 0.3rem;
}}
.platform-metric-value {{
    font-size: 1.6rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.5px;
    line-height: 1;
    margin-bottom: 1.2rem;
}}
.platform-sub {{
    font-size: 0.75rem;
    color: {T2};
    margin-top: 0.3rem;
}}
.section {{ font-size: 0.62rem; font-weight: 600; text-transform: uppercase; letter-spacing: 2.5px; color: {T3}; margin: 0 0 0.9rem 0; display: flex; align-items: center; gap: 1rem; }}
.section::after {{ content: ''; flex: 1; height: 1px; background: {BORDER}; }}
div[data-testid="stPageLink"] {{
    border: none !important; background: none !important; box-shadow: none !important;
    padding: 0 !important; margin: 0 !important; padding-top: 1rem !important;
}}
a[data-testid="stPageLink-NavLink"] {{
    color: {T2} !important; font-weight: 600 !important; font-size: 0.78rem !important;
    text-decoration: none !important; padding: 0.3rem 0.75rem !important;
    border-radius: 6px !important; background: transparent !important;
    border: none !important; display: inline-block !important;
}}
a[data-testid="stPageLink-NavLink"]:hover {{
    background: rgba(59,130,246,0.15) !important; color: {BLUE} !important;
}}
a[data-testid="stPageLink-NavLink"] svg {{ display: none !important; }}
</style>
""", unsafe_allow_html=True)

_c_logo, _c_h, _c_m, _c_s, _c_g, _ = st.columns([1.5, 1, 1, 1, 1.2, 5])
with _c_logo:
    if os.path.exists(LOGO_CROP):
        st.image(LOGO_CROP, width=90)
with _c_h:
    st.markdown(f'<div style="padding-top:1.1rem;"><span style="padding:0.35rem 0.9rem;border-radius:6px;font-size:0.8rem;font-weight:700;color:{BLUE};background:rgba(59,130,246,0.18);white-space:nowrap;">Home</span></div>', unsafe_allow_html=True)
with _c_m:
    st.page_link("pages/1_Meta_Ads.py", label="Meta Ads")
with _c_s:
    st.page_link("pages/2_Shopify.py", label="Shopify")
with _c_g:
    st.page_link("pages/3_Google_Ads.py", label="Google Ads")
st.markdown(f'<div style="border-top:1px solid {BORDER};margin:0.5rem 0 2rem;"></div>', unsafe_allow_html=True)

st.markdown(f"""
<div style="margin-bottom:2.5rem;">
  <div style="font-size:1.4rem;font-weight:700;color:{T1};letter-spacing:-0.5px;">Analytics Hub</div>
  <div style="font-size:0.7rem;font-weight:500;text-transform:uppercase;letter-spacing:2px;color:{T3};margin-top:0.3rem;">Shpapi &nbsp;·&nbsp; All Platforms Overview</div>
</div>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def get_meta_summary():
    try:
        r = requests.get(
            f"https://graph.facebook.com/v19.0/{AD_ACCOUNT_ID}/insights",
            params={"fields": "spend,impressions,actions",
                    "date_preset": "maximum", "level": "campaign",
                    "access_token": ACCESS_TOKEN},
            timeout=15,
        )
        rows = r.json().get("data", [])
        total_spend = sum(float(d.get("spend", 0)) for d in rows)
        total_impr  = sum(int(d.get("impressions", 0)) for d in rows)
        total_lclicks = 0
        for d in rows:
            for a in d.get("actions", []):
                if a["action_type"] == "link_click":
                    total_lclicks += int(float(a["value"]))
        return {"spend": total_spend, "impressions": total_impr, "clicks": total_lclicks}
    except:
        return None

@st.cache_data(ttl=1800)
def get_shopify_summary():
    try:
        import datetime as dt
        now   = dt.datetime.now(dt.timezone.utc)
        since = (now - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%SZ")
        r     = requests.get(f"{SHOP_URL}/admin/api/2024-01/orders.json",
                             headers=SHOPIFY_HEADERS,
                             params={"status":"any","limit":250,"created_at_min":since,
                                     "fields":"id,total_price,financial_status"},
                             timeout=10)
        orders  = r.json().get("orders", [])
        revenue = sum(float(o["total_price"]) for o in orders if o.get("financial_status") == "paid")
        r_all   = requests.get(f"{SHOP_URL}/admin/api/2024-01/orders/count.json",
                               headers=SHOPIFY_HEADERS, params={"status":"any"}, timeout=10)
        total   = r_all.json().get("count", 0)
        return {"orders_30d": len(orders), "revenue_30d": revenue, "total_orders": total}
    except:
        return None

with st.spinner("Loading overview..."):
    meta     = get_meta_summary()
    shopify  = get_shopify_summary()

st.markdown('<div class="section">Platform Overview</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    meta_spend  = f"${meta['spend']:,.2f}"   if meta else "—"
    meta_clicks = f"{meta['clicks']:,}"       if meta else "—"
    meta_impr   = f"{meta['impressions']:,}"  if meta else "—"
    st.markdown(f"""
    <div class="platform-card" style="border-top:3px solid #3b82f6;">
      <div class="platform-title">Meta Ads</div>
      <div class="platform-metric-label">Total Spend (All Time)</div>
      <div class="platform-metric-value">{meta_spend}</div>
      <div class="platform-metric-label">Link Clicks</div>
      <div class="platform-metric-value" style="font-size:1.2rem;">{meta_clicks}</div>
      <div class="platform-metric-label">Impressions</div>
      <div class="platform-metric-value" style="font-size:1.2rem;">{meta_impr}</div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_Meta_Ads.py", label="View Meta Ads details →")

with col2:
    sh_rev    = f"${shopify['revenue_30d']:,.2f}"  if shopify else "—"
    sh_orders = f"{shopify['orders_30d']:,}"         if shopify else "—"
    sh_total  = f"{shopify['total_orders']:,}"        if shopify else "—"
    st.markdown(f"""
    <div class="platform-card" style="border-top:3px solid #22c55e;">
      <div class="platform-title">Shopify</div>
      <div class="platform-metric-label">Revenue</div>
      <div class="platform-metric-value">{sh_rev}</div>
      <div class="platform-metric-label">Orders</div>
      <div class="platform-metric-value" style="font-size:1.2rem;">{sh_orders}</div>
      <div class="platform-metric-label">Total Orders (All Time)</div>
      <div class="platform-metric-value" style="font-size:1.2rem;">{sh_total}</div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_Shopify.py", label="View Shopify details →")

with col3:
    st.markdown(f"""
    <div class="platform-card" style="border-top:3px solid #8b5cf6;opacity:0.6;">
      <div class="platform-title">Google Ads</div>
      <div style="text-align:center;padding:3rem 1rem;">
        <div style="font-size:0.85rem;font-weight:600;color:{T2};margin-bottom:0.5rem;">Coming Soon</div>
        <div style="font-size:0.75rem;color:{T3};">Google Ads integration is being configured.</div>
      </div>
    </div>
    """, unsafe_allow_html=True)
