# app.py
import streamlit as st
import pandas as pd
import pydeck as pdk
import requests
from typing import List, Dict, Any

st.set_page_config(page_title="🌤 Global Weather Map PRO", layout="wide")

# =========================
# CONFIG
# =========================
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

DEFAULT_CITIES = [
    {"name": "Berlin", "lat": 52.5200, "lon": 13.4050},
    {"name": "New York", "lat": 40.7128, "lon": -74.0060},
    {"name": "Tashkent", "lat": 41.2995, "lon": 69.2401},
    {"name": "Tokyo", "lat": 35.6762, "lon": 139.6503},
    {"name": "Sydney", "lat": -33.8688, "lon": 151.2093},
]

COUNTRY_DATA = pd.DataFrame([
    {"country": "Germany", "lat": 51.1657, "lon": 10.4515},
    {"country": "USA", "lat": 37.0902, "lon": -95.7129},
    {"country": "Uzbekistan", "lat": 41.3775, "lon": 64.5853},
    {"country": "Japan", "lat": 36.2048, "lon": 138.2529},
])

# =========================
# UTILS
# =========================
def validate_df(df):
    required = {"name", "lat", "lon"}
    if not required.issubset(df.columns):
        raise ValueError("CSV must have name, lat, lon")
    return df.dropna()

@st.cache_data(ttl=600)
def fetch_weather(points):
    lats = ",".join(str(p["lat"]) for p in points)
    lons = ",".join(str(p["lon"]) for p in points)

    params = {
        "latitude": lats,
        "longitude": lons,
        "current_weather": True,
        "hourly": "temperature_2m",
        "timezone": "auto",
    }

    try:
        r = requests.get(OPEN_METEO_URL, params=params, timeout=10)
        r.raise_for_status()
        data = r.json()

        result = []
        cw = data.get("current_weather", [])
        hourly = data.get("hourly", {})

        for i, p in enumerate(points):
            temp = cw[i]["temperature"] if isinstance(cw, list) and i < len(cw) else None
            result.append({
                "name": p["name"],
                "lat": p["lat"],
                "lon": p["lon"],
                "temperature": temp,
                "trend": hourly.get("temperature_2m", [])[:24]
            })
        return result

    except:
        return [{"name": p["name"], "lat": p["lat"], "lon": p["lon"], "temperature": None, "trend": []} for p in points]

# =========================
# LOAD
# =========================
uploaded = st.file_uploader("Upload CSV", type=["csv"])

if uploaded:
    df = validate_df(pd.read_csv(uploaded))
else:
    df = pd.DataFrame(DEFAULT_CITIES)

points = df.to_dict("records")
weather = fetch_weather(points)
data = pd.DataFrame(weather)

# =========================
# SIDEBAR
# =========================
st.sidebar.title("Controls")

selected = st.sidebar.selectbox("Select City for Trend", data["name"])

# =========================
# HEATMAP LAYER
# =========================
heatmap = pdk.Layer(
    "HeatmapLayer",
    data=data,
    get_position='[lon, lat]',
    get_weight="temperature",
    radiusPixels=60,
)

# =========================
# SCATTER LAYER
# =========================
scatter = pdk.Layer(
    "ScatterplotLayer",
    data=data,
    get_position='[lon, lat]',
    get_radius="temperature * 3000",
    get_fill_color='[255, 50, 50, 160]',
    pickable=True,
)

# =========================
# COUNTRY LAYER (pseudo polygon)
# =========================
country_layer = pdk.Layer(
    "ScatterplotLayer",
    data=COUNTRY_DATA,
    get_position='[lon, lat]',
    get_radius=300000,
    get_fill_color='[50, 50, 200, 60]',
    pickable=True,
)

# =========================
# MAP
# =========================
tooltip = {
    "html": "<b>{name}</b><br/>Temp: {temperature}°C",
    "style": {"backgroundColor": "black", "color": "white"},
}

st.pydeck_chart(pdk.Deck(
    layers=[heatmap, scatter, country_layer],
    initial_view_state=pdk.ViewState(latitude=20, longitude=0, zoom=1.2),
    tooltip=tooltip
))

# =========================
# TREND CHART
# =========================
st.subheader("📈 24h Temperature Trend")

trend_data = data[data["name"] == selected]["trend"].values[0]
if trend_data:
    trend_df = pd.DataFrame({"temp": trend_data})
    st.line_chart(trend_df)
else:
    st.warning("No trend data")

# =========================
# TABLE
# =========================
st.subheader("📊 Data")
st.dataframe(data)
