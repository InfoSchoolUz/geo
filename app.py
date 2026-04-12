import streamlit as st
from streamlit_folium import st_folium
import folium
import requests
import pandas as pd
import json

st.set_page_config(page_title="🌍 Geo Intelligence AI", layout="wide")

# ===== NEON UI =====
st.markdown("""
<style>
body {
    background-color: #0f172a;
    color: white;
}
.block-container {
    padding-top: 1rem;
}
h1, h2, h3 {
    color: #38bdf8;
}
div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🌍 Geo Intelligence AI")
st.caption("Click country → Analyze → Compare → Understand")

# ===== LOAD GEOJSON =====
@st.cache_data
def load_geo():
    url = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json"
    return requests.get(url).json()

geo = load_geo()

# ===== WORLD BANK DATA =====
@st.cache_data
def wb_data(indicator):
    url = f"http://api.worldbank.org/v2/country/all/indicator/{indicator}?format=json&per_page=5000"
    data = requests.get(url).json()[1]
    df = pd.DataFrame(data)
    df = df[df["date"] == "2022"]
    return df[["countryiso3code", "value"]]

gdp = wb_data("NY.GDP.PCAP.CD")
life = wb_data("SP.DYN.LE00.IN")
pop = wb_data("SP.POP.TOTL")

# ===== MAP =====
m = folium.Map(location=[20,0], zoom_start=2, tiles="cartodb dark_matter")

folium.GeoJson(
    geo,
    name="countries",
    style_function=lambda x: {
        "fillColor": "#1e3a8a",
        "color": "#38bdf8",
        "weight": 1,
        "fillOpacity": 0.5,
    },
    highlight_function=lambda x: {
        "fillColor": "#22c55e",
        "fillOpacity": 0.8,
    },
).add_to(m)

map_data = st_folium(m, height=600, width=1200)

selected_iso = None

# ===== CLICK DETECTION =====
if map_data and map_data.get("last_active_drawing"):
    props = map_data["last_active_drawing"]["properties"]
    selected_iso = props.get("iso_a3")

# fallback
if map_data and map_data.get("last_clicked"):
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]

# ===== SELECT BOX (backup) =====
country_list = sorted(gdp["countryiso3code"].dropna().unique())
manual = st.selectbox("Yoki davlat tanlang:", ["None"] + list(country_list))

if manual != "None":
    selected_iso = manual

if not selected_iso:
    st.warning("Davlatni tanlang")
    st.stop()

# ===== GET DATA =====
def get_val(df, iso):
    row = df[df["countryiso3code"] == iso]
    return float(row["value"].values[0]) if not row.empty else 0

gdp_val = get_val(gdp, selected_iso)
life_val = get_val(life, selected_iso)
pop_val = get_val(pop, selected_iso)

st.header(f"📊 {selected_iso} statistikasi")

c1, c2, c3 = st.columns(3)
c1.metric("💰 GDP per capita", f"${gdp_val:,.0f}")
c2.metric("❤️ Life Expectancy", f"{life_val:.1f} years")
c3.metric("👥 Population", f"{pop_val:,.0f}")

# ===== AI EXPLAIN =====
st.subheader("🧠 AI Insight")

def explain(gdp, life, pop):
    if gdp > 20000:
        return "This is a high-income developed economy with strong infrastructure."
    elif gdp > 8000:
        return "This country is developing with moderate economic growth."
    else:
        return "This is a low-income or emerging economy with growth potential."

st.info(explain(gdp_val, life_val, pop_val))

# ===== COMPARE MODE =====
st.subheader("⚔️ Compare Countries")

compare_iso = st.selectbox("Compare with:", country_list)

if compare_iso:
    g2 = get_val(gdp, compare_iso)
    l2 = get_val(life, compare_iso)
    p2 = get_val(pop, compare_iso)

    df_compare = pd.DataFrame({
        "Metric": ["GDP", "Life Expectancy", "Population"],
        selected_iso: [gdp_val, life_val, pop_val],
        compare_iso: [g2, l2, p2]
    })

    st.dataframe(df_compare)

# ===== FOOTER =====
st.markdown("---")
st.markdown("Developed by Azamat Madrimov 🚀")
