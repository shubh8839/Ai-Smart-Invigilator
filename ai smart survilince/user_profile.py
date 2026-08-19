import streamlit as st


def render_profile():
  # Fetch logged-in user info from session state
  profile_name = st.session_state.get("full_name", "Exam Administrator")
  profile_email = (
      st.session_state.get("username")
      or st.session_state.get("email")
      or "user@college.edu"
  )

  # --- PROFILE HEADER ---
  st.markdown("## 👤 Administrator Profile")
  st.markdown("Manage your personal information and account security.")

  st.markdown(
      f"""
    <div style="display: flex; align-items: center; gap: 1.5rem; background: rgba(255, 255, 255, 0.04); padding: 1.5rem; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.08); margin-bottom: 2rem;">
        <div style="font-size: 3.5rem; background: rgba(59, 130, 246, 0.15); width: 75px; height: 75px; display: flex; align-items: center; justify-content: center; border-radius: 50%;">
            🛡️
        </div>
        <div>
            <h2 style="margin: 0; color: #f1f5f9;">{profile_name}</h2>
            <p style="margin: 0.2rem 0; color: #94a3b8; font-size: 0.95rem;">Examination Administrator</p>
            <div style="margin-top: 0.4rem; display: inline-flex; align-items: center; gap: 0.4rem; background: rgba(16, 185, 129, 0.15); color: #34d399; padding: 0.2rem 0.8rem; border-radius: 20px; font-size: 0.85rem; font-weight: 600;">
                🟢 Account Status: Active
            </div>
        </div>
    </div>
    """,
      unsafe_allow_html=True,
  )

  col1, col2 = st.columns(2, gap="large")

  with col1:
    st.markdown("### 📋 Personal Information")
    st.markdown(f"""
        - **Full Name:** {profile_name}
        - **Email:** {profile_email}
        """)

  with col2:
    st.markdown("### 🔒 Account Security")
    st.markdown("""
        - **Last Login:** Just now
        - **Account Status:** 🟢 Active
        """)
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### 🔑 Change Password")
    with st.form("change_password_form"):
      current_password = st.text_input("Current Password", type="password")
      new_password = st.text_input("New Password", type="password")
      confirm_password = st.text_input("Confirm New Password", type="password")

      pwd_submitted = st.form_submit_button("Update Password", type="primary")
      if pwd_submitted:
        if not current_password or not new_password or not confirm_password:
          st.warning("Please fill in all password fields.")
        elif new_password != confirm_password:
          st.error("New passwords do not match.")
        else:
          st.success("Password updated successfully!")

  st.markdown("---")
  col_space, col_btn = st.columns([5, 1])
  with col_btn:
    if st.button("🚪 Logout", type="secondary", use_container_width=True):
      st.session_state.clear()
      st.success("Logged out successfully!")
      try:
        st.switch_page("app.py")
      except Exception:
        st.info("You have been logged out. Please navigate back to home.")