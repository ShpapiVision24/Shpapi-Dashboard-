import streamlit as st
import os

ASSETS    = os.path.join(os.path.dirname(__file__), "..", "assets")
LOGO_CROP = os.path.join(ASSETS, "logo_cropped.png")

BG      = "#0a1628"
SURFACE = "#0e1f3c"
BORDER  = "rgba(255,255,255,0.08)"
T1      = "#ffffff"
T2      = "rgba(255,255,255,0.65)"
T3      = "rgba(255,255,255,0.38)"
BLUE    = "#3b82f6"

st.set_page_config(page_title="Shpapi · More", layout="wide", initial_sidebar_state="collapsed")

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
.section {{ font-size: 0.62rem; font-weight: 600; text-transform: uppercase; letter-spacing: 2.5px; color: {T3}; margin: 0 0 0.9rem 0; display: flex; align-items: center; gap: 1rem; }}
.section::after {{ content: ''; flex: 1; height: 1px; background: {BORDER}; }}
div[data-testid="stPageLink"] {{ border: none !important; background: none !important; box-shadow: none !important; padding: 0 !important; margin: 0 !important; padding-top: 1rem !important; }}
a[data-testid="stPageLink-NavLink"] {{
    color: {T2} !important; font-weight: 500 !important; font-size: 0.70rem !important;
    text-decoration: none !important; padding: 0.3rem 0.75rem !important;
    border-radius: 6px !important; background: transparent !important;
    border: none !important; display: inline-block !important;
}}
a[data-testid="stPageLink-NavLink"]:hover {{ background: rgba(59,130,246,0.15) !important; color: {BLUE} !important; }}
a[data-testid="stPageLink-NavLink"] svg {{ display: none !important; }}

/* Grouped list, iOS Settings-app style — only for rows inside .grouped-list */
.grouped-list {{ background: {SURFACE}; border: 1px solid {BORDER}; border-radius: 18px; overflow: hidden; margin-bottom: 1.5rem; }}
.grouped-list div[data-testid="stPageLink"] {{ padding: 0 !important; }}
.grouped-list a[data-testid="stPageLink-NavLink"] {{
    display: flex !important; align-items: center !important; gap: 0.85rem !important;
    width: 100% !important; padding: 1rem 1.2rem !important; border-radius: 0 !important;
    font-size: 0.95rem !important; font-weight: 500 !important; color: {T1} !important;
    border-bottom: 1px solid {BORDER} !important;
}}
.grouped-list a[data-testid="stPageLink-NavLink"]:hover {{ background: rgba(59,130,246,0.08) !important; }}
.grouped-list a[data-testid="stPageLink-NavLink"]::after {{
    content: '›'; margin-left: auto; color: {T3}; font-size: 1.3rem; font-weight: 400;
}}
.grouped-list [data-testid="stVerticalBlock"] > div:last-child a[data-testid="stPageLink-NavLink"] {{
    border-bottom: none !important;
}}
</style>
""", unsafe_allow_html=True)

# ── Nav (desktop top bar) ────────────────────────────────────────────────────
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
        st.page_link("pages/10_Partnerships.py", label="Partnerships")
st.markdown(f'<div style="border-top:1px solid {BORDER};margin:0.5rem 0 1.8rem;"></div>', unsafe_allow_html=True)

# ── Bottom tab bar (mobile) ──────────────────────────────────────────────────
with st.container(key="tabbar"):
    _t1, _t2, _t3, _t4, _t5 = st.columns(5)
    with _t1:
        st.page_link("app.py", label="Home", icon="🏠")
    with _t2:
        st.page_link("pages/1_Meta_Ads.py", label="Meta", icon="📣")
    with _t3:
        st.page_link("pages/2_Shopify.py", label="Shopify", icon="🛍️")
    with _t4:
        st.page_link("pages/3_Google_Ads.py", label="Google", icon="🔍")
    with _t5:
        st.markdown('<div class="tab-current">⚙️ More</div>', unsafe_allow_html=True)

# ── Page header ───────────────────────────────────────────────────────────────
st.markdown(f"""
<div style="padding-bottom:1.4rem;border-bottom:1px solid {BORDER};margin-bottom:2rem;">
  <div style="font-size:0.62rem;font-weight:600;text-transform:uppercase;letter-spacing:2.5px;color:{T3};">
    More &nbsp;·&nbsp; Everything Else
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section">Browse</div>', unsafe_allow_html=True)
st.markdown('<div class="grouped-list">', unsafe_allow_html=True)
st.page_link("pages/5_Instagram.py", label="Instagram", icon="📷")
st.page_link("pages/6_Report.py", label="Reports", icon="📄")
st.page_link("pages/7_AI_Assistant.py", label="AI Chat", icon="💬")
st.page_link("pages/8_Inventory.py", label="Inventory", icon="📦")
st.page_link("pages/9_UGC_Creators.py", label="UGC Creators", icon="🎬")
st.page_link("pages/10_Partnerships.py", label="Partnerships", icon="🤝")
st.markdown('</div>', unsafe_allow_html=True)
