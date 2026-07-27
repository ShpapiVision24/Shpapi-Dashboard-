import streamlit as st
import requests
import os
from datetime import datetime, timezone, date, timedelta
import json

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
button[kind="primaryFormSubmit"] {{
    background: {BLUE} !important; border: none !important; border-radius: 8px !important;
    color: #fff !important; font-weight: 700 !important; font-size: 0.85rem !important;
    margin-top: 0.5rem;
}}
button[kind="primaryFormSubmit"]:hover {{ background: #2563eb !important; }}
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
        if "error" in data:
            return [], data["error"].get("message", "Unknown API error")
        rows.extend(data.get("data", []))
        url    = data.get("paging", {}).get("next")
        params = {}
    return rows, None

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

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_thumbnails():
    try:
        r = requests.get(
            f"https://graph.facebook.com/v19.0/{IG_ACCOUNT}/ads",
            params={
                "fields": "campaign_id,creative{thumbnail_url,image_url}",
                "limit": 200,
                "access_token": ACCESS_TOKEN,
            },
            timeout=15,
        )
        thumbs = {}
        for ad in r.json().get("data", []):
            cid = ad.get("campaign_id")
            if cid and cid not in thumbs:
                creative = ad.get("creative", {})
                url = creative.get("thumbnail_url") or creative.get("image_url")
                if url:
                    thumbs[cid] = url
        return thumbs
    except Exception:
        return {}

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
    campaigns, api_error = fetch_insights(preset)
    camp_meta  = fetch_campaign_details()
    thumbnails = fetch_thumbnails()

if api_error:
    st.error(f"Instagram API error: {api_error}")
elif not campaigns:
    st.info("No boost data found for this period.")

if campaigns:
    total_spend     = sum(float(c.get("spend", 0)) for c in campaigns)
    total_reach     = sum(int(c.get("reach", 0)) for c in campaigns)
    total_impr      = sum(int(c.get("impressions", 0)) for c in campaigns)
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

        meta         = camp_meta.get(cid, {})
        effective    = meta.get("effective_status", "")
        end_time_str = meta.get("end_time", "") or meta.get("stop_time", "")
        now          = datetime.now(timezone.utc)
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

        lb         = int(meta.get("lifetime_budget", 0)) / 100
        db         = int(meta.get("daily_budget", 0)) / 100
        budget_str = f"${lb:,.0f} lifetime" if lb else (f"${db:,.0f}/day" if db else "")
        date_str   = fmt_date(meta.get("start_time", ""))

        status_color = GREEN if status == "Active" else (YELLOW if "Pending" in status or "Review" in status else T3)
        thumb_url    = thumbnails.get(cid, "")

        with st.container(border=True):
            hcol1, hcol2 = st.columns([4, 1])
            with hcol1:
                thumb_html = f'<img src="{thumb_url}" style="width:56px;height:56px;object-fit:cover;border-radius:8px;margin-right:0.85rem;flex-shrink:0;" />' if thumb_url else ''
                meta_parts = []
                if date_str:   meta_parts.append(f"Created {date_str}")
                if status:     meta_parts.append(f'<span style="color:{status_color};font-weight:600;">{status}</span>')
                if budget_str: meta_parts.append(f"Budget: {budget_str}")
                if pct:        meta_parts.append(f"{pct}% of total spend")
                meta_html = f'<div style="font-size:0.72rem;color:{T3};margin-top:0.2rem;">{" &nbsp;·&nbsp; ".join(meta_parts)}</div>' if meta_parts else ''
                st.markdown(f'''
                <div style="display:flex;align-items:center;">
                  {thumb_html}
                  <div>
                    <div style="font-size:0.9rem;font-weight:600;color:{T1};line-height:1.4;">{name}</div>
                    {meta_html}
                  </div>
                </div>''', unsafe_allow_html=True)
            with hcol2:
                st.markdown(f'<div style="text-align:right;font-size:1.15rem;font-weight:700;color:{PINK};padding-top:0.2rem;">${spend:,.2f}</div>', unsafe_allow_html=True)

            st.markdown(f'<div style="border-top:1px solid {BORDER};margin:0.75rem 0 0.6rem;"></div>', unsafe_allow_html=True)

            row1 = [(label, val) for label, val in [
                ("Reach",       f"{reach:,}"       if reach       else None),
                ("Impressions", f"{impr:,}"         if impr        else None),
                ("Link Clicks", f"{link_clicks:,}"  if link_clicks else None),
                ("Video Views", f"{video_views:,}"  if video_views else None),
            ] if val is not None]
            if row1:
                cols = st.columns(len(row1))
                for col, (label, val) in zip(cols, row1):
                    with col:
                        st.metric(label, val, help=METRIC_HELP.get(label))

            row2 = [(label, val) for label, val in [
                ("Purchases",     f"{purchases:,}"      if purchases  else None),
                ("Cost/Purchase", f"${cpp:,.2f}"         if cpp        else None),
                ("Conv. Value",   f"${conv_value:,.2f}"  if conv_value else None),
                ("Purchase ROAS", f"{roas}x"             if roas       else None),
            ] if val is not None]
            if row2:
                st.markdown(f'<div style="font-size:0.6rem;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;color:{T3};margin:0.6rem 0 0.3rem;">Goal &amp; Conversions</div>', unsafe_allow_html=True)
                cols = st.columns(len(row2))
                for col, (label, val) in zip(cols, row2):
                    with col:
                        st.metric(label, val, help=METRIC_HELP.get(label))

            row3 = [(label, val) for label, val in [
                ("Content Views", f"{content_views:,}" if content_views else None),
                ("Adds to Cart",  f"{adds_to_cart:,}"  if adds_to_cart  else None),
                ("Checkouts",     f"{checkouts:,}"      if checkouts     else None),
            ] if val is not None]
            if row3:
                st.markdown(f'<div style="font-size:0.6rem;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;color:{T3};margin:0.6rem 0 0.3rem;">Funnel</div>', unsafe_allow_html=True)
                cols = st.columns(len(row3))
                for col, (label, val) in zip(cols, row3):
                    with col:
                        st.metric(label, val, help=METRIC_HELP.get(label))

# ── Create New Boost ──────────────────────────────────────────────────────────
st.markdown(f"""
<div style="margin:3rem 0 1.5rem;border-top:2px solid {BORDER};padding-top:2rem;">
  <div style="font-size:1.3rem;font-weight:700;color:{T1};letter-spacing:-0.4px;">Create New Boost</div>
  <div style="font-size:0.72rem;color:{T3};margin-top:0.25rem;">Promote an existing Instagram post or Reel directly from your dashboard</div>
</div>
""", unsafe_allow_html=True)

@st.cache_data(ttl=600, show_spinner=False)
def fetch_ig_account():
    try:
        r = requests.get(
            "https://graph.facebook.com/v19.0/me/accounts",
            params={"fields": "id,name,access_token,instagram_business_account", "access_token": ACCESS_TOKEN},
            timeout=15,
        )
        data = r.json()
        if "error" in data:
            return None, None, None, data["error"].get("message", "Unknown error")
        for page in data.get("data", []):
            ig = page.get("instagram_business_account", {})
            if ig.get("id"):
                return ig["id"], page["id"], page.get("access_token", ACCESS_TOKEN), None
        return None, None, None, "No Instagram business account linked to any Facebook Page."
    except Exception as e:
        return None, None, None, str(e)

@st.cache_data(ttl=300, show_spinner=False)
def fetch_ig_recent_media(ig_uid, page_token):
    try:
        r = requests.get(
            f"https://graph.facebook.com/v19.0/{ig_uid}/media",
            params={
                "fields": "id,caption,media_type,thumbnail_url,media_url,timestamp",
                "limit": 24,
                "access_token": page_token,
            },
            timeout=15,
        )
        data = r.json()
        if "error" in data:
            return [], data["error"].get("message", "Unknown error")
        return data.get("data", []), None
    except Exception as e:
        return [], str(e)

@st.cache_data(ttl=600, show_spinner=False)
def fetch_ad_creatives():
    """Fallback: get posts already used in ads (works with ads_management)."""
    try:
        r = requests.get(
            f"https://graph.facebook.com/v19.0/{IG_ACCOUNT}/adcreatives",
            params={
                "fields": "id,name,source_instagram_media_id,thumbnail_url,image_url",
                "limit": 50,
                "access_token": ACCESS_TOKEN,
            },
            timeout=15,
        )
        items = []
        seen = set()
        for c in r.json().get("data", []):
            mid = c.get("source_instagram_media_id")
            if mid and mid not in seen:
                seen.add(mid)
                thumb = c.get("thumbnail_url") or c.get("image_url") or ""
                items.append({"id": mid, "caption": c.get("name", ""), "thumbnail_url": thumb})
        return items
    except Exception:
        return []

with st.spinner("Loading your Instagram posts…"):
    ig_uid, page_id, page_token, acct_error = fetch_ig_account()

media_list = []
if acct_error:
    st.warning(f"Instagram account lookup: {acct_error}")
elif ig_uid:
    media_list, media_error = fetch_ig_recent_media(ig_uid, page_token)
    if media_error or not media_list:
        media_list = fetch_ad_creatives()

if "boost_media_id" not in st.session_state:
    st.session_state["boost_media_id"] = None

sel_id       = st.session_state.get("boost_media_id")
selected_item = next((m for m in media_list if m["id"] == sel_id), None) if sel_id and media_list else None

# ── Side-by-side layout: picker LEFT, form+preview RIGHT ─────────────────────
pick_col, right_col = st.columns([3, 2], gap="large")

with pick_col:
    if not media_list:
        st.info("No Instagram posts found. Connect your Instagram account to pick a post.")
    else:
        st.markdown('<div class="section">Pick a post to boost</div>', unsafe_allow_html=True)
        n_cols = 3
        for row_start in range(0, min(len(media_list), 12), n_cols):
            row_items = media_list[row_start:row_start + n_cols]
            g_cols = st.columns(n_cols, gap="small")
            for g_col, item in zip(g_cols, row_items):
                mid    = item["id"]
                mtype  = item.get("media_type", "")
                if mtype == "VIDEO":
                    thumb = item.get("thumbnail_url") or ""
                else:
                    thumb = item.get("media_url") or item.get("thumbnail_url") or ""
                is_sel = (sel_id == mid)
                with g_col:
                    ring = f"box-shadow:0 0 0 3px {PINK};" if is_sel else ""
                    if thumb:
                        st.markdown(
                            f'<div style="border-radius:8px;overflow:hidden;margin-bottom:4px;{ring}">'
                            f'<img src="{thumb}" style="width:100%;aspect-ratio:1;object-fit:cover;display:block;" />'
                            f'</div>',
                            unsafe_allow_html=True,
                        )
                    if st.button(
                        "✓ Selected" if is_sel else "Select",
                        key=f"bp_{mid}",
                        use_container_width=True,
                    ):
                        st.session_state["boost_media_id"] = mid
                        st.rerun()

with right_col:
    if not selected_item:
        st.markdown(f"""
<div style="background:{SURFACE};border:1.5px dashed {BORDER};border-radius:14px;padding:3rem 2rem;text-align:center;">
  <div style="font-size:2rem;margin-bottom:0.75rem;">📸</div>
  <div style="font-size:0.9rem;font-weight:600;color:{T2};margin-bottom:0.4rem;">Select a post</div>
  <div style="font-size:0.75rem;color:{T3};">Pick any photo or reel from the left to see settings and preview here</div>
</div>
""", unsafe_allow_html=True)
    else:
        prev_thumb   = selected_item.get("media_url") or selected_item.get("thumbnail_url") or ""
        prev_caption = selected_item.get("caption") or ""

        # Ad preview card
        cap_preview = prev_caption[:100] + ("…" if len(prev_caption) > 100 else "")
        st.markdown(f"""
<div style="background:#fff;border-radius:12px;overflow:hidden;border:1px solid #dbdbdb;margin-bottom:1.25rem;">
  <div style="display:flex;align-items:center;padding:10px 12px;gap:10px;">
    <div style="width:32px;height:32px;border-radius:50%;background:linear-gradient(45deg,#f09433,#e6683c,#dc2743,#cc2366,#bc1888);display:flex;align-items:center;justify-content:center;flex-shrink:0;">
      <span style="color:#fff;font-size:0.6rem;font-weight:700;">S</span>
    </div>
    <div>
      <div style="font-size:0.8rem;font-weight:600;color:#000;line-height:1.2;">shpapi.vision</div>
      <div style="font-size:0.68rem;color:#737373;">Sponsored</div>
    </div>
    <div style="margin-left:auto;font-size:1.1rem;color:#262626;padding-right:4px;">···</div>
  </div>
  {"<img src='" + prev_thumb + "' style='width:100%;display:block;max-height:300px;object-fit:cover;' />" if prev_thumb else '<div style="width:100%;height:200px;background:#f0f0f0;"></div>'}
  <div style="padding:10px 12px;">
    <div style="font-size:0.75rem;color:#000;line-height:1.4;">{cap_preview}</div>
    <div style="margin-top:8px;padding:8px 0;border-top:1px solid #efefef;font-size:0.75rem;font-weight:600;color:#262626;text-align:center;">Learn More ›</div>
  </div>
</div>
""", unsafe_allow_html=True)

        # Settings form
        with st.form("boost_form"):
            campaign_name = st.text_input(
                "Campaign name",
                value=(f"Boost · {prev_caption[:40]}…" if len(prev_caption) > 40
                       else f"Boost · {prev_caption}" if prev_caption else "New Boost"),
            )

            st.markdown(f'<div style="font-size:0.65rem;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;color:{T3};margin:0.75rem 0 0.35rem;">Goal</div>', unsafe_allow_html=True)
            goal = st.radio("Goal", ["Reach more people", "More website traffic", "More engagement"], label_visibility="collapsed")

            st.markdown(f'<div style="font-size:0.65rem;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;color:{T3};margin:0.75rem 0 0.35rem;">Call to action</div>', unsafe_allow_html=True)
            cta_btn = st.selectbox("CTA", ["LEARN_MORE", "SHOP_NOW", "CONTACT_US", "WATCH_MORE", "BOOK_TRAVEL"], label_visibility="collapsed")

            st.markdown(f'<div style="font-size:0.65rem;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;color:{T3};margin:0.75rem 0 0.35rem;">Budget &amp; Duration</div>', unsafe_allow_html=True)
            fb1, fb2, fb3 = st.columns(3)
            with fb1:
                budget_usd = st.number_input("Budget ($)", min_value=1.0, max_value=50000.0, value=50.0, step=5.0, label_visibility="collapsed")
                st.caption("Budget (USD)")
            with fb2:
                budget_type = st.selectbox("Type", ["Lifetime", "Daily"], label_visibility="collapsed")
                st.caption("Budget type")
            with fb3:
                duration_days = st.number_input("Days", min_value=1, max_value=90, value=7, step=1, label_visibility="collapsed")
                st.caption("Duration")

            start_dt = date.today()
            end_dt   = start_dt + timedelta(days=int(duration_days))
            st.markdown(f'<div style="font-size:0.72rem;color:{T3};margin-top:-0.4rem;">{start_dt.strftime("%b %d")} → {end_dt.strftime("%b %d, %Y")}</div>', unsafe_allow_html=True)

            st.markdown(f'<div style="font-size:0.65rem;font-weight:600;text-transform:uppercase;letter-spacing:1.5px;color:{T3};margin:0.75rem 0 0.35rem;">Audience</div>', unsafe_allow_html=True)
            fa1, fa2, fa3 = st.columns(3)
            with fa1:
                age_min = st.number_input("Min age", min_value=18, max_value=64, value=18, step=1)
            with fa2:
                age_max = st.number_input("Max age", min_value=19, max_value=65, value=55, step=1)
            with fa3:
                country = st.selectbox("Country", ["US","CA","GB","AU","MX","BR","ES","FR","DE","IT","JP","KR"])

            launched = st.form_submit_button("Launch Boost", use_container_width=True, type="primary")

        if launched:
            GOAL_MAP = {
                "Reach more people":    ("OUTCOME_AWARENESS",  "REACH"),
                "More website traffic": ("OUTCOME_TRAFFIC",    "LINK_CLICKS"),
                "More engagement":      ("OUTCOME_ENGAGEMENT", "POST_ENGAGEMENT"),
            }
            objective, opt_goal = GOAL_MAP[goal]
            budget_cents = int(budget_usd * 100)
            start_ts = int(datetime(start_dt.year, start_dt.month, start_dt.day, 0, 0, tzinfo=timezone.utc).timestamp())
            end_ts   = int(datetime(end_dt.year,   end_dt.month,   end_dt.day,  23, 59, tzinfo=timezone.utc).timestamp())

            with st.spinner("Launching boost…"):
                try:
                    cr = requests.post(
                        f"https://graph.facebook.com/v19.0/{IG_ACCOUNT}/campaigns",
                        data={"name": campaign_name, "objective": objective,
                              "status": "ACTIVE", "special_ad_categories": "[]",
                              "access_token": ACCESS_TOKEN},
                        timeout=30,
                    ).json()
                    if "error" in cr:
                        st.error(f"Campaign error: {cr['error']['message']}")
                        st.stop()
                    campaign_id = cr["id"]

                    asp = {
                        "name": f"{campaign_name} — Ad Set",
                        "campaign_id": campaign_id,
                        "billing_event": "IMPRESSIONS",
                        "optimization_goal": opt_goal,
                        "targeting": json.dumps({
                            "age_min": int(age_min), "age_max": int(age_max),
                            "geo_locations": {"countries": [country]},
                        }),
                        "start_time": str(start_ts),
                        "end_time":   str(end_ts),
                        "access_token": ACCESS_TOKEN,
                    }
                    if ig_uid:
                        asp["instagram_actor_id"] = ig_uid
                    if budget_type == "Lifetime":
                        asp["lifetime_budget"] = str(budget_cents)
                    else:
                        asp["daily_budget"] = str(budget_cents)

                    ar = requests.post(
                        f"https://graph.facebook.com/v19.0/{IG_ACCOUNT}/adsets",
                        data=asp, timeout=30,
                    ).json()
                    if "error" in ar:
                        st.error(f"Ad set error: {ar['error']['message']}")
                        st.stop()
                    adset_id = ar["id"]

                    ccr_data = {
                        "name": f"{campaign_name} — Creative",
                        "source_instagram_media_id": sel_id,
                        "call_to_action": json.dumps({"type": cta_btn}),
                        "access_token": ACCESS_TOKEN,
                    }
                    if ig_uid:
                        ccr_data["instagram_actor_id"] = ig_uid
                    ccr = requests.post(
                        f"https://graph.facebook.com/v19.0/{IG_ACCOUNT}/adcreatives",
                        data=ccr_data, timeout=30,
                    ).json()
                    if "error" in ccr:
                        st.error(f"Creative error: {ccr['error']['message']}")
                        st.stop()
                    creative_id = ccr["id"]

                    adr = requests.post(
                        f"https://graph.facebook.com/v19.0/{IG_ACCOUNT}/ads",
                        data={"name": f"{campaign_name} — Ad", "adset_id": adset_id,
                              "creative": json.dumps({"creative_id": creative_id}),
                              "status": "ACTIVE", "access_token": ACCESS_TOKEN},
                        timeout=30,
                    ).json()
                    if "error" in adr:
                        st.error(f"Ad error: {adr['error']['message']}")
                        st.stop()

                    st.success(f"Boost launched! Campaign ID: {campaign_id}")
                    st.balloons()
                    st.session_state["boost_media_id"] = None
                    st.cache_data.clear()

                except Exception as ex:
                    st.error(f"Something went wrong: {str(ex)}")
