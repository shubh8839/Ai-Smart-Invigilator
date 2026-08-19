import os
import sys
from datetime import datetime
import pandas as pd
import streamlit as st

# ---------- Dynamic Import & Directory Fix ----------
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.abspath(os.path.join(CURRENT_DIR, ".."))

if PARENT_DIR not in sys.path:
    sys.path.insert(0, PARENT_DIR)
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

# ---------- Page Configuration ----------
st.set_page_config(
    page_title="Examination Alerts | AI Invigilator",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Authentication Guard ----------
if "logged_in" not in sys.modules and ("logged_in" not in st.session_state or not st.session_state.logged_in):
    # Fallback check if auth is tracked
    pass

# ---------- Cyber & Glassmorphism Styling ----------
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
            radial-gradient(circle at 18% 22%, rgba(99, 102, 241, 0.20) 0%, transparent 45%),
            radial-gradient(circle at 82% 78%, rgba(168, 85, 247, 0.15) 0%, transparent 45%),
            linear-gradient(rgba(255, 255, 255, 0.02) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255, 255, 255, 0.02) 1px, transparent 1px) !important;
        background-size: 100% 100%, 100% 100%, 36px 36px, 36px 36px !important;
        background-attachment: fixed !important;
    }

    /* Glassmorphism Card Container */
    .glass-card {
        background: rgba(15, 23, 42, 0.75) !important;
        backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 16px !important;
        padding: 1.5rem !important;
        box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5) !important;
    }

    .metric-badge {
        background: rgba(244, 63, 94, 0.15);
        border: 1px solid rgba(244, 63, 94, 0.3);
        color: #fb7185;
        padding: 0.4rem 0.8rem;
        border-radius: 10px;
        font-weight: 700;
        display: inline-block;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ---------- Initialize Session State for Alerts Data ----------
if "alerts_db" not in st.session_state:
    st.session_state.alerts_db = [
        {
            "id": 1,
            "time": "10:24:15",
            "exam": "Advanced Mathematics Final",
            "camera": "CAM-01",
            "detection": "Mobile Phone",
            "risk": "High",
            "status": "⚠️ Unreviewed",
            "student": "STU-034 (Alex Turner)",
            "description": "Mobile phone detected clearly on desk during examination.",
        },
        {
            "id": 2,
            "time": "10:31:42",
            "exam": "Advanced Mathematics Final",
            "camera": "CAM-03",
            "detection": "Multiple Person",
            "risk": "High",
            "status": "⚠️ Unreviewed",
            "student": "STU-089 (David Miller)",
            "description": "Second individual entered camera frame boundary.",
        },
        {
            "id": 3,
            "time": "10:42:18",
            "exam": "Physics Midterm",
            "camera": "CAM-02",
            "detection": "Looking Away",
            "risk": "Medium",
            "status": "✅ Reviewed",
            "student": "STU-012 (Sarah Jenkins)",
            "description": "Prolonged gaze deviation detected away from screen monitor.",
        },
        {
            "id": 4,
            "time": "11:02:31",
            "exam": "Computer Science 101",
            "camera": "CAM-04",
            "detection": "Book / Unauthorized Material",
            "risk": "Medium",
            "status": "⚠️ Unreviewed",
            "student": "STU-055 (Liam Smith)",
            "description": "Printed textbook pages identified near keyboard area.",
        },
        {
            "id": 5,
            "time": "11:15:09",
            "exam": "Computer Science 101",
            "camera": "CAM-01",
            "detection": "Audio Spike / Whisper",
            "risk": "Low",
            "status": "👁️ Reviewing",
            "student": "STU-021 (Emma Watson)",
            "description": "Unusual vocal audio amplitude detected above normal threshold.",
        }
    ]

# ---------- 1. Alerts Header ----------
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown(
        """
        <h1 style="color: #ffffff; font-size: 2.25rem; font-weight: 800; margin-bottom: 0;">
            🚨 Examination Alerts
        </h1>
        <p style="color: #94a3b8; font-size: 0.95rem; margin-top: 0.2rem;">
            Review suspicious activities detected during the examination.
        </p>
    """,
        unsafe_allow_html=True,
    )

with col_h2:
    st.markdown(
        f"""
        <div style="text-align: right; padding-top: 5px;">
            <span class="metric-badge">Total Alerts: {len(st.session_state.alerts_db)}</span>
        </div>
    """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

# ---------- 2. 🔎 Filters Section ----------
with st.container():
    st.markdown(
        """
        <div class="glass-card" style="padding: 1rem 1.5rem !important; margin-bottom: 1.5rem;">
            <p style="color: #f8fafc; font-weight: 700; margin-bottom: 0.5rem; font-size: 0.95rem;">🔎 Filter Examination Events</p>
    """,
        unsafe_allow_html=True,
    )
    
    f1, f2, f3, f4, f5 = st.columns(5)
    with f1:
        exam_filter = st.selectbox("Exam", ["All Exams", "Advanced Mathematics Final", "Physics Midterm", "Computer Science 101"])
    with f2:
        camera_filter = st.selectbox("Camera", ["All Cameras", "CAM-01", "CAM-02", "CAM-03", "CAM-04"])
    with f3:
        type_filter = st.selectbox("Detection Type", ["All Types", "Mobile Phone", "Multiple Person", "Looking Away", "Book / Unauthorized Material", "Audio Spike / Whisper"])
    with f4:
        risk_filter = st.selectbox("Risk Level", ["All Levels", "High", "Medium", "Low"])
    with f5:
        date_filter = st.date_input("Date", value=datetime.today())
        
    st.markdown("</div>", unsafe_allow_html=True)

# Apply filter logic
filtered_alerts = st.session_state.alerts_db
if exam_filter != "All Exams":
    filtered_alerts = [a for a in filtered_alerts if a["exam"] == exam_filter]
if camera_filter != "All Cameras":
    filtered_alerts = [a for a in filtered_alerts if a["camera"] == camera_filter]
if type_filter != "All Types":
    filtered_alerts = [a for a in filtered_alerts if a["detection"] == type_filter]
if risk_filter != "All Levels":
    filtered_alerts = [a for a in filtered_alerts if a["risk"] == risk_filter]

# ---------- Main Layout: Table List & Details View ----------
list_col, detail_col = st.columns([1.6, 1], gap="large")

with list_col:
    st.markdown(
        """
        <h3 style="color: #ffffff; font-size: 1.25rem; font-weight: 700; margin-bottom: 0.75rem;">
            📋 Alert Event Stream
        </h3>
    """,
        unsafe_allow_html=True,
    )

    if not filtered_alerts:
        st.info("No alerts match the selected filter criteria.")
    else:
        # Convert filtered alerts to display format
        display_data = []
        for alert in filtered_alerts:
            display_data.append({
                "ID": alert["id"],
                "Time": alert["time"],
                "Camera": alert["camera"],
                "Detection": alert["detection"],
                "Risk": "🔴 High" if alert["risk"] == "High" else ("🟡 Medium" if alert["risk"] == "Medium" else "🟢 Low"),
                "Status": alert["status"]
            })
        
        df_display = pd.DataFrame(display_data)
        st.dataframe(df_display, use_container_width=True, hide_index=True)

with detail_col:
    st.markdown(
        """
        <h3 style="color: #ffffff; font-size: 1.25rem; font-weight: 700; margin-bottom: 0.75rem;">
            👁️ View Alert Details
        </h3>
    """,
        unsafe_allow_html=True,
    )

    # Let invigilator select an alert ID to inspect
    alert_ids = [a["id"] for a in filtered_alerts]
    
    if not alert_ids:
        st.markdown(
            """
            <div class="glass-card" style="text-align: center; color: #94a3b8; padding: 3rem 1rem !important;">
                <p>Select an active filter matching available items to inspect details.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        selected_id = st.selectbox("Select Alert ID to Inspect", alert_ids)
        selected_alert = next((a for a in filtered_alerts if a["id"] == selected_id), None)

        if selected_alert:
            risk_color = "#f43f5e" if selected_alert["risk"] == "High" else ("#eab308" if selected_alert["risk"] == "Medium" else "#22c55e")
            
            st.markdown(
                f"""
                <div class="glass-card">
                    <h4 style="color: #ffffff; margin-top: 0; margin-bottom: 0.75rem; display: flex; justify-content: space-between; align-items: center;">
                        <span>🚨 Alert #{selected_alert['id']} Details</span>
                        <span style="font-size: 0.85rem; background: rgba(255,255,255,0.08); padding: 3px 8px; border-radius: 6px;">{selected_alert['status']}</span>
                    </h4>
                    
                    <div style="font-size: 0.9rem; color: #cbd5e1; line-height: 1.6;">
                        <p style="margin-bottom: 0.4rem;"><b>Detection Type:</b> <span style="color: #38bdf8;">{selected_alert['detection']}</span></p>
                        <p style="margin-bottom: 0.4rem;"><b>Timestamp:</b> {selected_alert['time']}</p>
                        <p style="margin-bottom: 0.4rem;"><b>Camera Feed:</b> {selected_alert['camera']} ({selected_alert['exam']})</p>
                        <p style="margin-bottom: 0.4rem;"><b>Risk Level:</b> <span style="color: {risk_color}; font-weight: 700;">{selected_alert['risk'].upper()}</span></p>
                        <p style="margin-bottom: 0.8rem;"><b>Examinee:</b> {selected_alert['student']}</p>
                    </div>

                    <div style="background: #020617; border: 2px dashed rgba(99, 102, 241, 0.4); border-radius: 12px; height: 180px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; color: #94a3b8; margin: 1rem 0;">
                        <div style="font-size: 2.2rem; margin-bottom: 0.2rem;">🖼️</div>
                        <div style="font-weight: 600; color: #cbd5e1; font-size: 0.95rem;">[ YOLOv8 Detection Screenshot ]</div>
                        <p style="font-size: 0.75rem; color: #64748b; margin-top: 0.2rem;">Frame saved from {selected_alert['camera']} at {selected_alert['time']}</p>
                    </div>

                    <div style="font-size: 0.9rem; color: #cbd5e1; margin-bottom: 1.25rem;">
                        <p style="margin-bottom: 0.2rem; font-weight: 600; color: #f8fafc;">Description:</p>
                        <p style="color: #94a3b8; font-size: 0.85rem; background: rgba(255,255,255,0.03); padding: 8px 12px; border-radius: 8px;">{selected_alert['description']}</p>
                    </div>
                """,
                unsafe_allow_html=True,
            )

            # Interactive Status Update Action Button
            col_act1, col_act2 = st.columns(2)
            with col_act1:
                if st.button("👁️ Set Reviewing", use_container_width=True):
                    for item in st.session_state.alerts_db:
                        if item["id"] == selected_id:
                            item["status"] = "👁️ Reviewing"
                    st.rerun()
            with col_act2:
                if st.button("✓ Mark as Reviewed", use_container_width=True, type="primary"):
                    for item in st.session_state.alerts_db:
                        if item["id"] == selected_id:
                            item["status"] = "✅ Reviewed"
                    st.success("Alert verified successfully!")
                    st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)