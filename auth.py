import streamlit as st
from datetime import datetime, timedelta

MAX_ATTEMPTS  = 5
LOCKOUT_MINS  = 15

def check_password():
    if st.session_state.get("authenticated"):
        return True

    BG      = "#0a1628"
    SURFACE = "#0e1f3c"
    BORDER  = "rgba(255,255,255,0.08)"
    BLUE    = "#3b82f6"
    T2      = "rgba(255,255,255,0.65)"
    T3      = "rgba(255,255,255,0.38)"
    RED     = "#ef4444"

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
    input[type="password"]::-ms-reveal,
    input[type="password"]::-ms-clear,
    input::-webkit-credentials-auto-fill-button,
    input::-webkit-contacts-auto-fill-button {{
        display: none !important;
        visibility: hidden !important;
    }}
    div[data-testid="stTextInput"] button,
    div[data-baseweb="input"] button,
    button[data-testid="InputInstructionsButton"] {{
        display: none !important;
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

        # Check if currently locked out
        lockout_until = st.session_state.get("lockout_until")
        if lockout_until and datetime.now() < lockout_until:
            remaining = int((lockout_until - datetime.now()).total_seconds() / 60) + 1
            st.markdown(f"""
            <div style="background:rgba(239,68,68,0.12);border:1px solid rgba(239,68,68,0.3);
                        border-radius:10px;padding:1rem 1.2rem;text-align:center;">
                <div style="color:{RED};font-weight:600;font-size:0.85rem;">Too many failed attempts</div>
                <div style="color:{T2};font-size:0.78rem;margin-top:0.3rem;">
                    Try again in {remaining} minute{"s" if remaining != 1 else ""}.
                </div>
            </div>
            """, unsafe_allow_html=True)
            return False

        attempts = st.session_state.get("login_attempts", 0)

        with st.form("login_form"):
            st.markdown(f'<div style="font-size:0.82rem;font-weight:600;color:{T2};margin-bottom:0.5rem;">Sign in to continue</div>', unsafe_allow_html=True)
            username  = st.text_input("Username")
            password  = st.text_input("Password", type="password")

            if attempts > 0:
                left = MAX_ATTEMPTS - attempts
                st.markdown(f'<div style="font-size:0.74rem;color:{RED};margin-top:0.25rem;">{left} attempt{"s" if left != 1 else ""} remaining before lockout.</div>', unsafe_allow_html=True)

            submitted = st.form_submit_button("Sign In", use_container_width=True)
            if submitted:
                if (username == st.secrets.get("USERNAME", "") and
                        password == st.secrets.get("PASSWORD", "")):
                    st.session_state["authenticated"]  = True
                    st.session_state["login_attempts"] = 0
                    st.session_state.pop("lockout_until", None)
                    st.rerun()
                else:
                    new_attempts = attempts + 1
                    st.session_state["login_attempts"] = new_attempts
                    if new_attempts >= MAX_ATTEMPTS:
                        st.session_state["lockout_until"] = datetime.now() + timedelta(minutes=LOCKOUT_MINS)
                        st.session_state["login_attempts"] = 0
                        st.rerun()
                    else:
                        st.error("Incorrect username or password.")
    return False
