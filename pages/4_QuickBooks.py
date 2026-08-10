import streamlit as st
import requests
import base64
import os
from urllib.parse import urlencode
from datetime import datetime

CLIENT_ID     = st.secrets["QB_CLIENT_ID"]
CLIENT_SECRET = st.secrets["QB_CLIENT_SECRET"]
REDIRECT_URI  = st.secrets["QB_REDIRECT_URI"]
ENV           = st.secrets.get("QB_ENVIRONMENT", "sandbox")

_STORED_TOKEN   = st.secrets.get("QB_ACCESS_TOKEN", "")
_STORED_REFRESH = st.secrets.get("QB_REFRESH_TOKEN", "")
_STORED_REALM   = st.secrets.get("QB_REALM_ID", "")

AUTH_URL  = "https://appcenter.intuit.com/connect/oauth2"
TOKEN_URL = "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer"
QB_BASE   = "https://sandbox-quickbooks.api.intuit.com" if ENV == "sandbox" else "https://quickbooks.api.intuit.com"
SCOPE     = "com.intuit.quickbooks.accounting"

ASSETS    = os.path.join(os.path.dirname(__file__), "..", "assets")
LOGO_CROP = os.path.join(ASSETS, "logo_cropped.png")

BG      = "#0a1628"
SURFACE = "#0e1f3c"
BORDER  = "rgba(255,255,255,0.08)"
T1      = "#ffffff"
T2      = "rgba(255,255,255,0.65)"
T3      = "rgba(255,255,255,0.38)"
BLUE    = "#3b82f6"
GREEN   = "#22c55e"

st.set_page_config(page_title="Shpapi · QuickBooks", layout="wide", initial_sidebar_state="collapsed")

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
_c_logo, _c_h, _c_m, _c_s, _c_g, _c_qb, _c_ig, _c_rp, _c_ai, _ = st.columns([1.5, 1, 1, 1, 1.2, 1.3, 1.0, 1.0, 0.9, 0.1])
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
    st.markdown(f'<div style="padding-top:1.1rem;"><span style="padding:0.35rem 0.9rem;border-radius:6px;font-size:0.8rem;font-weight:700;color:{BLUE};background:rgba(59,130,246,0.18);white-space:nowrap;">QuickBooks</span></div>', unsafe_allow_html=True)
with _c_ig:
    st.page_link("pages/5_Instagram.py", label="Instagram")
with _c_rp:
    st.page_link("pages/6_Report.py", label="Reports")
with _c_ai:
    st.page_link("pages/7_AI_Assistant.py", label="AI Chat")
st.markdown(f'<div style="border-top:1px solid {BORDER};margin:0.5rem 0 2rem;"></div>', unsafe_allow_html=True)

st.markdown(f"""
<div style="margin-bottom:2.5rem;">
  <div style="font-size:1.4rem;font-weight:700;color:{T1};letter-spacing:-0.5px;">QuickBooks</div>
  <div style="font-size:0.7rem;font-weight:500;text-transform:uppercase;letter-spacing:2px;color:{T3};margin-top:0.3rem;">Shpapi &nbsp;·&nbsp; Financial Overview</div>
</div>
""", unsafe_allow_html=True)

# ── Helpers ───────────────────────────────────────────────────────────────────
def get_auth_url():
    return f"{AUTH_URL}?" + urlencode({
        "client_id": CLIENT_ID, "response_type": "code",
        "scope": SCOPE, "redirect_uri": REDIRECT_URI, "state": "shpapi_qb",
        "prompt": "login",
    })

def exchange_code(code):
    creds = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    r = requests.post(TOKEN_URL,
        headers={"Authorization": f"Basic {creds}", "Content-Type": "application/x-www-form-urlencoded"},
        data={"grant_type": "authorization_code", "code": code, "redirect_uri": REDIRECT_URI},
        timeout=15)
    return r.json()

def refresh_access_token(refresh_tok):
    creds = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    r = requests.post(TOKEN_URL,
        headers={"Authorization": f"Basic {creds}", "Content-Type": "application/x-www-form-urlencoded"},
        data={"grant_type": "refresh_token", "refresh_token": refresh_tok},
        timeout=15)
    return r.json()

def qb_get(path, token, realm_id, params=None):
    r = requests.get(f"{QB_BASE}/v3/company/{realm_id}{path}",
        headers={"Authorization": f"Bearer {token}", "Accept": "application/json"},
        params={"minorversion": "65", **(params or {})}, timeout=30)
    return r.json()

def parse_pnl(data):
    result = {"income": 0.0, "expenses": 0.0, "net": 0.0, "rows": []}
    rows = data.get("Rows", {}).get("Row", [])
    for section in rows:
        group = section.get("group", "")
        summary = section.get("Summary", {}).get("ColData", [])
        if len(summary) >= 2:
            try:
                val = float(summary[1].get("value", 0) or 0)
            except (ValueError, TypeError):
                val = 0.0
            if group in ("Income", "GrossProfit", "TotalIncome", "OtherIncome"):
                result["income"] += val
            elif group in ("Expenses", "NetExpenses", "CostOfGoodsSold", "COGS",
                           "OtherExpenses", "TotalExpenses", "NetOtherIncome"):
                result["expenses"] += val
            elif group == "NetIncome":
                result["net"] = val
        if group in ("Income", "GrossProfit", "TotalIncome", "OtherIncome"):
            for row in section.get("Rows", {}).get("Row", []):
                cols = row.get("ColData", [])
                if len(cols) >= 2:
                    try:
                        result["rows"].append({
                            "name": cols[0].get("value", ""),
                            "amount": float(cols[1].get("value", 0) or 0),
                        })
                    except (ValueError, TypeError):
                        pass
    if result["net"] == 0.0 and (result["income"] or result["expenses"]):
        result["net"] = result["income"] - result["expenses"]
    return result

def disconnect():
    for k in ["qb_token", "qb_refresh", "qb_realm", "qb_just_connected"]:
        st.session_state.pop(k, None)
    st.cache_data.clear()
    st.rerun()

# ── Auto-load stored tokens from secrets ──────────────────────────────────────
if "qb_token" not in st.session_state and _STORED_REALM:
    if _STORED_TOKEN:
        st.session_state["qb_token"]   = _STORED_TOKEN
        st.session_state["qb_refresh"] = _STORED_REFRESH
        st.session_state["qb_realm"]   = _STORED_REALM
    elif _STORED_REFRESH:
        # No stored access token — use refresh token to get a fresh one
        new_tok = refresh_access_token(_STORED_REFRESH)
        if "access_token" in new_tok:
            st.session_state["qb_token"]   = new_tok["access_token"]
            st.session_state["qb_refresh"] = new_tok.get("refresh_token", _STORED_REFRESH)
            st.session_state["qb_realm"]   = _STORED_REALM
        else:
            st.session_state["qb_refresh_error"] = new_tok

# ── Handle OAuth callback ─────────────────────────────────────────────────────
qp = st.query_params
if "code" in qp and "realmId" in qp and "qb_token" not in st.session_state:
    with st.spinner("Connecting to QuickBooks..."):
        tok = exchange_code(qp["code"])
    if "access_token" in tok:
        st.session_state["qb_token"]        = tok["access_token"]
        st.session_state["qb_refresh"]      = tok.get("refresh_token", "")
        st.session_state["qb_realm"]        = qp["realmId"]
        st.session_state["qb_just_connected"] = True
        st.query_params.clear()
        st.rerun()
    else:
        st.error(f"OAuth failed: {tok.get('error', 'unknown')} — {tok.get('error_description', str(tok))}")
        st.caption(f"Client ID in use: `{CLIENT_ID[:12]}...` | Environment: `{ENV}`")
        st.stop()

# ── Not connected ─────────────────────────────────────────────────────────────
if "qb_token" not in st.session_state:
    # Show refresh error if any (helps diagnose invalid_client)
    refresh_err = st.session_state.pop("qb_refresh_error", None)
    if refresh_err:
        err_code = refresh_err.get("error", "unknown")
        err_desc = refresh_err.get("error_description", str(refresh_err))
        with st.expander("⚠️ Auto-connect failed — click for details"):
            st.error(f"**{err_code}**: {err_desc}")
            st.caption(f"Client ID in use: `{CLIENT_ID[:12]}...`")
            st.caption(f"Environment: `{ENV}`")
            st.caption(f"Refresh token prefix: `{_STORED_REFRESH[:12]}...`")

    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown(f"""
        <div style="background:{SURFACE};border:1px solid {BORDER};border-radius:20px;padding:3rem 2.5rem;text-align:center;margin-top:3rem;">
            <div style="font-size:2.5rem;margin-bottom:1rem;">📊</div>
            <div style="font-size:1.2rem;font-weight:700;color:{T1};margin-bottom:0.5rem;">Connect QuickBooks</div>
            <div style="font-size:0.8rem;color:{T2};margin-bottom:2rem;line-height:1.6;">
                Link your QuickBooks account to see your<br>P&L, revenue, expenses, and net income.
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)
        st.link_button("Connect QuickBooks →", url=get_auth_url(), use_container_width=True)
        if ENV == "sandbox":
            st.markdown(f'<div style="text-align:center;font-size:0.7rem;color:{T3};margin-top:0.75rem;">Using sandbox mode — connects to your Intuit sandbox company.</div>', unsafe_allow_html=True)
    st.stop()

# ── Connected ─────────────────────────────────────────────────────────────────
token    = st.session_state["qb_token"]
realm_id = st.session_state["qb_realm"]

# Disconnect button always rendered first so it's never hidden by loading/errors
dcol, _ = st.columns([1, 6])
with dcol:
    if st.button("Disconnect", key="qb_disconnect"):
        disconnect()


now         = datetime.now()
y, m        = now.year, now.month
start_month = f"{y}-{m:02d}-01"
start_year  = f"{y}-01-01"
end_today   = now.strftime("%Y-%m-%d")

@st.cache_data(ttl=1800, show_spinner=False)
def fetch_data(token, realm_id, start, end):
    pnl     = qb_get("/reports/ProfitAndLoss", token, realm_id, {"start_date": start, "end_date": end})
    company = qb_get(f"/companyinfo/{realm_id}", token, realm_id)
    return pnl, company

with st.spinner("Loading QuickBooks data..."):
    try:
        pnl_month, company_data = fetch_data(token, realm_id, start_month, end_today)
        pnl_ytd, _              = fetch_data(token, realm_id, start_year,  end_today)
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        st.stop()

# Auth error — try token refresh before giving up
if "fault" in pnl_month:
    st.cache_data.clear()
    refresh_tok = st.session_state.get("qb_refresh", "")
    if refresh_tok:
        new_tok = refresh_access_token(refresh_tok)
        if "access_token" in new_tok:
            st.session_state["qb_token"]   = new_tok["access_token"]
            st.session_state["qb_refresh"] = new_tok.get("refresh_token", refresh_tok)
            st.rerun()
    err_msg = pnl_month.get("fault", {}).get("error", [{}])[0].get("message", "Unknown error")
    st.error(f"QuickBooks API error: {err_msg}")
    st.info("Your access token has expired. Click **Disconnect** above, then reconnect to generate a fresh token.")
    st.stop()

month_data   = parse_pnl(pnl_month)
ytd_data     = parse_pnl(pnl_ytd)
company_name = company_data.get("CompanyInfo", {}).get("CompanyName", "Your Company")

st.markdown(f'<div style="font-size:0.78rem;color:{T2};margin-bottom:1.5rem;">Connected to <strong style="color:{T1};">{company_name}</strong></div>', unsafe_allow_html=True)

def fmt(v):
    return f"${v:,.0f}" if v >= 0 else f"-${abs(v):,.0f}"

# ── This Month KPIs ───────────────────────────────────────────────────────────
st.markdown('<div class="section">This Month</div>', unsafe_allow_html=True)

net_color = GREEN if month_data["net"] >= 0 else "#ef4444"
if month_data["income"]:
    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi" style="border-top:3px solid {GREEN};">
            <div class="kpi-label">Revenue</div>
            <div class="kpi-value">{fmt(month_data['income'])}</div>
            <div class="kpi-sub">Month to date</div>
        </div>
        <div class="kpi" style="border-top:3px solid #f59e0b;">
            <div class="kpi-label">Expenses</div>
            <div class="kpi-value">{fmt(month_data['expenses'])}</div>
            <div class="kpi-sub">Month to date</div>
        </div>
        <div class="kpi" style="border-top:3px solid {net_color};">
            <div class="kpi-label">Net Income</div>
            <div class="kpi-value" style="color:{net_color};">{fmt(month_data['net'])}</div>
            <div class="kpi-sub">Month to date</div>
        </div>
        <div class="kpi" style="border-top:3px solid {BLUE};">
            <div class="kpi-label">Margin</div>
            <div class="kpi-value">{(month_data['net']/month_data['income']*100):.1f}%</div>
            <div class="kpi-sub">Net margin</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("No income data found for this month yet.")
    with st.expander("Debug — raw QuickBooks response"):
        st.json(pnl_month)

# ── Year to Date KPIs ─────────────────────────────────────────────────────────
st.markdown('<div class="section">Year to Date</div>', unsafe_allow_html=True)
ytd_net_color = GREEN if ytd_data["net"] >= 0 else "#ef4444"
if ytd_data["income"]:
    st.markdown(f"""
    <div class="kpi-grid">
        <div class="kpi">
            <div class="kpi-label">YTD Revenue</div>
            <div class="kpi-value">{fmt(ytd_data['income'])}</div>
        </div>
        <div class="kpi">
            <div class="kpi-label">YTD Expenses</div>
            <div class="kpi-value">{fmt(ytd_data['expenses'])}</div>
        </div>
        <div class="kpi">
            <div class="kpi-label">YTD Net Income</div>
            <div class="kpi-value" style="color:{ytd_net_color};">{fmt(ytd_data['net'])}</div>
        </div>
        <div class="kpi">
            <div class="kpi-label">YTD Margin</div>
            <div class="kpi-value">{(ytd_data['net']/ytd_data['income']*100):.1f}%</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("No year-to-date data found.")

# ── Revenue Breakdown ─────────────────────────────────────────────────────────
if month_data["rows"]:
    st.markdown('<div class="section">Revenue Breakdown (This Month)</div>', unsafe_allow_html=True)
    for item in sorted(month_data["rows"], key=lambda x: x["amount"], reverse=True):
        if item["amount"] and item["name"]:
            pct = (item["amount"] / month_data["income"] * 100) if month_data["income"] else 0
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                        padding:0.65rem 1rem;background:{SURFACE};border:1px solid {BORDER};
                        border-radius:8px;margin-bottom:0.4rem;">
                <span style="font-size:0.8rem;color:{T2};">{item['name']}</span>
                <span style="font-size:0.8rem;font-weight:700;color:{T1};">{fmt(item['amount'])} &nbsp;<span style="color:{T3};font-weight:400;">{pct:.0f}%</span></span>
            </div>
            """, unsafe_allow_html=True)
