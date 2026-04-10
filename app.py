# app.py
# Single-file, production-ready Streamlit app
# Global stats map: Population, Weather, GDP, Internet, CO2
# Data sources (no API key):
# - World Bank (population, GDP per capita, internet users)
# - Our World in Data (CO2)
# - Open-Meteo (current weather)

import io
import math
import requests
import pandas as pd
import streamlit as st
import pydeck as pdk

st.set_page_config(page_title="🌍 Global Stats Map (Real Data)", layout="wide")

# =========================
# CONFIG
# =========================
WORLD_GEOJSON_URL = "https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json"
WB_API = "https://api.worldbank.org/v2/country/all/indicator/{indicator}?date=2022&format=json&per_page=20000"
OWID_CO2_CSV = "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-data.csv"
OPEN_METEO = "https://api.open-meteo.com/v1/forecast"

INDICATORS = {
    "Population": "SP.POP.TOTL",
    "GDP per Capita (USD)": "NY.GDP.PCAP.CD",
    "Internet Users (%)": "IT.NET.USER.ZS",
}

METRICS = ["Population", "GDP per Capita (USD)", "Internet Users (%)", "CO2 (Mt)", "Temperature (°C)"]

# =========================
# HELPERS
# =========================
def clamp(x, lo, hi):
    return max(lo, min(hi, x))

def human_format(n):
    if n is None or (isinstance(n, float) and math.isnan(n)):
        return "—"
    n = float(n)
    for unit in ["", "K", "M", "B", "T"]:
        if abs(n) < 1000.0:
            return f"{n:.2f}{unit}"
        n /= 1000.0
    return f"{n:.2f}P"

# =========================
# DATA LOADERS (cached)
# =========================
@st.cache_data(ttl=3600)
def load_world_geojson():
    r = requests.get(WORLD_GEOJSON_URL, timeout=20)
    r.raise_for_status()
    return r.json()

@st.cache_data(ttl=3600)
def load_worldbank_indicator(indicator_code):
    url = WB_API.format(indicator=indicator_code)
    r = requests.get(url, timeout=20)
    r.raise_for_status()
    js = r.json()
    rows = []
    if isinstance(js, list) and len(js) > 1:
        for item in js[1]:
            rows.append({
                "iso3": item["countryiso3code"],
                "value": item["value"]
            })
    df = pd.DataFrame(rows)
    df = df.dropna()
    df = df[df["iso3"].str.len() == 3]
    return df

@st.cache_data(ttl=3600)
def load_owid_co2():
    r = requests.get(OWID_CO2_CSV, timeout=30)
    r.raise_for_status()
    df = pd.read_csv(io.StringIO(r.text))
    # latest available year per country
    df = df.sort_values(["iso_code", "year"]).groupby("iso_code", as_index=False).tail(1)
    df = df[["iso_code", "co2"]].rename(columns={"iso_code": "iso3", "co2": "value"})
    # convert to megatonnes (already Mt in OWID "co2")
    df = df.dropna()
    df = df[df["iso3"].str.len() == 3]
    return df

@st.cache_data(ttl=600)
def load_country_centroids(geojson):
    feats = geojson.get("features", [])
    rows = []
    for f in feats:
        iso3 = f["id"]
        coords = f["geometry"]["coordinates"]
        # centroid (approx) from polygon/multipolygon
        pts = []
        if f["geometry"]["type"] == "Polygon":
            for ring in coords:
                pts += ring
        elif f["geometry"]["type"] == "MultiPolygon":
            for poly in coords:
                for ring in poly:
                    pts += ring
        if pts:
            xs = [p[0] for p in pts]
            ys = [p[1] for p in pts]
            lon = sum(xs) / len(xs)
            lat = sum(ys) / len(ys)
            rows.append({"iso3": iso3, "lat": lat, "lon": lon})
    return pd.DataFrame(rows)

@st.cache_data(ttl=600)
def fetch_weather_for_points(points_df):
    if points_df.empty:
        return pd.DataFrame(columns=["iso3", "temperature"])
    lats = ",".join(points_df["lat"].round(4).astype(str))
    lons = ",".join(points_df["lon"].round(4).astype(str))
    params = {
        "latitude": lats,
        "longitude": lons,
        "current_weather": True,
        "timezone": "auto"
    }
    try:
        r = requests.get(OPEN_METEO, params=params, timeout=20)
        r.raise_for_status()
        js = r.json()
        cw = js.get("current_weather", [])
        temps = []
        for i in range(len(points_df)):
            t = None
            if isinstance(cw, list) and i < len(cw):
                t = cw[i].get("temperature")
            temps.append(t)
        out = points_df[["iso3"]].copy()
        out["value"] = temps
        return out.dropna()
    except Exception:
        return pd.DataFrame(columns=["iso3", "value"])

# =========================
# UI
# =========================
st.title("🌍 Global Statistics Map (Real Data, Single File)")
metric = st.sidebar.selectbox("Metric", METRICS, index=0)

# =========================
# LOAD BASE DATA
# =========================
geojson = load_world_geojson()

# base df with iso3 codes from geojson
base = pd.DataFrame([{"iso3": f["id"]} for f in geojson["features"]])

# load selected metric
if metric in INDICATORS:
    df_val = load_worldbank_indicator(INDICATORS[metric])
elif metric == "CO2 (Mt)":
    df_val = load_owid_co2()
elif metric == "Temperature (°C)":
    centroids = load_country_centroids(geojson)
    df_val = fetch_weather_for_points(centroids)
else:
    df_val = pd.DataFrame(columns=["iso3", "value"])

data = base.merge(df_val, on="iso3", how="left")

# normalize values for coloring
vals = data["value"].dropna()
vmin = float(vals.min()) if len(vals) else 0.0
vmax = float(vals.max()) if len(vals) else 1.0

def color_for(v):
    if v is None or (isinstance(v, float) and math.isnan(v)):
        return [200, 200, 200, 80]
    # normalize 0..1
    t = 0 if vmax == vmin else (float(v) - vmin) / (vmax - vmin)
    # blue -> red gradient
    r = int(255 * t)
    b = int(255 * (1 - t))
    return [r, 80, b, 180]

data["color"] = data["value"].apply(color_for)
data["label"] = data["value"].apply(human_format)

# =========================
# MAP (Choropleth)
# =========================
layer = pdk.Layer(
    "GeoJsonLayer",
    data=geojson,
    get_fill_color="properties.color",
    get_line_color=[50, 50, 50],
    line_width_min_pixels=0.5,
    pickable=True,
    auto_highlight=True,
)

# inject properties.color into geojson features
for f in geojson["features"]:
    iso3 = f["id"]
    row = data.loc[data["iso3"] == iso3]
    if len(row):
        f["properties"]["color"] = row.iloc[0]["color"]
        f["properties"]["label"] = row.iloc[0]["label"]
    else:
        f["properties"]["color"] = [200, 200, 200, 80]
        f["properties"]["label"] = "—"

view = pdk.ViewState(latitude=20, longitude=0, zoom=1.2)

tooltip = {
    "html": f"<b>{{name}}</b><br/>{metric}: {{label}}",
    "style": {"backgroundColor": "black", "color": "white"},
}

st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view,
    tooltip=tooltip
))

# =========================
# KPIs
# =========================
col1, col2, col3 = st.columns(3)
col1.metric("Countries (with data)", int(data["value"].notna().sum()))
col2.metric("Min", human_format(vmin))
col3.metric("Max", human_format(vmax))

# =========================
# TABLE
# =========================
st.subheader("📊 Data Table")
st.dataframe(data.sort_values("value", ascending=False), use_container_width=True)

# =========================
# DOWNLOAD
# =========================
csv = data.to_csv(index=False).encode("utf-8")
st.download_button("⬇ Download CSV", csv, "global_stats.csv", "text/csv")
