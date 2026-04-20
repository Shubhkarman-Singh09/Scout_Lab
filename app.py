import streamlit as st
import pandas as pd
import plotly.express as px
import os
from parser import parse_squad
from Features import engineer_features
from cluster import cluster_players
import requests
import base64
from io import BytesIO

TEAMS = {
    "── Premier League ──": ("", ""),
    "Arsenal":                      ("fc-arsenal", "11"),
    "Aston Villa":                  ("aston-villa", "405"),
    "Chelsea":                      ("fc-chelsea", "631"),
    "Everton":                      ("fc-everton", "29"),
    "Fulham":                        ("fc-fulham", "931"),
    "Liverpool":                    ("fc-liverpool", "31"),
    "Manchester City":              ("manchester-city", "281"),
    "Manchester United":            ("manchester-united", "985"),
    "Newcastle United":             ("newcastle-united", "762"),
    "Nottingham Forest":            ("nottingham-forest", "703"),
    "Tottenham Hotspur":            ("tottenham-hotspur", "148"),
    "West Ham United":              ("west-ham-united", "379"),

    "── La Liga ──": ("", ""),
    "Athletic Bilbao":              ("athletic-bilbao", "621"),
    "Atletico Madrid":              ("atletico-madrid", "13"),
    "FC Barcelona":                 ("fc-barcelona", "131"),
    "Girona FC":                    ("girona-fc", "12321"),
    "Real Betis":                   ("real-betis-balompie", "150"),
    "Real Madrid":                  ("real-madrid", "418"),
    "Real Sociedad":                ("real-sociedad", "681"),
    "Sevilla FC":                   ("fc-sevilla", "368"),
    "Valencia CF":                  ("fc-valencia", "1049"),
    "Villarreal CF":                ("villarreal-cf", "1050"),

    "── Bundesliga ──": ("", ""),
    "Bayer Leverkusen":             ("bayer-04-leverkusen", "15"),
    "Bayern Munich":                ("fc-bayern-munchen", "27"),
    "Borussia Dortmund":            ("borussia-dortmund", "16"),
    "Borussia Monchengladbach":     ("borussia-monchengladbach", "23"),
    "Eintracht Frankfurt":          ("eintracht-frankfurt", "24"),
    "Freiburg":                     ("sc-freiburg", "17"),
    "Hoffenheim":                   ("tsv-hoffenheim", "533"),
    "RB Leipzig":                   ("rb-leipzig", "23826"),
    "Stuttgart":                    ("vfb-stuttgart", "79"),
    "Wolfsburg":                    ("vfl-wolfsburg", "82"),

    "── Serie A ──": ("", ""),
    "AC Milan":                     ("ac-milan", "5"),
    "AS Roma":                      ("as-rom", "12"),
    "Atalanta":                     ("atalanta-bc", "800"),
    "Bologna":                      ("bologna-fc-1909", "1025"),
    "Fiorentina":                   ("acf-fiorentina", "430"),
    "Inter Milan":                  ("inter-mailand", "46"),
    "Juventus":                     ("juventus-fc", "506"),
    "Lazio":                        ("lazio-rom", "398"),
    "Napoli":                       ("ssc-neapel", "6195"),
    "Torino":                       ("torino-fc", "416"),

    "── Ligue 1 ──": ("", ""),
    "AS Monaco":                    ("as-monaco", "162"),
    "Lens":                         ("rc-lens", "826"),
    "Lille":                        ("losc-lille", "1082"),
    "Lyon":                         ("olympique-lyon", "1041"),
    "Marseille":                    ("olympique-marseille", "244"),
    "Nice":                         ("ogc-nice", "417"),
    "Paris Saint-Germain":          ("paris-saint-germain", "583"),
    "Rennes":                       ("stade-rennes", "363"),
    "Strasbourg":                   ("rc-strasbourg-alsace", "667"),

    "── Eredivisie ──": ("", ""),
    "Ajax":                         ("ajax-amsterdam", "610"),
    "AZ Alkmaar":                   ("az-alkmaar", "139"),
    "Feyenoord":                    ("feyenoord-rotterdam", "234"),
    "PSV Eindhoven":                ("psv-eindhoven", "383"),

    "── Primeira Liga ──": ("", ""),
    "Benfica":                      ("sl-benfica", "294"),
    "Braga":                        ("sc-braga", "1075"),
    "FC Porto":                     ("fc-porto", "720"),
    "Sporting CP":                  ("sporting-cp", "336"),

    "── Scottish Premiership ──": ("", ""),
    "Celtic":                       ("celtic-fc", "371"),
    "Rangers":                      ("rangers-fc", "1003"),

    "── Super Lig ──": ("", ""),
    "Besiktas":                     ("besiktas-jk", "114"),
    "Fenerbahce":                   ("fenerbahce-sk", "36"),
    "Galatasaray":                  ("galatasaray-sk", "141"),
    "Trabzonspor":                  ("trabzonspor", "449"),
}
@st.cache_data(show_spinner=False)
def fetch_image_bytes(url: str) -> bytes:
    try:
        r = requests.get(url, headers={
            "Referer": "https://www.transfermarkt.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }, timeout=5)
        return r.content
    except:
        return None
st.set_page_config(
    page_title="ScoutLab",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.main { background-color: #0a0f0a; }

.scout-header {
    background: linear-gradient(135deg, #0d1f0d 0%, #0a3d1f 100%);
    border: 1px solid #1a4a1a;
    border-radius: 12px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
}
.scout-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3.5rem;
    letter-spacing: 4px;
    color: #ffffff;
    line-height: 1;
    margin: 0;
}
.scout-title span { color: #00e676; }
.scout-sub {
    color: rgba(255,255,255,0.4);
    font-size: 0.75rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 0.5rem;
}

.cluster-header {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.4rem;
    letter-spacing: 3px;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    margin-bottom: 1rem;
}

.player-card {
    background: #0d1a0d;
    border: 1px solid #1a3a1a;
    border-radius: 10px;
    padding: 1rem;
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    transition: border-color 0.2s;
}
.player-card:hover { border-color: #00e676; }

.player-name {
    font-weight: 500;
    font-size: 0.95rem;
    color: #ffffff;
    margin: 0;
}
.player-meta {
    font-size: 0.75rem;
    color: rgba(255,255,255,0.4);
    margin: 0;
}

.pos-badge {
    font-size: 0.65rem;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 4px;
    letter-spacing: 1px;
    text-transform: uppercase;
}

.value-tag {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.1rem;
    letter-spacing: 1px;
    color: #00e676;
}

.metric-card {
    background: #0d1a0d;
    border: 1px solid #1a3a1a;
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    text-align: center;
}
.metric-value {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.2rem;
    color: #00e676;
    letter-spacing: 2px;
    line-height: 1;
}
.metric-label {
    font-size: 0.7rem;
    color: rgba(255,255,255,0.4);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 0.25rem;
}

section[data-testid="stSidebar"] {
    background: #060f06;
    border-right: 1px solid #1a3a1a;
}
</style>
""", unsafe_allow_html=True)

CLUSTER_COLORS = {
    "High Value Youth": "#00e676",
    "Attack Core":      "#ff6b35",
    "Reliable Squad":   "#4fc3f7",
    "Veteran Depth":    "#9e9e9e"
}

POS_COLORS = {
    "Goalkeeper":         "#4fc3f7",
    "Centre-Back":        "#00e676",
    "Left-Back":          "#00c853",
    "Right-Back":         "#00c853",
    "Defensive Midfield": "#ff6b35",
    "Central Midfield":   "#ff8c42",
    "Attacking Midfield": "#ff9800",
    "Left Winger":        "#ef5350",
    "Right Winger":       "#ef5350",
    "Second Striker":     "#e53935",
    "Centre-Forward":     "#b71c1c",
}

with st.sidebar:
    st.markdown("### ⚽ ScoutLab Settings")
    st.markdown("---")
    valid_teams = {k: v for k, v in TEAMS.items() if v[1] != ""}
    dividers    = {k for k, v in TEAMS.items() if v[1] == ""}

    team_name = st.selectbox(
    "Select Team",
    list(TEAMS.keys()),
    format_func=lambda x: x if x not in dividers else x,
)

    if TEAMS[team_name][1] == "":
        st.warning("Please select a team.")
        st.stop()

    team_slug, team_id = TEAMS[team_name]
    k=4
    age_range = st.slider(
    "Filter by Age",
    min_value=15,
    max_value=45,
    value=(15, 45)
)    
    st.markdown("---")
    pos_filter = st.multiselect(
        "Filter by Position",
        ["Goalkeeper", "Centre-Back", "Left-Back", "Right-Back",
         "Defensive Midfield", "Central Midfield", "Attacking Midfield",
         "Left Winger", "Right Winger", "Second Striker", "Centre-Forward"],
        default=[]
    )
    st.markdown("---")
    run = st.button("🔍 Analyse Squad", use_container_width=True)


st.markdown("""
<div class="scout-header">
    <div class="scout-title">Scout<span>Lab</span></div>
    <div class="scout-sub">Player Intelligence Platform · Powered by Transfermarkt Data · KMeans Clustering</div>
</div>
""", unsafe_allow_html=True)

if not run:
    st.info("Enter a team slug and ID in the sidebar, then click Analyse Squad.")
    st.stop()

cache_path = f"data/{team_id}.html"
with st.spinner("Fetching squad data..."):
    if not os.path.exists(cache_path):
        from scraper import fetch_squad
        html = fetch_squad(team_id, team_slug)
        with open(cache_path, "w", encoding="utf-8") as f:
            f.write(html)
    else:
        with open(cache_path, "r", encoding="utf-8") as f:
            html = f.read()

df = cluster_players(engineer_features(parse_squad(html)), k=k)

total     = len(df)
avg_age   = df["Age"].mean()
avg_val   = df["Market Value_m"].mean()
top_val   = df["Market Value_m"].max()
top_name  = df.loc[df["Market Value_m"].idxmax(), "Name"]

if pos_filter:
    df = df[df["Position"].isin(pos_filter)]

df = df[(df["Age"] >= age_range[0]) & (df["Age"] <= age_range[1])]

if df.empty:
    st.warning("No players match the current filters.")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{total}</div>
        <div class="metric-label">Squad Size</div>
    </div>""", unsafe_allow_html=True)
with c2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{avg_age:.1f}</div>
        <div class="metric-label">Average Age</div>
    </div>""", unsafe_allow_html=True)
with c3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">€{avg_val:.1f}M</div>
        <div class="metric-label">Avg Market Value</div>
    </div>""", unsafe_allow_html=True)
with c4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">€{top_val:.0f}M</div>
        <div class="metric-label">Top Value · {top_name}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Charts Row ────────────────────────────────────────────────
col_l, col_r = st.columns(2)

with col_l:
    st.markdown("##### Age vs Market Value")
    fig = px.scatter(
        df, x="Age", y="Market Value_m",
        color="cluster_label",
        hover_name="Name",
        size="Market Value_m",
        color_discrete_map=CLUSTER_COLORS,
        labels={"Market Value_m": "Market Value (€M)"}
    )
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0d1a0d",
        plot_bgcolor="#0d1a0d",
        legend_title="Cluster",
        margin=dict(l=0, r=0, t=10, b=0),
        height=320
    )
    st.plotly_chart(fig, use_container_width=True)

with col_r:
    st.markdown("##### Cluster Distribution by Position")
    counts = df.groupby(["Position", "cluster_label"]).size().reset_index(name="count")
    fig2 = px.bar(
        counts, x="Position", y="count",
        color="cluster_label",
        color_discrete_map=CLUSTER_COLORS,
        barmode="stack"
    )
    fig2.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0d1a0d",
        plot_bgcolor="#0d1a0d",
        legend_title="Cluster",
        margin=dict(l=0, r=0, t=10, b=0),
        height=320,
        xaxis_tickangle=-35
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Player Cards by Cluster ───────────────────────────────────
st.markdown("##### Squad by Cluster")

clusters = df["cluster_label"].unique()
cols = st.columns(len(clusters))

for col, cluster_name in zip(cols, clusters):
    color = CLUSTER_COLORS.get(cluster_name, "#ffffff")
    cluster_df = df[df["cluster_label"] == cluster_name].sort_values("Market Value_m", ascending=False)

    with col:
        st.markdown(f"""
        <div class="cluster-header" style="background:{color}22;color:{color};border:1px solid {color}44;">
            {cluster_name.upper()}
            <span style="float:right;font-size:0.9rem;">{len(cluster_df)}</span>
        </div>""", unsafe_allow_html=True)

    for _, player in cluster_df.iterrows():
        pos   = player["Position"]
        pc    = POS_COLORS.get(pos, "#888")
        photo = player.get("photo", "")

        col_img, col_info = st.columns([1, 4])

        with col_img:
            img_bytes = fetch_image_bytes(photo)
            if img_bytes:
                st.image(img_bytes, width=55)
            else:
                st.markdown("""
        <div style="width:55px;height:55px;border-radius:50%;
        background:#1a3a1a;display:flex;align-items:center;
        justify-content:center;font-size:20px;">👤</div>
        """, unsafe_allow_html=True)

        with col_info:
            st.markdown(f"""
            <div style="padding:4px 0;">
            <p class="player-name">{player['Name']}</p>
            <p class="player-meta">{pos} · Age {int(player['Age'])}</p>
            <span class="pos-badge" style="background:{pc}22;color:{pc};">
                {pos[:3].upper()}
            </span>
        </div>
        <div class="value-tag">€{player['Market Value_m']:.0f}M</div>
        """, unsafe_allow_html=True)

        st.markdown("<hr style='border:0.5px solid #1a3a1a;margin:4px 0;'>", unsafe_allow_html=True) 

# ── Raw Data Table ────────────────────────────────────────────
with st.expander("📋 Full Squad Data"):
    st.dataframe(
        df[["Name", "Position", "Age", "Market Value_m", "Contract", "cluster_label"]],
        use_container_width=True
    )