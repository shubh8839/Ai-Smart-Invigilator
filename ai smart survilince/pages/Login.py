import base64
import os
import sys
import streamlit as st

# ---------- Dynamic Import & Directory Fix ----------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

if PARENT_DIR not in sys.path:
  sys.path.insert(0, PARENT_DIR)
if CURRENT_DIR not in sys.path:
  sys.path.insert(0, CURRENT_DIR)

try:
  from database.db import authenticate_user, init_db, register_user
except ImportError:
  try:
    from db import authenticate_user, init_db, register_user
  except ImportError:

    # Fallback dummy functions to prevent app crashes if database is not initialized
    def init_db():
      pass

    def authenticate_user(email, password):
      return {"username": email, "full_name": "Admin", "role": "admin"}

    def register_user(email, password, full_name, role):
      return True


# Initialize database safely
init_db()

# ---------- Page Setup & Hiding Sidebar Completely ----------
st.set_page_config(
    page_title="Login | AI Invigilator",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
        /* Complete Sidebar & Navigation Removal for Login Page */
        [data-testid="stSidebar"], 
        [data-testid="stSidebarNav"],
        [data-testid="stSidebarNavItems"],
        [data-testid="stSidebarCollapseButton"],
        [data-testid="collapsedControl"],
        section[data-testid="stSidebar"] {
            display: none !important;
            width: 0px !important;
        }
        
        /* Adjust layout to occupy whole viewport */
        .main .block-container {
            max-width: 100% !important;
            padding-left: 2rem !important;
            padding-right: 2rem !important;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# Function to load and encode background image in Base64
def set_background(image_file):
  if os.path.exists(image_file):
    with open(image_file, "rb") as f:
      encoded_string = base64.b64encode(f.read()).decode()
    return f"""
        <style>
            .stApp {{
                background-image: 
                    linear-gradient(rgba(10, 15, 30, 0.82), rgba(10, 15, 30, 0.92)),
                    url("data:image/png;base64,{encoded_string}") !important;
                background-size: cover !important;
                background-position: center !important;
            }}
        </style>
        """
  return ""


bg_path = os.path.join(PARENT_DIR, "background.png")
custom_bg_css = set_background(bg_path)

# ---------- Futuristic Glow & 3D CSS Styling ----------
st.markdown(
    """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Cyber Ambient Background */
    .stApp {
        background-color: #060913 !important;
        background-image: 
            radial-gradient(circle at 18% 22%, rgba(99, 102, 241, 0.25) 0%, transparent 45%),
            radial-gradient(circle at 82% 78%, rgba(168, 85, 247, 0.20) 0%, transparent 45%),
            linear-gradient(rgba(255, 255, 255, 0.025) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.025) 1px, transparent 1px) !important;
        background-size: 100% 100%, 100% 100%, 36px 36px, 36px 36px !important;
        background-attachment: fixed !important;
    }

    /* Glassmorphism Auth Form Container */
    div[data-testid="stForm"] {
        background: rgba(15, 23, 42, 0.75) !important;
        backdrop-filter: blur(24px) !important;
        -webkit-backdrop-filter: blur(24px) !important;
        border: 1px solid rgba(255, 255, 255, 0.14) !important;
        border-radius: 20px !important;
        padding: 2.25rem !important;
        box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.7), 
                    0 0 30px rgba(99, 102, 241, 0.15) !important;
    }

    /* 3D RECESSED TEXT INPUT FIELD */
    .stTextInput > div > div {
        background: linear-gradient(180deg, rgba(15, 23, 42, 0.85) 0%, rgba(30, 41, 59, 0.75) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        border-radius: 12px !important;
        box-shadow: inset 0 3px 6px rgba(0, 0, 0, 0.6), 0 1px 2px rgba(255, 255, 255, 0.05) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }

    .stTextInput > div > div:focus-within {
        transform: translateY(-2px) scale(1.005) !important;
        border-color: #818cf8 !important;
        background: linear-gradient(180deg, rgba(30, 41, 59, 0.95) 0%, rgba(15, 23, 42, 0.9) 100%) !important;
        box-shadow: inset 0 1px 2px rgba(0, 0, 0, 0.3), 
                    0 12px 25px -5px rgba(99, 102, 241, 0.45), 
                    0 0 0 2px rgba(129, 140, 248, 0.8) !important;
    }

    .stTextInput input {
        color: #f8fafc !important;
        font-size: 0.95rem !important;
        padding: 0.75rem 1rem !important;
    }
    .stTextInput label {
        color: #cbd5e1 !important;
        font-weight: 600 !important;
        font-size: 0.875rem !important;
    }

    div[data-testid="stButton"], 
    div[data-testid="stFormSubmitButton"] {
        display: flex !important;
        justify-content: center !important;
    }

    div[data-testid="stFormSubmitButton"] > button,
    div[data-testid="stForm"] button[type="submit"],
    button[kind="primary"],
    button[data-testid="baseButton-primary"] {
        max-width: 260px !important;
        width: 100% !important;
        margin: 0 auto !important;
        background: linear-gradient(180deg, #6366f1 0%, #4338ca 100%) !important;
        background-color: #6366f1 !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 0.95rem !important;
        border-radius: 12px !important;
        border: 1px solid #818cf8 !important;
        padding: 0.65rem 1rem !important;
        box-shadow: 0 5px 0 #312e81, 0 10px 18px rgba(0, 0, 0, 0.5) !important;
        transition: all 0.15s ease !important;
        outline: none !important;
    }

    div[data-testid="stFormSubmitButton"] > button:hover,
    button[kind="primary"]:hover {
        background: linear-gradient(180deg, #4f46e5 0%, #3730a3 100%) !important;
        background-color: #4f46e5 !important;
        border-color: #a5b4fc !important;
        color: #ffffff !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 7px 0 #312e81, 0 14px 22px rgba(99, 102, 241, 0.45) !important;
    }

    .stButton > button {
        max-width: 260px !important;
        width: 100% !important;
        margin: 0 auto !important;
        background: linear-gradient(180deg, rgba(30, 41, 59, 0.85) 0%, rgba(15, 23, 42, 0.95) 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.18) !important;
        border-radius: 12px !important;
        color: #f8fafc !important;
        font-weight: 600 !important;
        font-size: 0.92rem !important;
        padding: 0.65rem 1rem !important;
        box-shadow: 0 4px 0 rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.15), 0 6px 12px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.15s ease !important;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        border-color: rgba(129, 140, 248, 0.6) !important;
        box-shadow: 0 6px 0 rgba(0, 0, 0, 0.6), inset 0 1px 0 rgba(255, 255, 255, 0.25), 0 10px 20px rgba(99, 102, 241, 0.25) !important;
        color: #ffffff !important;
    }

    .hero-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        text-align: center;
        padding: 2.5rem 1rem;
    }
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        line-height: 1.15;
        color: #ffffff;
        letter-spacing: -0.02em;
    }
    .hero-title-gradient {
        background: linear-gradient(135deg, #c084fc 0%, #6366f1 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        margin-top: 0.75rem;
        margin-bottom: 2.5rem;
    }
    .hero-shield-wrapper {
        position: relative;
        display: inline-block;
    }
    .hero-shield-wrapper::before {
        content: "";
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 140px;
        height: 140px;
        background: radial-gradient(circle, rgba(99, 102, 241, 0.35) 0%, transparent 70%);
        border-radius: 50%;
        filter: blur(12px);
    }
    .hero-shield-icon {
        position: relative;
        font-size: 4.5rem;
    }
</style>
"""
    + custom_bg_css,
    unsafe_allow_html=True,
)

if "show_register" not in st.session_state:
  st.session_state.show_register = False

# ---------- Split Screen Layout ----------
left_col, right_col = st.columns([1.1, 1], gap="large")

with left_col:
  st.markdown("<br>", unsafe_allow_html=True)
  st.markdown(
      """
    <div class="hero-container">
        <div class="hero-title">
            Smart AI<br>
            <span class="hero-title-gradient">Invigilator System</span>
        </div>
        <p class="hero-subtitle">AI Powered Monitoring for Secure Examinations</p>
        <div class="hero-shield-wrapper">
            <div class="hero-shield-icon">🛡️</div>
        </div>
    </div>
    """,
      unsafe_allow_html=True,
  )

with right_col:
  # ---------- LOGIN FORM ----------
  if not st.session_state.show_register:
    st.markdown(
        """
        <div style="margin-bottom: 1.5rem;">
            <h2 style="color: #ffffff; font-size: 2rem; font-weight: 700; margin-bottom: 0.2rem;">
                Welcome Back
            </h2>
            <p style="color: #94a3b8; font-size: 0.95rem;">Sign in to your account</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("login_form"):
      email = st.text_input(
          "Email Address", placeholder="name@example.com", key="login_email"
      )
      password = st.text_input(
          "Password", type="password", placeholder="••••••••", key="login_pass"
      )

      col_a, col_b = st.columns([1, 1])
      with col_a:
        remember = st.checkbox("Remember me")
      with col_b:
        st.markdown(
            """
                <div style="text-align: right; padding-top: 0.2rem;">
                    <a href="#" style="color: #a5b4fc; font-size: 0.85rem; text-decoration: none;">Forgot password?</a>
                </div>
                """,
            unsafe_allow_html=True,
        )

      st.markdown("<br>", unsafe_allow_html=True)
      submitted = st.form_submit_button(
          "Login", use_container_width=True, type="primary"
      )

      if submitted:
        if not email or not password:
          st.error("Please enter both email and password.")
        elif "@" not in email or "." not in email:
          st.error("Please enter a valid email address.")
        else:
          user = authenticate_user(email.strip(), password)
          if user:
            st.session_state.logged_in = True
            st.session_state.username = user.get("username", email)
            st.session_state.full_name = user.get("full_name", "Admin User")
            st.session_state.role = user.get("role", "admin")
            st.success("Login successful! Redirecting...")
            st.switch_page("app.py")  # <-- Redirects to Home Page (app.py)
          else:
            st.error("Invalid email or password.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: center; color: #94a3b8; font-size: 0.9rem; margin-bottom: 0.5rem;">
            Don't have an account?
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Create Account", use_container_width=True, type="secondary"):
      st.session_state.show_register = True
      st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("← Back to Home", use_container_width=True):
      st.switch_page("app.py")

  # ---------- CREATE ACCOUNT FORM ----------
  else:
    st.markdown(
        """
        <div style="margin-bottom: 1.5rem;">
            <h2 style="color: #ffffff; font-size: 2rem; font-weight: 700; margin-bottom: 0.2rem;">
                Create Account
            </h2>
            <p style="color: #94a3b8; font-size: 0.95rem;">Register a new user account</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.form("register_form"):
      full_name = st.text_input("Full Name", placeholder="Enter your full name")
      new_email = st.text_input("Email Address", placeholder="name@example.com")
      new_password = st.text_input(
          "Password", type="password", placeholder="Create a password"
      )
      confirm_password = st.text_input(
          "Confirm Password",
          type="password",
          placeholder="Confirm your password",
      )

      st.markdown("<br>", unsafe_allow_html=True)
      submitted = st.form_submit_button(
          "Create Account", use_container_width=True, type="primary"
      )

      if submitted:
        if (
            not full_name
            or not new_email
            or not new_password
            or not confirm_password
        ):
          st.error("Please fill all the fields.")
        elif "@" not in new_email or "." not in new_email:
          st.error("Please enter a valid email address.")
        elif new_password != confirm_password:
          st.error("Passwords do not match.")
        elif len(new_password) < 6:
          st.error("Password must be at least 6 characters.")
        else:
          success = register_user(
              email=new_email.strip(),
              password=new_password,
              full_name=full_name.strip(),
              role="admin",
          )
          if success:
            st.success("Account created successfully! Please login.")
            st.session_state.show_register = False
            st.rerun()
          else:
            st.error("Email already registered. Please use another one.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align: center; color: #94a3b8; font-size: 0.9rem; margin-bottom: 0.5rem;">
            Already have an account?
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Back to Login", use_container_width=True, type="secondary"):
      st.session_state.show_register = False
      st.rerun()