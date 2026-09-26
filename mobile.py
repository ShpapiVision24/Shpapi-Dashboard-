import streamlit as st

def inject_mobile_css():
    """Responsive tweaks so pages stay readable on a phone-width screen.
    Call once per page, after that page's own <style> block, so these
    rules load last and can override the page's fixed-width layout."""
    st.markdown("""
    <style>
    /* Bottom tab bar: built for mobile, hidden on desktop by default */
    .st-key-tabbar {
        display: none;
    }

    @media (max-width: 640px) {
        .block-container { padding: 1rem 1rem 6.5rem 1rem !important; }

        .kpi-grid, .insights-grid, .stat-grid {
            grid-template-columns: repeat(2, 1fr) !important;
            gap: 0.6rem !important;
        }
        .kpi-value, .insight-value { font-size: 1.3rem !important; }

        /* Top nav bar is replaced by the bottom tab bar on mobile */
        .st-key-navbar { display: none !important; }

        [data-testid="stDataFrame"] { font-size: 0.78rem !important; }

        /* Fixed bottom tab bar, iOS style */
        .st-key-tabbar {
            display: block !important;
            position: fixed;
            left: 0; right: 0; bottom: 0;
            z-index: 9999;
            background: rgba(10, 22, 40, 0.85);
            backdrop-filter: blur(20px) saturate(160%);
            -webkit-backdrop-filter: blur(20px) saturate(160%);
            border-top: 1px solid rgba(255,255,255,0.08);
            padding: 0.4rem 0.3rem calc(0.3rem + env(safe-area-inset-bottom, 0px)) 0.3rem;
        }
        .st-key-tabbar [data-testid="stHorizontalBlock"] {
            flex-wrap: nowrap !important;
            gap: 0 !important;
        }
        .st-key-tabbar div[data-testid="stPageLink"] { padding-top: 0 !important; }
        .st-key-tabbar a[data-testid="stPageLink-NavLink"],
        .st-key-tabbar .tab-current {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            width: 100% !important;
            padding: 0.55rem 0.1rem !important;
            font-size: 0.66rem !important;
            font-weight: 600 !important;
            text-align: center;
            line-height: 1.3 !important;
            border-radius: 12px !important;
        }
        .st-key-tabbar a[data-testid="stPageLink-NavLink"] p,
        .st-key-tabbar .tab-current p { font-size: 0.66rem !important; margin: 0 !important; }
        .st-key-tabbar a[data-testid="stPageLink-NavLink"] { color: rgba(255,255,255,0.55) !important; }
        .st-key-tabbar .tab-current {
            color: #3b82f6 !important;
            background: rgba(59,130,246,0.14) !important;
        }
    }

    @media (max-width: 420px) {
        .kpi-grid, .insights-grid, .stat-grid {
            grid-template-columns: 1fr !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)
