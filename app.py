import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as gw

# 1. Page Configuration (Dark Mode & Tech Vibe)
st.set_page_config(
    page_title="EuroQ-Radar v2.0 🛰️",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Deep-Tech Styling
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .stHeadingContainer h1 { color: #00f2fe; font-family: 'Courier New', Courier, monospace; }
    </style>
""", unsafe_allow_html=True)

# 2. Core Data Matrix (v2.0 Expanded)
@st.cache_data
def load_data():
    data = {
        "Name": [
            "Petra Scudo", "Paolo Cremonesi", "Sabine Mehr", "Riccardo Manenti", 
            "Giorgio Zarantonello", "Davide Venturelli", "Giulio Amato", 
            "Daniele Dragoni", "Antonio Sturiale", "Vittorio Tartarini", 
            "Enrico Talinucci", "Antonio Policicchio", "Emilio Mango", "Lucia Occhiuto"
        ],
        "Role": [
            "Policy & Standards", "Computing Infra", "Computing Infra", "Hardware Foundry",
            "Hardware Foundry", "Algorithm Dev", "Algorithm Dev", "Industrial End-User",
            "Industrial End-User", "Industrial End-User", "System Integration", "System Integration",
            "Legal & Capital", "Legal & Capital"
        ],
        "Tech_Stack": [
            "Hybrid HPC+QC", "Hybrid HPC+QC", "Hybrid HPC+QC", "Superconducting",
            "Trapped-ion", "Quantum AI (QML)", "Hybrid HPC+QC", "Hybrid HPC+QC",
            "Quantum Security (QKD/PQC)", "Quantum AI (QML)", "Quantum Security (QKD/PQC)", "Hybrid HPC+QC",
            "Quantum Security (QKD/PQC)", "Quantum Security (QKD/PQC)"
        ],
        "Geography": [
            "EU HQ", "Italy", "France", "US Bridge", 
            "Germany", "US Bridge", "Italy", "Italy", 
            "Italy", "Italy", "Italy", "Italy", 
            "Italy", "Italy"
        ],
        "Organization": [
            "European Commission JRC", "Politecnico di Milano / ICSC", "GENCI", "Rigetti Computing",
            "Qudora Technologies", "NASA QuAIL / USRA", "Classiq Technologies", "Leonardo Group",
            "Thales Alenia Space Italia", "Credem Banca", "Accenture", "NTT DATA",
            "The Innovation Group (TIG)", "Italian Tech Alliance"
        ],
        "Readiness_Score": [4, 3, 3, 2, 1, 2, 4, 3, 3, 2, 4, 3, 4, 4]
    }
    return pd.DataFrame(data)

df = load_data()

# 3. Sidebar Layout - Complex Filters (The Data Scientist Standard)
st.sidebar.title("🛰️ Navigation & Filters")
st.sidebar.markdown("---")

# Filter 1: Geography
all_countries = sorted(df["Geography"].unique())
selected_countries = st.sidebar.multiselect("🌍 Select Geography / Hubs", all_countries, default=all_countries)

# Filter 2: Ecosystem Role
all_roles = sorted(df["Role"].unique())
selected_roles = st.sidebar.multiselect("🧬 Select Ecosystem Pillars", all_roles, default=all_roles)

# Filter 3: Tech Stack
all_tech = sorted(df["Tech_Stack"].unique())
selected_tech = st.sidebar.multiselect("💻 Select Tech Stack Layer", all_tech, default=all_tech)

# Filter 4: Readiness Score Slider
min_score, max_score = int(df["Readiness_Score"].min()), int(df["Readiness_Score"].max())
selected_readiness = st.sidebar.slider("🌟 Tech Readiness Score (NISQ)", min_score, max_score, (min_score, max_score))

# Apply Filters to Main Dataframe
filtered_df = df[
    (df["Geography"].isin(selected_countries)) &
    (df["Role"].isin(selected_roles)) &
    (df["Tech_Stack"].isin(selected_tech)) &
    (df["Readiness_Score"].between(selected_readiness[0], selected_readiness[1]))
]

# 4. Main Dashboard Layout
st.title("EuroQ-Radar v2.0")
st.markdown("### *European Quantum-AI Ecosystem Radar: The Live Interactive Database*")
st.markdown("---")

# Top Level KPI Metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Tracked Pioneers", len(filtered_df))
with col2:
    st.metric("Active Strategic Hubs", len(filtered_df["Geography"].unique()))
with col3:
    st.metric("Average Readiness Score", round(filtered_df["Readiness_Score"].mean(), 2) if len(filtered_df)>0 else 0)

st.markdown("---")

# Visualizations Row
vis_col1, vis_col2 = st.columns([1, 1])

with vis_col1:
    st.markdown("#### 🗺️ Ecosystem Radar Vector")
    if not filtered_df.empty:
        # Aggregating readiness scores by role for the Radar View
        radar_df = filtered_df.groupby("Role")["Readiness_Score"].mean().reset_index()
        fig_radar = gw.Figure()
        fig_radar.add_trace(gw.Scatterpolar(
            r=radar_df["Readiness_Score"],
            theta=radar_df["Role"],
            fill='toself',
            line_color='#00f2fe'
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
            showlegend=False,
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_radar, use_container_width=True)
    else:
        st.warning("No data available for the current filter selection.")

with vis_col2:
    st.markdown("#### 📊 Tech Stack Concentration")
    if not filtered_df.empty:
        fig_bar = px.bar(
            filtered_df, 
            x="Tech_Stack", 
            y="Readiness_Score", 
            color="Role",
            hover_data=["Name", "Organization"],
            title="Readiness Distribution across Tech Stack",
            template="plotly_dark"
        )
        fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.warning("No data available for the current filter selection.")

st.markdown("---")

# 5. The Dynamic Data Matrix Table
st.markdown("#### 📑 Query Results: Filtered Ecosystem Nodes")
st.dataframe(
    filtered_df.sort_values(by="Readiness_Score", ascending=False),
    column_config={
        "Name": st.column_config.TextColumn("Pioneer Name"),
        "Role": st.column_config.TextColumn("Ecosystem Pillar"),
        "Tech_Stack": st.column_config.TextColumn("Tech Stack Details"),
        "Readiness_Score": st.column_config.NumberColumn("Readiness (1-5) 🌟")
    },
    use_container_width=True,
    hide_index=True
)

st.markdown("---")
st.caption("EuroQ-Radar v2.0 • Open-Source Deep-Tech Database Hub • MIT License")
