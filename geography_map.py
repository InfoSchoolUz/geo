import streamlit as st
import folium
from streamlit_folium import st_folium
import requests

st.set_page_config(page_title="Geografiya Xarita", layout="wide", page_icon="🌍")

# ── STYLE ───────────────────────────────────
st.markdown("""
<style>
body { background:#060d1a; color:#e2e8f0; }
.card {
    background:#0d1f35;
    border:1px solid #1e3a5f;
    border-radius:12px;
    padding:15px;
    margin-bottom:10px;
}
</style>
""", unsafe_allow_html=True)

# ── DATA FETCH ──────────────────────────────
@st.cache_data(ttl=3600)
def fetch_data():
    res = requests.get("https://www.apicountries.com/countries")
    return res.json()

# ── PREPROCESS ──────────────────────────────
@st.cache_data
def preprocess(data):
    for c in data:
        pop = c.get("population") or 0
        area = c.get("area") or 0
        density = pop / area if area else 0
        c["density"] = density

        if density > 300:
            c["insight"] = "⚠️ Overpopulated"
        elif density < 50:
            c["insight"] = "🌱 Sparse"
        else:
            c["insight"] = "✅ Balanced"
    return data

data = preprocess(fetch_data())
name_map = {c["name"]: c for c in data if c.get("name")}
names = sorted(name_map.keys())

# ── SESSION ────────────────────────────────
if "country" not in st.session_state:
    st.session_state.country = None

# ── SIDEBAR ───────────────────────────────
with st.sidebar:
    st.title("🌍 Geografiya")
    selected = st.selectbox("Davlat", ["—"] + names)

    if selected != "—":
        st.session_state.country = selected

# ── MAP ────────────────────────────────────
active = st.session_state.country
active_c = name_map.get(active)

center = [20, 0]
zoom = 2

if active_c:
    center = [active_c["latitude"], active_c["longitude"]]
    zoom = 5

m = folium.Map(location=center, zoom_start=zoom)

for c in data:
    lat, lon = c.get("latitude"), c.get("longitude")
    if not lat or not lon:
        continue

    folium.CircleMarker(
        location=[lat, lon],
        radius=6,
        popup=c["name"],
        tooltip=c["name"]
    ).add_to(m)

map_data = st_folium(m, height=450)

clicked = map_data.get("last_object_clicked_tooltip")
if clicked:
    st.session_state.country = clicked
    st.rerun()

# ── GLOBAL ANALYTICS ───────────────────────
max_pop = max(data, key=lambda x: x.get("population") or 0)
max_area = max(data, key=lambda x: x.get("area") or 0)

st.markdown(f"""
<div class='card'>
<b>🌍 GLOBAL</b><br>
👥 Eng katta aholi: {max_pop["name"]}<br>
📏 Eng katta hudud: {max_area["name"]}
</div>
""", unsafe_allow_html=True)

# ── COUNTRY INFO ───────────────────────────
if active:
    c = name_map[active]

    st.markdown(f"""
<div class='card'>
<h3>{active}</h3>
👥 Population: {c.get("population")}<br>
📏 Area: {c.get("area")}<br>
📊 Density: {c.get("density"):.1f}<br>
🧠 Insight: {c.get("insight")}
</div>
""", unsafe_allow_html=True)

# ── COMPARE MODE ───────────────────────────
st.markdown("## ⚔️ Compare")

c1 = st.selectbox("1-davlat", names, key="c1")
c2 = st.selectbox("2-davlat", names, key="c2")

if c1 and c2:
    d1 = name_map[c1]
    d2 = name_map[c2]

    st.markdown(f"""
<div class='card'>
<b>{c1} vs {c2}</b><br>
👥 {d1["population"]} | {d2["population"]}<br>
📏 {d1["area"]} | {d2["area"]}<br>
📊 {d1["density"]:.1f} | {d2["density"]:.1f}
</div>
""", unsafe_allow_html=True)
