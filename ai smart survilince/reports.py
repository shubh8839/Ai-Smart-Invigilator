import io
from fpdf import FPDF
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def generate_sample_pdf():
    """Generates a valid binary PDF document for Streamlit download."""
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Document Header
    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(
        0,
        10,
        "CS-401 Final Examination Audit Report",
        new_x="LMARGIN",
        new_y="NEXT",
        align="C",
    )
    pdf.set_font("Helvetica", "I", 10)
    pdf.cell(
        0,
        6,
        "AI-Generated Invigilator Summary & Security Audit Log",
        new_x="LMARGIN",
        new_y="NEXT",
        align="C",
    )
    pdf.ln(8)

    # Section 1: Examination Metadata
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "1. Examination Information", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", size=10)

    pdf.cell(45, 6, "Exam Name: CS-401 Final Exam")
    pdf.cell(45, 6, "Date: 17-08-2026", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(45, 6, "Start Time: 10:00 AM")
    pdf.cell(45, 6, "End Time: 01:00 PM", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(45, 6, "Monitored: 120 Candidates")
    pdf.cell(45, 6, "Cameras: 03 (CAM-01..03)", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    # Section 2: Metrics Summary
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(
        0, 8, "2. Security & Risk Metrics Summary", new_x="LMARGIN", new_y="NEXT"
    )
    pdf.set_font("Helvetica", size=10)
    pdf.cell(
        0,
        6,
        "- Total Monitored: 120 Candidates (100% Attendance)",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.cell(
        0,
        6,
        "- High-Risk: 14 Candidates | Medium-Risk: 26 Candidates | Low-Risk: 66 Candidates",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.cell(
        0,
        6,
        "- Average Risk Score: 3.4 / 10 | Overall Integrity Score: 86.6%",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.ln(6)

    # Section 3: Candidate Roster Table
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(
        0, 8, "3. Flagged Candidate Audit Roster", new_x="LMARGIN", new_y="NEXT"
    )
    pdf.ln(2)

    # Table Header
    pdf.set_font("Helvetica", "B", 9)
    pdf.cell(28, 7, "Candidate ID", border=1)
    pdf.cell(32, 7, "Name", border=1)
    pdf.cell(20, 7, "Camera", border=1)
    pdf.cell(55, 7, "Primary Incident", border=1)
    pdf.cell(18, 7, "Flags", border=1)
    pdf.cell(37, 7, "Risk Score", border=1, new_x="LMARGIN", new_y="NEXT")

    # Table Rows
    pdf.set_font("Helvetica", size=9)
    candidates = [
        (
            "CS2026-004",
            "Alex Mercer",
            "CAM-01",
            "Mobile Device Detected",
            "5",
            "8.8 / 10 (High)",
        ),
        (
            "CS2026-019",
            "Sophia Chen",
            "CAM-02",
            "Multiple Faces Present",
            "4",
            "7.5 / 10 (High)",
        ),
        (
            "CS2026-042",
            "Liam Patel",
            "CAM-01",
            "Persistent Eye Off-Screen",
            "3",
            "5.2 / 10 (Med)",
        ),
        (
            "CS2026-088",
            "Emma Watson",
            "CAM-03",
            "Audio / Secondary Voice",
            "2",
            "4.1 / 10 (Med)",
        ),
        (
            "CS2026-105",
            "David Miller",
            "CAM-02",
            "Frequent Head Turning",
            "1",
            "2.0 / 10 (Low)",
        ),
    ]

    for cid, name, cam, incident, flags, risk in candidates:
        pdf.cell(28, 6, cid, border=1)
        pdf.cell(32, 6, name, border=1)
        pdf.cell(20, 6, cam, border=1)
        pdf.cell(55, 6, incident, border=1)
        pdf.cell(18, 6, flags, border=1)
        pdf.cell(37, 6, risk, border=1, new_x="LMARGIN", new_y="NEXT")

    return bytes(pdf.output())


def render_reports():
    # --- Custom CSS tailored to match Dashboard Theme ---
    st.markdown(
        """
        <style>
        .report-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.2rem;
        }
        .report-title {
            font-size: 22px;
            font-weight: 800;
            color: #f3f5ff;
            margin: 0;
        }
        .report-sub {
            color: #93a1c5;
            font-size: 13.5px;
            margin-top: 2px;
        }
        .info-card {
            background: linear-gradient(145deg, #10172a, #0d1223);
            border: 1px solid #222d47;
            border-radius: 10px;
            padding: 16px 20px;
            margin-bottom: 1.5rem;
        }
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
            gap: 16px;
        }
        .info-item {
            display: flex;
            flex-direction: column;
        }
        .info-label {
            font-size: 11px;
            font-family: 'DM Mono', monospace;
            color: #627299;
            text-transform: uppercase;
            letter-spacing: 0.8px;
            margin-bottom: 4px;
        }
        .info-val {
            font-size: 14px;
            font-weight: 700;
            color: #e2e8f0;
        }
        .metric-box {
            background: linear-gradient(145deg, #10172a, #0d1223);
            border: 1px solid #222d47;
            border-radius: 10px;
            padding: 14px 16px;
            position: relative;
            overflow: hidden;
        }
        .metric-box::before {
            content: "";
            position: absolute;
            top: 0; left: 16px; right: 16px;
            height: 2px;
            background: var(--accent-color, #8c5cff);
            box-shadow: 0 0 12px var(--accent-color, #8c5cff);
        }
        .metric-num {
            font-family: 'DM Mono', monospace;
            font-size: 24px;
            font-weight: 800;
            color: #ffffff;
            margin-top: 4px;
        }
        .metric-lbl {
            font-size: 12px;
            color: #8fa1d2;
            font-weight: 600;
        }
        .metric-sub {
            font-size: 10px;
            color: #627299;
            margin-top: 4px;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    # Candidate Dataset
    candidates_data = [
        {
            "Candidate ID": "CS2026-004",
            "Name": "Alex Mercer",
            "Camera Feed": "CAM-01",
            "Primary Incident": "Mobile Device Detected",
            "Total Flags": 5,
            "Risk Score": "8.8 / 10",
            "Audit Category": "🔴 High Risk",
        },
        {
            "Candidate ID": "CS2026-019",
            "Name": "Sophia Chen",
            "Camera Feed": "CAM-02",
            "Primary Incident": "Multiple Faces Present",
            "Total Flags": 4,
            "Risk Score": "7.5 / 10",
            "Audit Category": "🔴 High Risk",
        },
        {
            "Candidate ID": "CS2026-042",
            "Name": "Liam Patel",
            "Camera Feed": "CAM-01",
            "Primary Incident": "Persistent Eye Off-Screen",
            "Total Flags": 3,
            "Risk Score": "5.2 / 10",
            "Audit Category": "🟡 Medium Risk",
        },
        {
            "Candidate ID": "CS2026-088",
            "Name": "Emma Watson",
            "Camera Feed": "CAM-03",
            "Primary Incident": "Audio / Secondary Voice",
            "Total Flags": 2,
            "Risk Score": "4.1 / 10",
            "Audit Category": "🟡 Medium Risk",
        },
        {
            "Candidate ID": "CS2026-105",
            "Name": "David Miller",
            "Camera Feed": "CAM-02",
            "Primary Incident": "Frequent Head Turning",
            "Total Flags": 1,
            "Risk Score": "2.0 / 10",
            "Audit Category": "🟢 Low Risk",
        },
    ]
    df_candidates = pd.DataFrame(candidates_data)

    # Convert dataframe to CSV format for downloading
    csv_data = df_candidates.to_csv(index=False).encode("utf-8")

    # --- Header ---
    st.markdown(
        """
        <div>
            <h2 class="report-title">📋 Final Examination Report</h2>
            <div class="report-sub">AI-Generated Comprehensive Invigilator Summary & Audit Log</div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    st.write("")

    # --- 1. Examination Information ---
    st.markdown("##### 📌 1. Examination Information")
    st.markdown(
        """
        <div class="info-card">
            <div class="info-grid">
                <div class="info-item">
                    <span class="info-label">EXAM NAME</span>
                    <span class="info-val">CS-401 Final Exam</span>
                </div>
                <div class="info-item">
                    <span class="info-label">DATE</span>
                    <span class="info-val">17-08-2026</span>
                </div>
                <div class="info-item">
                    <span class="info-label">START TIME</span>
                    <span class="info-val">10:00 AM</span>
                </div>
                <div class="info-item">
                    <span class="info-label">END TIME</span>
                    <span class="info-val">01:00 PM</span>
                </div>
                <div class="info-item">
                    <span class="info-label">STUDENTS MONITORED</span>
                    <span class="info-val">120 Candidates</span>
                </div>
                <div class="info-item">
                    <span class="info-label">CAMERAS USED</span>
                    <span class="info-val">03 (CAM-01..03)</span>
                </div>
            </div>
        </div>
    """,
        unsafe_allow_html=True,
    )

    # --- 2. Examination Summary Metrics ---
    st.markdown("##### 📊 2. Examination Summary")
    m1, m2, m3, m4, m5, m6 = st.columns(6)

    with m1:
        st.markdown(
            """
            <div class="metric-box" style="--accent-color:#60a5fa;">
                <div class="metric-lbl">Total Students</div>
                <div class="metric-num">120</div>
                <div class="metric-sub">100% Present</div>
            </div>
        """,
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            """
            <div class="metric-box" style="--accent-color:#8c5cff;">
                <div class="metric-lbl">Total Activities</div>
                <div class="metric-num">106</div>
                <div class="metric-sub">Flagged Events</div>
            </div>
        """,
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            """
            <div class="metric-box" style="--accent-color:#ff5878;">
                <div class="metric-lbl">High-Risk</div>
                <div class="metric-num" style="color:#ff5878;">14</div>
                <div class="metric-sub">Requires Audit</div>
            </div>
        """,
            unsafe_allow_html=True,
        )
    with m4:
        st.markdown(
            """
            <div class="metric-box" style="--accent-color:#ffa629;">
                <div class="metric-lbl">Medium-Risk</div>
                <div class="metric-num" style="color:#ffa629;">26</div>
                <div class="metric-sub">Minor Warnings</div>
            </div>
        """,
            unsafe_allow_html=True,
        )
    with m5:
        st.markdown(
            """
            <div class="metric-box" style="--accent-color:#45e7a6;">
                <div class="metric-lbl">Low-Risk</div>
                <div class="metric-num" style="color:#45e7a6;">66</div>
                <div class="metric-sub">Clean Records</div>
            </div>
        """,
            unsafe_allow_html=True,
        )
    with m6:
        st.markdown(
            """
            <div class="metric-box" style="--accent-color:#38bdf8;">
                <div class="metric-lbl">Avg Risk Score</div>
                <div class="metric-num">3.4<span style="font-size:13px; color:#627299;">/10</span></div>
                <div class="metric-sub">Integrity: 86.6%</div>
            </div>
        """,
            unsafe_allow_html=True,
        )

    st.write("")
    st.write("")

    # --- 3. Detection Summary & 4. Risk Distribution Charts ---
    c_left, c_right = st.columns([1, 1], gap="medium")

    with c_left:
        with st.container(border=True):
            st.markdown(
                "<h4 style='font-size:15px; margin-bottom:10px;'>👁 3. Detection Summary</h4>",
                unsafe_allow_html=True,
            )

            detection_df = pd.DataFrame({
                "Detection Category": [
                    "Mobile Phone Detected",
                    "Looking Away / Off-Screen",
                    "Multiple Persons",
                    "Secondary Voice",
                    "Absence from Seat",
                ],
                "Count": [38, 32, 18, 12, 6],
            })

            fig_det = px.bar(
                detection_df,
                x="Count",
                y="Detection Category",
                orientation="h",
                color="Count",
                color_continuous_scale=["#60a5fa", "#8c5cff", "#ff5878"],
                text="Count",
            )
            fig_det.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#93a1c5", family="Manrope"),
                height=250,
                margin=dict(l=10, r=10, t=10, b=10),
                coloraxis_showscale=False,
                xaxis=dict(showgrid=True, gridcolor="#1b253e", title=None),
                yaxis=dict(showgrid=False, title=None, autorange="reversed"),
            )
            fig_det.update_traces(textposition="outside", marker_line_width=0)
            st.plotly_chart(
                fig_det,
                use_container_width=True,
                config={"displayModeBar": False},
            )

    with c_right:
        with st.container(border=True):
            st.markdown(
                "<h4 style='font-size:15px; margin-bottom:10px;'>🧠 4. Risk Distribution Breakdown</h4>",
                unsafe_allow_html=True,
            )

            risk_df = pd.DataFrame({
                "Risk Category": [
                    "Low-Risk (Clean)",
                    "Medium-Risk (Warning)",
                    "High-Risk (Infraction)",
                ],
                "Students": [66, 26, 14],
            })

            fig_risk = px.pie(
                risk_df,
                names="Risk Category",
                values="Students",
                hole=0.6,
                color_discrete_sequence=["#45e7a6", "#ffa629", "#ff5878"],
            )
            fig_risk.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#93a1c5", family="Manrope"),
                height=250,
                margin=dict(l=10, r=10, t=10, b=10),
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.2,
                    xanchor="center",
                    x=0.5,
                ),
            )
            st.plotly_chart(
                fig_risk,
                use_container_width=True,
                config={"displayModeBar": False},
            )

    st.write("")

    # --- 5. Candidate Audit Roster ---
    with st.container(border=True):
        st.markdown(
            "<h4 style='font-size:15px; margin-bottom:12px;'>🚨 5. Candidate Audit Roster & Flagged Candidates</h4>",
            unsafe_allow_html=True,
        )
        st.dataframe(df_candidates, use_container_width=True, hide_index=True)

    st.write("")

    # --- 6. Download & Export Report ---
    with st.container(border=True):
        st.markdown(
            "<h4 style='font-size:15px; margin-bottom:10px;'>📥 6. Export & Download Examination Report</h4>",
            unsafe_allow_html=True,
        )

        d_text, d_actions = st.columns([0.65, 0.35], gap="medium")

        with d_text:
            st.markdown(
                """
                <p style="color: #93a1c5; font-size: 13px; margin-top: 5px;">
                Export the complete examination audit log including candidate risk scores, 
                detection categories, and camera feed flags into your preferred format.
                </p>
                """,
                unsafe_allow_html=True,
            )

        with d_actions:
            btn_col1, btn_col2 = st.columns(2)

            with btn_col1:
                st.download_button(
                    label="📄 Export PDF",
                    data=generate_sample_pdf(),
                    file_name="CS401_Exam_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    type="primary",
                )

            with btn_col2:
                st.download_button(
                    label="📊 Export CSV",
                    data=csv_data,
                    file_name="CS401_Candidate_Audit.csv",
                    mime="text/csv",
                    use_container_width=True,
                )


if __name__ == "__main__":
    render_reports()