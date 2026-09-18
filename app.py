import streamlit as st
import requests
import os
from datetime import timedelta, date, datetime
from PIL import Image
import numpy as np
import pandas as pd
import plotly.graph_objects as go

try:
    from fpdf import FPDF
    FPDF_OK = True
except ImportError:
    FPDF_OK = False

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

ACCESS_TOKEN      = st.secrets["META_ACCESS_TOKEN"]
AD_ACCOUNT_ID     = st.secrets["AD_ACCOUNT_ID"]
IG_AD_ACCOUNT_ID  = "act_8429913163714900"
SHOPIFY_TOKEN     = st.secrets["SHOPIFY_TOKEN"]
SHOP_URL          = st.secrets["SHOP_URL"]
SHOPIFY_HEADERS   = {"X-Shopify-Access-Token": SHOPIFY_TOKEN}

st.set_page_config(page_title="Shpapi · Home", layout="wide", initial_sidebar_state="collapsed")

from auth import check_password
if not check_password():
    st.stop()

if "ai_messages" not in st.session_state:
    st.session_state.ai_messages = []

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
*, *::before, *::after {{ font-family: 'Inter', sans-serif !important; box-sizing: border-box; }}
html, body, .stApp {{ background: {BG} !important; color: {T1}; }}
#MainMenu, footer, header {{ visibility: hidden; }}
.block-container {{ padding: 1.5rem 3rem 4rem 3rem !important; max-width: 100% !important; }}
section[data-testid="stSidebar"] {{ display: none !important; }}
button[data-testid="collapsedControl"],
[data-testid="stSidebarCollapseButton"] {{ display: none !important; }}
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
    min-height: 280px;
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
    font-size: 1.6rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    letter-spacing: -0.5px;
    line-height: 1;
    margin-bottom: 1.2rem;
}}
.section {{ font-size: 0.62rem; font-weight: 600; text-transform: uppercase; letter-spacing: 2.5px; color: {T3}; margin: 0 0 0.9rem 0; display: flex; align-items: center; gap: 1rem; }}
.insights-block {{
    background: {SURFACE};
    border: 1px solid {BORDER};
    border-radius: 16px;
    padding: 1.6rem;
    margin-bottom: 2rem;
}}
.insights-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 1.4rem;
}}
.insight-label {{
    font-size: 0.62rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: {T3};
    margin-bottom: 0.5rem;
}}
.insight-value {{
    font-size: 1.5rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.5px;
    line-height: 1;
}}
.insight-sub {{
    font-size: 0.68rem;
    color: {T3};
    margin-top: 0.4rem;
}}
.insights-footnote {{
    font-size: 0.68rem;
    color: {T3};
    margin-top: 1.4rem;
    padding-top: 1.2rem;
    border-top: 1px solid {BORDER};
    line-height: 1.5;
}}
.section::after {{ content: ''; flex: 1; height: 1px; background: {BORDER}; }}
.surface {{ background: {SURFACE}; border: 1px solid {BORDER}; border-radius: 12px; padding: 1.4rem 1.4rem 0.6rem; margin-bottom: 1rem; }}
.chart-footnote {{ font-size: 0.68rem; color: {T3}; margin: -0.4rem 0 1rem 0; line-height: 1.5; }}
button[data-baseweb="tab"] {{
    background: transparent !important;
    color: {T3} !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
}}
button[data-baseweb="tab"][aria-selected="true"] {{ color: {BLUE} !important; }}
div[data-baseweb="tab-highlight"] {{ background-color: {BLUE} !important; }}
div[data-baseweb="tab-border"] {{ background-color: {BORDER} !important; }}
div[data-testid="stPageLink"] {{
    border: none !important; background: none !important; box-shadow: none !important;
    padding: 0 !important; margin: 0 !important; padding-top: 1rem !important;
}}
a[data-testid="stPageLink-NavLink"] {{
    color: {T2} !important; font-weight: 500 !important; font-size: 0.70rem !important;
    text-decoration: none !important; padding: 0.3rem 0.75rem !important;
    border-radius: 6px !important; background: transparent !important;
    border: none !important; display: inline-block !important;
}}
a[data-testid="stPageLink-NavLink"]:hover {{
    background: rgba(59,130,246,0.15) !important; color: {BLUE} !important;
}}
a[data-testid="stPageLink-NavLink"] svg {{ display: none !important; }}
/* AI chat messages */
[data-testid="stChatMessageContent"] h1,
[data-testid="stChatMessageContent"] h2,
[data-testid="stChatMessageContent"] h3,
[data-testid="stChatMessageContent"] h4 {{
    font-size: 0.82rem !important;
    font-weight: 700 !important;
    margin: 0.5rem 0 0.15rem !important;
    line-height: 1.4 !important;
    color: {T1} !important;
}}
[data-testid="stChatMessageContent"] p,
[data-testid="stChatMessageContent"] li {{
    font-size: 0.82rem !important;
    line-height: 1.6 !important;
    margin: 0 !important;
}}
[data-testid="stChatMessageContent"] ul {{ margin: 0.25rem 0 0.25rem 1rem !important; padding: 0 !important; }}
/* AI input box */
div[data-testid="stForm"] input {{
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid {BORDER} !important;
    border-radius: 10px !important;
    color: {T1} !important;
    font-size: 0.85rem !important;
}}
div[data-testid="stForm"] {{ border: none !important; }}
/* Suggestion chip buttons */
.chip-btn > button {{
    border-radius: 20px !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    background: rgba(255,255,255,0.04) !important;
    color: {T2} !important;
    font-size: 0.75rem !important;
    font-weight: 500 !important;
    padding: 0.4rem 1rem !important;
    white-space: nowrap !important;
    width: 100% !important;
}}
.chip-btn > button:hover {{
    background: rgba(59,130,246,0.12) !important;
    border-color: rgba(59,130,246,0.4) !important;
    color: {BLUE} !important;
}}
</style>
""", unsafe_allow_html=True)

# Nav bar
_c_logo, _c_h, _c_m, _c_s, _c_g, _c_ig, _c_rp, _c_ai, _c_inv, _c_ugc, _ = st.columns([1.5, 1, 1, 1, 1.2, 1.0, 1.0, 0.9, 1.0, 1.3, 0.1])
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
with _c_ig:
    st.page_link("pages/5_Instagram.py", label="Instagram")
with _c_rp:
    st.page_link("pages/6_Report.py", label="Reports")
with _c_ai:
    st.page_link("pages/7_AI_Assistant.py", label="AI Chat")
with _c_inv:
    st.page_link("pages/8_Inventory.py", label="Inventory")
with _c_ugc:
    st.page_link("pages/9_UGC_Creators.py", label="UGC Creators")
st.markdown(f'<div style="border-top:1px solid {BORDER};margin:0.5rem 0 2rem;"></div>', unsafe_allow_html=True)

st.markdown(f"""
<div style="margin-bottom:2rem;">
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
        total_spend   = sum(float(d.get("spend", 0)) for d in rows)
        total_impr    = sum(int(d.get("impressions", 0)) for d in rows)
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

@st.cache_data(ttl=1800)
def get_all_orders_full():
    all_orders = []
    url = f"{SHOP_URL}/admin/api/2024-01/orders.json"
    params = {"status": "any", "limit": 250,
              "fields": "id,created_at,total_price,financial_status,line_items,customer"}
    while url:
        r = requests.get(url, headers=SHOPIFY_HEADERS, params=params, timeout=15)
        data = r.json()
        all_orders.extend(data.get("orders", []))
        next_url = None
        for part in r.headers.get("Link", "").split(","):
            if 'rel="next"' in part:
                next_url = part.split(";")[0].strip().strip("<>")
        url, params = next_url, None
    return all_orders

@st.cache_data(ttl=1800)
def get_business_insights():
    try:
        import datetime as dt
        all_orders = get_all_orders_full()

        now = dt.datetime.now(dt.timezone.utc)
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

        revenue_orders = [o for o in all_orders if o.get("financial_status") in ("paid", "partially_refunded")]
        total_revenue  = sum(float(o["total_price"]) for o in revenue_orders)
        revenue_mtd    = sum(float(o["total_price"]) for o in revenue_orders
                              if dt.datetime.fromisoformat(o["created_at"]) >= month_start)

        total_orders = len(all_orders)
        orders_mtd   = sum(1 for o in all_orders if dt.datetime.fromisoformat(o["created_at"]) >= month_start)
        units_sold   = sum(item.get("quantity", 0) for o in all_orders for item in o.get("line_items", []))
        aov          = (total_revenue / len(revenue_orders)) if revenue_orders else 0

        refunded     = sum(1 for o in all_orders if o.get("financial_status") in ("refunded", "partially_refunded"))
        refund_rate  = (refunded / total_orders) if total_orders else 0

        cust_orders, cust_first_date = {}, {}
        for o in all_orders:
            c = o.get("customer")
            if not c:
                continue
            cid = c["id"]
            cust_orders[cid] = cust_orders.get(cid, 0) + 1
            d = dt.datetime.fromisoformat(o["created_at"])
            if cid not in cust_first_date or d < cust_first_date[cid]:
                cust_first_date[cid] = d

        unique_customers = len(cust_orders)
        repeat_customers = sum(1 for v in cust_orders.values() if v > 1)
        repeat_rate       = (repeat_customers / unique_customers) if unique_customers else 0

        return {
            "total_revenue": total_revenue,
            "revenue_mtd": revenue_mtd,
            "total_orders": total_orders,
            "orders_mtd": orders_mtd,
            "units_sold": units_sold,
            "aov": aov,
            "refund_rate": refund_rate,
            "repeat_rate": repeat_rate,
            "unique_customers": unique_customers,
        }
    except Exception:
        return None

@st.cache_data(ttl=1800)
def get_shopify_growth_monthly():
    """All-time monthly orders, revenue, and new-vs-repeat customers."""
    try:
        all_orders = get_all_orders_full()
        if not all_orders:
            return None

        rows = []
        for o in all_orders:
            cust = o.get("customer")
            rows.append({
                "date": pd.to_datetime(o["created_at"]).tz_localize(None),
                "revenue": float(o["total_price"]) if o.get("financial_status") in ("paid", "partially_refunded") else 0.0,
                "customer_id": cust["id"] if cust else None,
            })
        df = pd.DataFrame(rows)
        df["month"] = df["date"].dt.to_period("M")

        monthly = df.groupby("month").agg(orders=("date", "size"), revenue=("revenue", "sum")).reset_index()

        wc = df.dropna(subset=["customer_id"]).copy()
        if wc.empty:
            monthly["new_customers"] = 0
            monthly["repeat_customers"] = 0
        else:
            first_month = wc.groupby("customer_id")["month"].min()
            wc["first_month"] = wc["customer_id"].map(first_month)
            wc["segment"] = np.where(wc["month"] == wc["first_month"], "new", "repeat")
            cust_monthly = (wc.groupby(["month", "segment"])["customer_id"]
                              .nunique().unstack(fill_value=0)
                              .reindex(columns=["new", "repeat"], fill_value=0)
                              .rename(columns={"new": "new_customers", "repeat": "repeat_customers"})
                              .reset_index())
            monthly = monthly.merge(cust_monthly, on="month", how="left").fillna(0)
        monthly = monthly.sort_values("month")
        monthly["month_str"] = monthly["month"].astype(str)
        return monthly
    except Exception:
        return None

@st.cache_data(ttl=3600)
def get_ad_growth_monthly(account_id, token):
    """All-time monthly spend/impressions/reach/clicks for a Meta ad account (Ads or Instagram)."""
    try:
        r = requests.get(
            f"https://graph.facebook.com/v19.0/{account_id}/insights",
            params={"fields": "spend,impressions,reach,actions",
                    "date_preset": "maximum", "level": "account",
                    "time_increment": "monthly", "access_token": token},
            timeout=20,
        )
        rows = r.json().get("data", [])
        out = []
        for d in rows:
            clicks = 0
            for a in d.get("actions", []):
                if a.get("action_type") == "link_click":
                    clicks += int(float(a["value"]))
            out.append({
                "month_str": d["date_start"][:7],
                "spend": float(d.get("spend", 0)),
                "impressions": int(d.get("impressions", 0)),
                "reach": int(d.get("reach", 0)),
                "clicks": clicks,
            })
        return pd.DataFrame(out) if out else None
    except Exception:
        return None

@st.cache_data(ttl=3600)
def get_google_growth_monthly():
    """All-time monthly spend/impressions/clicks for Google Ads."""
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
        client = GoogleAdsClient.load_from_dict(config)
        ga_service = client.get_service("GoogleAdsService")
        customer_id = cfg["client_customer_id"].replace("-", "")
        query = """
            SELECT segments.date, metrics.impressions, metrics.clicks, metrics.cost_micros
            FROM campaign
            WHERE segments.date BETWEEN '2020-01-01' AND '2099-12-31'
              AND campaign.status != 'REMOVED'
        """
        response = ga_service.search(customer_id=customer_id, query=query)
        rows = [{"date": row.segments.date,
                 "spend": row.metrics.cost_micros / 1_000_000,
                 "impressions": row.metrics.impressions,
                 "clicks": row.metrics.clicks} for row in response]
        if not rows:
            return None
        df = pd.DataFrame(rows)
        df["month_str"] = pd.to_datetime(df["date"]).dt.to_period("M").astype(str)
        return df.groupby("month_str", as_index=False).agg(
            spend=("spend", "sum"), impressions=("impressions", "sum"), clicks=("clicks", "sum"))
    except Exception:
        return None

@st.cache_data(ttl=3600)
def get_google_ads_summary():
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
        client = GoogleAdsClient.load_from_dict(config)
        ga_service = client.get_service("GoogleAdsService")
        customer_id = cfg["client_customer_id"].replace("-", "")
        query = """
            SELECT metrics.impressions, metrics.clicks, metrics.cost_micros, metrics.conversions
            FROM campaign
            WHERE segments.date BETWEEN '2020-01-01' AND '2099-12-31'
              AND campaign.status != 'REMOVED'
        """
        response = ga_service.search(customer_id=customer_id, query=query)
        total_spend = 0.0
        total_clicks = 0
        total_impressions = 0
        total_conversions = 0.0
        for row in response:
            total_spend += row.metrics.cost_micros / 1_000_000
            total_clicks += row.metrics.clicks
            total_impressions += row.metrics.impressions
            total_conversions += row.metrics.conversions
        return {"spend": total_spend, "clicks": total_clicks,
                "impressions": total_impressions, "conversions": total_conversions}
    except Exception:
        return None

@st.cache_data(ttl=1800)
def get_instagram_summary():
    try:
        r = requests.get(
            f"https://graph.facebook.com/v19.0/{IG_AD_ACCOUNT_ID}/insights",
            params={"fields": "spend,reach,impressions,actions", "level": "account",
                    "date_preset": "maximum", "access_token": ACCESS_TOKEN},
            timeout=15,
        )
        d = r.json().get("data", [{}])[0]
        clicks = 0
        for a in d.get("actions", []):
            if a.get("action_type") == "link_click":
                clicks = int(float(a["value"]))
        return {"spend": float(d.get("spend", 0)), "reach": int(d.get("reach", 0)),
                "impressions": int(d.get("impressions", 0)), "clicks": clicks}
    except:
        return None

def _last_active_date(account_id):
    """Most recent date this ad account had any impressions."""
    try:
        rows, url = [], f"https://graph.facebook.com/v19.0/{account_id}/insights"
        params = {"fields": "impressions", "level": "account", "date_preset": "maximum",
                   "time_increment": 1, "access_token": ACCESS_TOKEN, "limit": 500}
        while url:
            r = requests.get(url, params=params, timeout=15)
            data = r.json()
            rows.extend(data.get("data", []))
            url    = data.get("paging", {}).get("next")
            params = {}
        active_dates = [d["date_start"] for d in rows if int(d.get("impressions", 0)) > 0]
        return max(active_dates) if active_dates else None
    except Exception:
        return None

def _days_since(date_str):
    if not date_str:
        return None
    return (date.today() - datetime.strptime(date_str, "%Y-%m-%d").date()).days

@st.cache_data(ttl=300)
def get_meta_live_status():
    try:
        r = requests.get(
            f"https://graph.facebook.com/v19.0/{AD_ACCOUNT_ID}/campaigns",
            params={"fields": "id,name,effective_status,updated_time",
                    "limit": 500, "access_token": ACCESS_TOKEN},
            timeout=15,
        )
        camps = r.json().get("data", [])
        if not camps:
            return None
        active = [c for c in camps if c.get("effective_status") == "ACTIVE"]
        pool    = active if active else camps
        current = max(pool, key=lambda c: c.get("updated_time", ""))
        if active:
            return {"status": "live", "campaign_name": current.get("name"), "days_since": 0}
        return {"status": "paused", "campaign_name": current.get("name"),
                "days_since": _days_since(_last_active_date(AD_ACCOUNT_ID))}
    except Exception:
        return None

@st.cache_data(ttl=300)
def get_instagram_live_status():
    try:
        r = requests.get(
            f"https://graph.facebook.com/v19.0/{IG_AD_ACCOUNT_ID}/campaigns",
            params={"fields": "id,name,effective_status,updated_time",
                    "limit": 500, "access_token": ACCESS_TOKEN},
            timeout=15,
        )
        camps = r.json().get("data", [])
        if not camps:
            return None
        active = [c for c in camps if c.get("effective_status") == "ACTIVE"]
        pool    = active if active else camps
        current = max(pool, key=lambda c: c.get("updated_time", ""))
        if active:
            return {"status": "live", "campaign_name": current.get("name"), "days_since": 0}
        return {"status": "paused", "campaign_name": current.get("name"),
                "days_since": _days_since(_last_active_date(IG_AD_ACCOUNT_ID))}
    except Exception:
        return None

@st.cache_data(ttl=300)
def get_google_live_status():
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
        client = GoogleAdsClient.load_from_dict(config)
        ga_service = client.get_service("GoogleAdsService")
        customer_id = cfg["client_customer_id"].replace("-", "")
        query = """
            SELECT campaign.name, campaign.status, campaign.start_date_time
            FROM campaign
            WHERE campaign.status != 'REMOVED'
        """
        response = ga_service.search(customer_id=customer_id, query=query)
        camps = [{"name": row.campaign.name, "status": row.campaign.status.name,
                   "start": row.campaign.start_date_time} for row in response]
        if not camps:
            return None
        active   = [c for c in camps if c["status"] == "ENABLED"]
        pool     = active if active else camps
        current  = max(pool, key=lambda c: c["start"])
        if active:
            return {"status": "live", "campaign_name": current["name"], "days_since": 0}

        today_str = date.today().isoformat()
        q2 = f"""
            SELECT segments.date, metrics.impressions
            FROM campaign
            WHERE segments.date BETWEEN '2020-01-01' AND '{today_str}'
              AND campaign.status != 'REMOVED'
        """
        resp2 = ga_service.search(customer_id=customer_id, query=q2)
        active_dates = [row.segments.date for row in resp2 if row.metrics.impressions > 0]
        last_active  = max(active_dates) if active_dates else None
        return {"status": "paused", "campaign_name": current["name"],
                "days_since": _days_since(last_active)}
    except Exception:
        return None

with st.spinner("Loading overview..."):
    meta      = get_meta_summary()
    shopify   = get_shopify_summary()
    instagram = get_instagram_summary()
    google    = get_google_ads_summary()
    insights  = get_business_insights()

with st.spinner("Loading live campaign status..."):
    meta_live   = get_meta_live_status()
    google_live = get_google_live_status()
    ig_live     = get_instagram_live_status()

def _ctr_str(summary):
    if not summary or not summary.get("impressions"):
        return "—"
    return f"{(summary.get('clicks', 0) / summary['impressions'] * 100):.2f}%"

def _live_row(label, color, summary, live, is_last):
    live = live or {}
    name = live.get("campaign_name") or "—"
    ctr  = _ctr_str(summary)
    if live.get("status") == "live":
        status_html = (
            '<span style="display:inline-flex;align-items:center;gap:0.45rem;">'
            '<span style="width:7px;height:7px;border-radius:50%;background:#22c55e;'
            'box-shadow:0 0 6px #22c55e;display:inline-block;"></span>'
            '<span style="font-size:0.72rem;font-weight:700;text-transform:uppercase;'
            f'letter-spacing:1px;color:#22c55e;">Live</span></span>'
        )
    elif live.get("status") == "paused" and live.get("days_since") is not None:
        d = live["days_since"]
        status_html = f'<span style="font-size:0.8rem;color:{T2};">{d} day{"s" if d != 1 else ""} since last ad</span>'
    else:
        status_html = f'<span style="font-size:0.8rem;color:{T3};">No data</span>'
    border = f"border-bottom:1px solid {BORDER};" if not is_last else ""
    return f"""
    <tr style="{border}">
      <td style="padding:1rem 1.4rem;">
        <div style="display:flex;align-items:center;gap:0.65rem;">
          <span style="width:8px;height:8px;border-radius:50%;background:{color};display:inline-block;flex-shrink:0;"></span>
          <div>
            <div style="font-size:0.6rem;font-weight:700;text-transform:uppercase;letter-spacing:1.2px;color:{T3};">{label}</div>
            <div style="font-size:0.85rem;font-weight:600;color:{T1};">{name}</div>
          </div>
        </div>
      </td>
      <td style="padding:1rem 1.4rem;font-size:0.95rem;font-weight:700;color:{T1};">{ctr}</td>
      <td style="padding:1rem 1.4rem;">{status_html}</td>
    </tr>"""

_platform_rows = [
    ("Meta Ads",   "#3b82f6", meta,      meta_live),
    ("Google Ads", "#8b5cf6", google,    google_live),
    ("Instagram",  "#ec4899", instagram, ig_live),
]
_rows_html = "".join(
    _live_row(label, color, summary, live, i == len(_platform_rows) - 1)
    for i, (label, color, summary, live) in enumerate(_platform_rows)
)

st.markdown('<div class="section">Live Campaigns</div>', unsafe_allow_html=True)
st.markdown(f"""
<div style="background:{SURFACE};border:1px solid {BORDER};border-radius:12px;overflow:hidden;margin-bottom:2rem;">
  <table style="width:100%;border-collapse:collapse;">
    <thead>
      <tr style="border-bottom:1px solid {BORDER};">
        <th style="text-align:left;padding:0.85rem 1.4rem;font-size:0.6rem;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;color:{T3};">Platform &amp; Current Campaign</th>
        <th style="text-align:left;padding:0.85rem 1.4rem;font-size:0.6rem;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;color:{T3};">CTR &nbsp;·&nbsp; % of people who clicked your ad after seeing it</th>
        <th style="text-align:left;padding:0.85rem 1.4rem;font-size:0.6rem;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;color:{T3};">Status</th>
      </tr>
    </thead>
    <tbody>
      {_rows_html}
    </tbody>
  </table>
</div>
""", unsafe_allow_html=True)

with st.spinner("Loading growth history..."):
    growth_shopify     = get_shopify_growth_monthly()
    growth_meta        = get_ad_growth_monthly(AD_ACCOUNT_ID, ACCESS_TOKEN)
    growth_instagram   = get_ad_growth_monthly(IG_AD_ACCOUNT_ID, ACCESS_TOKEN)
    growth_google      = get_google_growth_monthly()

# ── Business Insights ──────────────────────────────────────────────────────────
st.markdown('<div class="section">Business Insights</div>', unsafe_allow_html=True)

if insights:
    total_spend = sum(x["spend"] for x in (meta, google, instagram) if x)
    roas = (insights["total_revenue"] / total_spend) if total_spend else None
    cac  = (total_spend / insights["unique_customers"]) if total_spend and insights["unique_customers"] else None

    tiles = [
        ("Total Revenue", f"${insights['total_revenue']:,.2f}", "All time"),
        ("Revenue MTD", f"${insights['revenue_mtd']:,.2f}", "Month to date"),
        ("Orders", f"{insights['total_orders']:,}", f"{insights['orders_mtd']:,} MTD"),
        ("Units Sold", f"{insights['units_sold']:,}", "All time"),
        ("Avg. Order Value", f"${insights['aov']:,.2f}", "Revenue ÷ orders"),
        ("ROAS", f"{roas:.2f}x" if roas is not None else "—", "Revenue ÷ ad spend"),
        ("Est. CAC", f"${cac:,.2f}" if cac is not None else "—", "Ad spend ÷ customers"),
        ("Repeat Purchase Rate", f"{insights['repeat_rate']*100:.1f}%", "Customers who bought again"),
        ("Refund Rate", f"{insights['refund_rate']*100:.1f}%", "Of all orders"),
    ]
    tiles_html = "".join(f"""
      <div class="insight-tile">
        <div class="insight-label">{label}</div>
        <div class="insight-value">{value}</div>
        <div class="insight-sub">{sub}</div>
      </div>""" for label, value, sub in tiles)

    st.markdown(f"""
    <div class="insights-block">
      <div class="insights-grid">{tiles_html}</div>
      <div class="insights-footnote">
        Gross/net margin, conversion rate, cart abandonment, checkout funnel, and channel-level CAC/ROAS
        need additional setup (product cost data, and site/session tracking) not yet connected.
      </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f'<div style="background:{SURFACE};border:1px solid {BORDER};border-radius:12px;padding:1.5rem;text-align:center;color:{T3};font-size:0.85rem;">Business insights unavailable — could not load Shopify order data.</div>', unsafe_allow_html=True)

# ── Growth Over Time ────────────────────────────────────────────────────────────
st.markdown('<div class="section">Growth Over Time</div>', unsafe_allow_html=True)

def _rgba(hex_color, alpha):
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f"rgba({r},{g},{b},{alpha})"

def _axis_layout(height, showlegend=False):
    return dict(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=T2, family="Inter"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.06)", zeroline=False, tickfont=dict(size=10, color=T2)),
        yaxis=dict(gridcolor="rgba(255,255,255,0.06)", zeroline=False, tickfont=dict(size=10, color=T2)),
        margin=dict(l=0, r=0, t=10, b=0), height=height, showlegend=showlegend,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, x=0, font=dict(color=T2, size=10)),
    )

def _monthly_line_chart(x, y, color, prefix="", height=260):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y, mode="lines+markers",
        line=dict(color=color, width=2), marker=dict(color=color, size=5),
        fill="tozeroy", fillcolor=_rgba(color, 0.12),
        hovertemplate="<b>%{x}</b><br>%{y:,.2f}<extra></extra>",
    ))
    layout = _axis_layout(height)
    layout["yaxis"]["tickprefix"] = prefix
    fig.update_layout(**layout)
    st.plotly_chart(fig, use_container_width=True)

def _multi_line_chart(long_df, metric, color_map, prefix="", height=280):
    fig, plotted = go.Figure(), False
    for platform, sub in long_df.groupby("platform"):
        sub = sub.sort_values("month_str")
        if metric not in sub.columns or sub[metric].fillna(0).sum() == 0:
            continue
        fig.add_trace(go.Scatter(
            x=sub["month_str"], y=sub[metric], mode="lines+markers", name=platform,
            line=dict(width=2, color=color_map.get(platform)),
        ))
        plotted = True
    if not plotted:
        st.markdown(f'<div style="text-align:center;padding:2rem;color:{T3};">No data available.</div>', unsafe_allow_html=True)
        return
    layout = _axis_layout(height, showlegend=True)
    layout["yaxis"]["tickprefix"] = prefix
    fig.update_layout(**layout)
    st.plotly_chart(fig, use_container_width=True)

_ad_parts = []
for _df, _label in [(growth_meta, "Meta Ads"), (growth_instagram, "Instagram"), (growth_google, "Google Ads")]:
    if _df is not None and not _df.empty:
        _d = _df.copy()
        _d["platform"] = _label
        _ad_parts.append(_d)
ad_long   = pd.concat(_ad_parts, ignore_index=True) if _ad_parts else None
AD_COLORS = {"Meta Ads": "#3b82f6", "Instagram": "#ec4899", "Google Ads": "#8b5cf6"}

tab_rev, tab_cust, tab_ads, tab_brand = st.tabs(["Orders & Revenue", "Customers", "Ad Traction", "Brand Recognition"])

with tab_rev:
    st.markdown('<div class="surface">', unsafe_allow_html=True)
    if growth_shopify is not None and not growth_shopify.empty:
        st.markdown('<div class="platform-metric-label">Monthly Revenue — All Time Since Launch</div>', unsafe_allow_html=True)
        _monthly_line_chart(growth_shopify["month_str"], growth_shopify["revenue"], "#22c55e", prefix="$")
        st.markdown('<div class="platform-metric-label" style="margin-top:1rem;">Monthly Orders — All Time Since Launch</div>', unsafe_allow_html=True)
        fig_o = go.Figure(go.Bar(x=growth_shopify["month_str"], y=growth_shopify["orders"],
                                  marker=dict(color="#22c55e", opacity=0.85),
                                  hovertemplate="<b>%{x}</b><br>Orders: %{y}<extra></extra>"))
        fig_o.update_layout(**_axis_layout(220))
        st.plotly_chart(fig_o, use_container_width=True)
    else:
        st.markdown(f'<div style="text-align:center;padding:2rem;color:{T3};">No order history available.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab_cust:
    st.markdown('<div class="surface">', unsafe_allow_html=True)
    if growth_shopify is not None and not growth_shopify.empty:
        st.markdown('<div class="platform-metric-label">New vs. Repeat Customers — All Time Since Launch</div>', unsafe_allow_html=True)
        fig_c = go.Figure()
        fig_c.add_trace(go.Bar(x=growth_shopify["month_str"], y=growth_shopify["new_customers"],
                                name="New", marker=dict(color="#3b82f6")))
        fig_c.add_trace(go.Bar(x=growth_shopify["month_str"], y=growth_shopify["repeat_customers"],
                                name="Repeat", marker=dict(color="#22c55e")))
        layout = _axis_layout(280, showlegend=True)
        layout["barmode"] = "stack"
        fig_c.update_layout(**layout)
        st.plotly_chart(fig_c, use_container_width=True)
    else:
        st.markdown(f'<div style="text-align:center;padding:2rem;color:{T3};">No customer history available.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab_ads:
    st.markdown('<div class="surface">', unsafe_allow_html=True)
    if ad_long is not None:
        st.markdown('<div class="platform-metric-label">Monthly Ad Spend by Platform — All Time Since Launch</div>', unsafe_allow_html=True)
        _multi_line_chart(ad_long, "spend", AD_COLORS, prefix="$")
        st.markdown('<div class="platform-metric-label" style="margin-top:1rem;">Monthly Impressions by Platform — All Time Since Launch</div>', unsafe_allow_html=True)
        _multi_line_chart(ad_long, "impressions", AD_COLORS)
    else:
        st.markdown(f'<div style="text-align:center;padding:2rem;color:{T3};">No ad history available.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with tab_brand:
    st.markdown('<div class="surface">', unsafe_allow_html=True)
    if ad_long is not None:
        st.markdown('<div class="platform-metric-label">Monthly Reach by Platform — All Time Since Launch</div>', unsafe_allow_html=True)
        _multi_line_chart(ad_long, "reach", AD_COLORS)
        st.markdown(f"""
        <div class="chart-footnote">
          Reach here is paid reach from Meta &amp; Instagram ads — unique people your brand has been shown to.
          Organic follower/account growth isn't tracked yet because only the ad account is connected, not the
          Instagram Business Account — connecting it would let us chart true follower growth over time.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="text-align:center;padding:2rem;color:{T3};">No reach history available.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div style="height:1.5rem;"></div>', unsafe_allow_html=True)

# ── AI Growth Analyst (inline, above platform cards) ──────────────────────────
st.markdown('<div class="section">AI Growth Analyst</div>', unsafe_allow_html=True)

st.markdown(f"""
<div style="background:{SURFACE};border:1px solid {BORDER};border-radius:12px;
            padding:1.25rem 1.5rem;margin-bottom:1rem;">
  <div style="font-size:0.82rem;color:{T2};">
    Ask anything about your ads, revenue, or growth — powered by Claude AI.
  </div>
</div>
""", unsafe_allow_html=True)

with st.form("ai_form", clear_on_submit=True, border=False):
    user_q    = st.text_input("Ask AI", placeholder="Type your question here...", label_visibility="collapsed")
    submitted = st.form_submit_button("Ask →", use_container_width=False)
    if submitted and user_q:
        st.session_state.ai_messages.append({"role": "user", "content": user_q})

suggested = ["What are my top 3 growth opportunities?", "Why is my ROAS low?", "How can I improve my conversion rate?"]
s1, s2, s3 = st.columns(3)
for col, q in zip([s1, s2, s3], suggested):
    with col:
        st.markdown('<div class="chip-btn">', unsafe_allow_html=True)
        if st.button(q, key=f"suggest_{q[:20]}", use_container_width=True):
            st.session_state.ai_messages.append({"role": "user", "content": q})
        st.markdown('</div>', unsafe_allow_html=True)

if st.session_state.ai_messages:
    for msg in st.session_state.ai_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    last = st.session_state.ai_messages[-1]
    if last["role"] == "user":
        with st.chat_message("assistant"):
            with st.spinner("Analyzing your data..."):
                try:
                    import anthropic as ac
                    client   = ac.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
                    meta_ctx = (f"Spend ${meta['spend']:,.2f} (all-time) | Clicks {meta['clicks']:,} | "
                                f"Impressions {meta['impressions']:,}") if meta else "unavailable"
                    shop_ctx = (f"Revenue ${shopify['revenue_30d']:,.2f} (last 30d) | "
                                f"Orders {shopify['orders_30d']} (30d) | "
                                f"Total orders all-time {shopify['total_orders']}") if shopify else "unavailable"
                    ig_ctx   = (f"Spend ${instagram['spend']:,.2f} | Reach {instagram['reach']:,} | "
                                f"Impressions {instagram['impressions']:,}") if instagram else "unavailable"
                    g_ctx    = (f"Spend ${google['spend']:,.2f} | Clicks {google['clicks']:,} | "
                                f"Impressions {google['impressions']:,} | "
                                f"Conversions {google['conversions']:.1f}") if google else "unavailable"
                    system_p = f"""You are the AI growth analyst for Shpapi, a sunglasses and clothing brand. \
Speak directly like a trusted advisor — plain sentences, no corporate jargon. \
Always reference the actual numbers. Keep responses concise (under 200 words).

LIVE DATA (all-time unless noted):
- Meta Ads: {meta_ctx}
- Instagram Boosts: {ig_ctx}
- Shopify: {shop_ctx}
- Google Ads: {g_ctx}"""
                    resp = client.messages.create(
                        model="claude-opus-5",
                        max_tokens=600,
                        system=system_p,
                        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.ai_messages]
                    )
                    answer = next((b.text for b in resp.content if hasattr(b, "text")), "")
                    st.markdown(answer)
                    st.session_state.ai_messages.append({"role": "assistant", "content": answer})
                except Exception as e:
                    st.error(f"AI unavailable: {e}")

    if st.button("Clear conversation", key="clear_ai"):
        st.session_state.ai_messages = []
        st.rerun()

st.markdown('<div style="height:1.5rem;"></div>', unsafe_allow_html=True)

# ── Platform Overview ─────────────────────────────────────────────────────────
st.markdown('<div class="section">Platform Overview</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4, gap="medium")

with col1:
    meta_spend  = f"${meta['spend']:,.2f}"  if meta else "—"
    meta_clicks = f"{meta['clicks']:,}"      if meta else "—"
    meta_impr   = f"{meta['impressions']:,}" if meta else "—"
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
    sh_rev    = f"${shopify['revenue_30d']:,.2f}" if shopify else "—"
    sh_orders = f"{shopify['orders_30d']:,}"       if shopify else "—"
    sh_total  = f"{shopify['total_orders']:,}"     if shopify else "—"
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
    if google:
        g_spend = f"${google['spend']:,.2f}"
        g_clicks = f"{google['clicks']:,}"
        g_impr = f"{google['impressions']:,}"
        st.markdown(f"""
        <div class="platform-card" style="border-top:3px solid #8b5cf6;">
          <div class="platform-title">Google Ads</div>
          <div class="platform-metric-label">Total Spend (All Time)</div>
          <div class="platform-metric-value">{g_spend}</div>
          <div class="platform-metric-label">Clicks</div>
          <div class="platform-metric-value" style="font-size:1.2rem;">{g_clicks}</div>
          <div class="platform-metric-label">Impressions</div>
          <div class="platform-metric-value" style="font-size:1.2rem;">{g_impr}</div>
        </div>
        """, unsafe_allow_html=True)
        st.page_link("pages/3_Google_Ads.py", label="View Google Ads details →")
    else:
        st.markdown(f"""
        <div class="platform-card" style="border-top:3px solid #8b5cf6;opacity:0.6;">
          <div class="platform-title">Google Ads</div>
          <div style="text-align:center;padding:3rem 1rem;">
            <div style="font-size:0.85rem;font-weight:600;color:{T2};margin-bottom:0.5rem;">No Data</div>
            <div style="font-size:0.75rem;color:{T3};">No campaign activity found.</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.page_link("pages/3_Google_Ads.py", label="View Google Ads →")

with col4:
    if instagram:
        st.markdown(f"""
        <div class="platform-card" style="border-top:3px solid #ec4899;">
          <div class="platform-title">Instagram Boosts</div>
          <div class="platform-metric-label">Total Spend (All Time)</div>
          <div class="platform-metric-value">${instagram['spend']:,.2f}</div>
          <div class="platform-metric-label">Reach</div>
          <div class="platform-metric-value" style="font-size:1.2rem;">{instagram['reach']:,}</div>
          <div class="platform-metric-label">Impressions</div>
          <div class="platform-metric-value" style="font-size:1.2rem;">{instagram['impressions']:,}</div>
        </div>
        """, unsafe_allow_html=True)
        st.page_link("pages/5_Instagram.py", label="View Instagram details →")
    else:
        st.markdown(f"""
        <div class="platform-card" style="border-top:3px solid #ec4899;opacity:0.7;">
          <div class="platform-title">Instagram Boosts</div>
          <div style="text-align:center;padding:3rem 1rem;">
            <div style="font-size:0.85rem;font-weight:600;color:{T2};margin-bottom:0.5rem;">No Data</div>
            <div style="font-size:0.75rem;color:{T3};">No boost activity in the last 30 days.</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.page_link("pages/5_Instagram.py", label="View Instagram →")

# ── PDF Export ────────────────────────────────────────────────────────────────
st.markdown('<div style="height:1.5rem;"></div>', unsafe_allow_html=True)
st.markdown('<div class="section">Export</div>', unsafe_allow_html=True)

if not FPDF_OK:
    st.info("PDF export will be available after the next deploy (fpdf2 is installing).")
else:
    def _build_dashboard_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_margins(16, 16, 16)
        pdf.set_auto_page_break(auto=True, margin=20)

        # Header
        pdf.set_fill_color(10, 22, 40)
        pdf.rect(0, 0, 210, 38, "F")
        pdf.set_font("Helvetica", "B", 22)
        pdf.set_text_color(255, 255, 255)
        pdf.set_xy(0, 7)
        pdf.cell(210, 10, "SHPAPI", align="C")
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(150, 165, 190)
        pdf.set_xy(0, 20)
        pdf.cell(210, 6, f"Analytics Dashboard Export  -  {date.today().strftime('%B %d, %Y')}", align="C")
        pdf.set_y(46)

        def _section(title):
            pdf.set_font("Helvetica", "B", 8)
            pdf.set_text_color(80, 100, 140)
            pdf.cell(0, 5, title, ln=True)
            pdf.set_draw_color(59, 130, 246)
            pdf.line(16, pdf.get_y(), 194, pdf.get_y())
            pdf.ln(4)

        def _card(x, y, w, h, title, rows, accent_rgb):
            pdf.set_fill_color(14, 31, 60)
            pdf.set_draw_color(25, 45, 75)
            pdf.rect(x, y, w, h, "FD")
            pdf.set_fill_color(*accent_rgb)
            pdf.rect(x, y, w, 2, "F")
            pdf.set_font("Helvetica", "B", 7)
            pdf.set_text_color(120, 140, 175)
            pdf.set_xy(x + 4, y + 5)
            pdf.cell(w - 8, 4, title.upper())
            oy = y + 12
            for label, value in rows:
                pdf.set_font("Helvetica", "", 6)
                pdf.set_text_color(110, 130, 165)
                pdf.set_xy(x + 4, oy)
                pdf.cell(w - 8, 3.5, label.upper())
                oy += 4
                pdf.set_font("Helvetica", "B", 11)
                pdf.set_text_color(240, 245, 255)
                pdf.set_xy(x + 4, oy)
                pdf.cell(w - 8, 6, value)
                oy += 8

        _section("PLATFORM OVERVIEW")

        cw, gap = 85, 8
        x1, x2  = 16, 16 + cw + gap
        ch       = 72
        y0       = pdf.get_y()

        # Meta Ads
        _card(x1, y0, cw, ch, "Meta Ads", [
            ("Total Spend (All Time)", f"${meta['spend']:,.2f}" if meta else "-"),
            ("Link Clicks",            f"{meta['clicks']:,}"   if meta else "-"),
            ("Impressions",            f"{meta['impressions']:,}" if meta else "-"),
        ], (59, 130, 246))

        # Shopify
        _card(x2, y0, cw, ch, "Shopify", [
            ("Revenue (Last 30 Days)", f"${shopify['revenue_30d']:,.2f}" if shopify else "-"),
            ("Orders (Last 30 Days)",  f"{shopify['orders_30d']:,}"       if shopify else "-"),
            ("Total Orders (All Time)",f"{shopify['total_orders']:,}"     if shopify else "-"),
        ], (34, 197, 94))

        y1 = y0 + ch + gap

        # Google Ads
        _card(x1, y1, cw, ch, "Google Ads", [
            ("Total Spend (All Time)", f"${google['spend']:,.2f}"       if google else "-"),
            ("Clicks",                 f"{google['clicks']:,}"           if google else "-"),
            ("Impressions",            f"{google['impressions']:,}"      if google else "-"),
        ], (139, 92, 246))

        # Instagram
        _card(x2, y1, cw, ch, "Instagram Boosts", [
            ("Total Spend (All Time)", f"${instagram['spend']:,.2f}"     if instagram else "-"),
            ("Reach",                  f"{instagram['reach']:,}"          if instagram else "-"),
            ("Impressions",            f"{instagram['impressions']:,}"    if instagram else "-"),
        ], (236, 72, 153))

        pdf.set_y(y1 + ch + 10)

        # Footer
        pdf.set_y(-16)
        pdf.set_font("Helvetica", "", 7)
        pdf.set_text_color(110, 130, 165)
        pdf.cell(0, 5, f"Generated by Shpapi Vision  ·  shpapivision.streamlit.app  ·  {date.today().strftime('%B %d, %Y')}", align="C")

        return bytes(pdf.output())

    st.download_button(
        label="Download Dashboard PDF",
        data=_build_dashboard_pdf(),
        file_name=f"shpapi_dashboard_{date.today().strftime('%Y-%m-%d')}.pdf",
        mime="application/pdf",
    )
