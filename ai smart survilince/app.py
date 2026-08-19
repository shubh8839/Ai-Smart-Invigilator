import base64
import os
import streamlit as st

st.set_page_config(
    page_title="AI Invigilator | Smart AI Invigilator System",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------- Initialize Session State ----------
if "logged_in" not in st.session_state:
  st.session_state.logged_in = False

# ---------- Hide Streamlit Sidebar Completely ----------
st.markdown(
    """
    <style>
        [data-testid="stSidebar"] { display: none !important; }
        [data-testid="collapsedControl"] { display: none !important; }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- Load external CSS ----------
def load_css(file_name):
  try:
    with open(file_name, encoding="utf-8") as f:
      st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
  except FileNotFoundError:
    st.warning("style.css not found. Using fallback styles.")


load_css("style.css")


# ---------- Helper: convert local image to base64 ----------
def get_base64_image(image_path):
  try:
    with open(image_path, "rb") as f:
      data = f.read()
    return base64.b64encode(data).decode()
  except Exception:
    return None


# Load hero image
hero_img_path = "cctv_bg.jpg"
if not os.path.exists(hero_img_path):
  hero_img_path = "webbg.jpg"

hero_base64 = get_base64_image(hero_img_path)

# ---------- UNIFIED STICKY NAVBAR WITH DYNAMIC LOGIN/LOGOUT & DASHBOARD ----------
# We use Streamlit columns inside a layout header or render dynamic buttons below/inside the nav style container.
# To keep your custom sticky navbar layout intact while allowing dynamic Streamlit buttons:

col_brand, col_links, col_action1, col_action2 = st.columns(
    [2.2, 2.5, 0.8, 0.8], gap="small"
)

with col_brand:
  st.markdown(
      """
    <div class="nav-brand" style="display: flex; align-items: center; gap: 0.75rem; padding-top: 0.4rem;">
        <span class="nav-brand-icon" style="font-size: 1.8rem;">🛡️</span>
        <div>
            <div class="nav-brand-main" style="font-weight: 800; font-size: 1.1rem; color: #ffffff; letter-spacing: 0.05em;">AI INVIGILATOR</div>
            <div class="nav-brand-sub" style="font-size: 0.75rem; color: #94a3b8;">Smart AI Invigilator System</div>
        </div>
    </div>
    """,
      unsafe_allow_html=True,
  )

with col_links:
  st.markdown(
      """
    <div class="nav-links" style="display: flex; align-items: center; gap: 1.5rem; padding-top: 0.8rem;">
        <a href="#home" style="color: #cbd5e1; text-decoration: none; font-size: 0.9rem; font-weight: 500;">Home</a>
        <a href="#features" style="color: #cbd5e1; text-decoration: none; font-size: 0.9rem; font-weight: 500;">Features</a>
        <a href="#how-it-works" style="color: #cbd5e1; text-decoration: none; font-size: 0.9rem; font-weight: 500;">How It Works</a>
        <a href="#technology" style="color: #cbd5e1; text-decoration: none; font-size: 0.9rem; font-weight: 500;">Technology</a>
        <a href="#about" style="color: #cbd5e1; text-decoration: none; font-size: 0.9rem; font-weight: 500;">About</a>
    </div>
    """,
      unsafe_allow_html=True,
  )

with col_action1:
  st.markdown('<div style="padding-top: 0.3rem;">', unsafe_allow_html=True)
  # Show Dashboard navigation button ONLY if the user is logged in
  if st.session_state.logged_in:
    if st.button("📊 Dashboard", use_container_width=True):
      st.switch_page("pages/Dashboard.py")
  st.markdown("</div>", unsafe_allow_html=True)

with col_action2:
  st.markdown('<div style="padding-top: 0.3rem;">', unsafe_allow_html=True)
  # Toggle dynamically between Login and Logout buttons
  if not st.session_state.logged_in:
    if st.button("🔑 Login", use_container_width=True, type="primary"):
      st.switch_page("pages/Login.py")
  else:
    if st.button("🚪 Logout", use_container_width=True, type="secondary"):
      st.session_state.logged_in = False
      st.rerun()
  st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div id="home"></div>', unsafe_allow_html=True)
st.markdown("<hr style='border: 0.5px solid rgba(255,255,255,0.1); margin: 0.5rem 0 2rem 0;'>", unsafe_allow_html=True)

# ---------- HERO SECTION ----------
left, right = st.columns([1.1, 1], gap="medium")

with left:
  st.markdown(
      """
    <div class="hero-text-block">
        <h1 class="hero-title">
            AI-powered monitoring for<br>
            <span class="hero-highlight">secure</span> examinations.
        </h1>
        <p class="hero-description">
            Smart AI Invigilator System helps colleges maintain examination fairness 
            and integrity through real-time monitoring, AI-assisted detection, 
            and reviewable alerts.
        </p>
    </div>
    """,
      unsafe_allow_html=True,
  )

with right:
  if hero_base64:
    st.markdown(
        f"""
        <div class="hero-image-wrapper">
            <div class="hero-glow"></div>
            <img src="data:image/jpeg;base64,{hero_base64}" alt="AI CCTV Monitoring" />
        </div>
        """,
        unsafe_allow_html=True,
    )
  else:
    st.markdown(
        """
        <div class="hero-image-wrapper" style="color:#64748b; text-align:center;">
            <div>
                <div style="font-size:3.5rem;">📹</div>
                <div style="font-size:0.85rem; margin-top: 0.5rem;">Place cctv_bg.jpg in project root</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------- FEATURES ----------
st.markdown('<div class="section-container" id="features">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Features</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Core capabilities of the Smart AI Invigilator System</div>',
    unsafe_allow_html=True,
)

f1, f2, f3 = st.columns(3, gap="medium")
f4, f5, f6 = st.columns(3, gap="medium")

features = [
    (
        f1,
        "🤖",
        "AI-Based Detection",
        "Uses YOLOv8 and computer vision to detect suspicious objects and activities from examination footage.",
    ),
    (
        f2,
        "📹",
        "Live CCTV Monitoring",
        "Monitor examination halls through live camera feeds and observe activities in real time.",
    ),
    (
        f3,
        "🔔",
        "Intelligent Alerts",
        "Generates alerts for mobile phone detected, multiple persons, looking away, and unauthorized objects.",
    ),
    (
        f4,
        "📤",
        "Video Upload & Analysis",
        "Administrators can upload recorded examination videos and analyze them for suspicious activities.",
    ),
    (
        f5,
        "📊",
        "Analytics & Reports",
        "View examination statistics, candidates monitored, detection trends, and generate reviewable reports.",
    ),
    (
        f6,
        "🔒",
        "Secure Monitoring",
        "Maintains examination integrity by recording detection events in a centralized monitoring system.",
    ),
]

for col, icon, title, desc in features:
  with col:
    st.markdown(
        f"""
        <div class="feature-card">
            <div class="feature-icon-badge">{icon}</div>
            <div class="feature-title">{title}</div>
            <div class="feature-desc">{desc}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
st.markdown("</div>", unsafe_allow_html=True)

# ---------- HOW IT WORKS ----------
st.markdown('<div class="section-container" id="how-it-works">', unsafe_allow_html=True)
st.markdown('<div class="section-title">How It Works</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Simple five-step examination monitoring process</div>',
    unsafe_allow_html=True,
)

s1, s2, s3, s4, s5 = st.columns(5, gap="small")

steps = [
    (
        s1,
        "01",
        "Start Session",
        "Administrator starts and configures an examination session.",
    ),
    (
        s2,
        "02",
        "Camera Feed",
        "CCTV cameras capture the examination environment in real time.",
    ),
    (
        s3,
        "03",
        "AI Detection",
        "OpenCV and YOLOv8 process video to identify suspicious acts.",
    ),
    (
        s4,
        "04",
        "Alert Generation",
        "System logs event and generates alert with time & severity.",
    ),
    (
        s5,
        "05",
        "Review & Report",
        "Administrator reviews alerts, recordings, and analytics.",
    ),
]

for col, num, title, desc in steps:
  with col:
    st.markdown(
        f"""
        <div class="step-card">
            <div class="step-number">{num}</div>
            <div class="step-title">{title}</div>
            <div class="step-desc">{desc}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
st.markdown("</div>", unsafe_allow_html=True)

# ---------- TECHNOLOGY ----------
st.markdown('<div class="section-container" id="technology">', unsafe_allow_html=True)
st.markdown('<div class="section-title">Technology</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-subtitle">Tools and frameworks powering the system</div>',
    unsafe_allow_html=True,
)

t1, t2, t3, t4 = st.columns(4, gap="small")
t5, t6, t7, t8 = st.columns(4, gap="small")

techs = [
    (t1, "Python 3.11"),
    (t2, "Streamlit"),
    (t3, "SQLite"),
    (t4, "OpenCV"),
    (t5, "YOLOv8 / Ultralytics"),
    (t6, "NumPy"),
    (t7, "Pandas"),
    (t8, "HTML / CSS"),
]

for col, name in techs:
  with col:
    st.markdown(
        f"""
        <div class="tech-card">
            <div class="tech-name">{name}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
st.markdown("</div>", unsafe_allow_html=True)

# ---------- ABOUT US ----------
st.markdown('<div class="section-container" id="about">', unsafe_allow_html=True)
st.markdown('<div class="section-title">About Us</div>', unsafe_allow_html=True)
st.markdown(
    """
<div class="about-card">
    Smart AI Invigilator System is a college project developed to improve examination 
    monitoring using computer vision and artificial intelligence.  
    The system aims to support educational institutions in maintaining fairness and 
    integrity during online and offline examinations through real-time detection, 
    alerts, and reviewable reports.
</div>
""",
    unsafe_allow_html=True,
)
st.markdown("</div>", unsafe_allow_html=True)

# ---------- CONTACT + FOOTER ----------
st.markdown(
    """
<div class="footer-box" id="contact">
    <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 2rem;">
        <div style="max-width: 320px;">
            <div style="font-weight: 700; font-size: 1.1rem; color: #f1f5f9; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.5rem;">
                🛡️ AI INVIGILATOR
            </div>
            <div style="color: #94a3b8; font-size: 0.88rem; line-height: 1.6;">
                Smart AI Invigilator System – A computer vision based examination monitoring project.
            </div>
        </div>
        <div>
            <div style="font-weight: 600; color: #e2e8f0; margin-bottom: 0.6rem; font-size: 0.95rem;">Quick Links</div>
            <div style="color: #94a3b8; font-size: 0.88rem; line-height: 1.8;">
                <a href="#home" style="color: #94a3b8; text-decoration: none;">Home</a><br>
                <a href="#features" style="color: #94a3b8; text-decoration: none;">Features</a><br>
                <a href="#how-it-works" style="color: #94a3b8; text-decoration: none;">How It Works</a><br>
                <a href="#technology" style="color: #94a3b8; text-decoration: none;">Technology</a><br>
                <a href="#about" style="color: #94a3b8; text-decoration: none;">About Us</a>
            </div>
        </div>
        <div>
            <div style="font-weight: 600; color: #e2e8f0; margin-bottom: 0.6rem; font-size: 0.95rem;">Contact</div>
            <div style="color: #94a3b8; font-size: 0.88rem; line-height: 1.8;">
                Email: support@example.com<br>
                Phone: +91 XXXXX XXXXX<br>
                Location: Campus Academic Block
            </div>
        </div>
    </div>
    <div style="text-align: center; color: #64748b; font-size: 0.82rem; margin-top: 2rem; 
                padding-top: 1.2rem; border-top: 1px solid rgba(255, 255, 255, 0.08);">
        © 2026 Smart AI Invigilator System. College Project.
    </div>
</div>
""",
    unsafe_allow_html=True,
)