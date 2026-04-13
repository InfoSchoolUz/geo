import folium
from streamlit_folium import st_folium

def render_map(data, active):
    center = [20, 0]
    zoom = 2

    if active:
        center = [active["latitude"], active["longitude"]]
        zoom = 5

    m = folium.Map(location=center, zoom_start=zoom)

    for c in data:
        lat, lon = c.get("latitude"), c.get("longitude")
        if not lat or not lon:
            continue

        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            tooltip=c["name"]
        ).add_to(m)

    return st_folium(m, height=450)
