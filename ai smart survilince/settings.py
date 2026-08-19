import streamlit as st


def render_settings():
  st.markdown("## ⚙️ System Settings")
  st.markdown(
      "Manage your examination monitoring preferences, alert rules, camera"
      " configurations, reports, and appearance."
  )
  st.markdown("---")

  # Initialize session state for settings if not already present
  if "settings" not in st.session_state:
    st.session_state.settings = {
        # 1. Monitoring Settings
        "detection_sensitivity": "Medium",
        "monitoring_mode": "Standard",
        "auto_start_monitoring": False,
        "save_detection_evidence": True,
        # 2. Alert Settings
        "enable_alerts": True,
        "sound_alerts": True,
        "popup_alerts": True,
        "alert_severity_threshold": "Medium",
        # 3. Camera Settings
        "selected_camera": "Camera 0 (Default)",
        "camera_resolution": "1280x720 (HD)",
        "camera_enabled": True,
        "number_of_cameras": 1,
        # 4. Report Settings
        "include_evidence_images": True,
        "include_student_ids": True,
        "report_format": "PDF",
        "auto_save_reports": True,
        # 5. Appearance
        "theme": "Dark",
        "compact_mode": False,
    }

  s = st.session_state.settings

  with st.form("settings_form"):
    # --- 1. MONITORING SETTINGS ---
    st.markdown("### 🎥 1. Monitoring Settings")
    st.markdown(
        "*Controls related to examination monitoring and AI behavior.*"
    )
    col1, col2 = st.columns(2, gap="large")
    with col1:
      s["detection_sensitivity"] = st.selectbox(
          "Detection Sensitivity",
          ["Low", "Medium", "High"],
          index=["Low", "Medium", "High"].index(s["detection_sensitivity"]),
      )
      s["auto_start_monitoring"] = st.toggle(
          "Auto-start monitoring", value=s["auto_start_monitoring"]
      )
    with col2:
      s["monitoring_mode"] = st.selectbox(
          "Monitoring Mode",
          ["Standard", "Strict"],
          index=["Standard", "Strict"].index(s["monitoring_mode"]),
      )
      s["save_detection_evidence"] = st.toggle(
          "Save detection evidence", value=s["save_detection_evidence"]
      )

    st.markdown("---")

    # --- 2. ALERT SETTINGS ---
    st.markdown("### 🚨 2. Alert Settings")
    st.markdown("*Controls how the invigilator receives live alerts.*")
    col1, col2 = st.columns(2, gap="large")
    with col1:
      s["enable_alerts"] = st.toggle("Enable alerts", value=s["enable_alerts"])
      s["sound_alerts"] = st.toggle("Sound alerts", value=s["sound_alerts"])
    with col2:
      s["popup_alerts"] = st.toggle("Popup alerts", value=s["popup_alerts"])
      s["alert_severity_threshold"] = st.selectbox(
          "Alert severity threshold",
          ["Low", "Medium", "High"],
          index=["Low", "Medium", "High"].index(
              s["alert_severity_threshold"]
          ),
      )

    st.markdown("---")

    # --- 3. CAMERA SETTINGS ---
    st.markdown("### 📹 3. Camera Settings")
    st.markdown(
        "*Basic camera configuration designed for OpenCV integration.*"
    )
    col1, col2 = st.columns(2, gap="large")
    with col1:
      camera_options = [
          "Camera 0 (Default)",
          "Camera 1 (External USB)",
          "IP Camera Stream",
      ]
      s["selected_camera"] = st.selectbox(
          "Select camera",
          camera_options,
          index=(
              camera_options.index(s["selected_camera"])
              if s["selected_camera"] in camera_options
              else 0
          ),
      )
      s["camera_enabled"] = st.toggle(
          "Enable/disable camera", value=s["camera_enabled"]
      )
    with col2:
      res_options = [
          "640x480 (VGA)",
          "1280x720 (HD)",
          "1920x1080 (Full HD)",
      ]
      s["camera_resolution"] = st.selectbox(
          "Camera resolution",
          res_options,
          index=(
              res_options.index(s["camera_resolution"])
              if s["camera_resolution"] in res_options
              else 1
          ),
      )
      s["number_of_cameras"] = st.number_input(
          "Number of cameras",
          min_value=1,
          max_value=4,
          value=int(s["number_of_cameras"]),
      )

    st.markdown("---")

    # --- 4. REPORT SETTINGS ---
    st.markdown("### 📄 4. Report Settings")
    st.markdown("*Controls for generated post-exam reports.*")
    col1, col2 = st.columns(2, gap="large")
    with col1:
      s["include_evidence_images"] = st.toggle(
          "Include evidence images", value=s["include_evidence_images"]
      )
      s["report_format"] = st.selectbox(
          "Report format", ["PDF"], index=0
      )  # Default/locked to PDF as requested
    with col2:
      s["include_student_ids"] = st.toggle(
          "Include student IDs", value=s["include_student_ids"]
      )
      s["auto_save_reports"] = st.toggle(
          "Automatically save reports", value=s["auto_save_reports"]
      )

    st.markdown("---")

    # --- 5. APPEARANCE ---
    st.markdown("### 🎨 5. Appearance")
    st.markdown("*Customize the dashboard look and feel.*")
    col1, col2 = st.columns(2, gap="large")
    with col1:
      s["theme"] = st.selectbox(
          "Theme", ["Dark", "Light"], index=["Dark", "Light"].index(s["theme"])
      )
    with col2:
      s["compact_mode"] = st.toggle("Compact mode", value=s["compact_mode"])

    st.markdown("---")

    # Save button
    submitted = st.form_submit_button(
        "💾 Save All Settings", type="primary", use_container_width=True
    )
    if submitted:
      st.session_state.settings = s
      st.success("Settings saved successfully!")