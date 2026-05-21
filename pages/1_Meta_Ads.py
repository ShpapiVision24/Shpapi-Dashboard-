import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import numpy as np
import os

ACCESS_TOKEN  = st.secrets["META_ACCESS_TOKEN"]
AD_ACCOUNT_ID = st.secrets["AD_ACCOUNT_ID"]
ASSETS        = os.path.join(os.path.dirname(__file__), "..", "assets")
LOGO_SRC      = os.path.join(ASSETS, "logo.png")
LOGO_CROP     = os.path.join(ASSETS, "logo_cropped.png")

BG      = "#0a1628"
SURFACE = "#0e1f3c"
BORDER  = "rgba(255,255,255,0.08)"
T1      = "#ffffff"
T2      = "rgba(255,255,255,0.65)"
T3      = "rgba(255,255,255,0.38)"
GOLD    = "#3b82f6"
CHART_C = "#3b82f6"

st.set_page_config(page_title="Shpapi · Meta Ads", layout="wide", initial_sidebar_state="collapsed")

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
.kpi-value.gold {{ color: {GOLD}; }}
.stat-grid {{ display: grid; grid-template-columns: repeat(4,1fr); gap: 1rem; margin-bottom: 2.4rem; }}
.stat {{ background: rgba(0,0,0,0.02); border: 1px solid rgba(0,0,0,0.06); border-radius: 10px; padding: 1rem 1.4rem; }}
.stat-label {{ font-size: 0.6rem; font-weight: 600; text-transform: uppercase; letter-spacing: 1.8px; color: {T3}; margin-bottom: 0.4rem; }}
.stat-value {{ font-size: 1.15rem; font-weight: 600; color: #ffffff; letter-spacing: -0.3px; line-height: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
.section {{ font-size: 0.62rem; font-weight: 600; text-transform: uppercase; letter-spacing: 2.5px; color: {T3}; margin: 0 0 0.9rem 0; display: flex; align-items: center; gap: 1rem; }}
.section::after {{ content: ''; flex: 1; height: 1px; background: {BORDER}; }}
.surface {{ background: {SURFACE}; border: 1px solid {BORDER}; border-radius: 12px; padding: 1.4rem 1.4rem 0.6rem; margin-bottom: 1rem; }}
div[data-testid="stDataFrame"] iframe {{ border-radius: 8px; }}
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
    color: {GOLD} !important;
    border: none !important;
}}
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
    background: rgba(59,130,246,0.15) !important; color: {GOLD} !important;
}}
a[data-testid="stPageLink-NavLink"] svg {{ display: none !important; }}
</style>
""", unsafe_allow_html=True)

_c_logo, _c_h, _c_m, _c_s, _c_g, _ = st.columns([1.5, 1, 1, 1, 1.2, 5])
with _c_logo:
    if os.path.exists(LOGO_CROP):
        st.image(LOGO_CROP, width=90)
with _c_h:
    st.page_link("app.py", label="Home")
with _c_m:
    st.markdown(f'<div style="padding-top:1.1rem;"><span style="padding:0.35rem 0.9rem;border-radius:6px;font-size:0.8rem;font-weight:700;color:{GOLD};background:rgba(59,130,246,0.18);white-space:nowrap;">Meta Ads</span></div>', unsafe_allow_html=True)
with _c_s:
    st.page_link("pages/2_Shopify.py", label="Shopify")
with _c_g:
    st.page_link("pages/3_Google_Ads.py", label="Google Ads")
st.markdown(f'<div style="border-top:1px solid {BORDER};margin:0.5rem 0 1.8rem;"></div>', unsafe_allow_html=True)

st.markdown(f"""
<div style="padding-bottom:1.4rem;border-bottom:1px solid {BORDER};margin-bottom:2rem;">
  <div style="font-size:0.62rem;font-weight:600;text-transform:uppercase;letter-spacing:2.5px;color:{T3};">
    Ad Performance Dashboard &nbsp;·&nbsp; Meta Ads &nbsp;·&nbsp; All Time
  </div>
</div>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def get_ad_data():
    import datetime
    today = datetime.date.today().isoformat()
    camp_r = requests.get(
        f"https://graph.facebook.com/v19.0/{AD_ACCOUNT_ID}/campaigns",
        params={"fields": "id,start_time,stop_time", "limit": 500, "access_token": ACCESS_TOKEN},
    )
    camp_dates = {}
    for c in camp_r.json().get("data", []):
        start = c["start_time"][:10] if c.get("start_time") else ""
        stop  = c["stop_time"][:10]  if c.get("stop_time")  else today
        camp_dates[c["id"]] = (start, stop)
    url = f"https://graph.facebook.com/v19.0/{AD_ACCOUNT_ID}/insights"
    params = {
        "fields": "campaign_id,campaign_name,spend,impressions,clicks,actions,action_values,date_start,date_stop",
        "date_preset": "maximum", "level": "campaign", "access_token": ACCESS_TOKEN,
    }
    r    = requests.get(url, params=params)
    data = r.json()
    if "error" in data:
        st.error(f"API Error: {data['error']['message']}")
        return pd.DataFrame()
    if "data" not in data or not data["data"]:
        return pd.DataFrame()
    PURCHASE_TYPES     = {"purchase", "offsite_conversion.fb_pixel_purchase", "omni_purchase"}
    PRODUCT_VIEW_TYPES = {"offsite_conversion.fb_pixel_view_content", "view_content", "omni_view_content"}
    WISHLIST_TYPES     = {"onsite_conversion.add_to_wishlist", "omni_add_to_wishlist"}
    rows = []
    for item in data["data"]:
        purchases, revenue = 0, 0.0
        link_clicks, lpv, product_views, wishlist, video_views = 0, 0, 0, 0, 0
        for a in item.get("actions", []):
            t, v = a["action_type"], int(float(a["value"]))
            if t in PURCHASE_TYPES:                              purchases     = v
            elif t == "link_click":                              link_clicks   = v
            elif t == "landing_page_view":                       lpv           = v
            elif t in PRODUCT_VIEW_TYPES and product_views == 0: product_views = v
            elif t in WISHLIST_TYPES and wishlist == 0:          wishlist      = v
            elif t == "video_view":                              video_views   = v
        for av in item.get("action_values", []):
            if av["action_type"] in PURCHASE_TYPES:
                revenue = float(av["value"])
        cid = item.get("campaign_id", "")
        start_date, end_date = camp_dates.get(cid, (item.get("date_start", ""), item.get("date_stop", "")))
        rows.append({
            "Campaign": item.get("campaign_name", "Unknown"), "Start Date": start_date, "End Date": end_date,
            "Spend ($)": float(item.get("spend", 0)), "Impressions": int(item.get("impressions", 0)),
            "Link Clicks": link_clicks, "Landing Page Views": lpv, "Product Views": product_views,
            "Wishlist Adds": wishlist, "Video Views": video_views, "Purchases": purchases, "Revenue ($)": revenue,
        })
    return pd.DataFrame(rows)

def make_bar(series_x, series_y, fmt="number", order=None):
    df_bar = pd.DataFrame({"x": series_x.values, "y": series_y.values})
    if order is not None:
        df_bar = df_bar[df_bar["y"].isin(order)].groupby("y", as_index=False).sum()
        df_bar["y"] = pd.Categorical(df_bar["y"], categories=order, ordered=True)
        df_bar = df_bar.sort_values("y")
    else:
        df_bar = df_bar.groupby("y", as_index=False).sum().nlargest(8, "x")
        df_bar = df_bar.sort_values("x", ascending=True)
    labels = [f"${v:,.0f}" if fmt == "money" else f"{int(v):,}" for v in df_bar["x"]]
    fig = go.Figure(go.Bar(
        x=df_bar["x"], y=df_bar["y"].astype(str).str[:32], orientation="h",
        marker=dict(color=CHART_C, opacity=0.8, line=dict(width=0)),
        text=labels, textposition="outside", textfont=dict(color=T2, size=10, family="Inter"),
        hovertemplate="%{y}<br>%{text}<extra></extra>",
    ))
    fig.update_xaxes(showgrid=False, showticklabels=False, zeroline=False, visible=False)
    fig.update_yaxes(showgrid=False, zeroline=False, tickfont=dict(size=10, color=T2, family="Inter"), ticksuffix="  ")
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      margin=dict(l=0, r=60, t=0, b=0), height=280, showlegend=False, font=dict(family="Inter"))
    return fig

def make_gantt(df):
    gdf = df[["Campaign","Start Date","End Date","Spend ($)","Purchases"]].copy()
    gdf["Start"] = pd.to_datetime(gdf["Start Date"], errors="coerce")
    gdf["End"]   = pd.to_datetime(gdf["End Date"],   errors="coerce")
    gdf = gdf.dropna(subset=["Start","End"]).sort_values("Start", ascending=False)
    gdf["Label"] = gdf["Campaign"].str[:36]
    fig = px.timeline(gdf, x_start="Start", x_end="End", y="Label", color_discrete_sequence=[CHART_C],
                      hover_name="Campaign",
                      hover_data={"Label": False, "Start": True, "End": True, "Spend ($)": True, "Purchases": True})
    fig.update_traces(opacity=0.75, marker_line_width=0)
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font=dict(color=T2, family="Inter"),
                      xaxis=dict(gridcolor="rgba(255,255,255,0.06)", zeroline=False,
                                 tickfont=dict(size=10, color=T2, family="Inter"), title=None),
                      yaxis=dict(showgrid=False, zeroline=False, title=None,
                                 tickfont=dict(size=10, color=T2, family="Inter"), ticksuffix="  "),
                      margin=dict(l=0, r=20, t=0, b=0), height=max(220, len(gdf)*38), showlegend=False)
    return fig

def make_funnel_html(totals):
    stages = list(totals.items())
    if not stages or stages[0][1] == 0:
        return ""
    top  = stages[0][1]
    rows = ""
    for i, (label, val) in enumerate(stages):
        bar_w   = max(val / top * 100, 0.4) if val > 0 else 0
        opacity = max(1.0 - i * 0.13, 0.45)
        if i == 0:
            sub = f'<span style="color:{T3};font-size:0.7rem;font-weight:500;">Top of funnel</span>'
        elif stages[i-1][1] > 0 and val > 0:
            step  = val / stages[i-1][1] * 100
            total = val / top * 100
            sub   = (f'<span style="color:{T3};font-size:0.7rem;font-weight:500;">'
                     f'{step:.1f}% of {stages[i-1][0].lower()}&nbsp;&nbsp;·&nbsp;&nbsp;{total:.2f}% of impressions</span>')
        else:
            sub = f'<span style="color:{T3};font-size:0.7rem;font-weight:500;">No data yet</span>'
        rows += f"""
        <div style="margin-bottom:1.4rem;">
          <div style="display:flex;justify-content:space-between;align-items:baseline;margin-bottom:0.4rem;">
            <span style="font-size:0.62rem;font-weight:600;text-transform:uppercase;letter-spacing:1.8px;color:{T3};">{label}</span>
            <div>{sub}&nbsp;&nbsp;<span style="font-size:1.25rem;font-weight:700;color:{T1};letter-spacing:-0.5px;">{val:,}</span></div>
          </div>
          <div style="background:rgba(255,255,255,0.08);border-radius:6px;height:10px;">
            <div style="width:{bar_w:.2f}%;height:100%;background:{CHART_C};border-radius:6px;opacity:{opacity:.2f};"></div>
          </div>
        </div>"""
    return f'<div style="padding:0.25rem 0.5rem 0.5rem;">{rows}</div>'

df = get_ad_data()

if not df.empty:
    df["CTR (%)"] = (df["Link Clicks"] / df["Impressions"].replace(0, 1) * 100).round(2)
    df["CPC ($)"] = (df["Spend ($)"] / df["Link Clicks"].replace(0, 1)).round(2)
    df["ROAS"]    = (df["Revenue ($)"] / df["Spend ($)"].replace(0, np.nan)).round(2).fillna(0)
    df["CPA ($)"] = (df["Spend ($)"] / df["Purchases"].replace(0, np.nan)).round(2).fillna(0)

    total_spend     = df["Spend ($)"].sum()
    total_impr      = df["Impressions"].sum()
    total_lclicks   = int(df["Link Clicks"].sum())
    total_lpv       = int(df["Landing Page Views"].sum())
    total_pviews    = int(df["Product Views"].sum())
    total_purchases = int(df["Purchases"].sum())
    total_revenue   = df["Revenue ($)"].sum()
    avg_ctr         = (total_lclicks / total_impr * 100) if total_impr else 0
    avg_cpm         = (total_spend / total_impr * 1000) if total_impr else 0
    avg_cpc         = (total_spend / total_lclicks) if total_lclicks else 0
    roas            = (total_revenue / total_spend) if total_spend else 0
    cpa             = (total_spend / total_purchases) if total_purchases else 0
    has_conv        = total_purchases > 0
    roas_str        = f"{roas:.2f}x" if roas else "—"
    cpa_str         = f"${cpa:,.2f}" if has_conv else "—"

    st.markdown(f"""
    <div class="kpi-grid">
      <div class="kpi"><div class="kpi-label">Total Purchases</div><div class="kpi-value gold">{total_purchases:,}</div></div>
      <div class="kpi"><div class="kpi-label">Revenue</div><div class="kpi-value gold">${total_revenue:,.2f}</div></div>
      <div class="kpi"><div class="kpi-label">ROAS</div><div class="kpi-value">{roas_str}</div></div>
      <div class="kpi"><div class="kpi-label">Total Spend</div><div class="kpi-value">${total_spend:,.2f}</div></div>
    </div>
    <div class="stat-grid">
      <div class="stat"><div class="stat-label">Impressions</div><div class="stat-value">{total_impr:,}</div></div>
      <div class="stat"><div class="stat-label">Link Clicks</div><div class="stat-value">{total_lclicks:,}</div></div>
      <div class="stat"><div class="stat-label">Landing Page Views</div><div class="stat-value">{total_lpv:,}</div></div>
      <div class="stat"><div class="stat-label">Product Views</div><div class="stat-value">{total_pviews:,}</div></div>
    </div>
    <div class="stat-grid">
      <div class="stat"><div class="stat-label">Avg CTR</div><div class="stat-value">{avg_ctr:.2f}%</div></div>
      <div class="stat"><div class="stat-label">Avg CPC</div><div class="stat-value">${avg_cpc:,.2f}</div></div>
      <div class="stat"><div class="stat-label">Avg CPM</div><div class="stat-value">${avg_cpm:,.2f}</div></div>
      <div class="stat"><div class="stat-label">Avg CPA</div><div class="stat-value">{cpa_str}</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section">Performance by Campaign (All Time)</div>', unsafe_allow_html=True)
    display_cols = ["Start Date","End Date","Campaign","Spend ($)","Purchases","Revenue ($)","ROAS","CPA ($)",
                    "Impressions","Link Clicks","Landing Page Views","Product Views","Wishlist Adds","CTR (%)","CPC ($)"]
    display = df[display_cols].copy()
    display["Start Date"] = pd.to_datetime(display["Start Date"], errors="coerce")
    display = display.sort_values("Start Date", ascending=False)
    display["Start Date"] = display["Start Date"].dt.strftime("%Y-%m-%d")
    display["End Date"]   = pd.to_datetime(display["End Date"], errors="coerce").dt.strftime("%Y-%m-%d")
    st.dataframe(
        display.style
            .background_gradient(subset=["Spend ($)"],          cmap="YlOrBr")
            .background_gradient(subset=["Purchases"],          cmap="Greens")
            .background_gradient(subset=["Revenue ($)"],        cmap="Greens")
            .background_gradient(subset=["Landing Page Views"], cmap="Blues")
            .background_gradient(subset=["Product Views"],      cmap="Blues")
            .format({"Spend ($)":"${:,.2f}","Revenue ($)":"${:,.2f}","ROAS":"{:.2f}x",
                     "CPA ($)":"${:,.2f}","CTR (%)":"{:.2f}%","CPC ($)":"${:,.2f}"}),
        use_container_width=True, height=430)

    st.markdown('<div class="section">Campaign Performance</div>', unsafe_allow_html=True)
    top8 = df.groupby("Campaign", as_index=False)["Spend ($)"].sum().nlargest(8,"Spend ($)")["Campaign"].tolist()
    shared_order = list(reversed(top8))
    c1, c2, c3 = st.columns(3, gap="medium")
    with c1:
        st.markdown('<div class="surface">', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:0.65rem;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;color:{T3};margin-bottom:1rem;">Spend by Campaign</div>', unsafe_allow_html=True)
        st.plotly_chart(make_bar(df["Spend ($)"], df["Campaign"], fmt="money", order=shared_order), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="surface">', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:0.65rem;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;color:{T3};margin-bottom:1rem;">Purchases by Campaign</div>', unsafe_allow_html=True)
        st.plotly_chart(make_bar(df["Purchases"], df["Campaign"], order=shared_order), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="surface">', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:0.65rem;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;color:{T3};margin-bottom:1rem;">Link Clicks by Campaign</div>', unsafe_allow_html=True)
        st.plotly_chart(make_bar(df["Link Clicks"], df["Campaign"], order=shared_order), use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    if has_conv:
        st.markdown('<div class="section">Efficiency</div>', unsafe_allow_html=True)
        e1, e2 = st.columns(2, gap="medium")
        roas_order = list(reversed(df.groupby("Campaign", as_index=False)["ROAS"].mean().nlargest(8,"ROAS")["Campaign"].tolist()))
        with e1:
            st.markdown('<div class="surface">', unsafe_allow_html=True)
            st.markdown(f'<div style="font-size:0.65rem;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;color:{T3};margin-bottom:1rem;">ROAS by Campaign</div>', unsafe_allow_html=True)
            st.plotly_chart(make_bar(df["ROAS"], df["Campaign"], order=roas_order), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        cpa_df    = df[df["Purchases"] > 0].copy()
        cpa_order = list(reversed(cpa_df.groupby("Campaign", as_index=False)["CPA ($)"].mean().nsmallest(8,"CPA ($)")["Campaign"].tolist()))
        with e2:
            st.markdown('<div class="surface">', unsafe_allow_html=True)
            st.markdown(f'<div style="font-size:0.65rem;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;color:{T3};margin-bottom:1rem;">Cost Per Acquisition by Campaign</div>', unsafe_allow_html=True)
            st.plotly_chart(make_bar(cpa_df["CPA ($)"], cpa_df["Campaign"], fmt="money", order=cpa_order), use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section">Conversion Funnel</div>', unsafe_allow_html=True)
    st.markdown('<div class="surface">', unsafe_allow_html=True)
    funnel_html = make_funnel_html({"Impressions": int(total_impr), "Link Clicks": total_lclicks,
                                    "Landing Page Views": total_lpv, "Product Views": total_pviews,
                                    "Purchases": total_purchases})
    st.markdown(funnel_html if funnel_html else f'<div style="text-align:center;padding:2rem;color:{T3};font-size:0.8rem;">No funnel data yet.</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section">Campaign Timeline</div>', unsafe_allow_html=True)
    st.markdown('<div class="surface">', unsafe_allow_html=True)
    st.plotly_chart(make_gantt(df), use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    y_col   = "Revenue ($)" if total_revenue > 0 else "Impressions"
    y_label = "Revenue ($)" if total_revenue > 0 else "Impressions"
    y_fmt   = "Revenue: $%{y:,.2f}" if total_revenue > 0 else "Impressions: %{y:,}"
    st.markdown(f'<div class="section">Spend vs {y_label}</div>', unsafe_allow_html=True)
    st.markdown('<div class="surface">', unsafe_allow_html=True)
    active    = df[df["Spend ($)"] > 0].copy()
    click_max = active["Link Clicks"].max()
    fig_s = go.Figure(go.Scatter(
        x=active["Spend ($)"], y=active[y_col], mode="markers",
        marker=dict(size=(active["Link Clicks"]/click_max*40+8) if click_max > 0 else 12,
                    color=CHART_C, opacity=0.7, line=dict(color="rgba(255,255,255,0.15)", width=1)),
        text=active["Campaign"],
        hovertemplate=f"<b>%{{text}}</b><br>Spend: $%{{x:,.2f}}<br>{y_fmt}<extra></extra>",
    ))
    fig_s.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                        font=dict(color=T2, family="Inter"),
                        xaxis=dict(gridcolor="rgba(255,255,255,0.06)", zeroline=False,
                                   title=dict(text="Spend ($)", font=dict(size=10, color=T3))),
                        yaxis=dict(gridcolor="rgba(255,255,255,0.06)", zeroline=False,
                                   title=dict(text=y_label, font=dict(size=10, color=T3))),
                        margin=dict(l=0, r=0, t=0, b=0), height=340, showlegend=False)
    st.plotly_chart(fig_s, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown(f'<div style="text-align:center;padding:6rem 2rem;color:{T3};"><div style="font-size:0.85rem;font-weight:500;letter-spacing:1px;text-transform:uppercase;margin-bottom:0.4rem;">No data found</div><div style="font-size:0.75rem;">Check your access token and ad account ID</div></div>', unsafe_allow_html=True)
