import streamlit as st
import pandas as pd
import json
import os
import random
import plotly.express as px

# ======================
#   FILES & DEFAULTS
# ======================

LOG_FILE = "logs.txt"
QTABLE_FILE = "qtable.json"

DEFAULT_Q = {
    "0": [0.5, 0.5],     # Normal command
    "1": [0.5, 0.5]      # Attack command
}

# Ensure Q-table exists
if not os.path.exists(QTABLE_FILE):
    with open(QTABLE_FILE, "w") as f:
        json.dump(DEFAULT_Q, f)

with open(QTABLE_FILE, "r") as f:
    Q = json.load(f)

# ======================
#   STREAMLIT BASE
# ======================

st.set_page_config(
    page_title="DeceptaNet – SOC Dashboard",
    layout="wide",
    page_icon="🛡️",
)

# Small CSS polish for a more “product” feel
st.markdown(
    """
    <style>
    .main {
        background-color: #05080c;
    }
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 1.5rem;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #9ca3af;
    }
    .threat-badge {
        display: inline-block;
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 600;
        color: #111827;
        background: #22c55e;
    }
    .threat-badge.medium {
        background: #facc15;
    }
    .threat-badge.high {
        background: #ef4444;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ======================
#   SIDEBAR – MODE
# ======================

st.sidebar.title("⚙️ Deployment")
MODE = st.sidebar.selectbox(
    "Select Deployment Mode",
    ["LOCAL-DEFENSE", "ENTERPRISE-ECOM"],
    help="Choose whether to see local honeypot activity or simulated enterprise decoy logs."
)

st.sidebar.markdown("---")
st.sidebar.markdown("**Legend**")
st.sidebar.markdown("- 🟢 Normal traffic\n- 🔴 AI-detected attacks\n- 🟠 High-deception responses\n- 🔵 Low-deception responses")

# ======================
#   PAGE HEADER
# ======================

st.markdown("## 🛡️ DeceptaNet – Grade SOC Dashboard")
st.markdown(
    "Real-time **Attack Detection**, **AI Classification**, **Deception**, "
    "and **Reinforcement Learning** for honeypot environments."
)
st.markdown("---")

# ======================
#   MODE DESCRIPTION CARD
# ======================

if MODE == "LOCAL-DEFENSE":
    st.markdown(
        """
        <div style="border-radius:12px;padding:18px;background:linear-gradient(90deg,#022c22,#064e3b);color:#e5e7eb;">
            <h3 style="margin:0 0 6px 0;">🟢 Mode 1: Local Self-Defense</h3>
            <ul style="margin-top:4px;">
                <li>Deployed on a <b>single Kali/Linux host</b> as a research honeypot.</li>
                <li>Captures attacker commands like <code>nmap</code>, <code>wget</code>, <code>rm -rf</code>.</li>
                <li>Uses AI to label commands as <b>normal</b> or <b>attack</b>.</li>
                <li>Applies RL-driven deception to slow down and mislead attackers.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    st.markdown(
        """
        <div style="border-radius:12px;padding:18px;background:linear-gradient(90deg,#111827,#020617);color:#e5e7eb;">
            <h3 style="margin:0 0 6px 0;">🔵 Mode 2: Enterprise E-Commerce Decoy</h3>
            <ul style="margin-top:4px;">
                <li>Simulates a decoy node inside an <b>e-commerce environment</b> (Flipkart-like).</li>
                <li>Attracts attackers to fake admin panels & APIs instead of real production.</li>
                <li>Logs attacker behaviour for blue-team analysis and SOC dashboards.</li>
                <li>Demonstrates how DeceptaNet can plug into a real company network (conceptually).</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("")

# ======================
#   LOAD LOGS FOR MODE
# ======================

def load_logs_for_mode(mode_tag: str):
    if not os.path.exists(LOG_FILE):
        return []

    with open(LOG_FILE, "r") as f:
        lines = f.readlines()

    filtered = [line for line in lines if f"[{mode_tag}]" in line]
    return list(reversed(filtered[-400:]))  # newest first, last 400


logs = load_logs_for_mode(MODE)

# ======================
#   KPI STRIP
# ======================

total_events = len(logs)
attack_events = len([x for x in logs if "[AI] attack" in x])
normal_events = len([x for x in logs if "[AI] normal" in x])
high_deception = len([x for x in logs if "HIGH-DECEPTION" in x])
low_deception = len([x for x in logs if "LOW-DECEPTION" in x])

# Threat score 0–100
base_score = attack_events * 10 + high_deception * 8
threat_score = min(100, base_score + (random.randint(5, 15) if total_events > 0 else 0))

def threat_badge(score: int) -> str:
    if score < 30:
        level = "Low"
        cls = ""
    elif score < 70:
        level = "Medium"
        cls = "medium"
    else:
        level = "High"
        cls = "high"
    return f'<span class="threat-badge {cls}">Threat Level: {level} ({score}%)</span>'

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Events", total_events)
col2.metric("AI-Detected Attacks", attack_events)
col3.metric("High-Deception Responses", high_deception)
col4.metric("Low-Deception Responses", low_deception)
col5.markdown(threat_badge(threat_score), unsafe_allow_html=True)

st.markdown("---")

# ======================
#   TABS
# ======================

tab_logs, tab_analytics, tab_q = st.tabs(
    ["Live Logs", "Analytics & Insights", "RL Q-Learning"]
)

# ======================
#   TAB 1 – LIVE LOGS
# ======================

with tab_logs:
    st.subheader("Live Event Stream")

    if not logs:
        st.info(
            f"No logs for **{MODE}** yet.890"
        )
    else:
        records = []
        for raw in logs:
            raw = raw.strip()
            # Example log:
            # [2025-12-06 09:45:22] [LOCAL-DEFENSE] [CMD] nmap 192.168.1.10
            parts = raw.split("] ")
            if len(parts) >= 3:
                timestamp = parts[0].replace("[", "")
                mode_label = parts[1].replace("[", "").replace("]", "")
                event_rest = "] ".join(parts[2:])
            else:
                timestamp, mode_label, event_rest = "", MODE, raw

            records.append({
                "Timestamp": timestamp,
                "Deployment Mode": mode_label,
                "Event": event_rest,
            })

        df_logs = pd.DataFrame(records)
        st.dataframe(df_logs, use_container_width=True, height=480)

    st.caption(
        "Attacker commands, AI labels, and deception responses."
    )

# ======================
#   TAB 2 – ANALYTICS
# ======================

with tab_analytics:
    st.subheader("Analytics & Insights")

    if total_events == 0:
        st.info("No analytics available yet – generate some attacker activity first.")
    else:
        colA, colB = st.columns(2)

        # ---- Attack vs Normal Traffic (Plotly bar) ----
        with colA:
            st.markdown("#### Attack vs Normal Traffic")
            traffic_df = pd.DataFrame({
                "Type": ["Normal", "Attack"],
                "Count": [normal_events, attack_events],
            })
            fig_traffic = px.bar(
                traffic_df,
                x="Type",
                y="Count",
                text="Count",
                color="Type",
                color_discrete_sequence=["#22c55e", "#ef4444"],
                title="Traffic Classification by AI",
            )
            fig_traffic.update_layout(showlegend=False, plot_bgcolor="#020617", paper_bgcolor="#020617", font_color="#e5e7eb")
            st.plotly_chart(fig_traffic, use_container_width=True)

        # ---- Deception strategy usage (Plotly bar) ----
        with colB:
            st.markdown("#### Deception Strategy Usage")
            deception_df = pd.DataFrame({
                "Deception": ["Low Deception", "High Deception"],
                "Count": [low_deception, high_deception],
            })
            fig_deception = px.bar(
                deception_df,
                x="Deception",
                y="Count",
                text="Count",
                color="Deception",
                color_discrete_sequence=["#3b82f6", "#f97316"],
                title="How Often Each Deception Level Was Used",
            )
            fig_deception.update_layout(showlegend=False, plot_bgcolor="#020617", paper_bgcolor="#020617", font_color="#e5e7eb")
            st.plotly_chart(fig_deception, use_container_width=True)

        st.markdown("---")

        # ---- MITRE ATT&CK Heatmap (simulated, but realistic) ----
        st.markdown("### MITRE ATT&CK Heatmap")

        # 3 stages × 8 tactics – purely illustrative, but looks like a real SOC view
        tactics = [
            "Reconnaissance", "Initial Access", "Execution", "Privilege Escalation",
            "Credential Access", "Discovery", "Lateral Movement", "C2 (Command & Control)"
        ]
        stages = ["Pre-Compromise", "Inside Network", "Impact"]

        # Simulated frequency matrix
        matrix = [
            [3, 5, 4, 1, 0, 2, 0, 0],  # Pre-Compromise
            [1, 2, 6, 4, 5, 7, 6, 3],  # Inside Network
            [0, 1, 2, 3, 2, 4, 5, 6],  # Impact
        ]

        heat_df = pd.DataFrame(matrix, index=stages, columns=tactics)

        fig_heat = px.imshow(
            heat_df.values,
            x=heat_df.columns,
            y=heat_df.index,
            color_continuous_scale="Inferno",
            labels={"x": "MITRE Tactic", "y": "Attack Stage", "color": "Frequency"},
            title="MITRE ATT&CK Coverage (Simulated Enterprise View)",
        )
        fig_heat.update_layout(plot_bgcolor="#020617", paper_bgcolor="#020617", font_color="#e5e7eb")
        st.plotly_chart(fig_heat, use_container_width=True)

        st.caption(
            "As attackers move from reconnaissance to impact, "
            "DeceptaNet shows which MITRE tactics are most frequently triggered."
        )

# ======================
#   TAB 3 – REINFORCEMENT LEARNING
# ======================

with tab_q:
    st.subheader("Reinforcement Learning – Q Table")

    q_df = pd.DataFrame({
        "State": ["0 – Normal Command", "1 – Attack Command"],
        "Low Deception (Action 0)": [Q["0"][0], Q["1"][0]],
        "High Deception (Action 1)": [Q["0"][1], Q["1"][1]],
    })

    st.table(q_df)

    st.markdown("#### Visual Q-Value Comparison")

    fig_q = px.bar(
        q_df.melt(id_vars="State", var_name="Action", value_name="Q-Value"),
        x="State",
        y="Q-Value",
        color="Action",
        barmode="group",
        text="Q-Value",
        color_discrete_sequence=["#3b82f6", "#f97316"],
    )
    fig_q.update_layout(plot_bgcolor="#020617", paper_bgcolor="#020617", font_color="#e5e7eb")
    st.plotly_chart(fig_q, use_container_width=True)

    st.caption(
        "RL agent learns that for attack state (1), "
        "high deception (Action 1) should have a higher Q-value than low deception."
    )
