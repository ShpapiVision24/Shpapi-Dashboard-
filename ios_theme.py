import streamlit as st

def inject_ios_theme():
    """Nudges the whole app toward an iOS look and feel, on top of each
    page's own colors and layout:

    - System font stack — renders as actual San Francisco on iOS/macOS
      Safari, falls back gracefully elsewhere.
    - Rounder "continuous corner" card shapes instead of the sharper 12px
      boxes.
    - A frosted, translucent nav bar (backdrop-filter blur), like an iOS
      navigation/tab bar floating over content.
    - Pill-shaped buttons and nav links with iOS-style press feedback
      (a quick scale-down on tap instead of an instant, flat click).
    - Slightly rounder form inputs.

    Pure CSS — doesn't touch any page's colors, layout, or markup, so it's
    safe to call on every page right alongside inject_mobile_css().
    """
    st.markdown("""
    <style>
    *, *::before, *::after {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display",
                      "Inter", "Helvetica Neue", Arial, sans-serif !important;
    }

    /* Rounder, "continuous corner" card look across every page */
    .kpi, .surface, .platform-card, .insights-block, .kpi-tile,
    [data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 18px !important;
    }

    /* Frosted glass nav bar, floating over the page like an iOS tab/nav bar */
    .st-key-navbar {
        background: rgba(20, 40, 75, 0.55) !important;
        backdrop-filter: blur(20px) saturate(160%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(160%) !important;
        border-radius: 18px !important;
        padding: 0.3rem 0.5rem !important;
        margin-bottom: 0.25rem !important;
    }

    /* Pill-shaped nav links with iOS-style tap feedback */
    a[data-testid="stPageLink-NavLink"] {
        border-radius: 20px !important;
        transition: background-color 0.15s ease, color 0.15s ease, transform 0.1s ease !important;
    }
    a[data-testid="stPageLink-NavLink"]:active {
        transform: scale(0.95) !important;
    }

    /* Pill-shaped buttons with the same tap feedback */
    .stButton > button {
        border-radius: 20px !important;
        transition: transform 0.1s ease, background-color 0.15s ease !important;
    }
    .stButton > button:active {
        transform: scale(0.96) !important;
    }
    div[data-testid="stDownloadButton"] > button {
        border-radius: 20px !important;
    }

    /* Rounder form inputs */
    div[data-baseweb="select"] > div,
    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stForm"] {
        border-radius: 14px !important;
    }
    </style>
    """, unsafe_allow_html=True)
