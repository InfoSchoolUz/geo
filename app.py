import streamlit as st
from streamlit_folium import st_folium
import folium
import requests
import pandas as pd

st.set_page_config(page_title="🌍 World Map Explorer", layout="wide")

st.title("🌍 World Map Explorer (Real Data)")
st.write("Davlat ustiga bosing → statistikani ko‘rasiz")

# ===== COUNTRY DATA API =====
@st.cache_data
def get_all_countries():
    url = "https://restcountries.com/v3.1/all"
    return requests.get(url).json()

countries = get_all_countries()

# ===== CREATE MAP =====
m = folium.Map(location=[20, 0], zoom_start=2)

# ===== ADD MARKERS =====
country_coords = {}

for c in countries:
    try:
        name = c["name"]["common"]
        latlng = c.get("latlng", None)

        if latlng:
            lat, lon = latlng
            country_coords[name] = (lat, lon)

            folium.CircleMarker(
                location=[lat, lon],
                radius=5,
                popup=name,
                color="blue",
                fill=True,
                fill_opacity=0.7,
            ).add_to(m)
    except:
        continue

# ===== DISPLAY MAP =====
map_data = st_folium(m, height=600, width=1200)

selected_country = None

# ===== CLICK EVENT =====
if map_data and map_data.get("last_object_clicked"):
    lat = map_data["last_object_clicked"]["lat"]
    lon = map_data["last_object_clicked"]["lng"]

    # nearest country find
    def find_country(lat, lon):
        closest = None
        min_dist = 999999

        for name, (clat, clon) in country_coords.items():
            dist = (lat - clat) ** 2 + (lon - clon) ** 2
            if dist < min_dist:
                min_dist = dist
                closest = name

        return closest

    selected_country = find_country(lat, lon)

# ===== SHOW INFO =====
if selected_country:
    st.subheader(f"📊 {selected_country} haqida ma'lumot")

    # get full data
    country_data = next(
        (c for c in countries if c["name"]["common"] == selected_country),
        None
    )

    if country_data:
        col1, col2, col3 = st.columns(3)

        population = country_data.get("population", "N/A")
        region = country_data.get("region", "N/A")
        capital = country_data.get("capital", ["N/A"])[0]

        col1.metric("👥 Aholi", f"{population:,}")
        col2.metric("🌍 Region", region)
        col3.metric("🏙 Poytaxt", capital)

        # ===== EXTRA DATA =====
        st.subheader("📈 Qo‘shimcha info")

        area = country_data.get("area", "N/A")
        currencies = country_data.get("currencies", {})
        currency_names = ", ".join([v["name"] for v in currencies.values()]) if currencies else "N/A"

        languages = country_data.get("languages", {})
        langs = ", ".join(languages.values()) if languages else "N/A"

        df = pd.DataFrame({
            "Metric": ["Maydon (km²)", "Valyuta", "Til"],
            "Value": [area, currency_names, langs]
        })

        st.table(df)

else:
    st.info("👆 Xarita ustiga bosib davlat tanlang")

# ===== FOOTER =====
st.markdown("---")
st.markdown("Developed by Azamat Madrimov 🚀")
