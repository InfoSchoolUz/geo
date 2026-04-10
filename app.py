import streamlit as st
import requests
import json
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

st.title("🌍 Global Statistics Map (No API Key)")

# ===== STATIC DATA =====
stats = {
    "Uzbekistan": {"gdp": 80, "literacy": 99, "risk": "Low"},
    "United States of America": {"gdp": 25000, "literacy": 99, "risk": "Low"},
    "Ukraine": {"gdp": 200, "literacy": 99, "risk": "High"},
    "Palestine": {"gdp": 20, "literacy": 97, "risk": "High"},
}

# ===== MAP INIT =====
m = folium.Map(location=[20, 0], zoom_start=2)

# ===== COLOR LOGIC =====
def get_color(country):
    d = stats.get(country)
    if not d:
        return "gray"
    if d["gdp"] > 10000:
        return "green"
    elif d["gdp"] > 1000:
        return "orange"
    return "red"

# ===== LOAD GEOJSON =====
geo_url = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
geo_data = requests.get(geo_url).json()

# ===== COUNTRY CLICK FUNCTION =====
selected_country = st.session_state.get("country", None)

def style_function(feature):
    return {
        "fillColor": get_color(feature["properties"]["name"]),
        "color": "blue",
        "weight": 1,
        "fillOpacity": 0.5,
    }

# Add GeoJSON
folium.GeoJson(
    geo_data,
    style_function=style_function,
    name="countries",
).add_to(m)

# ===== EARTHQUAKE LAYER =====
eq_url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
eq_data = requests.get(eq_url).json()

for eq in eq_data["features"]:
    coords = eq["geometry"]["coordinates"]
    folium.CircleMarker(
        location=[coords[1], coords[0]],
        radius=3,
        color="red",
        fill=True
    ).add_to(m)

# ===== DISPLAY MAP =====
map_data = st_folium(m, width=1200, height=600)

# ===== CLICK DETECTION =====
if map_data and map_data["last_clicked"]:
    lat = map_data["last_clicked"]["lat"]
    lng = map_data["last_clicked"]["lng"]

    st.session_state["coords"] = (lat, lng)

# ===== COUNTRY INFO =====
st.subheader("📊 Country Info")

country_name = st.text_input("Enter country name (English):")

def generate_insight(s):
    if not s:
        return "No data"
    if s["risk"] == "High":
        return "Geopolitical tension region"
    if s["gdp"] > 10000:
        return "Highly developed economy"
    if s["gdp"] > 1000:
        return "Developing country"
    return "Low income region"

if country_name:
    try:
        url = f"https://restcountries.com/v3.1/name/{country_name}"
        data = requests.get(url).json()[0]

        s = stats.get(country_name, {})

        st.image(data["flags"]["png"])
        st.write("👥 Population:", f"{data['population']:,}")
        st.write("🏙 Capital:", data.get("capital", ["N/A"])[0])
        st.write("🌍 Region:", data["region"])
        st.write("📐 Area:", data["area"], "km²")

        st.write("💰 GDP:", s.get("gdp", "N/A"))
        st.write("📚 Literacy:", s.get("literacy", "N/A"))
        st.write("⚠ Risk:", s.get("risk", "Unknown"))

        st.success("🧠 Insight: " + generate_insight(s))

    except:
        st.error("Country not found")
