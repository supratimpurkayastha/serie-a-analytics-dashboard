import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st

# 1. Page Configuration
st.set_page_config(
    page_title="Serie A Dynamic Analytics Hub", page_icon="⚽", layout="wide"
)

st.title("⚽ Serie A 2025–2026 Interactive Analytics Hub")
st.markdown(
    "Select a stat category and specific metric from the dropdowns below to explore league insights."
)


# 2. Load & Preprocess Data
@st.cache_data
def load_data():
    df = pd.read_csv("I1.csv")

    def get_home_points(row):
        return (
            3
            if row["FTHG"] > row["FTAG"]
            else (1 if row["FTHG"] == row["FTAG"] else 0)
        )

    def get_away_points(row):
        return (
            3
            if row["FTAG"] > row["FTHG"]
            else (1 if row["FTHG"] == row["FTAG"] else 0)
        )

    df["HomePoints"] = df.apply(get_home_points, axis=1)
    df["AwayPoints"] = df.apply(get_away_points, axis=1)
    return df


df = load_data()

# Pre-calculations for League Summary
home_goals = df.groupby("HomeTeam")["FTHG"].sum()
away_goals = df.groupby("AwayTeam")["FTAG"].sum()
total_goals = home_goals + away_goals

home_conceded = df.groupby("HomeTeam")["FTAG"].sum()
away_conceded = df.groupby("AwayTeam")["FTHG"].sum()
total_conceded = home_conceded + away_conceded

home_pts = df.groupby("HomeTeam")["HomePoints"].sum()
away_pts = df.groupby("AwayTeam")["AwayPoints"].sum()
total_points = home_pts + away_pts

home_shots = df.groupby("HomeTeam")["HS"].sum()
away_shots = df.groupby("AwayTeam")["AS"].sum()
total_shots = home_shots + away_shots

home_shots_target = df.groupby("HomeTeam")["HST"].sum()
away_shots_target = df.groupby("AwayTeam")["AST"].sum()
total_shots_target = home_shots_target + away_shots_target

# --- DROPDOWN CONTROL CENTER ---
st.subheader("🛠️ Data Selector Controls")
col_cat, col_metric = st.columns(2)

with col_cat:
    category = st.selectbox(
        "Choose Analysis Category:",
        [
            "Goals & Scoring Stats",
            "Shots & Efficiency",
            "Home vs Away Performance",
            "Tactical & Match Dynamics",
            "Individual Club Inspection",
        ],
    )

with col_metric:
    if category == "Goals & Scoring Stats":
        stat_choice = st.selectbox(
            "Select Specific Stat View:",
            [
                "Most Goals Scored",
                "Most Goals Conceded",
                "Attack vs Defence Matrix",
            ],
        )
    elif category == "Shots & Efficiency":
        stat_choice = st.selectbox(
            "Select Specific Stat View:",
            [
                "Total Shots Leaderboard",
                "Shots on Target Leaderboard",
                "Shots on Target vs Total Points Correlation",
            ],
        )
    elif category == "Home vs Away Performance":
        stat_choice = st.selectbox(
            "Select Specific Stat View:",
            [
                "Home Points vs Away Points Comparison",
                "Largest Home Ground Advantage",
            ],
        )
    elif category == "Tactical & Match Dynamics":
        stat_choice = st.selectbox(
            "Select Specific Stat View:",
            ["Outcome When Scoring First"],
        )
    elif category == "Individual Club Inspection":
        stat_choice = st.selectbox(
            "Select Team to Inspect:",
            sorted(df["HomeTeam"].unique()),
        )

st.divider()

# --- RENDER SELECTED STAT VIEW ---

# 1. GOALS & SCORING MODULE
if category == "Goals & Scoring Stats":
    team_stats = pd.DataFrame(
        {
            "Team": total_goals.index,
            "Goals Scored": total_goals.values,
            "Goals Conceded": total_conceded.values,
        }
    )

    if stat_choice == "Most Goals Scored":
        st.header("⚽ Most Goals Scored by Team")
        sorted_df = team_stats.sort_values(
            by="Goals Scored", ascending=False
        )
        fig = px.bar(
            sorted_df,
            x="Team",
            y="Goals Scored",
            text="Goals Scored",
            color="Goals Scored",
            color_continuous_scale="Viridis",
            title="Total League Goals Scored",
        )
        st.plotly_chart(fig, use_container_width=True)

    elif stat_choice == "Most Goals Conceded":
        st.header("🛡️ Most Goals Conceded (Leakiest Defences)")
        sorted_df = team_stats.sort_values(
            by="Goals Conceded", ascending=False
        )
        fig = px.bar(
            sorted_df,
            x="Team",
            y="Goals Conceded",
            text="Goals Conceded",
            color="Goals Conceded",
            color_continuous_scale="Reds",
            title="Total League Goals Conceded",
        )
        st.plotly_chart(fig, use_container_width=True)

    elif stat_choice == "Attack vs Defence Matrix":
        st.header("🎯 Attack vs Defence Quadrant Matrix")
        fig = px.scatter(
            team_stats,
            x="Goals Scored",
            y="Goals Conceded",
            text="Team",
            title="Goals Scored vs Goals Conceded Matrix",
            hover_data=["Goals Scored", "Goals Conceded"],
        )
        fig.update_yaxes(autorange="reversed")
        fig.update_traces(
            textposition="top center", marker=dict(size=12, color="crimson")
        )
        st.plotly_chart(fig, use_container_width=True)

# 2. SHOTS & EFFICIENCY MODULE
elif category == "Shots & Efficiency":
    shots_df = pd.DataFrame(
        {
            "Team": total_shots.index,
            "Total Shots": total_shots.values,
            "Shots on Target": total_shots_target.values,
            "Total Points": total_points.values,
        }
    )

    if stat_choice == "Total Shots Leaderboard":
        st.header("🎯 Total Shots Attempted")
        sorted_df = shots_df.sort_values(by="Total Shots", ascending=False)
        fig = px.bar(
            sorted_df,
            x="Team",
            y="Total Shots",
            text="Total Shots",
            color="Total Shots",
            color_continuous_scale="Blues",
        )
        st.plotly_chart(fig, use_container_width=True)

    elif stat_choice == "Shots on Target Leaderboard":
        st.header("🔥 Shots on Target Leaderboard")
        sorted_df = shots_df.sort_values(
            by="Shots on Target", ascending=False
        )
        fig = px.bar(
            sorted_df,
            x="Team",
            y="Shots on Target",
            text="Shots on Target",
            color="Shots on Target",
            color_continuous_scale="Plasma",
        )
        st.plotly_chart(fig, use_container_width=True)

    elif stat_choice == "Shots on Target vs Total Points Correlation":
        st.header("📊 Shots on Target vs Total Points Correlation")
        fig, ax = plt.subplots(figsize=(10, 5))
        sns.regplot(
            data=shots_df,
            x="Shots on Target",
            y="Total Points",
            color="crimson",
            ax=ax,
        )
        for i, row in shots_df.iterrows():
            ax.text(
                row["Shots on Target"] + 0.8,
                row["Total Points"],
                row["Team"],
                fontsize=9,
            )
        ax.set_title("Correlation: Accuracy vs Points", fontweight="bold")
        ax.grid(True, linestyle="--", alpha=0.5)
        st.pyplot(fig)

# 3. HOME VS AWAY MODULE
elif category == "Home vs Away Performance":
    ha_df = pd.DataFrame(
        {
            "Team": home_pts.index,
            "Home Points": home_pts.values,
            "Away Points": away_pts.values,
            "Home Advantage Diff": home_pts.values - away_pts.values,
        }
    )

    if stat_choice == "Home Points vs Away Points Comparison":
        st.header("🏟️ Home vs Away Points Side-by-Side")
        fig = px.bar(
            ha_df,
            x="Team",
            y=["Home Points", "Away Points"],
            barmode="group",
            title="Home Points vs Away Points Split",
        )
        st.plotly_chart(fig, use_container_width=True)

    elif stat_choice == "Largest Home Ground Advantage":
        st.header("🏰 Home Soil Dominance (Home Points Minus Away Points)")
        sorted_df = ha_df.sort_values(
            by="Home Advantage Diff", ascending=False
        )
        fig = px.bar(
            sorted_df,
            x="Team",
            y="Home Advantage Diff",
            text="Home Advantage Diff",
            color="Home Advantage Diff",
            color_continuous_scale="Tealgrn",
        )
        st.plotly_chart(fig, use_container_width=True)

# 4. TACTICAL MODULE
elif category == "Tactical & Match Dynamics":
    if stat_choice == "Outcome When Scoring First":
        st.header("⏱️ Match Outcomes After Scoring First")
        first_half_goals = df[(df["HTHG"] > 0) | (df["HTAG"] > 0)].copy()

        def analyze_first_scorer_outcome(row):
            if row["HTHG"] > row["HTAG"]:
                return (
                    "Win"
                    if row["FTHG"] > row["FTAG"]
                    else ("Draw" if row["FTHG"] == row["FTAG"] else "Loss")
                )
            elif row["HTAG"] > row["HTHG"]:
                return (
                    "Win"
                    if row["FTAG"] > row["FTHG"]
                    else ("Draw" if row["FTAG"] == row["FTHG"] else "Loss")
                )
            return "Equal"

        first_half_goals["Outcome"] = first_half_goals.apply(
            analyze_first_scorer_outcome, axis=1
        )
        outcomes = first_half_goals[first_half_goals["Outcome"] != "Equal"][
            "Outcome"
        ].value_counts(normalize=True) * 100

        fig, ax = plt.subplots(figsize=(6, 6))
        outcomes.plot(
            kind="pie",
            autopct="%1.1f%%",
            colors=["#2ca02c", "#ff7f0e", "#d62728"],
            startangle=90,
            ax=ax,
        )
        ax.set_ylabel("")
        st.pyplot(fig)

# 5. INDIVIDUAL CLUB INSPECTION MODULE
elif category == "Individual Club Inspection":
    selected_team = stat_choice
    st.header(f"🔍 Detailed Analysis: {selected_team}")

    team_matches = df[
        (df["HomeTeam"] == selected_team) | (df["AwayTeam"] == selected_team)
    ].copy()

    def process_team_performance(row):
        if row["HomeTeam"] == selected_team:
            gf = row["FTHG"]
            ga = row["FTAG"]
            pts = 3 if gf > ga else (1 if gf == ga else 0)
            venue = "Home"
        else:
            gf = row["FTAG"]
            ga = row["FTHG"]
            pts = 3 if gf > ga else (1 if gf == ga else 0)
            venue = "Away"
        return pd.Series([gf, ga, pts, venue])

    team_matches[["GF", "GA", "Points", "Venue"]] = team_matches.apply(
        process_team_performance, axis=1
    )

    tot_pts = team_matches["Points"].sum()
    tot_gf = team_matches["GF"].sum()
    tot_ga = team_matches["GA"].sum()

    m1, m2, m3 = st.columns(3)
    m1.metric("Total Season Points", tot_pts)
    m2.metric("Total Goals Scored", tot_gf)
    m3.metric("Total Goals Conceded", tot_ga)

    team_matches["Matchday"] = range(1, len(team_matches) + 1)
    team_matches["Cumulative Points"] = team_matches["Points"].cumsum()

    fig = px.line(
        team_matches,
        x="Matchday",
        y="Cumulative Points",
        markers=True,
        title=f"{selected_team} Cumulative Point Trajectory",
    )
    st.plotly_chart(fig, use_container_width=True)