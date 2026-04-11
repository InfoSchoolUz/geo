import streamlit as st
import folium
from streamlit_folium import st_folium

# ================= CONFIG =================
st.set_page_config(
    layout="wide",
    page_title="🌍 Global Platform",
    page_icon="🌍"
)

# ================= CYBER UI =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Rajdhani', sans-serif;
}

/* BACKGROUND */
.stApp {
    background: radial-gradient(circle at 20% 20%, #020617, #000);
    color: #e2e8f0;
}

/* TITLE */
.main-title {
    font-family: Orbitron;
    font-size: 3rem;
    text-align:center;
    color:#00f5ff;
    text-shadow:0 0 15px #00f5ff;
}

/* GLASS */
.glass {
    background: rgba(0,0,0,0.5);
    border:1px solid #00f5ff22;
    backdrop-filter: blur(10px);
    border-radius:12px;
    padding:1rem;
    margin-bottom:1rem;
}

/* HERO */
.hero-name {
    font-family: Orbitron;
    font-size:2rem;
    color:#00f5ff;
}

/* INFO */
.info-row {
    display:flex;
    justify-content:space-between;
    border-bottom:1px solid #111;
    padding:5px;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background:#000;
}

/* BUTTON */
.stButton button {
    border:1px solid #00f5ff;
    color:#00f5ff;
    background:transparent;
}

/* SCANLINES */
.stApp::after {
    content:"";
    position:fixed;
    width:100%;
    height:100%;
    background: repeating-linear-gradient(
        to bottom,
        rgba(255,255,255,0.02),
        rgba(255,255,255,0.02) 1px,
        transparent 1px,
        transparent 3px
    );
    pointer-events:none;
}
</style>
""", unsafe_allow_html=True)

# ================= DATA =================
countries = [
    {"name": "O'zbekiston", "capital": "Toshkent", "lat":41.3, "lon":69.2, "code":"uz", "region":"Osiyo", "population":"36 mln", "gdp":"$90B"},
    {"name": "AQSh", "capital": "Washington", "lat":38.9, "lon":-77.0, "code":"us", "region":"Amerika", "population":"331 mln", "gdp":"$25T"},
    {"name": "Xitoy", "capital": "Pekin", "lat":39.9, "lon":116.4, "code":"cn", "region":"Osiyo", "population":"1.4B", "gdp":"$18T"},
]

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("### 🌍 FILTER")
    region = st.selectbox("Region", ["All"] + list(set(c["region"] for c in countries)))

    compare_mode = st.checkbox("⚖️ Compare mode")

    if compare_mode:
        c1 = st.selectbox("Country 1", [c["name"] for c in countries])
        c2 = st.selectbox("Country 2", [c["name"] for c in countries], index=1)

# ================= TITLE =================
st.markdown('<div class="main-title">GLOBAL INTELLIGENCE</div>', unsafe_allow_html=True)

# ================= MAP =================
filtered = [c for c in countries if region == "All" or c["region"] == region]

m = folium.Map(location=[20,0], zoom_start=2, tiles="CartoDB dark_matter")

for c in filtered:
    folium.CircleMarker(
        [c["lat"], c["lon"]],
        radius=8,
        color="#00f5ff",
        fill=True
    ).add_to(m)

map_data = st_folium(m, width="100%", height=450, returned_objects=["last_object_clicked"])

# ================= HUD OVERLAY =================
st.markdown("""
<div style="position:relative;margin-top:-420px;height:0;pointer-events:none;">

<div style="position:absolute;left:20px;bottom:60px;width:100px;height:100px;border:2px solid #00f5ff;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#00f5ff;font-family:Orbitron;box-shadow:0 0 15px #00f5ff;">
33%
</div>

<div style="position:absolute;right:20px;bottom:60px;width:80px;height:80px;border:2px solid #00f5ff;border-radius:50%;display:flex;align-items:center;justify-content:center;color:#00f5ff;font-family:Orbitron;box-shadow:0 0 15px #00f5ff;">
12%
</div>

<div style="position:absolute;left:50%;transform:translateX(-50%);bottom:30px;width:60%;height:40px;border:1px solid #00f5ff33;background:rgba(0,255,255,0.05);color:#00f5ff;font-family:monospace;font-size:10px;padding:5px;">
SYSTEM ANALYZING GLOBAL DATA...
</div>

</div>
""", unsafe_allow_html=True)

# ================= COMPARE =================
if compare_mode:
    c1_data = next(c for c in countries if c["name"] == c1)
    c2_data = next(c for c in countries if c["name"] == c2)

    col1, col2 = st.columns(2)

    def render(c):
        st.markdown(f"""
        <div class="glass">
            <img src="https://flagcdn.com/w160/{c['code']}.png">
            <div class="hero-name">{c['name']}</div>
            <div>{c['capital']}</div>
            <div class="info-row"><span>Population</span><span>{c['population']}</span></div>
            <div class="info-row"><span>GDP</span><span>{c['gdp']}</span></div>
        </div>
        """, unsafe_allow_html=True)

    with col1:
        render(c1_data)

    with col2:
        render(c2_data)

    st.stop()

# ================= CLICK DETAIL =================
if map_data and map_data.get("last_object_clicked"):
    lat = map_data["last_object_clicked"]["lat"]
    lon = map_data["last_object_clicked"]["lng"]

    c = min(countries, key=lambda x: (x["lat"]-lat)**2 + (x["lon"]-lon)**2)

    st.markdown(f"""
    <div class="glass">
        <img src="https://flagcdn.com/w320/{c['code']}.png">
        <div class="hero-name">{c['name']}</div>
        <div>{c['capital']} · {c['region']}</div>
        <div class="info-row"><span>Population</span><span>{c['population']}</span></div>
        <div class="info-row"><span>GDP</span><span>{c['gdp']}</span></div>
    </div>
    """, unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="glass" style="text-align:center;">
        CLICK COUNTRY ON MAP
    </div>
    """, unsafe_allow_html=True)
