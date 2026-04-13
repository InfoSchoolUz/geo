import streamlit as st
import folium
from streamlit_folium import st_folium
import requests

st.set_page_config(page_title="Global Country Data Pro", layout="wide", page_icon="🌍")

# ───────── FIXED API FUNCTION ─────────
@st.cache_data(ttl=3600)
def get_all_data():
    url = "https://restcountries.com/v3.1/all"
    fields = "name,capital,flags,population,area,region,subregion,currencies,languages,latlng,timezones,tld,idd,car,coatOfArms"

    try:
        resp = requests.get(f"{url}?fields={fields}", timeout=20)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        return None

st.title("🌍 Dunyo Davlatlari Explorer")

data = get_all_data()

if not data:
    st.error("❌ API ishlamadi")
    st.stop()

countries = sorted([c['name']['common'] for c in data])
selected = st.selectbox("Davlat tanlang", countries)

c = next((item for item in data if item["name"]["common"] == selected), None)

st.write("Poytaxt:", c.get("capital", ["Noma'lum"])[0])
st.write("Aholi:", c.get("population", 0))
st.write("Maydon:", c.get("area", 0))

