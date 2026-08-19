import time
import streamlit as st


def render_live_monitoring():
  # Initialize session states
  if "is_monitoring" not in st.session_state:
    st.session_state.is_monitoring = False
  if "is_paused" not in st.session_state:
    st.session_state.is_paused = False
  if "alerts_muted" not in st.session_state:
    st.session_state.alerts_muted = False

  # --- 1. MONITORING HEADER ---
  st.markdown(
      """
        <div style="display: flex; justify-content: space-between; align-items: center; background: rgba(255, 255, 255, 0.03); padding: 1rem 1.5rem; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.08); margin-bottom: 1.5rem;">
            <div>
                <h2 style="margin: 0; color: #f1f5f9; font-size: 1.5rem;">🔴 LIVE EXAMINATION MONITORING</h2>
                <p style="margin: 0.2rem 0 0 0; color: #94a3b8; font-size: 0.95rem;">Mid-Term Examination</p>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 0.9rem; font-weight: 600; color: #34d399; margin-bottom: 0.2rem;">
                    🟢 Monitoring Active
                </div>
                <div style="font-family: monospace; font-size: 1.1rem; color: #38bdf8; background: rgba(56, 189, 248, 0.1); padding: 2px 10px; border-radius: 6px; border: 1px solid rgba(56, 189, 248, 0.2);">
                    ⏱ 01:24:35
                </div>
            </div>
        </div>
        """,
      unsafe_allow_html=True,
  )

  # --- 5. MONITORING CONTROLS ---
  c1, c2, c3, c4, c5 = st.columns(5)
  with c1:
    if not st.session_state.is_monitoring:
      if st.button("▶ Start Monitoring", type="primary", use_container_width=True):
        st.session_state.is_monitoring = True
        st.session_state.is_paused = False
        st.rerun()
    else:
      st.button("▶ Running", disabled=True, type="primary", use_container_width=True)
  with c2:
    if st.session_state.is_monitoring:
      pause_label = "▶ Resume" if st.session_state.is_paused else "⏸ Pause"
      if st.button(pause_label, use_container_width=True):
        st.session_state.is_paused = not st.session_state.is_paused
        st.rerun()
    else:
      st.button("⏸ Pause", disabled=True, use_container_width=True)
  with c3:
    if st.button("⏹ Stop", type="secondary", use_container_width=True):
      st.session_state.is_monitoring = False
      st.session_state.is_paused = False
      st.rerun()
  with c4:
    mute_label = (
        "🔔 Unmute Alerts" if st.session_state.alerts_muted else "🔔 Mute/Unmute"
    )
    if st.button(mute_label, use_container_width=True):
      st.session_state.alerts_muted = not st.session_state.alerts_muted
      st.toast(
          f"Alerts {'muted' if st.session_state.alerts_muted else 'unmuted'}.",
          icon="🔔",
      )
  with c5:
    if st.button("🖥️ Fullscreen", use_container_width=True):
      st.toast("Fullscreen camera mode triggered.", icon="🖥️")

  st.markdown("<br>", unsafe_allow_html=True)

  # --- MAIN LAYOUT: 2X2 CCTV GRID & LIVE ALERTS ---
  grid_col, alert_col = st.columns([2.3, 1], gap="large")

  with grid_col:
    st.markdown("### 📹 Live CCTV Grid")

    if st.session_state.is_monitoring and not st.session_state.is_paused:
      # --- 2. LIVE CCTV GRID (2x2) WITH 4. AI DETECTION OVERLAY ---
      row1_c1, row1_c2 = st.columns(2)
      with row1_c1:
        st.markdown(
            """
                <div style="position: relative; background: #020617; border: 1px solid rgba(52, 211, 153, 0.4); border-radius: 12px; height: 210px; padding: 10px; overflow: hidden; box-shadow: 0 0 15px rgba(52, 211, 153, 0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span style="font-family: monospace; font-size: 0.8rem; color: #38bdf8; font-weight: 700;">CAM 01</span>
                        <span style="background: rgba(52, 211, 153, 0.2); color: #34d399; font-size: 0.7rem; font-weight: 700; padding: 1px 6px; border-radius: 4px;">🟢 LIVE</span>
                    </div>
                    <!-- AI Detection Overlay -->
                    <div style="position: absolute; top: 40px; left: 35px; width: 95px; height: 120px; border: 2px dashed #34d399; border-radius: 6px; background: rgba(52, 211, 153, 0.05);">
                        <span style="position: absolute; top: -18px; left: 0; background: #34d399; color: #000; font-size: 0.65rem; font-weight: 700; padding: 1px 4px; border-radius: 3px;">👤 Student</span>
                    </div>
                    <div style="position: absolute; top: 70px; left: 75px; width: 40px; height: 30px; border: 2px solid #f87171; border-radius: 4px; background: rgba(248, 113, 113, 0.2);">
                        <span style="position: absolute; bottom: -18px; left: -10px; font-size: 0.75rem;">📱 🔴</span>
                    </div>
                    <div style="position: absolute; bottom: 8px; left: 10px; color: #64748b; font-size: 0.75rem;">CCTV FEED (Sector A)</div>
                </div>
                """,
            unsafe_allow_html=True,
        )
      with row1_c2:
        st.markdown(
            """
                <div style="position: relative; background: #020617; border: 1px solid rgba(248, 113, 113, 0.5); border-radius: 12px; height: 210px; padding: 10px; overflow: hidden; box-shadow: 0 0 15px rgba(248, 113, 113, 0.15);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span style="font-family: monospace; font-size: 0.8rem; color: #38bdf8; font-weight: 700;">CAM 02</span>
                        <span style="background: rgba(52, 211, 153, 0.2); color: #34d399; font-size: 0.7rem; font-weight: 700; padding: 1px 6px; border-radius: 4px;">🟢 LIVE</span>
                    </div>
                    <div style="position: absolute; top: 40px; left: 60px; width: 110px; height: 130px; border: 2px solid #f87171; border-radius: 6px; background: rgba(248, 113, 113, 0.08);">
                        <span style="position: absolute; top: -18px; left: 0; background: #f87171; color: #fff; font-size: 0.65rem; font-weight: 700; padding: 1px 4px; border-radius: 3px;">👥 Multiple Persons</span>
                    </div>
                    <div style="position: absolute; bottom: 8px; left: 10px; color: #64748b; font-size: 0.75rem;">CCTV FEED (Sector B)</div>
                </div>
                """,
            unsafe_allow_html=True,
        )

      st.markdown("<br>", unsafe_allow_html=True)

      row2_c1, row2_c2 = st.columns(2)
      with row2_c1:
        st.markdown(
            """
                <div style="position: relative; background: #020617; border: 1px solid rgba(250, 204, 21, 0.5); border-radius: 12px; height: 210px; padding: 10px; overflow: hidden; box-shadow: 0 0 15px rgba(250, 204, 21, 0.1);">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span style="font-family: monospace; font-size: 0.8rem; color: #38bdf8; font-weight: 700;">CAM 03</span>
                        <span style="background: rgba(52, 211, 153, 0.2); color: #34d399; font-size: 0.7rem; font-weight: 700; padding: 1px 6px; border-radius: 4px;">🟢 LIVE</span>
                    </div>
                    <div style="position: absolute; top: 45px; left: 70px; width: 100px; height: 120px; border: 2px solid #facc15; border-radius: 6px; background: rgba(250, 204, 21, 0.06);">
                        <span style="position: absolute; top: -18px; left: 0; background: #facc15; color: #000; font-size: 0.65rem; font-weight: 700; padding: 1px 4px; border-radius: 3px;">👀 Looking Away</span>
                    </div>
                    <div style="position: absolute; bottom: 8px; left: 10px; color: #64748b; font-size: 0.75rem;">CCTV FEED (Sector C)</div>
                </div>
                """,
            unsafe_allow_html=True,
        )
      with row2_c2:
        st.markdown(
            """
                <div style="position: relative; background: #020617; border: 1px solid rgba(52, 211, 153, 0.4); border-radius: 12px; height: 210px; padding: 10px; overflow: hidden;">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                        <span style="font-family: monospace; font-size: 0.8rem; color: #38bdf8; font-weight: 700;">CAM 04</span>
                        <span style="background: rgba(52, 211, 153, 0.2); color: #34d399; font-size: 0.7rem; font-weight: 700; padding: 1px 6px; border-radius: 4px;">🟢 LIVE</span>
                    </div>
                    <div style="position: absolute; top: 45px; left: 75px; width: 95px; height: 115px; border: 2px solid #34d399; border-radius: 6px; background: rgba(52, 211, 153, 0.05);">
                        <span style="position: absolute; top: -18px; left: 0; background: #34d399; color: #000; font-size: 0.65rem; font-weight: 700; padding: 1px 4px; border-radius: 3px;">👤 Student</span>
                    </div>
                    <div style="position: absolute; bottom: 8px; left: 10px; color: #64748b; font-size: 0.75rem;">CCTV FEED (Sector D)</div>
                </div>
                """,
            unsafe_allow_html=True,
        )

    elif st.session_state.is_monitoring and st.session_state.is_paused:
      st.markdown(
          """
            <div style="background: #0f172a; border: 1px dashed rgba(250, 204, 21, 0.4); border-radius: 16px; height: 445px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;">
                <div style="font-size: 3.5rem; margin-bottom: 0.5rem;">⏸️</div>
                <h3 style="color: #facc15; margin-bottom: 0.2rem;">Monitoring Paused</h3>
                <p style="color: #94a3b8; font-size: 0.9rem;">Surveillance feeds are paused. Click "Resume" above to continue.</p>
            </div>
            """,
          unsafe_allow_html=True,
      )
    else:
      st.markdown(
          """
            <div style="background: #0f172a; border: 1px dashed rgba(255, 255, 255, 0.15); border-radius: 16px; height: 445px; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center;">
                <div style="font-size: 3.5rem; margin-bottom: 0.5rem;">🔴</div>
                <h3 style="color: #cbd5e1; margin-bottom: 0.2rem;">Monitoring Offline</h3>
                <p style="color: #64748b; font-size: 0.9rem;">Click "Start Monitoring" above to initialize CCTV streams.</p>
            </div>
            """,
          unsafe_allow_html=True,
      )

  # --- 3. LIVE ALERTS (Clean native Streamlit Markdown rendering) ---
  with alert_col:
    st.markdown("### 🚨 LIVE ALERTS")
    st.markdown("*Suspicious events as they happen.*")

    with st.container(height=445):
      if st.session_state.is_monitoring and not st.session_state.is_paused:
        st.markdown(
            """
            <div style="background: rgba(248, 113, 113, 0.12); border-left: 3px solid #f87171; padding: 10px; border-radius: 6px; margin-bottom: 10px;">
                <div style="font-family: monospace; font-size: 0.75rem; color: #94a3b8; margin-bottom: 2px;">10:25:02</div>
                <strong style="color: #f87171; font-size: 0.9rem;">👥 Multiple Persons</strong><br>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 6px;">
                    <span style="color: #cbd5e1; font-family: monospace; font-size: 0.8rem;">CAM-02</span>
                    <span style="background: rgba(248, 113, 113, 0.2); color: #f87171; padding: 1px 6px; border-radius: 4px; font-size: 0.7rem; font-weight: 700;">🔴 HIGH</span>
                </div>
            </div>

            <div style="background: rgba(250, 204, 21, 0.1); border-left: 3px solid #facc15; padding: 10px; border-radius: 6px; margin-bottom: 10px;">
                <div style="font-family: monospace; font-size: 0.75rem; color: #94a3b8; margin-bottom: 2px;">10:24:31</div>
                <strong style="color: #facc15; font-size: 0.9rem;">👀 Looking Away</strong><br>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 6px;">
                    <span style="color: #cbd5e1; font-family: monospace; font-size: 0.8rem;">CAM-03</span>
                    <span style="background: rgba(250, 204, 21, 0.2); color: #facc15; padding: 1px 6px; border-radius: 4px; font-size: 0.7rem; font-weight: 700;">🟡 MEDIUM</span>
                </div>
            </div>

            <div style="background: rgba(248, 113, 113, 0.12); border-left: 3px solid #f87171; padding: 10px; border-radius: 6px;">
                <div style="font-family: monospace; font-size: 0.75rem; color: #94a3b8; margin-bottom: 2px;">10:24:15</div>
                <strong style="color: #f87171; font-size: 0.9rem;">📱 Mobile Detected</strong><br>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 6px;">
                    <span style="color: #cbd5e1; font-family: monospace; font-size: 0.8rem;">CAM-01</span>
                    <span style="background: rgba(248, 113, 113, 0.2); color: #f87171; padding: 1px 6px; border-radius: 4px; font-size: 0.7rem; font-weight: 700;">🔴 HIGH</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
      else:
        st.info("System offline. No live alerts.")