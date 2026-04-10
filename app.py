import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.graph_objects as go
import plotly.express as px
import requests
import json
import math

# ─────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────
st.set_page_config(
    page_title="🌍 Dunyo Inson Kapitali",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────
# CUSTOM CSS  — dark luxury theme
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Syne', sans-serif !important;
    background-color: #06090f !important;
    color: #c8d8f0 !important;
}
.stApp { background: #06090f; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0b1120 !important;
    border-right: 1px solid #1a2540 !important;
}
[data-testid="stSidebar"] * { color: #c8d8f0 !important; }

/* ── Header ── */
.hero-header {
    background: linear-gradient(135deg, #0d1e3a 0%, #060d1a 60%, #0a1a10 100%);
    border: 1px solid #1a2540;
    border-radius: 16px;
    padding: 36px 40px 28px;
    margin-bottom: 28px;
    position: relative;
    overflow: hidden;
}
.hero-header::before {
    content: '';
    position: absolute;
    top: -60px; right: -60px;
    width: 300px; height: 300px;
    background: radial-gradient(circle, rgba(0,229,255,0.08) 0%, transparent 70%);
    pointer-events: none;
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 800;
    line-height: 1.1;
    margin: 0 0 8px;
    background: linear-gradient(90deg, #00e5ff, #00ff9d);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: #4a7090;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* ── KPI cards ── */
.kpi-card {
    background: #0d1420;
    border: 1px solid #1a2540;
    border-radius: 14px;
    padding: 22px 20px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: border-color 0.3s;
}
.kpi-card:hover { border-color: #00e5ff44; }
.kpi-card::after {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: var(--accent, #00e5ff);
}
.kpi-number {
    font-size: 2.0rem;
    font-weight: 800;
    color: var(--accent, #00e5ff);
    line-height: 1;
    margin-bottom: 4px;
    font-family: 'JetBrains Mono', monospace;
}
.kpi-label {
    font-size: 0.72rem;
    color: #4a6080;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}
.kpi-icon { font-size: 1.6rem; margin-bottom: 8px; }

/* ── Section title ── */
.section-title {
    font-size: 0.75rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 2px;
    color: #4a7090;
    font-family: 'JetBrains Mono', monospace;
    border-left: 3px solid #00e5ff;
    padding-left: 10px;
    margin: 24px 0 14px;
}

/* ── Tabs override ── */
.stTabs [data-baseweb="tab-list"] {
    background: #0b1120;
    border-radius: 10px;
    padding: 4px;
    gap: 4px;
    border: 1px solid #1a2540;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #4a6080;
    border-radius: 7px;
    font-family: 'Syne', sans-serif;
    font-weight: 600;
    padding: 10px 20px;
}
.stTabs [aria-selected="true"] {
    background: #00e5ff !important;
    color: #000 !important;
}

/* ── Dataframe ── */
.stDataFrame { border-radius: 10px; overflow: hidden; }

/* ── Selectbox / slider ── */
.stSelectbox > div > div,
.stMultiSelect > div > div {
    background: #0d1420 !important;
    border: 1px solid #1a2540 !important;
    border-radius: 8px !important;
    color: #c8d8f0 !important;
}

/* ── Metric delta ── */
[data-testid="stMetricDelta"] { color: #00ff9d !important; }

/* ── Chart containers ── */
.chart-wrap {
    background: #0d1420;
    border: 1px solid #1a2540;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 20px;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: #06090f; }
::-webkit-scrollbar-thumb { background: #1a2540; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# DATA — Dunyo mehnat bozori statistikasi
# (ILO, UNESCO, World Bank, OECD 2023-2024)
# ─────────────────────────────────────────
COUNTRIES = [
    # name, lat, lon, flag,
    # it_workers(000), teachers(000), engineers(000),
    # doctors(000), researchers(000), students_mln,
    # literacy_pct, gdp_trillion, population_mln, region
    ("🇺🇸 AQSh",         37.09, -95.71, "🇺🇸",  4800, 3200, 5100, 1100,  890, 20.3, 99.0, 25.5, 335,  "Amerika"),
    ("🇨🇳 Xitoy",         35.86, 104.19, "🇨🇳",  8500, 12000,9300, 3600, 1700, 44.0, 97.0, 18.5, 1410, "Osiyo"),
    ("🇮🇳 Hindiston",     20.59,  78.96, "🇮🇳",  5400, 8700, 5600, 1200,  550, 38.5, 77.7,  3.9, 1430, "Osiyo"),
    ("🇩🇪 Germaniya",     51.16,  10.45, "🇩🇪",  1050,  840,  970,  420,  340,  2.9, 99.0,  4.5,   84, "Yevropa"),
    ("🇬🇧 Britaniya",     55.37,  -3.43, "🇬🇧",   920,  680,  730,  310,  290,  2.8, 99.0,  3.1,   67, "Yevropa"),
    ("🇫🇷 Fransiya",      46.22,   2.21, "🇫🇷",   760,  880,  640,  290,  280,  2.5, 99.0,  3.0,   68, "Yevropa"),
    ("🇯🇵 Yaponiya",      36.20, 138.25, "🇯🇵",  1380, 1060, 1200,  320,  680,  2.9, 99.0,  4.2,  125, "Osiyo"),
    ("🇰🇷 Janubiy Koreya",35.90, 127.76, "🇰🇷",   950,  430,  870,  100,  400,  3.3, 99.0,  1.7,   52, "Osiyo"),
    ("🇷🇺 Rossiya",       61.52,  105.3, "🇷🇺",  1250, 1600, 1400,  700,  430,  8.2, 99.7,  1.8,  143, "Yevropa"),
    ("🇧🇷 Braziliya",    -14.23, -51.92, "🇧🇷",   900, 2200,  670,  380,  180, 11.6, 94.2,  2.1,  215, "Amerika"),
    ("🇨🇦 Kanada",        56.13, -106.3, "🇨🇦",   750,  480,  590,  110,  190,  2.1, 99.0,  2.1,   38, "Amerika"),
    ("🇦🇺 Avstraliya",   -25.27,  133.7, "🇦🇺",   560,  320,  430,  100,  210,  1.5, 99.0,  1.7,   26, "Osiyo"),
    ("🇸🇦 Saudiya Arab.", 23.88,   45.07,"🇸🇦",   280,  330,  250,   80,   55,  1.8, 99.0,  1.0,   35, "Yaqin Sharq"),
    ("🇵🇰 Pokiston",      30.37,   69.34,"🇵🇰",   220, 1400,  190,   80,   30, 10.2, 59.1,  0.4,  231, "Osiyo"),
    ("🇳🇬 Nigeriya",       9.08,    8.67,"🇳🇬",   115, 1100,   90,   35,   15,  9.8, 62.0,  0.5,  220, "Afrika"),
    ("🇿🇦 J.Afrika",     -30.55,   22.93,"🇿🇦",   180,  400,  160,   50,   45,  2.1, 95.0,  0.4,   60, "Afrika"),
    ("🇪🇬 Misr",          26.82,   30.80,"🇪🇬",   165,  900,  150,   90,   30,  7.2, 73.1,  0.5,  105, "Afrika"),
    ("🇮🇩 Indoneziya",    -0.78,  113.92,"🇮🇩",   600, 3000,  430,  180,   55, 14.5, 96.0,  1.4,  278, "Osiyo"),
    ("🇲🇽 Meksika",       23.63,  -102.5,"🇲🇽",   480,  900,  370,  130,   60,  5.5, 95.0,  1.3,  130, "Amerika"),
    ("🇦🇷 Argentina",    -38.41,  -63.61,"🇦🇷",   160,  520,  170,   60,   35,  2.8, 99.0,  0.6,   45, "Amerika"),
    ("🇹🇷 Turkiya",       38.96,   35.24,"🇹🇷",   320,  820,  310,  120,   60,  4.8, 96.7,  1.1,   85, "Yevropa"),
    ("🇮🇷 Eron",          32.42,   53.68,"🇮🇷",   280,  900,  350,  130,   65,  4.3, 88.7,  0.4,   88, "Yaqin Sharq"),
    ("🇸🇪 Shvetsiya",     60.12,   18.64,"🇸🇪",   200,  180,  190,   40,  100,  0.5, 99.0,  0.6,   10, "Yevropa"),
    ("🇳🇱 Niderlandiya",  52.13,    5.29,"🇳🇱",   260,  210,  220,   55,  115,  0.8, 99.0,  1.0,   18, "Yevropa"),
    ("🇸🇬 Singapur",       1.35,  103.82,"🇸🇬",   200,   33,  155,   14,   50,  0.2, 97.5,  0.5,    6, "Osiyo"),
    ("🇦🇪 BAA",           23.42,   53.84,"🇦🇪",   190,   95,  140,   25,   20,  0.3, 93.8,  0.5,   10, "Yaqin Sharq"),
    ("🇮🇱 Isroil",        31.04,   34.85,"🇮🇱",   350,   95,  200,   30,   85,  0.4, 97.8,  0.5,    9, "Yaqin Sharq"),
    ("🇵🇱 Polsha",        51.91,   19.14,"🇵🇱",   340,  490,  300,   90,   55,  2.2, 99.8,  0.7,   38, "Yevropa"),
    ("🇺🇿 O'zbekiston",   41.37,   64.58,"🇺🇿",    65,  430,   95,   55,   18,  3.4, 99.9,  0.1,   37, "Osiyo"),
    ("🇰🇿 Qozog'iston",   48.01,   66.92,"🇰🇿",    90,  260,  120,   40,   22,  0.8, 99.8,  0.2,   19, "Osiyo"),
    ("🇦🇿 Ozarbayjon",    40.14,   47.57,"🇦🇿",    40,  160,   55,   30,   12,  0.4, 99.8,  0.07,  10, "Osiyo"),
    ("🇫🇮 Finlandiya",    61.92,   25.74,"🇫🇮",   120,  120,  115,   20,   70,  0.3, 99.0,  0.3,    6, "Yevropa"),
    ("🇨🇭 Shveytsariya",  46.81,    8.22,"🇨🇭",   210,  120,  170,   40,  120,  0.3, 99.0,  0.8,    9, "Yevropa"),
    ("🇵🇹 Portugaliya",   39.39,   -8.22,"🇵🇹",   110,  150,  100,   45,   45,  0.4, 95.9,  0.3,   10, "Yevropa"),
    ("🇬🇷 Gretsiya",      39.07,   21.82,"🇬🇷",    90,  120,   80,   60,   30,  0.4, 97.9,  0.2,   10, "Yevropa"),
]

COLS = [
    "name","lat","lon","flag",
    "it_workers","teachers","engineers",
    "doctors","researchers","students_mln",
    "literacy_pct","gdp_trillion","population_mln","region"
]
df = pd.DataFrame(COUNTRIES, columns=COLS)

# Derived columns
df["it_per_1k"]      = (df["it_workers"]   / df["population_mln"] * 1000).round(1)
df["teacher_per_1k"] = (df["teachers"]     / df["population_mln"] * 1000).round(1)
df["doctor_per_1k"]  = (df["doctors"]      / df["population_mln"] * 1000).round(1)
df["researcher_per_1k"]= (df["researchers"]/ df["population_mln"] * 1000).round(1)
df["stem_index"]     = (
    df["it_workers"] * 0.35 +
    df["engineers"]  * 0.30 +
    df["researchers"]* 0.35
) / df["population_mln"]
df["stem_index"]     = (df["stem_index"] / df["stem_index"].max() * 100).round(1)

# ─────────────────────────────────────────
# PLOTLY THEME
# ─────────────────────────────────────────
PLOTLY_BG   = "#0d1420"
PLOTLY_GRID = "#1a2540"
PLOTLY_TEXT = "#c8d8f0"

def base_layout(**kwargs):
    defaults = dict(
        paper_bgcolor=PLOTLY_BG,
        plot_bgcolor=PLOTLY_BG,
        font=dict(family="Syne, sans-serif", color=PLOTLY_TEXT, size=12),
        margin=dict(l=10, r=10, t=40, b=10),
    )
    defaults.update(kwargs)
    return defaults

PALETTE = [
    "#00e5ff","#00ff9d","#ffa500","#bf5af2",
    "#ff4560","#ffdd00","#ff6eb4","#7fff00",
    "#40e0d0","#ff7f50","#a78bfa","#34d399",
]

# ─────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:12px 0 20px'>
      <div style='font-size:2rem'>🌍</div>
      <div style='font-size:1rem;font-weight:800;color:#00e5ff'>Dunyo Inson Kapitali</div>
      <div style='font-size:0.68rem;color:#4a6080;font-family:JetBrains Mono,monospace'>GLOBAL HUMAN CAPITAL INDEX</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### 🔍 Filtr")
    regions = ["Barchasi"] + sorted(df["region"].unique().tolist())
    sel_region = st.selectbox("Mintaqa", regions)

    metric_map = {
        "IT mutaxassislar": "it_workers",
        "O'qituvchilar":    "teachers",
        "Muhandislar":      "engineers",
        "Shifokorlar":      "doctors",
        "Tadqiqotchilar":   "researchers",
        "STEM indeksi":     "stem_index",
        "Savodxonlik %":    "literacy_pct",
    }
    sel_metric_label = st.selectbox("Asosiy metrika", list(metric_map.keys()))
    sel_metric       = metric_map[sel_metric_label]

    top_n = st.slider("Top N davlat", 5, len(df), 15)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.7rem;color:#4a6080;font-family:JetBrains Mono,monospace;line-height:1.8'>
    📡 Ma'lumot manbalari:<br>
    • ILO Labour Statistics 2024<br>
    • UNESCO Institute for Statistics<br>
    • World Bank Open Data<br>
    • OECD Education at a Glance<br>
    • WHO Global Health Observatory
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# FILTER
# ─────────────────────────────────────────
dff = df if sel_region == "Barchasi" else df[df["region"] == sel_region]
dff_sorted = dff.nlargest(top_n, sel_metric)

# ─────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────
st.markdown(f"""
<div class="hero-header">
  <div class="hero-title">🌍 Dunyo Inson Kapitali Atlasi</div>
  <div class="hero-sub">
    {len(df)} davlat · {df['population_mln'].sum():.0f}M+ aholi · ILO · UNESCO · World Bank · 2024
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────
k1, k2, k3, k4, k5, k6 = st.columns(6)

def kpi(col, icon, number, label, color):
    col.markdown(f"""
    <div class="kpi-card" style="--accent:{color}">
      <div class="kpi-icon">{icon}</div>
      <div class="kpi-number">{number}</div>
      <div class="kpi-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)

kpi(k1, "💻", f"{df['it_workers'].sum()/1000:.0f}M", "IT mutaxassis", "#00e5ff")
kpi(k2, "📚", f"{df['teachers'].sum()/1000:.0f}M",   "O'qituvchi",   "#00ff9d")
kpi(k3, "⚙️", f"{df['engineers'].sum()/1000:.0f}M",  "Muhandis",     "#ffa500")
kpi(k4, "🩺", f"{df['doctors'].sum()/1000:.0f}M",    "Shifokor",     "#ff4560")
kpi(k5, "🔬", f"{df['researchers'].sum()/1000:.0f}M","Tadqiqotchi",  "#bf5af2")
kpi(k6, "🎓", f"{df['students_mln'].sum():.0f}M",    "Talaba",       "#ffdd00")

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────
# TABS
# ─────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🗺️ Xarita",
    "📊 Reytinglar",
    "🔬 Tahlil",
    "🌐 Mintaqalar",
    "📋 Ma'lumotlar",
])

# ══════════════════════════════════════════
# TAB 1 — XARITA
# ══════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-title">Interaktiv Dunyo Xaritasi</div>', unsafe_allow_html=True)

    map_metric = st.selectbox(
        "Xarita metrikasi",
        list(metric_map.keys()),
        index=list(metric_map.keys()).index(sel_metric_label),
        key="map_metric"
    )
    mm = metric_map[map_metric]

    map_df = dff.copy()
    map_df["value"]  = map_df[mm]
    map_df["radius"] = map_df["value"].apply(
        lambda v: max(math.sqrt(abs(v)) * 3000, 80000) if pd.notna(v) else 80000
    )
    # Color gradient: low=blue → high=cyan/green
    vmin, vmax = map_df["value"].min(), map_df["value"].max()
    def val_to_rgb(v):
        if pd.isna(v) or vmax == vmin: return [30, 80, 140, 160]
        t = (v - vmin) / (vmax - vmin)
        r = int(0   + t * 0)
        g = int(100 + t * 155)
        b = int(200 - t * 50)
        a = int(120 + t * 120)
        return [r, g, b, a]

    map_df["color"] = map_df["value"].apply(val_to_rgb)
    map_df["label"] = map_df.apply(
        lambda r: f"{r['flag']} {r['name'].split(' ',1)[-1]}: {r['value']:,.0f}", axis=1
    )

    scatter_layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_df,
        get_position=["lon","lat"],
        get_radius="radius",
        get_fill_color="color",
        pickable=True,
        auto_highlight=True,
    )

    hex_layer = pdk.Layer(
        "HexagonLayer",
        data=map_df,
        get_position=["lon","lat"],
        radius=400000,
        elevation_scale=4000,
        elevation_range=[0, 3000],
        get_elevation="value",
        extruded=True,
        coverage=0.9,
        opacity=0.25,
        get_color_range=[
            [0, 50, 120, 80],
            [0, 180, 255, 160],
        ],
    )

    tooltip = {
        "html": """
        <div style='font-family:Syne,sans-serif;background:#0d1420;border:1px solid #00e5ff;
                    border-radius:10px;padding:14px 18px;min-width:200px'>
          <div style='font-size:1.1rem;font-weight:800;color:#00e5ff;margin-bottom:6px'>{label}</div>
          <div style='font-size:0.8rem;color:#8aa8c0'>
            👥 Aholi: {population_mln}M<br>
            💻 IT: {it_workers}K<br>
            📚 O'qituvchi: {teachers}K<br>
            🔬 Tadqiqotchi: {researchers}K<br>
            📖 Savodxonlik: {literacy_pct}%
          </div>
        </div>""",
        "style": {"backgroundColor": "transparent", "padding": "0"},
    }

    view = pdk.ViewState(latitude=25, longitude=15, zoom=1.4, pitch=30)

    col_map, col_legend = st.columns([4,1])
    with col_map:
        st.pydeck_chart(pdk.Deck(
            layers=[hex_layer, scatter_layer],
            initial_view_state=view,
            tooltip=tooltip,
            map_style="mapbox://styles/mapbox/dark-v10",
        ), use_container_width=True, height=500)

    with col_legend:
        st.markdown(f"""
        <div style='background:#0d1420;border:1px solid #1a2540;border-radius:12px;padding:16px;margin-top:8px'>
          <div style='font-size:0.68rem;color:#4a6080;text-transform:uppercase;letter-spacing:1px;
                      font-family:JetBrains Mono;margin-bottom:14px'>Rang shkalasi</div>
          <div style='background:linear-gradient(to top,#003280,#006ecc,#00ccff,#00ffaa);
                      height:140px;border-radius:6px;margin-bottom:8px'></div>
          <div style='font-family:JetBrains Mono;font-size:0.72rem;color:#8aa8c0'>
            <div>▲ {vmax:,.0f} — yuqori</div>
            <div style='margin-top:80px'>▼ {vmin:,.0f} — past</div>
          </div>
          <div style='margin-top:16px;font-size:0.72rem;color:#4a6080'>
            🔵 Doira = mutlaq qiymat<br>
            📦 Balandlik = zichlik
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── Small multiples maps ──
    st.markdown('<div class="section-title">Sohalarga ko\'ra xaritalar</div>', unsafe_allow_html=True)
    mc1, mc2 = st.columns(2)

    for i, (m_label, m_key, col_widget) in enumerate([
        ("💻 IT mutaxassislar", "it_workers", mc1),
        ("📚 O'qituvchilar",    "teachers",   mc2),
    ]):
        mini_df = dff.copy()
        mini_df["value"] = mini_df[m_key]
        mini_df["radius"]= mini_df["value"].apply(lambda v: max(math.sqrt(abs(v))*3500,60000))
        def col_it(v, mn=mini_df["value"].min(), mx=mini_df["value"].max()):
            if mx==mn: return [0,150,200,160]
            t=(v-mn)/(mx-mn)
            return [int(0+t*0),int(180+t*75),int(255-t*55),int(130+t*110)]
        mini_df["color"] = mini_df["value"].apply(col_it)
        with col_widget:
            st.caption(m_label)
            st.pydeck_chart(pdk.Deck(
                layers=[pdk.Layer("ScatterplotLayer",data=mini_df,
                    get_position=["lon","lat"],get_radius="radius",
                    get_fill_color="color",pickable=True,auto_highlight=True)],
                initial_view_state=pdk.ViewState(latitude=20,longitude=10,zoom=0.9),
                tooltip={"html":"<b>{name}</b><br/>{value:,.0f}K"},
                map_style="mapbox://styles/mapbox/dark-v10",
            ), use_container_width=True, height=280)

# ══════════════════════════════════════════
# TAB 2 — REYTINGLAR
# ══════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">Davlatlar reytingi</div>', unsafe_allow_html=True)

    rc1, rc2 = st.columns([3,2])

    with rc1:
        # Horizontal bar — selected metric
        fig_bar = go.Figure()
        sorted_df = dff.nlargest(top_n, sel_metric)
        colors_bar = [PALETTE[i % len(PALETTE)] for i in range(len(sorted_df))]
        fig_bar.add_trace(go.Bar(
            x=sorted_df[sel_metric],
            y=sorted_df["name"],
            orientation="h",
            marker=dict(
                color=sorted_df[sel_metric],
                colorscale=[[0,"#003d7a"],[0.5,"#0099ff"],[1,"#00ffcc"]],
                line=dict(width=0),
            ),
            text=sorted_df[sel_metric].apply(lambda v: f"{v:,.0f}"),
            textposition="outside",
            textfont=dict(size=10, color="#8aa8c0", family="JetBrains Mono"),
            hovertemplate="<b>%{y}</b><br>%{x:,.0f}<extra></extra>",
        ))
        fig_bar.update_layout(
            **base_layout(title=f"Top {top_n} — {sel_metric_label}"),
            xaxis=dict(gridcolor=PLOTLY_GRID, zeroline=False),
            yaxis=dict(gridcolor=PLOTLY_GRID, autorange="reversed"),
            height=500,
            showlegend=False,
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with rc2:
        # Treemap
        fig_tree = px.treemap(
            dff.nlargest(20, sel_metric),
            path=["region","name"],
            values=sel_metric,
            color=sel_metric,
            color_continuous_scale=[[0,"#002060"],[0.5,"#0066cc"],[1,"#00ffcc"]],
            title=f"Treemap — {sel_metric_label}",
            hover_data={"literacy_pct":True},
        )
        fig_tree.update_layout(
            **base_layout(),
            height=500,
            coloraxis_showscale=False,
        )
        fig_tree.update_traces(
            textfont=dict(family="Syne", size=11),
            marker=dict(line=dict(width=1, color="#06090f")),
        )
        st.plotly_chart(fig_tree, use_container_width=True)

    # ── Per-capita ranking ──
    st.markdown('<div class="section-title">1000 kishiga nisbatan (nisbiy ko\'rsatkich)</div>', unsafe_allow_html=True)

    per_k_metrics = {
        "💻 IT / 1K":           "it_per_1k",
        "📚 O'qituvchi / 1K":   "teacher_per_1k",
        "🩺 Shifokor / 1K":     "doctor_per_1k",
        "🔬 Tadqiqotchi / 1K":  "researcher_per_1k",
    }

    cols_pk = st.columns(len(per_k_metrics))
    for i, (lbl, key) in enumerate(per_k_metrics.items()):
        top5 = dff.nlargest(5, key)[["name", key]].reset_index(drop=True)
        fig_mini = go.Figure(go.Bar(
            x=top5[key],
            y=top5["name"].str.split(" ", n=1).str[-1],
            orientation="h",
            marker_color=PALETTE[i*2 % len(PALETTE)],
            text=top5[key].apply(lambda v: f"{v:.1f}"),
            textposition="outside",
            textfont=dict(size=9, color=PALETTE[i*2 % len(PALETTE)], family="JetBrains Mono"),
        ))
        fig_mini.update_layout(
            **base_layout(title=lbl, margin=dict(l=5,r=30,t=40,b=5)),
            height=240,
            xaxis=dict(visible=False),
            yaxis=dict(gridcolor=PLOTLY_GRID, autorange="reversed"),
            showlegend=False,
        )
        cols_pk[i].plotly_chart(fig_mini, use_container_width=True)

# ══════════════════════════════════════════
# TAB 3 — TAHLIL
# ══════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">Korrelyatsiya va STEM tahlili</div>', unsafe_allow_html=True)

    ta1, ta2 = st.columns(2)

    with ta1:
        # Scatter — GDP vs IT workers
        fig_sc = px.scatter(
            dff,
            x="gdp_trillion",
            y="it_per_1k",
            size="population_mln",
            color="region",
            hover_name="name",
            text="flag",
            color_discrete_sequence=PALETTE,
            title="💰 YaIM vs 💻 IT mutaxassislar (1000 kishiga)",
            labels={"gdp_trillion":"YaIM (trillion $)", "it_per_1k":"IT / 1000 kishi"},
        )
        fig_sc.update_traces(
            textposition="top center",
            marker=dict(opacity=0.8, line=dict(width=0)),
        )
        fig_sc.update_layout(**base_layout(), height=420,
            xaxis=dict(gridcolor=PLOTLY_GRID),
            yaxis=dict(gridcolor=PLOTLY_GRID))
        st.plotly_chart(fig_sc, use_container_width=True)

    with ta2:
        # Radar — top 5 countries
        top5_radar = dff.nlargest(5, "stem_index")
        cats = ["IT / 1K", "O'qituvchi / 1K", "Shifokor / 1K", "Tadqiqotchi / 1K", "Savodxonlik"]
        keys = ["it_per_1k","teacher_per_1k","doctor_per_1k","researcher_per_1k","literacy_pct"]

        fig_radar = go.Figure()
        for idx, row in top5_radar.iterrows():
            vals = [row[k] for k in keys]
            norm = [v / max(dff[k].max(),1) * 100 for v,k in zip(vals,keys)]
            fig_radar.add_trace(go.Scatterpolar(
                r=norm + [norm[0]],
                theta=cats + [cats[0]],
                name=row["name"].split(" ",1)[-1],
                line=dict(color=PALETTE[list(top5_radar.index).index(idx) % len(PALETTE)], width=2),
                fill="toself",
                fillcolor=PALETTE[list(top5_radar.index).index(idx) % len(PALETTE)],
                opacity=0.12,
            ))
        fig_radar.update_layout(
            **base_layout(title="🕸️ Top 5 — STEM Radar"),
            polar=dict(
                bgcolor=PLOTLY_BG,
                radialaxis=dict(visible=True, gridcolor=PLOTLY_GRID, color="#4a6080"),
                angularaxis=dict(gridcolor=PLOTLY_GRID, color="#8aa8c0"),
            ),
            height=420,
            legend=dict(font=dict(size=10, color=PLOTLY_TEXT)),
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # ── STEM Index ranking ──
    st.markdown('<div class="section-title">STEM Indeksi (IT + Muhandis + Tadqiqotchi zichligi)</div>', unsafe_allow_html=True)
    stem_sorted = dff.sort_values("stem_index", ascending=False).head(top_n)
    fig_stem = go.Figure()
    fig_stem.add_trace(go.Scatter(
        x=stem_sorted["name"].str.split(" ",n=1).str[-1],
        y=stem_sorted["stem_index"],
        mode="lines+markers+text",
        marker=dict(size=12, color="#00e5ff",
                    line=dict(width=2, color="#003d7a")),
        line=dict(color="rgba(0,229,255,0.25)", width=2),
        text=stem_sorted["stem_index"].apply(lambda v: f"{v:.0f}"),
        textposition="top center",
        textfont=dict(size=9, color="#00e5ff", family="JetBrains Mono"),
        fill="tozeroy",
        fillcolor="rgba(0,229,255,0.05)",
        hovertemplate="<b>%{x}</b><br>STEM index: %{y:.1f}<extra></extra>",
    ))
    fig_stem.update_layout(
        **base_layout(),
        height=280,
        xaxis=dict(gridcolor=PLOTLY_GRID, tickangle=-30),
        yaxis=dict(gridcolor=PLOTLY_GRID, title="STEM indeksi (0-100)"),
    )
    st.plotly_chart(fig_stem, use_container_width=True)

    # ── Literacy vs Researchers ──
    ta3, ta4 = st.columns(2)
    with ta3:
        fig_lit = px.scatter(dff, x="literacy_pct", y="researcher_per_1k",
            size="gdp_trillion", color="region",
            hover_name="name", color_discrete_sequence=PALETTE,
            title="📖 Savodxonlik vs 🔬 Tadqiqotchilar",
            labels={"literacy_pct":"Savodxonlik %","researcher_per_1k":"Tadqiqotchi / 1K"})
        fig_lit.update_layout(**base_layout(), height=340,
            xaxis=dict(gridcolor=PLOTLY_GRID),
            yaxis=dict(gridcolor=PLOTLY_GRID))
        st.plotly_chart(fig_lit, use_container_width=True)

    with ta4:
        # Bubble: students vs teachers
        fig_bub = px.scatter(dff, x="teachers", y="students_mln",
            size="population_mln", color="region",
            hover_name="name", color_discrete_sequence=PALETTE,
            title="📚 O'qituvchi vs 🎓 Talabalar (mln)",
            labels={"teachers":"O'qituvchilar (000)","students_mln":"Talabalar (mln)"})
        fig_bub.update_layout(**base_layout(), height=340,
            xaxis=dict(gridcolor=PLOTLY_GRID, type="log"),
            yaxis=dict(gridcolor=PLOTLY_GRID))
        st.plotly_chart(fig_bub, use_container_width=True)

# ══════════════════════════════════════════
# TAB 4 — MINTAQALAR
# ══════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">Mintaqaviy taqqoslama</div>', unsafe_allow_html=True)

    reg_agg = df.groupby("region").agg(
        it_workers=("it_workers","sum"),
        teachers=("teachers","sum"),
        engineers=("engineers","sum"),
        doctors=("doctors","sum"),
        researchers=("researchers","sum"),
        students_mln=("students_mln","sum"),
        gdp_trillion=("gdp_trillion","sum"),
        population_mln=("population_mln","sum"),
        countries=("name","count"),
    ).reset_index()
    reg_agg["it_per_1k"] = (reg_agg["it_workers"] / reg_agg["population_mln"] * 1000).round(1)

    ma1, ma2 = st.columns(2)

    with ma1:
        # Grouped bar
        fig_grp = go.Figure()
        for i,(lbl,key,col) in enumerate([
            ("IT",       "it_workers",  PALETTE[0]),
            ("O'qituvchi","teachers",   PALETTE[1]),
            ("Muhandis", "engineers",   PALETTE[2]),
            ("Shifokor", "doctors",     PALETTE[3]),
        ]):
            fig_grp.add_trace(go.Bar(
                name=lbl,
                x=reg_agg["region"],
                y=reg_agg[key],
                marker_color=col,
                opacity=0.85,
            ))
        fig_grp.update_layout(
            **base_layout(title="Mintaqalar bo'yicha kasb zichligi"),
            barmode="group",
            height=380,
            xaxis=dict(gridcolor=PLOTLY_GRID),
            yaxis=dict(gridcolor=PLOTLY_GRID, title="Soni (000)"),
            legend=dict(orientation="h", y=-0.2, font=dict(size=10)),
        )
        st.plotly_chart(fig_grp, use_container_width=True)

    with ma2:
        # Sunburst
        fig_sun = px.sunburst(
            df,
            path=["region","name"],
            values=sel_metric,
            color=sel_metric,
            color_continuous_scale=[[0,"#002060"],[0.5,"#0066cc"],[1,"#00ffcc"]],
            title=f"☀️ {sel_metric_label} — Mintaqa → Davlat",
        )
        fig_sun.update_layout(**base_layout(), height=380, coloraxis_showscale=False)
        fig_sun.update_traces(
            textfont=dict(family="Syne", size=10),
            insidetextorientation="radial",
        )
        st.plotly_chart(fig_sun, use_container_width=True)

    # ── Parallel categories ──
    st.markdown('<div class="section-title">Ko\'p o\'lchovli taqqoslash</div>', unsafe_allow_html=True)

    fig_par = go.Figure(go.Parcats(
        dimensions=[
            dict(label="Mintaqa",    values=df["region"]),
            dict(label="Savodxonlik",values=pd.cut(df["literacy_pct"],
                bins=[0,70,90,95,100],labels=["<70%","70-90%","90-95%","95%+"])),
            dict(label="STEM darajasi",values=pd.cut(df["stem_index"],
                bins=[0,20,40,60,100],labels=["Past","O'rta","Yuqori","Top"])),
        ],
        line=dict(
            color=df["stem_index"],
            colorscale=[[0,"#003d7a"],[0.5,"#0099ff"],[1,"#00ffcc"]],
            showscale=True,
            colorbar=dict(thickness=10, title="STEM"),
        ),
        hoveron="color",
        hoverinfo="count+probability",
        labelfont=dict(family="Syne", size=11, color=PLOTLY_TEXT),
        tickfont=dict(family="JetBrains Mono", size=9, color="#8aa8c0"),
    ))
    fig_par.update_layout(**base_layout(title="Parallel koordinatalar — Mintaqa · Savodxonlik · STEM"), height=340)
    st.plotly_chart(fig_par, use_container_width=True)

    # ── Region cards ──
    st.markdown('<div class="section-title">Mintaqa kartochkalari</div>', unsafe_allow_html=True)
    rcols = st.columns(len(reg_agg))
    for i, row in reg_agg.iterrows():
        rcols[i].markdown(f"""
        <div class="kpi-card" style="--accent:{PALETTE[i % len(PALETTE)]};text-align:left">
          <div style="font-weight:800;font-size:0.9rem;color:{PALETTE[i%len(PALETTE)]};margin-bottom:8px">
            {row['region']}
          </div>
          <div style="font-size:0.72rem;color:#8aa8c0;line-height:2;font-family:'JetBrains Mono',monospace">
            🌍 {row['countries']} davlat<br>
            👥 {row['population_mln']:.0f}M aholi<br>
            💻 {row['it_workers']:,.0f}K IT<br>
            📚 {row['teachers']:,.0f}K uqt.<br>
            💰 ${row['gdp_trillion']:.1f}T YaIM
          </div>
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════
# TAB 5 — MA'LUMOTLAR
# ══════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-title">To\'liq ma\'lumotlar jadvali</div>', unsafe_allow_html=True)

    show_cols = {
        "name":          "Davlat",
        "region":        "Mintaqa",
        "population_mln":"Aholi (M)",
        "it_workers":    "IT (K)",
        "teachers":      "O'qituvchi (K)",
        "engineers":     "Muhandis (K)",
        "doctors":       "Shifokor (K)",
        "researchers":   "Tadqiqotchi (K)",
        "students_mln":  "Talaba (M)",
        "literacy_pct":  "Savodxonlik %",
        "it_per_1k":     "IT / 1K",
        "stem_index":    "STEM indeksi",
        "gdp_trillion":  "YaIM ($T)",
    }

    display_df = dff[list(show_cols.keys())].rename(columns=show_cols)
    display_df = display_df.sort_values("STEM indeksi", ascending=False).reset_index(drop=True)
    display_df.index += 1

    st.dataframe(
        display_df.style
            .background_gradient(subset=["STEM indeksi","IT / 1K","Savodxonlik %"],
                                  cmap="YlGnBu")
            .format({
                "Aholi (M)": "{:.1f}",
                "IT (K)": "{:,.0f}",
                "O'qituvchi (K)": "{:,.0f}",
                "Muhandis (K)": "{:,.0f}",
                "Shifokor (K)": "{:,.0f}",
                "Tadqiqotchi (K)": "{:,.0f}",
                "Talaba (M)": "{:.1f}",
                "Savodxonlik %": "{:.1f}",
                "IT / 1K": "{:.1f}",
                "STEM indeksi": "{:.1f}",
                "YaIM ($T)": "{:.2f}",
            }),
        use_container_width=True,
        height=600,
    )

    dc1, dc2 = st.columns(2)
    with dc1:
        csv = display_df.to_csv(index=True).encode("utf-8")
        st.download_button(
            "⬇️ CSV yuklab olish",
            csv, "dunyo_inson_kapitali.csv", "text/csv"
        )
    with dc2:
        st.markdown("""
        <div style='font-family:JetBrains Mono,monospace;font-size:0.72rem;color:#4a6080;padding:8px 0'>
        📌 Ma'lumotlar: ILO 2024, UNESCO UIS 2023, WHO 2023, World Bank 2024<br>
        📌 K = ming, M = million, T = trillion
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────
st.markdown("""
<div style='margin-top:40px;padding:20px;border-top:1px solid #1a2540;
            text-align:center;font-family:JetBrains Mono,monospace;
            font-size:0.72rem;color:#2a4060'>
  🌍 Dunyo Inson Kapitali Atlasi · ILO · UNESCO · World Bank · WHO · OECD · 2024
  <br>InfoSchoolUz | Barcha huquqlar himoyalangan
</div>
""", unsafe_allow_html=True)
