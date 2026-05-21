import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import os
from datetime import datetime, timedelta

SHOPIFY_TOKEN = st.secrets["SHOPIFY_TOKEN"]
SHOP_URL      = st.secrets["SHOP_URL"]
HEADERS       = {"X-Shopify-Access-Token": SHOPIFY_TOKEN, "Content-Type": "application/json"}
ASSETS        = os.path.join(os.path.dirname(__file__), "..", "assets")
LOGO_CROP     = os.path.join(ASSETS, "logo_cropped.png")

BG      = "#0a1628"
SURFACE = "#0e1f3c"
BORDER  = "rgba(255,255,255,0.08)"
T1      = "#ffffff"
T2      = "rgba(255,255,255,0.65)"
T3      = "rgba(255,255,255,0.38)"
BLUE    = "#3b82f6"
CHART_C = "#3b82f6"

st.set_page_config(page_title="Shpapi · Shopify", layout="wide", initial_sidebar_state="collapsed")

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
.stat-grid {{ display: grid; grid-template-columns: repeat(4,1fr); gap: 1rem; margin-bottom: 2.4rem; }}
.stat {{ background: rgba(0,0,0,0.02); border: 1px solid rgba(0,0,0,0.06); border-radius: 10px; padding: 1rem 1.4rem; }}
.stat-label {{ font-size: 0.6rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1.8px; color: {T3}; margin-bottom: 0.4rem; }}
.stat-value {{ font-size: 1.15rem; font-weight: 600; color: #ffffff; letter-spacing: -0.3px; line-height: 1; }}
.section {{ font-size: 0.62rem; font-weight: 600; text-transform: uppercase; letter-spacing: 2.5px; color: {T3}; margin: 0 0 0.9rem 0; display: flex; align-items: center; gap: 1rem; }}
.section::after {{ content: ''; flex: 1; height: 1px; background: {BORDER}; }}
.surface {{ background: {SURFACE}; border: 1px solid {BORDER}; border-radius: 12px; padding: 1.4rem 1.4rem 0.6rem; margin-bottom: 1rem; }}
div[data-testid="stDataFrame"] > div {{ background: {SURFACE} !important; border: 1px solid {BORDER} !important; border-radius: 12px !important; }}
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
a[data-testid="stPageLink-NavLink"] {{
    color: {T2} !important; font-weight: 600 !important; font-size: 0.8rem !important;
    text-decoration: none !important; padding: 0.35rem 0.9rem !important;
    border-radius: 6px !important; background: transparent !important; display: inline-block;
}}
a[data-testid="stPageLink-NavLink"]:hover {{
    background: rgba(59,130,246,0.18) !important; color: {BLUE} !important;
}}
div[data-testid="stPageLink"] {{ padding-top: 0.85rem; }}
</style>
""", unsafe_allow_html=True)

_c_logo, _c_h, _c_m, _c_s, _c_g, _ = st.columns([1.5, 1, 1, 1, 1.2, 5])
with _c_logo:
    if os.path.exists(LOGO_CROP):
        st.image(LOGO_CROP, width=90)
with _c_h:
    st.page_link("app.py", label="Home")
with _c_m:
    st.page_link("pages/1_Meta_Ads.py", label="Meta Ads")
with _c_s:
    st.markdown(f'<div style="padding-top:1.1rem;"><span style="padding:0.35rem 0.9rem;border-radius:6px;font-size:0.8rem;font-weight:700;color:{BLUE};background:rgba(59,130,246,0.18);white-space:nowrap;">Shopify</span></div>', unsafe_allow_html=True)
with _c_g:
    st.page_link("pages/3_Google_Ads.py", label="Google Ads")
st.markdown(f'<div style="border-top:1px solid {BORDER};margin:0.5rem 0 1.8rem;"></div>', unsafe_allow_html=True)

st.markdown(f"""
<div style="padding-bottom:1.4rem;border-bottom:1px solid {BORDER};margin-bottom:2rem;">
  <div style="font-size:0.62rem;font-weight:600;text-transform:uppercase;letter-spacing:2.5px;color:{T3};">
    Store Overview &nbsp;·&nbsp; Shopify &nbsp;·&nbsp; All Time
  </div>
</div>
""", unsafe_allow_html=True)

@st.cache_data(ttl=1800)
def get_orders():
    all_orders = []
    url    = f"{SHOP_URL}/admin/api/2024-01/orders.json"
    params = {"status": "any", "limit": 250,
              "fields": "id,created_at,total_price,financial_status,fulfillment_status,line_items,customer"}
    while url:
        r    = requests.get(url, headers=HEADERS, params=params)
        data = r.json()
        all_orders.extend(data.get("orders", []))
        link = r.headers.get("Link", "")
        if 'rel="next"' in link:
            parts = [p.strip() for p in link.split(",")]
            next_part = next((p for p in parts if 'rel="next"' in p), None)
            url    = next_part.split(";")[0].strip().strip("<>") if next_part else None
            params = {}
        else:
            url = None
    return all_orders

with st.spinner("Loading Shopify data..."):
    orders_raw = get_orders()

if not orders_raw:
    st.warning("No orders found or could not connect to Shopify.")
    st.stop()

# Build orders DataFrame
rows = []
for o in orders_raw:
    rows.append({
        "Order ID":   o["id"],
        "Date":       pd.to_datetime(o["created_at"]).tz_localize(None),
        "Revenue":    float(o.get("total_price", 0)),
        "Status":     o.get("financial_status", "").title(),
        "Fulfillment": o.get("fulfillment_status") or "Unfulfilled",
    })
df = pd.DataFrame(rows)
df["Date"] = pd.to_datetime(df["Date"])

now      = pd.Timestamp.now()
df_7d    = df[df["Date"] >= now - timedelta(days=7)]
df_30d   = df[df["Date"] >= now - timedelta(days=30)]
df_paid  = df[df["Status"] == "Paid"]

total_orders    = len(df)
total_revenue   = df_paid["Revenue"].sum()
avg_order_value = df_paid["Revenue"].mean() if len(df_paid) > 0 else 0
orders_7d       = len(df_7d)
revenue_7d      = df_7d[df_7d["Status"] == "Paid"]["Revenue"].sum()
orders_30d      = len(df_30d)
revenue_30d     = df_30d[df_30d["Status"] == "Paid"]["Revenue"].sum()

# KPI cards
st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi"><div class="kpi-label">Total Revenue (All Time)</div><div class="kpi-value">${total_revenue:,.2f}</div></div>
  <div class="kpi"><div class="kpi-label">Total Orders (All Time)</div><div class="kpi-value">{total_orders:,}</div></div>
  <div class="kpi"><div class="kpi-label">Revenue (Last 30 Days)</div><div class="kpi-value">${revenue_30d:,.2f}</div></div>
  <div class="kpi"><div class="kpi-label">Orders (Last 30 Days)</div><div class="kpi-value">{orders_30d:,}</div></div>
</div>
<div class="stat-grid">
  <div class="stat"><div class="stat-label">Avg Order Value</div><div class="stat-value">${avg_order_value:,.2f}</div></div>
  <div class="stat"><div class="stat-label">Revenue (Last 7 Days)</div><div class="stat-value">${revenue_7d:,.2f}</div></div>
  <div class="stat"><div class="stat-label">Orders (Last 7 Days)</div><div class="stat-value">{orders_7d:,}</div></div>
  <div class="stat"><div class="stat-label">Paid Orders</div><div class="stat-value">{len(df_paid):,}</div></div>
</div>
""", unsafe_allow_html=True)

# Revenue trend chart (last 90 days)
st.markdown('<div class="section">Revenue Trend (Last 90 Days)</div>', unsafe_allow_html=True)
st.markdown('<div class="surface">', unsafe_allow_html=True)
df_90d = df[df["Date"] >= now - timedelta(days=90)].copy()
if not df_90d.empty:
    daily = df_90d[df_90d["Status"] == "Paid"].groupby(df_90d["Date"].dt.date)["Revenue"].sum().reset_index()
    daily.columns = ["Date", "Revenue"]
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=daily["Date"], y=daily["Revenue"], mode="lines+markers",
        line=dict(color=CHART_C, width=2),
        marker=dict(color=CHART_C, size=5),
        fill="tozeroy", fillcolor=f"rgba(59,130,246,0.12)",
        hovertemplate="<b>%{x}</b><br>Revenue: $%{y:,.2f}<extra></extra>",
    ))
    fig_trend.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=T2, family="Inter"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.06)", zeroline=False, tickfont=dict(size=10, color=T2)),
        yaxis=dict(gridcolor="rgba(255,255,255,0.06)", zeroline=False, tickfont=dict(size=10, color=T2),
                   tickprefix="$"),
        margin=dict(l=0, r=0, t=0, b=0), height=280, showlegend=False,
    )
    st.plotly_chart(fig_trend, use_container_width=True)
else:
    st.markdown(f'<div style="text-align:center;padding:2rem;color:{T3};">No revenue data in the last 90 days.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Orders per day chart
st.markdown('<div class="section">Orders per Day (Last 90 Days)</div>', unsafe_allow_html=True)
st.markdown('<div class="surface">', unsafe_allow_html=True)
if not df_90d.empty:
    daily_orders = df_90d.groupby(df_90d["Date"].dt.date)["Order ID"].count().reset_index()
    daily_orders.columns = ["Date", "Orders"]
    fig_orders = go.Figure(go.Bar(
        x=daily_orders["Date"], y=daily_orders["Orders"],
        marker=dict(color=CHART_C, opacity=0.8),
        hovertemplate="<b>%{x}</b><br>Orders: %{y}<extra></extra>",
    ))
    fig_orders.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color=T2, family="Inter"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.06)", zeroline=False, tickfont=dict(size=10, color=T2)),
        yaxis=dict(gridcolor="rgba(255,255,255,0.06)", zeroline=False, tickfont=dict(size=10, color=T2)),
        margin=dict(l=0, r=0, t=0, b=0), height=220, showlegend=False,
    )
    st.plotly_chart(fig_orders, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Top products
st.markdown('<div class="section">Top Products by Revenue</div>', unsafe_allow_html=True)
product_rows = []
for o in orders_raw:
    if o.get("financial_status") == "paid":
        for item in o.get("line_items", []):
            product_rows.append({
                "Product":  item.get("title", "Unknown"),
                "Qty":      int(item.get("quantity", 0)),
                "Revenue":  float(item.get("price", 0)) * int(item.get("quantity", 0)),
            })
if product_rows:
    df_products = (pd.DataFrame(product_rows)
                   .groupby("Product", as_index=False)
                   .agg({"Qty": "sum", "Revenue": "sum"})
                   .sort_values("Revenue", ascending=False)
                   .head(10))
    st.dataframe(
        df_products.style
            .background_gradient(subset=["Revenue"], cmap="Blues")
            .format({"Revenue": "${:,.2f}"}),
        use_container_width=True, height=350,
    )

# Recent orders table
st.markdown('<div class="section">Recent Orders</div>', unsafe_allow_html=True)
recent = df.sort_values("Date", ascending=False).head(20).copy()
recent["Date"] = recent["Date"].dt.strftime("%Y-%m-%d %H:%M")
st.dataframe(
    recent.style
        .background_gradient(subset=["Revenue"], cmap="Greens")
        .format({"Revenue": "${:,.2f}"}),
    use_container_width=True, height=430,
)
