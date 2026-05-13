import streamlit as st
import os

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
.section {{ font-size: 0.62rem; font-weight: 600; text-transform: uppercase; letter-spacing: 2.5px; color: {T3}; margin: 0 0 0.9rem 0; display: flex; align-items: center; gap: 1rem; }}
.section::after {{ content: ''; flex: 1; height: 1px; background: {BORDER}; }}
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
</style>
""", unsafe_allow_html=True)

_NAV_LINK  = f"padding:0.35rem 0.9rem;border-radius:6px;font-size:0.8rem;font-weight:600;color:{T2};text-decoration:none;white-space:nowrap;"
_NAV_ACTIVE = f"padding:0.35rem 0.9rem;border-radius:6px;font-size:0.8rem;font-weight:700;color:{BLUE};background:rgba(59,130,246,0.18);text-decoration:none;white-space:nowrap;"

_c_logo, _c_nav = st.columns([1, 11])
with _c_logo:
    if os.path.exists(LOGO_CROP):
        st.image(LOGO_CROP, width=90)
with _c_nav:
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:0.15rem;padding-top:1.1rem;">
      <a href="/" target="_self" style="{_NAV_LINK}">Home</a>
      <a href="/Meta_Ads" target="_self" style="{_NAV_LINK}">Meta Ads</a>
      <a href="/Shopify" target="_self" style="{_NAV_LINK}">Shopify</a>
      <a href="/Google_Ads" target="_self" style="{_NAV_ACTIVE}">Google Ads</a>
    </div>
    """, unsafe_allow_html=True)
st.markdown(f'<div style="border-top:1px solid {BORDER};margin:0.5rem 0 1.8rem;"></div>', unsafe_allow_html=True)

st.markdown(f"""
<div style="padding-bottom:1.4rem;border-bottom:1px solid {BORDER};margin-bottom:3rem;">
  <div style="font-size:0.62rem;font-weight:600;text-transform:uppercase;letter-spacing:2.5px;color:{T3};">
    Google Ads &nbsp;·&nbsp; Coming Soon
  </div>
</div>
<div style="text-align:center;padding:5rem 2rem;">
  <div style="font-size:1.5rem;font-weight:700;color:{T1};margin-bottom:0.75rem;">Google Ads — Coming Soon</div>
  <div style="font-size:0.9rem;color:{T3};max-width:400px;margin:0 auto;">
    Google Ads integration is being set up. Check back soon for campaign performance, keyword data, and conversion tracking.
  </div>
</div>
""", unsafe_allow_html=True)
