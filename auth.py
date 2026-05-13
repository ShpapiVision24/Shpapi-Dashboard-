import streamlit as st

BG      = "#0a1628"
SURFACE = "#0e1f3c"
BORDER  = "rgba(255,255,255,0.08)"
BLUE    = "#3b82f6"
T2      = "rgba(255,255,255,0.65)"
T3      = "rgba(255,255,255,0.38)"

def check_password():
    if st.session_state.get("authenticated"):
        return True

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    *, *::before, *::after {{ font-family: 'Inter', sans-serif !important; box-sizing: border-box; }}
    html, body, .stApp {{ background: {BG} !important; color: #ffffff; }}
    #MainMenu, footer, header {{ visibility: hidden; }}
    section[data-testid="stSidebar"] {{ display: none !important; }}
    .block-container {{ padding: 0 !important; max-width: 100% !important; }}
    div[data-testid="stForm"] {{
        background: {SURFACE};
        border: 1px solid {BORDER};
        border-radius: 16px;
        padding: 2.5rem;
        max-width: 380px;
        margin: 0 auto;
    }}
    div[data-testid="stForm"] input {{
        background: rgba(255,255,255,0.06) !important;
        border: 1px solid {BORDER} !important;
        border-radius: 8px !important;
        color: #ffffff !important;
    }}
    div[data-testid="stForm"] button[kind="primaryFormSubmit"] {{
        background: {BLUE} !important;
        border: none !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        font-weight: 600 !important;
    }}
    label {{ color: {T2} !important; font-size: 0.78rem !important; font-weight: 600 !important; }}
    </style>
    <div style="display:flex;flex-direction:column;justify-content:center;align-items:center;min-height:100vh;padding:2rem;">
      <div style="text-align:center;margin-bottom:2.5rem;">
        <div style="font-size:2rem;font-weight:700;color:#ffffff;letter-spacing:-0.5px;">Shpapi</div>
        <div style="font-size:0.72rem;font-weight:600;text-transform:uppercase;letter-spacing:2.5px;color:{T3};margin-top:0.4rem;">Analytics Dashboard</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            st.markdown(f'<div style="font-size:0.85rem;font-weight:600;color:{T2};margin-bottom:1rem;">Sign in to continue</div>', unsafe_allow_html=True)
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Sign In", use_container_width=True)
            if submitted:
                valid_user = st.secrets.get("USERNAME", "")
                valid_pass = st.secrets.get("PASSWORD", "")
                if username == valid_user and password == valid_pass:
                    st.session_state["authenticated"] = True
                    st.rerun()
                else:
                    st.error("Incorrect username or password.")
    return False
