# app.py
import streamlit as st
import pandas as pd
import pydeck as pdk
import requests
from datetime import datetime, timedelta

st.set_page_config(page_title="🌍 Global Events Map (Earthquakes + Conflicts)", layout="wide")

# =========================
# CONFIG (no API keys)
# =========================
USGS_FEED = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.geojson"
# ACLED public export (CSV). If it fails, we fallback gracefully.
ACLED_CSV = "https://api.acleddata.com/acled/read?format=csv"

# =========================
# HELPERS
# =========================
def safe_get_json(url, timeout=20):
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        return r.json()
    except Exception:
        return None

def safe_get_csv(url, timeout=20):
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        return pd.read_csv(pd.io.common.BytesIO(r.content))
    except Exception:
        return pd.DataFrame()

# =========================
# LOADERS (cached)
# =========================
@st.cache_data(ttl=300)
def load_earthquakes():
    js = safe_get_json(USGS_FEED)
    rows = []
    if js and "features" in js:
        for f in js["features"]:
            prop = f.get("properties", {})
            geom = f.get("geometry", {})
            coords = geom.get("coordinates", [None, None, None])
            lon, lat = coords[0], coords[1]
            mag = prop.get("mag")
            place = prop.get("place")
            time_ms = prop.get("time")
            if lat is None or lon is None or mag is None:
                continue
            t = datetime.utcfromtimestamp(time_ms/1000) if time_ms else None
            rows.append({
                "lat": lat,
                "lon": lon,
                "magnitude": float(mag),
                "place": place,
                "time": t
            })
    return pd.DataFrame(rows)

@st.cache_data(ttl=600)
def load_conflicts():
    df = safe_get_csv(ACLED_CSV)
    # Normalize minimal columns if present
    if df.empty:
        return pd.DataFrame(columns=["latitude","longitude","event_type","fatalities","event_date","country"])
    cols = {c.lower(): c for c in df.columns}
    # try to map common ACLED fields
    lat_c = cols.get("latitude")
    lon_c = cols.get("longitude")
    type_c = cols.get("event_type") or cols.get("event type")
    fat_c = cols.get("fatalities")
    date_c = cols.get("event_date") or cols.get("event date")
    country_c = cols.get("country")
    if not lat_c or not lon_c:
        return pd.DataFrame(columns=["latitude","longitude","event_type","fatalities","event_date","country"])
    out = pd.DataFrame({
        "lat": pd.to_numeric(df[lat_c], errors="coerce"),
        "lon": pd.to_numeric(df[lon_c], errors="coerce"),
        "event_type": df[type_c] if type_c in df else "Event",
        "fatalities": pd.to_numeric(df[fat_c], errors="coerce") if fat_c in df else 0,
        "event_date": pd.to_datetime(df[date_c], errors="coerce") if date_c in df else pd.NaT,
        "country": df[country_c] if country_c in df else ""
    }).dropna(subset=["lat","lon"])
    # keep last 30 days for clarity
    cutoff = datetime.utcnow() - timedelta(days=30)
    if "event_date" in out and out["event_date"].notna().any():
        out = out[out["event_date"] >= cutoff]
    return out

# =========================
# UI
# =========================
st.title("🌍 Global Events Map")
st.caption("Real-time earthquakes (USGS) + recent conflicts (ACLED public). No API keys.")

with st.sidebar:
    st.header("Filters")
    show_eq = st.toggle("Show Earthquakes", True)
    show_cf = st.toggle("Show Conflicts", True)

    mag_min = st.slider("Min Magnitude", 0.0, 8.0, 2.5, 0.1)
    fat_min = st.slider("Min Fatalities (conflicts)", 0, 500, 0, 5)

# =========================
# DATA
# =========================
eq = load_earthquakes()
cf = load_conflicts()

if show_eq and not eq.empty:
    eq = eq[eq["magnitude"] >= mag_min]

if show_cf and not cf.empty:
    cf = cf[cf["fatalities"].fillna(0) >= fat_min]

# =========================
# LAYERS
# =========================
layers = []

# Earthquakes layer (size by magnitude)
if show_eq and not eq.empty:
    eq_layer = pdk.Layer(
        "ScatterplotLayer",
        data=eq,
        get_position='[lon, lat]',
        get_radius="magnitude * 20000",
        get_fill_color='[255, 140, 0, 180]',  # orange
        pickable=True,
    )
    layers.append(eq_layer)

# Conflicts layer (size by fatalities)
if show_cf and not cf.empty:
    cf_layer = pdk.Layer(
        "ScatterplotLayer",
        data=cf,
        get_position='[lon, lat]',
        get_radius="max(20000, fatalities * 15000)",
        get_fill_color='[220, 20, 60, 180]',  # crimson
        pickable=True,
    )
    layers.append(cf_layer)

view = pdk.ViewState(latitude=20, longitude=0, zoom=1.2)

tooltip = {
    "html": """
    <b>{place}</b><br/>
    Magnitude: {magnitude}<br/>
    Time: {time}
    """,
    "style": {"backgroundColor": "black", "color": "white"}
}

# Separate tooltip for conflicts via Deck "getTooltip" limitation workaround:
# we include both fields; if missing, they render blank
tooltip["html"] += """
<br/><br/>
<b>{country}</b><br/>
Type: {event_type}<br/>
Fatalities: {fatalities}<br/>
Date: {event_date}
"""

st.pydeck_chart(pdk.Deck(layers=layers, initial_view_state=view, tooltip=tooltip))

# =========================
# KPIs
# =========================
c1, c2 = st.columns(2)
c1.metric("Earthquakes (filtered)", int(len(eq)) if show_eq else 0)
c2.metric("Conflicts (filtered)", int(len(cf)) if show_cf else 0)

# =========================
# TABLES
# =========================
with st.expander("📊 Earthquakes Data"):
    st.dataframe(eq.sort_values("magnitude", ascending=False), use_container_width=True)

with st.expander("📊 Conflicts Data"):
    st.dataframe(cf.sort_values("fatalities", ascending=False), use_container_width=True)
