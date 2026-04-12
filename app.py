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
    res = requests.get(url)
    if res.status_code != 200:
        return []
    return res.json()

countries = load_data()

# ===== SAFE NAME FUNCTION =====
def get_name(c):
    return c.get("name", {}).get("common")

# ===== MAP =====
m = folium.Map(location=[20, 0], zoom_start=2, tiles="cartodb dark_matter")

country_coords = {}

for c in countries:
    name = get_name(c)
    latlng = c.get("latlng")

    if name and latlng:
        lat, lon = latlng
        country_coords[name] = (lat, lon)

        folium.CircleMarker(
            location=[lat, lon],
            radius=4,
            color="#38bdf8",
            fill=True
        ).add_to(m)

map_data = st_folium(m, height=600)

selected = None

# ===== CLICK =====
if map_data and map_data.get("last_object_clicked"):
    lat = map_data["last_object_clicked"]["lat"]
    lon = map_data["last_object_clicked"]["lng"]

    def nearest(lat, lon):
        closest = None
        dist_min = float("inf")

        for name, (clat, clon) in country_coords.items():
            dist = (lat - clat) ** 2 + (lon - clon) ** 2
            if dist < dist_min:
                dist_min = dist
                closest = name
        return closest

    selected = nearest(lat, lon)

# ===== SELECTBOX =====
names = sorted(filter(None, [get_name(c) for c in countries]))
manual = st.selectbox("Davlat tanlang:", ["None"] + names)

if manual != "None":
    selected = manual

if not selected:
    st.info("👆 Xarita ustiga bosib davlat tanlang")
    st.stop()

# ===== GET COUNTRY (SAFE) =====
country = next(
    (c for c in countries if get_name(c) == selected),
    None
)

if not country:
    st.error("❌ Davlat topilmadi")
    st.stop()

# ===== REAL DATA =====
flag = country.get("flags", {}).get("png", "")
capital = country.get("capital", ["N/A"])[0]
population = country.get("population", 0)
area = country.get("area", 0)

# currency
currencies = country.get("currencies", {})
currency = ", ".join([v.get("name", "") for v in currencies.values()]) if currencies else "N/A"

# languages
languages = country.get("languages", {})
langs = ", ".join(languages.values()) if languages else "N/A"

region = country.get("region", "N/A")

# ===== FAKE DATA =====
universities = random.randint(50, 5000)
schools = random.randint(1000, 200000)
colleges = random.randint(100, 10000)
agriculture = random.randint(5, 40)

# ===== DISPLAY =====
st.subheader(f"📊 {selected}")

col1, col2 = st.columns([1, 2])

with col1:
    if flag:
        st.image(flag, width=200)

with col2:
    st.markdown(f"### 🌍 {region}")

# ===== TABLE =====
df = pd.DataFrame({
    "Ko‘rsatkich": [
        "🏙 Poytaxt",
        "👥 Aholi",
        "📏 Maydon (km²)",
        "💰 Valyuta",
        "🗣 Til(lar)",
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
        langs,
        universities,
        schools,
        colleges,
        f"{agriculture}%"
    ]
})

st.table(df)

# ===== FOOTER =====
st.markdown("---")
st.caption("⚠️ Education va agriculture ma'lumotlari demo (random)")
st.markdown("Developed by Azamat Madrimov 🚀")
