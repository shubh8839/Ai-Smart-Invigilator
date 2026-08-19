import streamlit as st
from reports import render_reports
from live_monitoring import render_live_monitoring
from user_profile import render_profile
from settings import render_settings

# --- IMPORT ANALYTICS MODULE ---
try:
    from analytics import analytics_page
except ImportError:
    # Fallback in case analytics.py is missing or named differently
    def analytics_page():
        st.error(
            "analytics.py module not found. Please ensure analytics.py is in the same directory."
        )


st.set_page_config(
    page_title="AI Invigilator | Dashboard",
    page_icon="◉",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
    :root { --bg:#070b18; --surface:#0d1325; --surface2:#10182c; --line:#222d47; --text:#f3f5ff; --muted:#93a1c5; --purple:#8c5cff; --green:#45e7a6; --orange:#ffa629; --red:#ff5878; --blue:#60a5fa; }
    .stApp { background:radial-gradient(circle at 55% -20%,#17133b 0,#070b18 42%); color:var(--text); }
    html, body, [class*="css"] { font-family:Manrope,sans-serif; }
    
    /* Transparent Header Layout */
    header[data-testid="stHeader"] {
        background: transparent !important;
        z-index: 100 !important;
    }
    footer, #MainMenu { visibility: hidden !important; display: none !important; }
    [data-testid="stSidebarNav"] { display: none !important; }

    /* Custom Styled Sidebar Toggle Button (Close / Open Sidebar) */
    [data-testid="stSidebarCollapseButton"] button,
    [data-testid="stSidebarCollapsedControl"] button {
        color: #c4d1f2 !important;
        background: #10182c !important;
        border: 1px solid #222d47 !important;
        border-radius: 8px !important;
        padding: 4px 8px !important;
        transition: all 0.2s ease-in-out !important;
    }
    [data-testid="stSidebarCollapseButton"] button:hover,
    [data-testid="stSidebarCollapsedControl"] button:hover {
        background: #18233f !important;
        border-color: #5b42b1 !important;
        color: #a77bff !important;
        box-shadow: 0 0 10px rgba(167, 123, 255, 0.25) !important;
    }

    /* Sidebar Outer Layout & Spacing */
    [data-testid="stSidebar"] {
        background: #080d1d !important;
        border-right: 1px solid #1e2940 !important;
    }
    [data-testid="stSidebar"] > div:first-child { 
        padding: 1rem 0.8rem 1rem !important; 
    }
    [data-testid="stSidebar"] hr { 
        border-color: #202a42; 
        margin: 0.8rem 0; 
    }

    /* Main Canvas - Compact Spacing */
    .block-container {
        max-width: 1460px;
        padding-top: 1rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
    }

    /* Sidebar Nav Expanders */
    section[data-testid="stSidebar"] [data-testid="stExpander"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        margin-bottom: 0px !important;
    }
    section[data-testid="stSidebar"] [data-testid="stExpanderSummary"] {
        color: #d0d7ed !important;
        font-weight: 600 !important;
        font-size: 13px !important;
        padding: 0.3rem 0.4rem !important;
    }
    section[data-testid="stSidebar"] [data-testid="stExpanderSummary"]:hover {
        color: #a77bff !important;
    }
    section[data-testid="stSidebar"] [data-testid="stExpanderDetails"] {
        padding: 0rem 0rem 0.4rem 0.2rem !important;
    }

    /* Sidebar Custom Buttons */
    section[data-testid="stSidebar"] .stButton { margin-bottom: 2px !important; }
    section[data-testid="stSidebar"] .stButton > button { 
        text-align: left; 
        justify-content: flex-start; 
        padding: 0.4rem 0.65rem; 
        color: #9caabf; 
        background: transparent; 
        border: none; 
        box-shadow: none; 
        font-size: 12.5px; 
        width: 100%; 
        border-radius: 6px;
    }
    section[data-testid="stSidebar"] .stButton > button:hover { 
        background: #151632; 
        color: #f2f4ff; 
    }

    /* Sidebar Logo Header */
    .logo { font-size:15px; font-weight:800; letter-spacing:-.5px; display:flex; align-items:center; gap:10px; margin:0 0 1rem .2rem; }
    .logo-mark { display:grid; place-items:center; width:36px; height:36px; background:radial-gradient(circle at 50% 45%,#5c30cb,#17133c 66%); border:1px solid #5b42b1; border-radius:9px; color:#e0d6ff; font-size:16px; box-shadow:0 0 18px #6f4de233; }
    .logo b { color:#a77bff; }
    .logo small { display:block; color:#8f9cb8; font-size:9px; font-weight:500; margin-top:1px; }
    .side-section { font:700 9.5px 'DM Mono'; letter-spacing:1.15px; color:#627299; margin:.8rem 0 .3rem .65rem; }
    
    .sub-nav-active {
        color: #f2efff !important;
        background: linear-gradient(90deg, #45258f, #181334) !important;
        box-shadow: inset 3px 0 #a16eff !important;
        font-weight: 600;
        padding: 0.45rem 0.65rem;
        border-radius: 6px;
        font-size: 12.5px;
        margin-bottom: 2px;
    }

    /* Dashboard Metric Cards */
    .metric-card { min-height:110px; padding:15px 17px; border-radius:10px; border:1px solid var(--line); background:linear-gradient(145deg,#10172a,#0d1223); position:relative; overflow:hidden; }
    .metric-card:before { content:""; position:absolute; height:2px; left:18px; right:18px; top:0; background:var(--accent); box-shadow:0 0 15px var(--accent); }
    .metric-icon { float:left; width:42px; height:42px; display:grid; place-items:center; border-radius:9px; background:color-mix(in srgb,var(--accent) 16%, transparent); color:var(--accent); font-size:20px; margin-right:15px; }
    .metric-label { font-size:12px; color:#8fa1d2; margin-top:2px; font-weight:600; }
    .metric-value { font:800 26px 'DM Mono'; line-height:1.1; margin-top:3px; }
    .metric-foot { font-size:10px; color:var(--accent); margin-top:4px; }

    [data-testid="stVerticalBlockBorderWrapper"] { background:linear-gradient(145deg,#0f1629,#0b1120); border:1px solid var(--line)!important; border-radius:10px; padding:17px 19px; height:100%; }
    .panel-head { display:flex; justify-content:space-between; align-items:center; margin-bottom:13px; }
    .panel-head h3 { font-size:15px; margin:0; }
    .pill { font:700 10px Manrope; padding:4px 8px; border-radius:4px; display:inline-block; }
    .high { color:#ff7c90; background:#351a2a; border:1px solid #5c2033; }
    .medium { color:#ffb449; background:#342a1b; border:1px solid #5c421e; }
    </style>
    """,
    unsafe_allow_html=True,
)


def metric_card(icon, label, value, caption, accent):
    st.markdown(
        f"""<div class="metric-card" style="--accent:{accent}">
          <div class="metric-icon">{icon}</div><div class="metric-label">{label}</div>
          <div class="metric-value">{value}</div><div class="metric-foot">{caption}</div></div>""",
        unsafe_allow_html=True,
    )


def dashboard_page():
    # 1. Welcome / Header
    st.markdown(
        """
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1.2rem; flex-wrap:wrap; gap:10px;">
            <div>
                <h2 style="font-size:22px; font-weight:800; margin:0 0 4px 0; color:#f3f5ff;">Welcome back, Admin 👋</h2>
                <p style="color:#93a1c5; font-size:13.5px; margin:0;">Real-time overview of active examination rooms and monitoring status.</p>
            </div>
            <div style="background:#112a20; border:1px solid #235d46; color:#45e7a6; padding:6px 14px; border-radius:20px; font-size:12px; font-weight:700; display:flex; align-items:center; gap:8px;">
                <span style="height:8px; width:8px; background-color:#45e7a6; border-radius:50%; display:inline-block; box-shadow: 0 0 8px #45e7a6;"></span>
                🟢 AI System Online
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 2. Key Statistics
    metrics = [
        ("📹", "Total Cameras", "12", "Active feeds", "#8c5cff"),
        ("👨‍🎓", "Students Monitored", "156", "Live candidates", "#45e7a6"),
        ("🚨", "Active Alerts", "03", "Requires attention", "#ff5878"),
        ("🤖", "AI Accuracy", "98.4%", "Optimal performance", "#60a5fa"),
    ]
    cols = st.columns(4, gap="small")
    for col, item in zip(cols, metrics):
        with col:
            metric_card(*item)

    st.write("")

    # 3. Live CCTV Preview & 4. Recent Alerts Layout
    cctv_col, alerts_col = st.columns([1.25, 0.75], gap="small")

    with cctv_col:
        with st.container(border=True):
            st.markdown(
                "<div class='panel-head'><h3>📹 Live CCTV Preview</h3></div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                """
                <div style="
                    height: 310px;
                    background: radial-gradient(circle at 50% 50%, #161c32 0%, #090c1a 100%);
                    border: 1px dashed #283556;
                    border-radius: 8px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    text-align: center;
                    padding: 20px;
                ">
                    <div style="font-size: 40px; margin-bottom: 12px; opacity: 0.85;">📹</div>
                    <div style="font-family: 'DM Mono', monospace; font-size: 13px; font-weight: 700; letter-spacing: 0.8px; color: #a5b6e1;">
                        LIVE CCTV PREVIEW — Camera feed will be connected later
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    with alerts_col:
        with st.container(border=True):
            st.markdown(
                "<div class='panel-head'><h3>🚨 Recent Alerts</h3></div>",
                unsafe_allow_html=True,
            )
            st.markdown(
                """
                <table style="width:100%; border-collapse:collapse; color:#f3f5ff; font-size:12.5px; margin-top:4px;">
                    <thead>
                        <tr style="border-bottom: 1px solid #222d47; color:#8190b8; text-align:left; font-size:11px; font-family:'DM Mono';">
                            <th style="padding: 8px 4px;">TIME</th>
                            <th style="padding: 8px 4px;">DETECTION</th>
                            <th style="padding: 8px 4px; text-align:right;">RISK</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr style="border-bottom: 1px solid #182035;">
                            <td style="padding: 14px 4px; font-family:'DM Mono'; color:#8f9fc2;">10:24</td>
                            <td style="padding: 14px 4px; font-weight:600;">📱 Mobile Detected</td>
                            <td style="padding: 14px 4px; text-align:right;"><span class="pill high">🔴 High</span></td>
                        </tr>
                        <tr style="border-bottom: 1px solid #182035;">
                            <td style="padding: 14px 4px; font-family:'DM Mono'; color:#8f9fc2;">10:21</td>
                            <td style="padding: 14px 4px; font-weight:600;">👀 Looking Away</td>
                            <td style="padding: 14px 4px; text-align:right;"><span class="pill medium">🟡 Medium</span></td>
                        </tr>
                        <tr>
                            <td style="padding: 14px 4px; font-family:'DM Mono'; color:#8f9fc2;">10:18</td>
                            <td style="padding: 14px 4px; font-weight:600;">👥 Multiple Persons</td>
                            <td style="padding: 14px 4px; text-align:right;"><span class="pill high">🔴 High</span></td>
                        </tr>
                    </tbody>
                </table>
                """,
                unsafe_allow_html=True,
            )


def placeholder_page(title):
    st.markdown(
        f"<div style='color:#93a1c5; font-size:13px; margin-bottom:1rem;'>WORKSPACE / {title.upper()}</div><div style='background:linear-gradient(145deg,#0f1629,#0b1120); border:1px solid #222d47; border-radius:10px; padding:48px;'><h2 style='font-size:24px; font-weight:800;'>{title}</h2><p style='color:#93a1c5;'>This module is ready to connect.</p></div>",
        unsafe_allow_html=True,
    )


if "active_page" not in st.session_state:
    st.session_state.active_page = "Dashboard"


def render_nav_button(label, page_name):
    if st.session_state.active_page == page_name:
        st.markdown(
            f"<div class='sub-nav-active'>{label}</div>", unsafe_allow_html=True
        )
    else:
        if st.button(label, key=f"btn_{page_name}"):
            st.session_state.active_page = page_name
            st.rerun()


# Render Sidebar Content
with st.sidebar:
    st.markdown(
        "<div class='logo'><div class='logo-mark'>◉</div><div>AI <b>INVIGILATOR</b><small>Smart AI Invigilator System</small></div></div>",
        unsafe_allow_html=True,
    )

    st.markdown(
        "<div class='side-section'>WORKSPACE</div>", unsafe_allow_html=True
    )

    with st.expander("▦  Dashboard", expanded=True):
        render_nav_button("Overview", "Dashboard")
        render_nav_button("Analytics", "Analytics")
        render_nav_button("Reports", "Reports")

    with st.expander("▣  Exams", expanded=True):
        render_nav_button("Live Monitoring", "Live Monitoring")
        render_nav_button("Recordings", "Recordings")
        render_nav_button("Alerts", "Alerts")

    st.divider()

    st.markdown(
        "<div class='side-section'>ACCOUNT</div>", unsafe_allow_html=True
    )
    render_nav_button("👤  Profile", "Profile")
    render_nav_button("⚙  Settings", "Settings")

# --- UPDATED PAGE ROUTER ---
if st.session_state.active_page == "Dashboard":
    dashboard_page()
elif st.session_state.active_page == "Analytics":
    analytics_page()
elif st.session_state.active_page == "Reports":
    render_reports()
elif st.session_state.active_page == "Live Monitoring":
  render_live_monitoring()
elif st.session_state.active_page == "Profile":  # <-- Add this block
  render_profile()
elif st.session_state.get("active_page") == "Settings":
  render_settings()
else:
    placeholder_page(st.session_state.active_page)