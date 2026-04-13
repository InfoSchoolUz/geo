import streamlit as st
import folium
from streamlit_folium import st_folium
import requests

st.set_page_config(page_title="Geografiya Xarita", layout="wide")

# ─────────────────────────────────────────────
# DATA FETCH (APICOUNTRIES)
# ─────────────────────────────────────────────
@st.cache_data(ttl=3600)
def fetch_data():
    try:
        url = "https://www.apicountries.com/countries"
        res = requests.get(url, timeout=15)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"API xato: {e}")
        return None

data = fetch_data()

if not data:
    st.stop()

# ─────────────────────────────────────────────
# TITLE
# ─────────────────────────────────────────────
st.markdown("""
<h1 style='text-align:center;color:#38bdf8;'>🌍 Interaktiv Geografiya Xarita</h1>
<p style='text-align:center;'>Marker ustiga bosing</p>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAP
# ─────────────────────────────────────────────
m = folium.Map(location=[20, 0], zoom_start=2)

for c in data:
    lat = c.get("latitude")
    lon = c.get("longitude")

    if lat is None or lon is None:
        continue

    folium.Marker(
        location=[lat, lon],
        tooltip=c.get("name"),
        icon=folium.Icon(color="blue")
    ).add_to(m)

map_data = st_folium(
    m,
    height=500,
    returned_objects=["last_clicked"]
)

# ─────────────────────────────────────────────
# COUNTRY FINDER
# ─────────────────────────────────────────────
def find_country(lat, lon):
    closest = None
    min_dist = float("inf")

    for c in data:
        clat = c.get("latitude")
        clon = c.get("longitude")

        if clat is None or clon is None:
            continue

        d = (lat - clat)**2 + (lon - clon)**2

        if d < min_dist:
            min_dist = d
            closest = c

    return closest

clicked = map_data.get("last_clicked")

# ─────────────────────────────────────────────
# SHOW DATA
# ─────────────────────────────────────────────
if clicked:
    lat = clicked.get("lat")
    lon = clicked.get("lng")

    if lat and lon:
        c = find_country(lat, lon)

        if c:
            # 🟢 Asosiy
            name = c.get("name", "Noma'lum")
            capital = c.get("capital", "Noma'lum")
            population = c.get("population", 0)
            area = c.get("area", 0)
            density = population / area if area else 0

            # 🌍 Geografiya
            region = c.get("region", "—")
            subregion = c.get("subregion", "—")
            borders = c.get("borders", [])

            # 🗣️ Til
            languages = ", ".join(c.get("languages", [])) if c.get("languages") else "—"

            # 💱 Valyuta
            currencies = c.get("currencies", [])
            currency_text = ", ".join([x.get("name","") for x in currencies]) if currencies else "—"

            # 📡 Texnologiya
            tld = ", ".join(c.get("topLevelDomain", []))
            phone = ", ".join(c.get("callingCodes", []))
            timezones = c.get("timezones", [])

            # 🚗 Transport
            car_side = c.get("carSide", "—")
            car_signs = ", ".join(c.get("carSigns", [])) if c.get("carSigns") else "—"

            # 🌐 Global
            fifa = c.get("alpha3Code", "—")
            independent = c.get("independent", None)
            un_member = c.get("unMember", None)

            ind_text = "✅ Ha" if independent else "❌ Yo‘q"
            un_text = "✅ Ha" if un_member else "❌ Yo‘q"

            # 📊 Analytics
            gini = c.get("gini", "—")

            flag = c.get("flag", "")

            st.markdown("---")

            st.markdown(f"""
            <div style="background:#0f172a;padding:20px;border-radius:16px">

            <h2 style="color:#38bdf8;">🌍 {name}</h2>

            <img src="{flag}" width="120">

            <h4>📌 Asosiy</h4>
            <p>Poytaxt: {capital}</p>
            <p>Aholi: {population:,}</p>
            <p>Maydon: {area:,.0f} km²</p>
            <p>Zichlik: {density:.1f}</p>

            <h4>🌍 Geografiya</h4>
            <p>Mintaqa: {region} ({subregion})</p>
            <p>Qo‘shnilar: {", ".join(borders) if borders else "Yo‘q"}</p>

            <h4>🗣️ Madaniyat</h4>
            <p>Tillar: {languages}</p>
            <p>Valyuta: {currency_text}</p>

            <h4>📡 Texnologiya</h4>
            <p>Domen: {tld}</p>
            <p>Telefon kodi: {phone}</p>
            <p>Timezone: {len(timezones)} ta</p>

            <h4>🚗 Transport</h4>
            <p>Yo‘l tomoni: {car_side}</p>
            <p>Belgilar: {car_signs}</p>

            <h4>🌐 Global</h4>
            <p>Mustaqil: {ind_text}</p>
            <p>BMT a’zosi: {un_text}</p>
            <p>Kodi (ISO): {fifa}</p>

            <h4>📊 Tahlil</h4>
            <p>GINI: {gini}</p>

            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.caption("Geografiya Platformasi · APICountries API")
