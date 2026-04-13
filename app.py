import streamlit as st
import folium
from streamlit_folium import st_folium
import requests

st.set_page_config(page_title="Global Country Data Pro", layout="wide")

# ─────────────────────────────────────────────
# DATA FETCH (PRIMARY + FALLBACK)
# ─────────────────────────────────────────────

@st.cache_data(ttl=3600)
def fetch_data():
    # 1. PRIMARY → APICountries
    try:
        res = requests.get("https://www.apicountries.com/countries", timeout=10)
        if res.status_code == 200:
            raw = res.json()
            return format_api_countries(raw)
    except:
        pass

    # 2. FALLBACK → REST Countries
    try:
        res = requests.get("https://restcountries.com/v3.1/all", timeout=10)
        if res.status_code == 200:
            return res.json()
    except:
        pass

    return None


# ─────────────────────────────────────────────
# FORMATTER (APICountries → REST format)
# ─────────────────────────────────────────────

def format_api_countries(data):
    formatted = []

    for c in data:
        lat = c.get("latitude")
        lon = c.get("longitude")

        if lat and lon:
            latlng = [lat, lon]
        else:
            latlng = [0, 0]

        formatted.append({
            "name": {
                "common": c.get("name", ""),
                "official": c.get("officialName", "")
            },
            "capital": [c.get("capital")] if c.get("capital") else [],
            "population": c.get("population", 0),
            "area": c.get("area", 0),
            "region": c.get("region", ""),
            "subregion": c.get("subregion", ""),
            "flags": {
                "png": c.get("flag", "")
            },
            "latlng": latlng,
            "unMember": None
        })

    return formatted


# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────

data = fetch_data()

if not data:
    st.error("❌ API ishlamadi")
    st.stop()

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────

countries = sorted([c["name"]["common"] for c in data if c["name"]["common"]])

selected = st.sidebar.selectbox("Davlat tanlang", countries)

# ─────────────────────────────────────────────
# FIND COUNTRY
# ─────────────────────────────────────────────

c = next((x for x in data if x["name"]["common"] == selected), None)

if not c:
    st.warning("Ma'lumot topilmadi")
    st.stop()

# ─────────────────────────────────────────────
# SAFE DATA EXTRACTION
# ─────────────────────────────────────────────

capital = c.get("capital", ["Noma'lum"])
capital = capital[0] if capital else "Noma'lum"

population = c.get("population", 0)
area = c.get("area", 0)

latlng = c.get("latlng", [0, 0])
lat, lon = latlng if len(latlng) == 2 else (0, 0)

flag = c.get("flags", {}).get("png", "")

# ─────────────────────────────────────────────
# UI
# ─────────────────────────────────────────────

st.title(f"🌍 {selected}")

col1, col2 = st.columns([1, 2])

with col1:
    if flag:
        st.image(flag, caption="Bayroq")

with col2:
    st.metric("👥 Aholi", f"{population:,}")
    st.metric("📐 Maydon", f"{area:,.0f} km²")

    density = population / area if area else 0
    st.metric("🏘️ Zichlik", f"{density:.1f}")

    st.write(f"🏛️ Poytaxt: **{capital}**")
    st.write(f"🌐 Region: **{c.get('region','')}**")

# ─────────────────────────────────────────────
# MAP
# ─────────────────────────────────────────────

st.subheader("🗺️ Xarita")

m = folium.Map(location=[lat, lon], zoom_start=5)
folium.Marker([lat, lon], popup=selected).add_to(m)

st_folium(m, height=500)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────

st.markdown("---")
st.caption("Global Country Data Pro · InfoSchoolUz")
