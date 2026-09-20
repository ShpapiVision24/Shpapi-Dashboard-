import streamlit as st

def inject_mobile_css():
    """Responsive tweaks so pages stay readable on a phone-width screen.
    Call once per page, after that page's own <style> block, so these
    rules load last and can override the page's fixed-width layout."""
    st.markdown("""
    <style>
    @media (max-width: 640px) {
        .block-container { padding: 1rem 1rem 3rem 1rem !important; }

        .kpi-grid, .insights-grid, .stat-grid {
            grid-template-columns: repeat(2, 1fr) !important;
            gap: 0.6rem !important;
        }
        .kpi-value, .insight-value { font-size: 1.3rem !important; }

        .st-key-navbar [data-testid="stHorizontalBlock"] {
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch !important;
            gap: 0.15rem !important;
        }
        .st-key-navbar [data-testid="stHorizontalBlock"] > div {
            flex: 0 0 auto !important;
            width: auto !important;
            min-width: fit-content !important;
        }
        a[data-testid="stPageLink-NavLink"] {
            padding: 0.3rem 0.55rem !important;
            font-size: 0.68rem !important;
        }

        [data-testid="stDataFrame"] { font-size: 0.78rem !important; }
    }

    @media (max-width: 420px) {
        .kpi-grid, .insights-grid, .stat-grid {
            grid-template-columns: 1fr !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)
