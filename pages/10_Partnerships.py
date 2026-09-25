import streamlit as st
import pandas as pd
import json
import os
import sys
import uuid
import requests
from datetime import date, datetime

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import github_store

ASSETS      = os.path.join(os.path.dirname(__file__), "..", "assets")
LOGO_CROP   = os.path.join(ASSETS, "logo_cropped.png")
DATA_FILE   = os.path.join(os.path.dirname(__file__), "..", "data", "partnerships.json")
GITHUB_PATH = "data/partnerships.json"

BG      = "#0a1628"
SURFACE = "#0e1f3c"
BORDER  = "rgba(255,255,255,0.08)"
T1      = "#ffffff"
T2      = "rgba(255,255,255,0.65)"
T3      = "rgba(255,255,255,0.38)"
BLUE    = "#3b82f6"
GREEN   = "#22c55e"
RED     = "#ef4444"

STATUS_OPTIONS  = ["Sent", "Replied", "Declined", "Partnered", "Bounced"]
REPLIED_STATUSES = {"Replied", "Declined", "Partnered"}

st.set_page_config(page_title="Shpapi · Partnerships", layout="wide", initial_sidebar_state="collapsed")

from auth import check_password
if not check_password():
    st.stop()

from mobile import inject_mobile_css
inject_mobile_css()

from ios_theme import inject_ios_theme
inject_ios_theme()

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
.surface {{ background: {SURFACE}; border: 1px solid {BORDER}; border-radius: 12px; padding: 1.4rem 1.4rem 1.2rem; margin-bottom: 1.2rem; }}
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
with st.container(key="navbar"):
    _c_logo, _c_h, _c_m, _c_s, _c_g, _c_ig, _c_rp, _c_ai, _c_inv, _c_ugc, _c_pt, _ = st.columns([1.5, 1, 1, 1, 1.2, 1.0, 1.0, 0.9, 1.0, 1.3, 1.3, 0.1])
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
    with _c_pt:
        st.markdown(f'<div style="padding-top:1.1rem;"><span style="padding:0.35rem 0.9rem;border-radius:6px;font-size:0.8rem;font-weight:700;color:{BLUE};background:rgba(59,130,246,0.18);white-space:nowrap;">Partnerships</span></div>', unsafe_allow_html=True)
st.markdown(f'<div style="border-top:1px solid {BORDER};margin:0.5rem 0 1.8rem;"></div>', unsafe_allow_html=True)

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="padding-bottom:1.4rem;border-bottom:1px solid {BORDER};margin-bottom:2rem;">
  <div style="font-size:0.62rem;font-weight:600;text-transform:uppercase;letter-spacing:2.5px;color:{T3};">
    Partnerships &nbsp;·&nbsp; Boutique &amp; Shop Outreach Tracker
  </div>
</div>
""", unsafe_allow_html=True)

# ── Load data ────────────────────────────────────────────────────────────────
COLUMNS = ["id", "business_name", "contact_name", "contact_email", "date_sent",
           "email_style", "status", "reply_date", "notes"]

def load_outreach():
    if github_store.available():
        data, sha = github_store.load_json(GITHUB_PATH, {"outreach": []})
        st.session_state["_partnerships_sha"] = sha
        return data.get("outreach", [])
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE) as f:
        return json.load(f).get("outreach", [])

def save_outreach(records):
    if github_store.available():
        new_sha = github_store.save_json(
            GITHUB_PATH, {"outreach": records},
            st.session_state.get("_partnerships_sha"),
            "Update partnerships outreach log",
        )
        st.session_state["_partnerships_sha"] = new_sha
        return
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump({"outreach": records}, f, indent=2, default=str)

if github_store.available():
    st.caption("Synced to GitHub — changes are saved permanently.")
else:
    st.warning("GITHUB_TOKEN secret not set — changes are only saved to this session's local disk and will be lost on restart. See github_store.py for setup.", icon="⚠️")

outreach = load_outreach()

df = pd.DataFrame(outreach, columns=COLUMNS) if outreach else pd.DataFrame(columns=COLUMNS)
if "date_sent" in df.columns:
    df["date_sent"] = pd.to_datetime(df["date_sent"], errors="coerce").dt.date
if "reply_date" in df.columns:
    df["reply_date"] = pd.to_datetime(df["reply_date"], errors="coerce").dt.date

# ── KPIs ─────────────────────────────────────────────────────────────────────
total_sent  = len(df)
bounced     = int((df["status"] == "Bounced").sum()) if total_sent else 0
deliverable = total_sent - bounced
replied     = int(df["status"].isin(REPLIED_STATUSES).sum()) if total_sent else 0
reply_rate  = (replied / deliverable * 100) if deliverable else 0
partnered   = int((df["status"] == "Partnered").sum()) if total_sent else 0

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi">
    <div class="kpi-label">Emails Sent</div>
    <div class="kpi-value">{total_sent}</div>
    <div class="kpi-sub">{bounced} bounced</div>
  </div>
  <div class="kpi">
    <div class="kpi-label">Replies</div>
    <div class="kpi-value">{replied}</div>
    <div class="kpi-sub">Replied, declined, or partnered</div>
  </div>
  <div class="kpi">
    <div class="kpi-label">Reply Rate</div>
    <div class="kpi-value" style="color:{GREEN if reply_rate >= 20 else (T1 if reply_rate >= 10 else RED)};">{reply_rate:.0f}%</div>
    <div class="kpi-sub">Of deliverable emails ({deliverable})</div>
  </div>
  <div class="kpi">
    <div class="kpi-label">Partnered</div>
    <div class="kpi-value" style="color:{GREEN};">{partnered}</div>
    <div class="kpi-sub">Turned into an actual partnership</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Reply rate by email style ────────────────────────────────────────────────
st.markdown('<div class="section">Reply Rate by Email Style</div>', unsafe_allow_html=True)
st.markdown(f'<div style="font-size:0.78rem;color:{T3};margin:-0.6rem 0 1rem;">This is the whole point — tag each outreach with whatever you called that version of the email (e.g. "Casual v1", "Direct pitch", "Story-driven"), and see which one actually gets replies.</div>', unsafe_allow_html=True)

style_df = df[df["email_style"].astype(str).str.strip() != ""].copy() if total_sent else df.copy()
style_df = style_df[style_df["status"] != "Bounced"]
if not style_df.empty:
    style_df["replied_flag"] = style_df["status"].isin(REPLIED_STATUSES)
    by_style = (style_df.groupby("email_style")
                .agg(sent=("status", "size"), replies=("replied_flag", "sum"))
                .reset_index())
    by_style["reply_rate"] = (by_style["replies"] / by_style["sent"] * 100).round(0)
    by_style = by_style.sort_values("reply_rate", ascending=False)
    by_style["Reply Rate"] = by_style["reply_rate"].map(lambda x: f"{x:.0f}%")
    by_style = by_style.rename(columns={"email_style": "Email Style", "sent": "Sent", "replies": "Replies"})
    st.dataframe(by_style[["Email Style", "Sent", "Replies", "Reply Rate"]],
                 use_container_width=True, hide_index=True)
else:
    st.markdown(f'<div style="text-align:center;padding:2rem;color:{T3};font-size:0.85rem;">Log some outreach with an Email Style tag below to see this breakdown.</div>', unsafe_allow_html=True)

# ── Gmail reply check ────────────────────────────────────────────────────────
st.markdown('<div class="section">Check Gmail for Replies</div>', unsafe_allow_html=True)

def _gmail_access_token():
    cfg = st.secrets.get("gmail")
    if not cfg:
        return None
    r = requests.post("https://oauth2.googleapis.com/token", data={
        "client_id": cfg["client_id"], "client_secret": cfg["client_secret"],
        "refresh_token": cfg["refresh_token"], "grant_type": "refresh_token",
    }, timeout=15)
    r.raise_for_status()
    return r.json()["access_token"]

def check_gmail_replies(records):
    token = _gmail_access_token()
    checked, found = 0, 0
    for r in records:
        if r.get("status") != "Sent" or not r.get("contact_email") or not r.get("date_sent"):
            continue
        checked += 1
        after = str(r["date_sent"])[:10].replace("-", "/")
        resp = requests.get(
            "https://gmail.googleapis.com/gmail/v1/users/me/messages",
            headers={"Authorization": f"Bearer {token}"},
            params={"q": f"from:{r['contact_email']} after:{after}", "maxResults": 1},
            timeout=15,
        )
        resp.raise_for_status()
        if resp.json().get("messages"):
            r["status"] = "Replied"
            r["reply_date"] = date.today().isoformat()
            found += 1
    return records, checked, found

if not st.secrets.get("gmail"):
    st.markdown(f"""
    <div style="background:{SURFACE};border:1px solid {BORDER};border-radius:12px;padding:1.25rem 1.5rem;font-size:0.82rem;color:{T2};line-height:1.6;">
      Not connected yet — replies have to be marked manually below (set Status to "Replied" on the row) until this is set up.
      <br><br>
      To turn this on: create (or reuse) a Google OAuth client with Gmail API access, run a token script to get a refresh token
      for your business Gmail account (scope <code>gmail.readonly</code>), then add a <code>[gmail]</code> block to Streamlit
      secrets with <code>client_id</code>, <code>client_secret</code>, and <code>refresh_token</code>. Once that's there, this
      button will check every "Sent" row against your inbox automatically.
    </div>
    """, unsafe_allow_html=True)
else:
    if st.button("Check now", key="check_gmail_replies"):
        try:
            with st.spinner("Checking Gmail for replies..."):
                updated, checked, found = check_gmail_replies(outreach)
            save_outreach(updated)
            st.success(f"Checked {checked} pending outreach — found {found} new repl{'y' if found == 1 else 'ies'}.")
            st.rerun()
        except Exception as e:
            st.error(f"Couldn't check Gmail: {e}")

# ── Editable outreach log ────────────────────────────────────────────────────
st.markdown('<div class="section">Outreach Log</div>', unsafe_allow_html=True)
st.markdown(f'<div style="font-size:0.78rem;color:{T3};margin:-0.6rem 0 1rem;">Add a row every time you send a partnership pitch. Edit any cell directly — changes save automatically. Use the trash icon on a row to remove an entry.</div>', unsafe_allow_html=True)

edited_df = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
    key="partnerships_editor",
    column_order=["business_name", "contact_name", "contact_email", "date_sent",
                  "email_style", "status", "reply_date", "notes"],
    column_config={
        "id": None,
        "business_name": st.column_config.TextColumn("Business / Boutique", width="medium"),
        "contact_name": st.column_config.TextColumn("Contact Name", width="small"),
        "contact_email": st.column_config.TextColumn("Contact Email", width="medium"),
        "date_sent": st.column_config.DateColumn("Date Sent", width="small"),
        "email_style": st.column_config.TextColumn("Email Style", width="small",
            help="Tag it with whatever name you're using for this version of the email, so the breakdown above can compare styles."),
        "status": st.column_config.SelectboxColumn("Status", options=STATUS_OPTIONS, width="small", required=True, default="Sent"),
        "reply_date": st.column_config.DateColumn("Reply Date", width="small"),
        "notes": st.column_config.TextColumn("Notes", width="large"),
    },
)

# ── Persist changes ──────────────────────────────────────────────────────────
to_save = edited_df.copy()
to_save["status"] = to_save["status"].fillna("Sent")
if "id" in to_save.columns:
    to_save["id"] = to_save["id"].apply(lambda x: x if isinstance(x, str) and x else str(uuid.uuid4()))
else:
    to_save["id"] = [str(uuid.uuid4()) for _ in range(len(to_save))]
to_save = to_save.dropna(subset=["business_name"])
to_save = to_save[to_save["business_name"].astype(str).str.strip() != ""]

records = json.loads(to_save.to_json(orient="records", date_format="iso"))
for r in records:
    if r.get("date_sent"):
        r["date_sent"] = str(r["date_sent"])[:10]
    if r.get("reply_date"):
        r["reply_date"] = str(r["reply_date"])[:10]

if records != outreach:
    try:
        save_outreach(records)
        st.rerun()
    except Exception as e:
        st.error(f"Couldn't save changes to GitHub: {e}")

st.markdown(f"""
<div style="font-size:0.72rem;color:{T3};margin-top:1rem;padding-top:1.2rem;border-top:1px solid {BORDER};line-height:1.6;">
  Status moves through: Sent → Replied / Declined / Partnered / Bounced. Anything other than "Sent" or "Bounced" counts
  as a reply for the reply-rate math above — a decline still means they responded.
</div>
""", unsafe_allow_html=True)
