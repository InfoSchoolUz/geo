import streamlit as st
import requests
import json
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

st.title("🌍 Global Analitika Platformasi")

# ===== LOAD DATA =====
@st.cache_data
def load_countries():
    return requests.get("https://restcountries.com/v3.1/all").json()

@st.cache_data
def load_stats():
    with open("stats.json", "r", encoding="utf-8") as f:
        return json.load(f)

countries_data = load_countries()
stats = load_stats()

# ===== FLAG =====
def flag(code):
    return ''.join(chr(127397 + ord(c)) for c in code.upper())

country_dict = {c["name"]["common"]: c.get("cca2","") for c in countries_data}
countries = sorted(country_dict.keys())

selected = st.selectbox(
    "🌍 Davlatni tanlang:",
    countries,
    format_func=lambda x: f"{flag(country_dict[x])} {x}"
)

country = next(c for c in countries_data if c["name"]["common"] == selected)
s = stats.get(selected, {})

# ===== MAP =====
st.subheader("🗺 Interaktiv xarita")

m = folium.Map(location=[20,0], zoom_start=2)

# GeoJSON
geo_url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
geo_data = requests.get(geo_url).json()

def get_color(name):
    d = stats.get(name)
    if not d: return "gray"
    if d["gdp"] > 10000: return "green"
    if d["gdp"] > 1000: return "orange"
    return "red"

folium.GeoJson(
    geo_data,
    style_function=lambda f: {
        "fillColor": get_color(f["properties"]["name"]),
        "color": "blue",
        "weight": 1,
        "fillOpacity": 0.6,
    },
    tooltip=folium.GeoJsonTooltip(fields=["name"])
).add_to(m)

# ===== EARTHQUAKE =====
eq = requests.get("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson").json()

for q in eq["features"]:
    lng, lat, *_ = q["geometry"]["coordinates"]
    folium.CircleMarker(
        location=[lat, lng],
        radius=3,
        color="red",
        fill=True
    ).add_to(m)

# ===== CONFLICT (STATIC) =====
conflicts = [
    {"name": "Ukraine War", "lat": 48.3, "lon": 31.1},
    {"name": "Gaza Conflict", "lat": 31.5, "lon": 34.4}
]

for c in conflicts:
    folium.Marker(
        location=[c["lat"], c["lon"]],
        popup="⚔ " + c["name"],
        icon=folium.Icon(color="red")
    ).add_to(m)

st_folium(m, width=1200, height=500)

# ===== COUNTRY INFO =====
st.subheader("📊 Davlat ma'lumotlari")

col1, col2 = st.columns(2)

with col1:
    st.image(country["flags"]["png"], width=150)
    st.write("👥 Aholi:", f"{country['population']:,}")
    st.write("🏙 Poytaxt:", country.get("capital", ["N/A"])[0])
    st.write("🌍 Mintaqa:", country["region"])

with col2:
    st.write("💰 GDP:", s.get("gdp", "N/A"))
    st.write("📚 Savodxonlik:", s.get("literacy", "N/A"))
    st.write("🌐 Internet:", s.get("internet", "N/A"))

# ===== CHART =====
st.subheader("📈 Grafik")

df = pd.DataFrame([
    {"metric": "GDP", "value": s.get("gdp", 0)},
    {"metric": "Literacy", "value": s.get("literacy", 0)},
    {"metric": "Internet", "value": s.get("internet", 0)}
])

st.bar_chart(df.set_index("metric"))

# ===== INSIGHT =====
def insight(s):
    if not s: return "No data"
    if s.get("risk") == "High": return "⚠ Xavfli hudud"
    if s.get("gdp",0) > 10000: return "💎 Rivojlangan"
    if s.get("gdp",0) > 1000: return "📈 Rivojlanmoqda"
    return "📉 Past iqtisod"

st.success("🧠 Tahlil: " + insight(s))

# ===== EXPORT =====
st.subheader("📥 Export")

export_data = {
    "Country": selected,
    "Population": country["population"],
    "GDP": s.get("gdp"),
    "Literacy": s.get("literacy"),
    "Internet": s.get("internet")
}

df_export = pd.DataFrame([export_data])

st.download_button(
    "📥 Excel yuklab olish",
    df_export.to_csv(index=False),
    file_name=f"{selected}_data.csv"
    )
