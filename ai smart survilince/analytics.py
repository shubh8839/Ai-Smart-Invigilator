import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def analytics_page():
    # ------------------ TOP BAR & FILTERS ------------------
    st.markdown(
        """
        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:1rem; flex-wrap:wrap; gap:10px;">
            <div>
                <h2 style="font-size:24px; font-weight:800; margin:0 0 4px 0; color:#f3f5ff; letter-spacing:-0.5px;">
                    📈 Invigilation Analytics
                </h2>
                <p style="color:#93a1c5; font-size:13.5px; margin:0;">
                    Real-time detection statistics, room risk distribution, and AI model metrics.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Filter Controls inside a styled row
    f_col1, f_col2, f_col3 = st.columns([1, 1, 2], gap="small")
    with f_col1:
        time_range = st.selectbox(
            "📅 Time Horizon",
            ["Live Today", "Last 24 Hours", "Last 7 Days", "Full Term"],
            index=0,
        )
    with f_col2:
        selected_room = st.selectbox(
            "🏫 Examination Hall",
            ["All Halls", "Hall A (Main)", "Hall B (Lab)", "Hall C"],
            index=0,
        )

    st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)

    # ------------------ TOP METRIC CARDS ------------------
    m1, m2, m3, m4 = st.columns(4, gap="small")
    with m1:
        st.metric("Total Detections", "103", delta="+12% vs avg")
    with m2:
        st.metric("Suspicious Acts", "42", delta="+5% vs avg")
    with m3:
        st.metric(
            "High-Risk Incidents",
            "10",
            delta="-2% lower",
            delta_color="inverse",
        )
    with m4:
        st.metric(
            "Avg ANN Risk Score",
            "24.8%",
            delta="-1.2%",
            delta_color="inverse",
        )

    st.markdown("<div style='margin-bottom:20px;'></div>", unsafe_allow_html=True)

    # Base chart layout template for dark mode styling
    base_layout = dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#a0aec0", family="Manrope, sans-serif", size=12),
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(
            showgrid=True, gridcolor="rgba(255,255,255,0.06)", zeroline=False
        ),
        yaxis=dict(
            showgrid=True, gridcolor="rgba(255,255,255,0.06)", zeroline=False
        ),
    )

    # ------------------ ROW 1: CHARTS ------------------
    row1_left, row1_right = st.columns([1.1, 0.9], gap="medium")

    # 1. Detection Breakdown (Horizontal Multi-Color Bars)
    with row1_left:
        with st.container(border=True):
            st.markdown(
                "<h4 style='font-size:15px; font-weight:700; margin-bottom:12px; color:#f3f5ff;'>📊 Detection Categories Breakdown</h4>",
                unsafe_allow_html=True,
            )

            det_df = pd.DataFrame(
                {
                    "Category": [
                        "Mobile Phone",
                        "Looking Away",
                        "Book / Material",
                        "Multiple Persons",
                    ],
                    "Detections": [35, 22, 15, 12],
                }
            )

            fig_det = px.bar(
                det_df,
                x="Detections",
                y="Category",
                orientation="h",
                text="Detections",
                color="Category",
                color_discrete_map={
                    "Mobile Phone": "#ec4899",  # Neon Pink
                    "Looking Away": "#3b82f6",  # Neon Blue
                    "Book / Material": "#f59e0b",  # Amber/Orange
                    "Multiple Persons": "#a855f7",  # Vivid Purple
                },
            )

            fig_det.update_traces(
                textposition="outside",
                textfont=dict(color="#ffffff", size=12),
                hovertemplate="<b>%{y}</b><br>Count: %{x}<extra></extra>",
                marker=dict(line=dict(width=1, color="rgba(255,255,255,0.2)")),
            )
            fig_det.update_layout(**base_layout, showlegend=False, height=280)
            st.plotly_chart(
                fig_det,
                use_container_width=True,
                config={"displayModeBar": False},
            )

    # 2. ANN Risk Classification Donut Chart
    with row1_right:
        with st.container(border=True):
            st.markdown(
                "<h4 style='font-size:15px; font-weight:700; margin-bottom:12px; color:#f3f5ff;'>🧠 ANN Risk Level Distribution</h4>",
                unsafe_allow_html=True,
            )

            risk_df = pd.DataFrame(
                {
                    "Level": [
                        "Low Risk (0-30%)",
                        "Medium Risk (31-70%)",
                        "High Risk (71-100%)",
                    ],
                    "Count": [65, 25, 10],
                }
            )

            fig_risk = px.pie(
                risk_df,
                names="Level",
                values="Count",
                hole=0.62,
                color="Level",
                color_discrete_map={
                    "Low Risk (0-30%)": "#10b981",  # Emerald Green
                    "Medium Risk (31-70%)": "#f59e0b",  # Neon Amber
                    "High Risk (71-100%)": "#f43f5e",  # Coral Red
                },
            )

            fig_risk.update_traces(
                textinfo="percent+label",
                textfont=dict(size=11, color="#ffffff"),
                marker=dict(line=dict(color="#0d1325", width=3)),
                hovertemplate="<b>%{label}</b><br>Share: %{percent}<extra></extra>",
            )

            # Center Callout Label
            fig_risk.add_annotation(
                text="<b>RISK</b><br><span style='font-size:11px; color:#93a1c5;'>EVALUATION</span>",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(size=13, color="#f3f5ff"),
            )

            fig_risk.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#93a1c5"),
                showlegend=False,
                margin=dict(l=10, r=10, t=20, b=10),
                height=280,
            )
            st.plotly_chart(
                fig_risk,
                use_container_width=True,
                config={"displayModeBar": False},
            )

    st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)

    # ------------------ ROW 2: CHARTS ------------------
    row2_left, row2_right = st.columns([0.9, 1.1], gap="medium")

    # 3. Camera Load (Individual Neon Columns)
    with row2_left:
        with st.container(border=True):
            st.markdown(
                "<h4 style='font-size:15px; font-weight:700; margin-bottom:12px; color:#f3f5ff;'>📹 Camera Detection Activity</h4>",
                unsafe_allow_html=True,
            )

            cam_df = pd.DataFrame(
                {
                    "Camera": [
                        "Camera 01",
                        "Camera 02",
                        "Camera 03",
                        "Camera 04",
                    ],
                    "Events": [32, 18, 41, 12],
                }
            )

            fig_cam = px.bar(
                cam_df,
                x="Camera",
                y="Events",
                text="Events",
                color="Camera",
                color_discrete_sequence=[
                    "#8b5cf6",
                    "#06b6d4",
                    "#ec4899",
                    "#10b981",
                ],
            )

            fig_cam.update_traces(
                textposition="outside",
                textfont=dict(color="#ffffff", size=12),
                hovertemplate="<b>%{x}</b><br>Detections: %{y}<extra></extra>",
                marker=dict(line=dict(width=1, color="rgba(255,255,255,0.2)")),
            )
            fig_cam.update_layout(**base_layout, showlegend=False, height=280)
            st.plotly_chart(
                fig_cam,
                use_container_width=True,
                config={"displayModeBar": False},
            )

    # 4. Hourly Detection Timeline (Glowing Cyan Curved Line)
    with row2_right:
        with st.container(border=True):
            st.markdown(
                "<h4 style='font-size:15px; font-weight:700; margin-bottom:12px; color:#f3f5ff;'>📅 Hourly Incident Timeline</h4>",
                unsafe_allow_html=True,
            )

            trend_df = pd.DataFrame(
                {
                    "Time": [
                        "10:00 AM",
                        "11:00 AM",
                        "12:00 PM",
                        "01:00 PM",
                        "02:00 PM",
                        "03:00 PM",
                    ],
                    "Alerts": [10, 14, 20, 18, 12, 8],
                }
            )

            fig_trend = go.Figure()
            fig_trend.add_trace(
                go.Scatter(
                    x=trend_df["Time"],
                    y=trend_df["Alerts"],
                    mode="lines+markers",
                    name="Alerts",
                    line=dict(color="#00f2fe", width=3, shape="spline"),
                    marker=dict(
                        size=8,
                        color="#ffffff",
                        line=dict(color="#00f2fe", width=2),
                    ),
                    fill="tozeroy",
                    fillcolor="rgba(0, 242, 254, 0.15)",
                    hovertemplate="<b>%{x}</b><br>Incidents: %{y}<extra></extra>",
                )
            )

            fig_trend.update_layout(**base_layout, height=280)
            st.plotly_chart(
                fig_trend,
                use_container_width=True,
                config={"displayModeBar": False},
            )

    st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)

    # ------------------ ROW 3: RECENT HIGH RISK EVENTS LOG TABLE ------------------
    with st.container(border=True):
        st.markdown(
            "<h4 style='font-size:15px; font-weight:700; margin-bottom:12px; color:#f3f5ff;'>📋 Recent High-Risk Audit Log</h4>",
            unsafe_allow_html=True,
        )

        logs_df = pd.DataFrame(
            [
                {
                    "Timestamp": "10:24:12 AM",
                    "Camera Feed": "Camera 03 (Hall A)",
                    "Detection Flag": "📱 Mobile Phone Detected",
                    "ANN Confidence": "94.2%",
                    "Risk Status": "🔴 High Risk",
                },
                {
                    "Timestamp": "10:21:05 AM",
                    "Camera Feed": "Camera 01 (Hall A)",
                    "Detection Flag": "👀 Looking Away > 10s",
                    "ANN Confidence": "81.0%",
                    "Risk Status": "🟡 Medium Risk",
                },
                {
                    "Timestamp": "10:18:44 AM",
                    "Camera Feed": "Camera 03 (Hall A)",
                    "Detection Flag": "👥 Multiple Persons In Frame",
                    "ANN Confidence": "98.5%",
                    "Risk Status": "🔴 High Risk",
                },
                {
                    "Timestamp": "09:55:10 AM",
                    "Camera Feed": "Camera 02 (Hall B)",
                    "Detection Flag": "📚 Book/Notes Sheet Detected",
                    "ANN Confidence": "88.7%",
                    "Risk Status": "🔴 High Risk",
                },
            ]
        )

        st.dataframe(
            logs_df,
            use_container_width=True,
            hide_index=True,
        )


if __name__ == "__main__":
    analytics_page()