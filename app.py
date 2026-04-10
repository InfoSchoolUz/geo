# app.py
import streamlit as st
import pandas as pd
import pydeck as pdk

st.set_page_config(page_title="Global Employees Map", layout="wide")

# ======================
# SAMPLE DATA (extendable)
# ======================
data = pd.DataFrame([
    {"name": "Germany", "lat": 51.1657, "lon": 10.4515, "employees": 102},
    {"name": "USA", "lat": 37.0902, "lon": -95.7129, "employees": 600},
    {"name": "Uzbekistan", "lat": 41.3775, "lon": 64.5853, "employees": 80},
    {"name": "Tashkent", "lat": 41.2995, "lon": 69.2401, "employees": 35},
    {"name": "Samarkand", "lat": 39.6542, "lon": 66.9597, "employees": 20},
    {"name": "Berlin", "lat": 52.5200, "lon": 13.4050, "employees": 60},
    {"name": "New York", "lat": 40.7128, "lon": -74.0060, "employees": 150},
])

# ======================
# UI
# ======================
st.title("🌍 Global Employees Interactive Map")
st.markdown("Hover over locations to see employee counts")

# ======================
# LAYER (interactive)
# ======================
layer = pdk.Layer(
    "ScatterplotLayer",
    data=data,
    get_position='[lon, lat]',
    get_radius="employees * 1000",
    get_fill_color='[255 - employees, 50, employees * 2]',
    pickable=True,
)

# ======================
# VIEW
# ======================
view_state = pdk.ViewState(
    latitude=30,
    longitude=0,
    zoom=1.5,
    pitch=0,
)

# ======================
# TOOLTIP
# ======================
tooltip = {
    "html": "<b>{name}</b><br/>Employees: {employees}",
    "style": {"backgroundColor": "black", "color": "white"}
}

# ======================
# MAP RENDER
# ======================
st.pydeck_chart(pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip=tooltip
))

# ======================
# OPTIONAL TABLE VIEW
# ======================
with st.expander("📊 Data Table"):
    st.dataframe(data)

# ======================
# ADD DATA UI
# ======================
st.subheader("➕ Add New Location")

with st.form("add_data"):
    name = st.text_input("Location Name")
    lat = st.number_input("Latitude", format="%.6f")
    lon = st.number_input("Longitude", format="%.6f")
    employees = st.number_input("Employees", min_value=1)

    submitted = st.form_submit_button("Add")

    if submitted:
        new_row = pd.DataFrame([{
            "name": name,
            "lat": lat,
            "lon": lon,
            "employees": employees
        }])
        data = pd.concat([data, new_row], ignore_index=True)
        st.success("Added successfully! Refresh to see update.")
