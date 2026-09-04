import streamlit as st
import pandas as pd
import json
import os
import sys
import uuid
from datetime import date

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import github_store

ASSETS      = os.path.join(os.path.dirname(__file__), "..", "assets")
LOGO_CROP   = os.path.join(ASSETS, "logo_cropped.png")
DATA_FILE   = os.path.join(os.path.dirname(__file__), "..", "data", "ugc_creators.json")
GITHUB_PATH = "data/ugc_creators.json"

BG      = "#0a1628"
SURFACE = "#0e1f3c"
BORDER  = "rgba(255,255,255,0.08)"
T1      = "#ffffff"
T2      = "rgba(255,255,255,0.65)"
T3      = "rgba(255,255,255,0.38)"
BLUE    = "#3b82f6"
GREEN   = "#22c55e"

STATUS_OPTIONS   = ["Not Contacted", "Reached Out", "Negotiating", "Live", "Declined"]
PLATFORM_OPTIONS = ["Instagram", "TikTok", "YouTube", "Other"]

st.set_page_config(page_title="Shpapi · UGC Creators", layout="wide", initial_sidebar_state="collapsed")

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
_c_logo, _c_h, _c_m, _c_s, _c_g, _c_ig, _c_rp, _c_ai, _c_inv, _c_ugc, _ = st.columns([1.5, 1, 1, 1, 1.2, 1.0, 1.0, 0.9, 1.0, 1.3, 0.1])
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
    st.markdown(f'<div style="padding-top:1.1rem;"><span style="padding:0.35rem 0.9rem;border-radius:6px;font-size:0.8rem;font-weight:700;color:{BLUE};background:rgba(59,130,246,0.18);white-space:nowrap;">UGC Creators</span></div>', unsafe_allow_html=True)
st.markdown(f'<div style="border-top:1px solid {BORDER};margin:0.5rem 0 1.8rem;"></div>', unsafe_allow_html=True)

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="padding-bottom:1.4rem;border-bottom:1px solid {BORDER};margin-bottom:2rem;">
  <div style="font-size:0.62rem;font-weight:600;text-transform:uppercase;letter-spacing:2.5px;color:{T3};">
    UGC Creators &nbsp;·&nbsp; Outreach &amp; Live Content Tracker
  </div>
</div>
""", unsafe_allow_html=True)

# ── Load data ────────────────────────────────────────────────────────────────
COLUMNS = ["id", "name", "platform", "handle", "contact", "status", "date_reached_out", "content_url", "notes"]

def load_creators():
    if github_store.available():
        data, sha = github_store.load_json(GITHUB_PATH, {"creators": []})
        st.session_state["_ugc_sha"] = sha
        return data.get("creators", [])
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE) as f:
        return json.load(f).get("creators", [])

def save_creators(records):
    if github_store.available():
        new_sha = github_store.save_json(
            GITHUB_PATH, {"creators": records},
            st.session_state.get("_ugc_sha"),
            "Update UGC creator roster",
        )
        st.session_state["_ugc_sha"] = new_sha
        return
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump({"creators": records}, f, indent=2, default=str)

if github_store.available():
    st.caption("Synced to GitHub — changes are saved permanently.")
else:
    st.warning("GITHUB_TOKEN secret not set — changes are only saved to this session's local disk and will be lost on restart. See github_store.py for setup.", icon="⚠️")

creators = load_creators()

df = pd.DataFrame(creators, columns=COLUMNS) if creators else pd.DataFrame(columns=COLUMNS)
if "date_reached_out" in df.columns:
    df["date_reached_out"] = pd.to_datetime(df["date_reached_out"], errors="coerce").dt.date

# ── KPIs ─────────────────────────────────────────────────────────────────────
total_creators = len(df)
reached_out_or_further = df[df["status"] != "Not Contacted"] if total_creators else df
reached_out_count = len(reached_out_or_further)
live_count = len(df[df["status"] == "Live"]) if total_creators else 0
conversion_rate = (live_count / reached_out_count * 100) if reached_out_count else 0

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi">
    <div class="kpi-label">Total Creators Tracked</div>
    <div class="kpi-value">{total_creators}</div>
    <div class="kpi-sub">All creators on your radar</div>
  </div>
  <div class="kpi">
    <div class="kpi-label">Reached Out</div>
    <div class="kpi-value">{reached_out_count}</div>
    <div class="kpi-sub">Contacted, negotiating, live, or declined</div>
  </div>
  <div class="kpi">
    <div class="kpi-label">Currently Live</div>
    <div class="kpi-value" style="color:{GREEN};">{live_count}</div>
    <div class="kpi-sub">Content posted and running</div>
  </div>
  <div class="kpi">
    <div class="kpi-label">Reach-Out → Live Rate</div>
    <div class="kpi-value">{conversion_rate:.0f}%</div>
    <div class="kpi-sub">Of everyone you've contacted</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Editable roster ──────────────────────────────────────────────────────────
st.markdown('<div class="section">Creator Roster</div>', unsafe_allow_html=True)
st.markdown(f'<div style="font-size:0.78rem;color:{T3};margin:-0.6rem 0 1rem;">Add a row for every creator you\'re tracking. Edit any cell directly — changes save automatically. Use the trash icon on a row to remove a creator.</div>', unsafe_allow_html=True)

edited_df = st.data_editor(
    df,
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
    key="ugc_editor",
    column_order=["name", "platform", "handle", "contact", "status", "date_reached_out", "content_url", "notes"],
    column_config={
        "id": None,
        "name": st.column_config.TextColumn("Name", width="medium"),
        "platform": st.column_config.SelectboxColumn("Platform", options=PLATFORM_OPTIONS, width="small"),
        "handle": st.column_config.TextColumn("Handle", width="small"),
        "contact": st.column_config.TextColumn("Contact (email / DM)", width="medium"),
        "status": st.column_config.SelectboxColumn("Status", options=STATUS_OPTIONS, width="small", required=True, default="Not Contacted"),
        "date_reached_out": st.column_config.DateColumn("Date Reached Out", width="small"),
        "content_url": st.column_config.LinkColumn("Live Content Link", width="medium"),
        "notes": st.column_config.TextColumn("Notes", width="large"),
    },
)

# ── Persist changes ──────────────────────────────────────────────────────────
to_save = edited_df.copy()
to_save["status"] = to_save["status"].fillna("Not Contacted")
if "id" in to_save.columns:
    to_save["id"] = to_save["id"].apply(lambda x: x if isinstance(x, str) and x else str(uuid.uuid4()))
else:
    to_save["id"] = [str(uuid.uuid4()) for _ in range(len(to_save))]
to_save = to_save.dropna(subset=["name"])
to_save = to_save[to_save["name"].astype(str).str.strip() != ""]

records = json.loads(to_save.to_json(orient="records", date_format="iso"))
for r in records:
    if r.get("date_reached_out"):
        r["date_reached_out"] = str(r["date_reached_out"])[:10]

if records != creators:
    try:
        save_creators(records)
        st.rerun()
    except Exception as e:
        st.error(f"Couldn't save changes to GitHub: {e}")

st.markdown(f"""
<div style="font-size:0.72rem;color:{T3};margin-top:1rem;padding-top:1.2rem;border-top:1px solid {BORDER};line-height:1.6;">
  Status moves through: Not Contacted → Reached Out → Negotiating → Live (or Declined). Drop the live post/reel/video link in "Live Content Link" once it's posted.
</div>
""", unsafe_allow_html=True)
