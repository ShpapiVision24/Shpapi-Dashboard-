import streamlit as st

def check_password():
    if st.session_state.get("authenticated"):
        return True

    BG      = "#0a1628"
    SURFACE = "#0e1f3c"
    BORDER  = "rgba(255,255,255,0.08)"
    BLUE    = "#3b82f6"
    T2      = "rgba(255,255,255,0.65)"
    T3      = "rgba(255,255,255,0.38)"

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    *, *::before, *::after {{ font-family: 'Inter', sans-serif !important; }}
    html, body, .stApp {{ background: {BG} !important; color: #fff; }}
    #MainMenu, footer, header {{ visibility: hidden; }}
    section[data-testid="stSidebar"] {{ display: none !important; }}
    .block-container {{ padding: 0 !important; max-width: 100% !important; }}
    div[data-testid="stForm"] {{
        background: {SURFACE};
        border: 1px solid {BORDER};
        border-radius: 16px;
        padding: 2.5rem 2.5rem 2rem;
        margin-top: 1rem;
    }}
    div[data-testid="stForm"] input {{
        background: rgba(255,255,255,0.07) !important;
        border: 1px solid {BORDER} !important;
        border-radius: 8px !important;
        color: #fff !important;
    }}
    button[kind="primaryFormSubmit"] {{
        background: {BLUE} !important;
        border: none !important;
        border-radius: 8px !important;
        color: #fff !important;
        font-weight: 600 !important;
        margin-top: 0.5rem;
    }}
    label {{ color: {T2} !important; font-size: 0.78rem !important; font-weight: 600 !important; }}
    p {{ color: {T2}; }}
    </style>
    """, unsafe_allow_html=True)

    # Vertical centering via padding
    for _ in range(6):
        st.markdown(" ")

    _, col, _ = st.columns([1, 1.2, 1])
    with col:
        st.markdown(f"""
        <div style="text-align:center;margin-bottom:2rem;">
          <div style="font-size:2.2rem;font-weight:700;color:#ffffff;letter-spacing:-0.5px;">Shpapi</div>
          <div style="font-size:0.7rem;font-weight:600;text-transform:uppercase;letter-spacing:2.5px;color:{T3};margin-top:0.4rem;">Analytics Dashboard</div>
        </div>
        """, unsafe_allow_html=True)
        with st.form("login_form"):
            st.markdown(f'<div style="font-size:0.82rem;font-weight:600;color:{T2};margin-bottom:0.5rem;">Sign in to continue</div>', unsafe_allow_html=True)
            username  = st.text_input("Username")
            password  = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Sign In", use_container_width=True)
            if submitted:
                if (username == st.secrets.get("USERNAME", "") and
                        password == st.secrets.get("PASSWORD", "")):
                    st.session_state["authenticated"] = True
                    st.rerun()
                else:
                    st.error("Incorrect username or password.")
    return False
