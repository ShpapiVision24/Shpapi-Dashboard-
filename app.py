import streamlit as st
import requests
import base64
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
.section::after {{ content: ''; flex: 1; height: 1px; background: {BORDER}; }}
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
_c_logo, _c_h, _c_m, _c_s, _c_g, _c_qb, _c_ig, _ = st.columns([1.5, 1, 1, 1, 1.2, 1.3, 1.2, 1.8])
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
with _c_qb:
    st.page_link("pages/4_QuickBooks.py", label="QuickBooks")
with _c_ig:
    st.page_link("pages/5_Instagram.py", label="Instagram")
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

@st.cache_data(ttl=3600)
def get_qb_summary():
    try:
        import datetime as dt
        client_id     = st.secrets["QB_CLIENT_ID"]
        client_secret = st.secrets["QB_CLIENT_SECRET"]
        refresh_token = st.secrets.get("QB_REFRESH_TOKEN", "")
        realm_id      = st.secrets.get("QB_REALM_ID", "")
        env           = st.secrets.get("QB_ENVIRONMENT", "sandbox")
        if not refresh_token or not realm_id:
            return None
        creds = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()
        r = requests.post(
            "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer",
            headers={"Authorization": f"Basic {creds}", "Accept": "application/json"},
            data={"grant_type": "refresh_token", "refresh_token": refresh_token},
            timeout=30,
        )
        token_data = r.json()
        if "access_token" not in token_data:
            return None
        access_token = token_data["access_token"]
        base_url = "https://quickbooks.api.intuit.com" if env == "production" else "https://sandbox-quickbooks.api.intuit.com"
        now = dt.datetime.now()
        r2 = requests.get(
            f"{base_url}/v3/company/{realm_id}/reports/ProfitAndLoss",
            headers={"Authorization": f"Bearer {access_token}", "Accept": "application/json"},
            params={"start_date": f"{now.year}-01-01", "end_date": now.strftime("%Y-%m-%d"), "accounting_method": "Accrual"},
            timeout=30,
        )
        report = r2.json()
        net_income = None
        for row in report.get("Rows", {}).get("Row", []):
            if row.get("type") == "Section" and row.get("group") == "NetIncome":
                cols = row.get("Summary", {}).get("ColData", [])
                if len(cols) > 1:
                    try:
                        net_income = float(cols[1].get("value", 0))
                    except Exception:
                        pass
        return {"net_income": net_income}
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
            "https://graph.facebook.com/v19.0/act_8429913163714900/insights",
            params={"fields": "spend,reach,impressions", "level": "account",
                    "date_preset": "maximum", "access_token": ACCESS_TOKEN},
            timeout=15,
        )
        d = r.json().get("data", [{}])[0]
        return {"spend": float(d.get("spend", 0)), "reach": int(d.get("reach", 0)),
                "impressions": int(d.get("impressions", 0))}
    except:
        return None

with st.spinner("Loading overview..."):
    meta      = get_meta_summary()
    shopify   = get_shopify_summary()
    qb        = get_qb_summary()
    instagram = get_instagram_summary()
    google    = get_google_ads_summary()

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
                    client    = ac.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
                    meta_ctx  = f"Spend ${meta['spend']:,.2f} | Clicks {meta['clicks']:,} | Impressions {meta['impressions']:,}" if meta else "unavailable"
                    shop_ctx  = f"Revenue ${shopify['revenue_30d']:,.2f} (30d) | Orders {shopify['orders_30d']} (30d) | Total Orders All-Time {shopify['total_orders']}" if shopify else "unavailable"
                    qb_ctx    = f"Net Income YTD ${qb['net_income']:,.2f}" if qb and qb.get("net_income") is not None else "unavailable"
                    system_p  = f"""You are a growth analyst for Shpapi, a clothing and sunglasses brand. Speak directly and conversationally — like a smart advisor talking to the founder, not a consultant writing a report. No bullet points. No headers. Just clear, plain sentences that get straight to the point. Keep responses under 150 words.
Current live data:
- Meta Ads: {meta_ctx}
- Shopify: {shop_ctx}
- QuickBooks: {qb_ctx}"""
                    resp = client.messages.create(
                        model="claude-haiku-4-5-20251001",
                        max_tokens=512,
                        system=system_p,
                        messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.ai_messages]
                    )
                    answer = resp.content[0].text
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

col1, col2, col3, col4, col5 = st.columns(5, gap="medium")

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
    if qb and qb.get("net_income") is not None:
        ni      = qb["net_income"]
        ni_str  = f"${ni:,.2f}"
        ni_col  = "#22c55e" if ni >= 0 else "#ef4444"
        st.markdown(f"""
        <div class="platform-card" style="border-top:3px solid #f59e0b;">
          <div class="platform-title">QuickBooks</div>
          <div class="platform-metric-label">Net Income (YTD)</div>
          <div class="platform-metric-value" style="color:{ni_col};">{ni_str}</div>
        </div>
        """, unsafe_allow_html=True)
        st.page_link("pages/4_QuickBooks.py", label="View QuickBooks details →")
    else:
        st.markdown(f"""
        <div class="platform-card" style="border-top:3px solid #f59e0b;opacity:0.7;">
          <div class="platform-title">QuickBooks</div>
          <div style="text-align:center;padding:3rem 1rem;">
            <div style="font-size:0.85rem;font-weight:600;color:{T2};margin-bottom:0.5rem;">Not Connected</div>
            <div style="font-size:0.75rem;color:{T3};">Connect QuickBooks to view financial data.</div>
          </div>
        </div>
        """, unsafe_allow_html=True)
        st.page_link("pages/4_QuickBooks.py", label="Connect QuickBooks →")

with col5:
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
