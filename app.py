import streamlit as st
import folium
from streamlit_folium import st_folium
import requests

st.set_page_config(page_title="Global Country Data Pro", layout="wide")

@st.cache_data(ttl=3600)
def fetch_data():
    try:
        res = requests.get("https://restcountries.com/v3.1/all", timeout=10)
        if res.status_code == 200:
            return res.json()
    except:
        pass
    return None

data = fetch_data()

if not data:
    st.error("API ishlamadi")
    st.stop()

st.title("🌍 Interaktiv Geografiya Xarita")

m = folium.Map(location=[20, 0], zoom_start=2)

for c in data:
    latlng = c.get("latlng", [0, 0])
    if len(latlng) != 2:
        continue

    folium.CircleMarker(
        location=latlng,
        radius=4,
        color="#38bdf8",
        fill=True,
        fill_opacity=0.7,
        tooltip=c["name"]["common"]
    ).add_to(m)

map_data = st_folium(m, height=500)

def find_country(lat, lon):
    closest = None
    min_dist = float("inf")
    for c in data:
        latlng = c.get("latlng", [0, 0])
        if len(latlng) != 2:
            continue
        d = (lat - latlng[0])**2 + (lon - latlng[1])**2
        if d < min_dist:
            min_dist = d
            closest = c
    return closest

clicked = map_data.get("last_clicked")

if clicked:
    c = find_country(clicked["lat"], clicked["lng"])

    capital = c.get("capital", ["Noma'lum"])
    capital = capital[0] if capital else "Noma'lum"

    population = c.get("population", 0)
    area = c.get("area", 0)
    density = population / area if area else 0

    languages = ", ".join(c.get("languages", {}).values()) if c.get("languages") else "—"

    currencies = c.get("currencies", {})
    currency_text = "—"
    if currencies:
        code = list(currencies.keys())[0]
        name = currencies[code].get("name", "")
        symbol = currencies[code].get("symbol", "")
        currency_text = f"{name} ({code}) {symbol}"

    flag = c.get("flags", {}).get("png", "")

    st.markdown("---")

    st.markdown(f'''
    <div style="background:#0f172a;padding:20px;border-radius:12px;">
        <h2 style="color:#38bdf8;">{c["name"]["common"]}</h2>
        <img src="{flag}" width="120">
        <p>Poytaxt: {capital}</p>
        <p>Aholi: {population:,}</p>
        <p>Maydon: {area:,.0f}</p>
        <p>Zichlik: {density:.1f}</p>
        <p>Til: {languages}</p>
        <p>Valyuta: {currency_text}</p>
    </div>
    ''', unsafe_allow_html=True)

st.markdown("---")
st.caption("Global Country Data Pro · InfoSchoolUz")
