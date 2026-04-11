
import streamlit as st
import folium
from streamlit_folium import st_folium
import requests

st.set_page_config(layout="wide", page_title="🌍 Global Platform", page_icon="🌍")

# ===== LOAD DATA =====
@st.cache_data
def load_countries():
    try:
        res = requests.get("https://restcountries.com/v3.1/all", timeout=10)
        data = res.json()

        countries = []
        for c in data:
            try:
                countries.append({
                    "name": c["name"]["common"],
                    "code": c["cca2"].lower(),
                    "capital": c.get("capital", ["N/A"])[0],
                    "region": c.get("region", "Other"),
                    "lat": c["latlng"][0],
                    "lon": c["latlng"][1],
                    "color": "#00f5ff",

                    "population": f"{round(c.get('population',0)/1e6,1)} mln",
                    "area": f"{round(c.get('area',0),0)} km²",
                    "language": ", ".join(c.get("languages", {}).values()) if c.get("languages") else "N/A",
                    "currency": ", ".join([v["name"] for v in c.get("currencies", {}).values()]) if c.get("currencies") else "N/A",
                })
            except:
                continue

        return countries

    except:
        return []

countries = load_countries()

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown("### 🌍 Filter")
    regions = sorted(set(c["region"] for c in countries))
    selected_region = st.selectbox("Region", ["All"] + regions)

    compare_mode = st.checkbox("⚖️ Compare")

    if compare_mode:
        c1 = st.selectbox("Country 1", [c["name"] for c in countries])
        c2 = st.selectbox("Country 2", [c["name"] for c in countries], index=1)

# ===== TITLE =====
st.title("🌍 Global Intelligence Map")

# ===== MAP =====
filtered = [c for c in countries if selected_region == "All" or c["region"] == selected_region]

m = folium.Map(location=[20,0], zoom_start=2, tiles="CartoDB dark_matter")

for c in filtered:
    folium.CircleMarker(
        [c["lat"], c["lon"]],
        radius=6,
        color=c["color"],
        fill=True
    ).add_to(m)

map_data = st_folium(m, width="100%", height=500, returned_objects=["last_object_clicked"])

# ===== COMPARE =====
if compare_mode:
    col1, col2 = st.columns(2)

    def render(c):
        st.image(f"https://flagcdn.com/w160/{c['code']}.png")
        st.subheader(c["name"])
        st.write("Capital:", c["capital"])
        st.write("Population:", c["population"])
        st.write("Area:", c["area"])

    with col1:
        render(next(c for c in countries if c["name"] == c1))

    with col2:
        render(next(c for c in countries if c["name"] == c2))

    st.stop()

# ===== DETAIL =====
if map_data and map_data.get("last_object_clicked"):
    lat = map_data["last_object_clicked"]["lat"]
    lon = map_data["last_object_clicked"]["lng"]

    c = min(countries, key=lambda x: (x["lat"]-lat)**2 + (x["lon"]-lon)**2)

    st.image(f"https://flagcdn.com/w320/{c['code']}.png")
    st.header(c["name"])
    st.write("Capital:", c["capital"])
    st.write("Region:", c["region"])
    st.write("Population:", c["population"])
    st.write("Area:", c["area"])
    st.write("Language:", c["language"])
    st.write("Currency:", c["currency"])

else:
    st.info("Click a country on the map")
