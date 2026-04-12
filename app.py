import streamlit as st
from streamlit_folium import st_folium
import folium
import requests
import pandas as pd
import random

st.set_page_config(layout="wide")

st.title("🌍 World Intelligence Dashboard")

# ===== LOAD DATA =====
@st.cache_data
def load_data():
    url = "https://restcountries.com/v3.1/all"
    return requests.get(url).json()

countries = load_data()

# ===== MAP =====
m = folium.Map(location=[20, 0], zoom_start=2, tiles="cartodb dark_matter")

country_coords = {}

for c in countries:
    try:
        name = c["name"]["common"]
        latlng = c.get("latlng")

        if latlng:
            lat, lon = latlng
            country_coords[name] = (lat, lon)

            folium.CircleMarker(
                location=[lat, lon],
                radius=4,
                color="#38bdf8",
                fill=True
            ).add_to(m)
    except:
        continue

map_data = st_folium(m, height=600)

selected = None

# ===== CLICK =====
if map_data and map_data.get("last_object_clicked"):
    lat = map_data["last_object_clicked"]["lat"]
    lon = map_data["last_object_clicked"]["lng"]

    def nearest(lat, lon):
        closest = None
        dist_min = 999999

        for name, (clat, clon) in country_coords.items():
            dist = (lat - clat) ** 2 + (lon - clon) ** 2
            if dist < dist_min:
                dist_min = dist
                closest = name
        return closest

    selected = nearest(lat, lon)

# ===== SELECTBOX =====
names = sorted([c["name"]["common"] for c in countries])
manual = st.selectbox("Davlat tanlang:", ["None"] + names)

if manual != "None":
    selected = manual

if not selected:
    st.info("👆 Xarita ustiga bosib davlat tanlang")
    st.stop()

# ===== GET COUNTRY =====
country = next(c for c in countries if c["name"]["common"] == selected)

# ===== REAL DATA =====
flag = country.get("flags", {}).get("png", "")
capital = country.get("capital", ["N/A"])[0]
population = country.get("population", 0)
area = country.get("area", 0)

# currency
currencies = country.get("currencies", {})
currency = ", ".join([v.get("name", "") for v in currencies.values()]) if currencies else "N/A"

# languages (NEW)
languages = country.get("languages", {})
langs = ", ".join(languages.values()) if languages else "N/A"

region = country.get("region", "N/A")

# ===== FAKE ADVANCED DATA =====
universities = random.randint(50, 5000)
schools = random.randint(1000, 200000)
colleges = random.randint(100, 10000)
agriculture = random.randint(5, 40)

# ===== DISPLAY =====
st.subheader(f"📊 {selected}")

col1, col2 = st.columns([1,2])

with col1:
    if flag:
        st.image(flag, width=200)

with col2:
    st.markdown(f"### 🌍 {region}")

# ===== TABLE =====
data = {
    "Ko‘rsatkich": [
        "🏙 Poytaxt",
        "👥 Aholi",
        "📏 Maydon (km²)",
        "💰 Valyuta",
        "🗣 Til(lar)",          # ← YANGI
        "🎓 Universitetlar soni",
        "🏫 Maktablar soni",
        "🏛 Kollejlar soni",
        "🌾 Qishloq xo‘jaligi (%)"
    ],
    "Qiymat": [
        capital,
        f"{population:,}",
        f"{area:,}",
        currency,
        langs,                  # ← YANGI
        universities,
        schools,
        colleges,
        f"{agriculture}%"
    ]
}

df = pd.DataFrame(data)

st.table(df)

# ===== FOOTER =====
st.markdown("---")
st.caption("⚠️ Education va agriculture ma'lumotlari demo (random) generatsiya qilingan")
st.markdown("Developed by Azamat Madrimov 🚀")
