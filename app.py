# app.py
import streamlit as st
import pandas as pd
import pydeck as pdk
import requests

st.set_page_config(page_title="🌍 Global Events Map", layout="wide")

# =========================
# EARTHQUAKE (REAL WORKING)
# =========================
@st.cache_data(ttl=300)
def load_earthquakes():
    url = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
    r = requests.get(url)
    data = r.json()

    rows = []
    for f in data["features"]:
        coords = f["geometry"]["coordinates"]
        prop = f["properties"]

        rows.append({
            "lat": coords[1],
            "lon": coords[0],
            "magnitude": prop["mag"],
            "place": prop["place"]
        })

    return pd.DataFrame(rows)

# =========================
# CONFLICT (FALLBACK DATA)
# =========================
def load_conflicts():
    # REALISTIC STATIC DATA (hackathon-safe)
    return pd.DataFrame([
        {"lat": 48.3794, "lon": 31.1656, "country": "Ukraine", "fatalities": 120},
        {"lat": 31.0461, "lon": 34.8516, "country": "Israel", "fatalities": 80},
        {"lat": 33.2232, "lon": 43.6793, "country": "Iraq", "fatalities": 40},
        {"lat": 15.5527, "lon": 48.5164, "country": "Yemen", "fatalities": 60},
        {"lat": 9.0820, "lon": 8.6753, "country": "Nigeria", "fatalities": 30},
    ])

eq = load_earthquakes()
cf = load_conflicts()

# =========================
# FILTERS
# =========================
st.sidebar.title("Filters")

min_mag = st.sidebar.slider("Min Magnitude", 0.0, 8.0, 2.5)
min_fat = st.sidebar.slider("Min Fatalities", 0, 200, 0)

eq = eq[eq["magnitude"] >= min_mag]
cf = cf[cf["fatalities"] >= min_fat]

# =========================
# LAYERS
# =========================
layers = []

# Earthquakes
layers.append(pdk.Layer(
    "ScatterplotLayer",
    data=eq,
    get_position='[lon, lat]',
    get_radius="magnitude * 20000",
    get_fill_color='[255,140,0,180]',
    pickable=True
))

# Conflicts
layers.append(pdk.Layer(
    "ScatterplotLayer",
    data=cf,
    get_position='[lon, lat]',
    get_radius="fatalities * 20000",
    get_fill_color='[220,20,60,180]',
    pickable=True
))

# =========================
# MAP
# =========================
st.pydeck_chart(pdk.Deck(
    layers=layers,
    initial_view_state=pdk.ViewState(latitude=20, longitude=0, zoom=1.2),
    tooltip={"text": "{place} {country}"}
))

# =========================
# KPI (NOW ALWAYS WORKS)
# =========================
col1, col2 = st.columns(2)

col1.metric("🌋 Earthquakes", len(eq))
col2.metric("⚔️ Conflicts", len(cf))

# =========================
# TABLES (FIXED)
# =========================
st.subheader("📊 Earthquakes")
st.dataframe(eq)

st.subheader("📊 Conflicts")
st.dataframe(cf)
