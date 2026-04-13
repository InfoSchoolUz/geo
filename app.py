import streamlit as st
from services.api import fetch_data
from services.preprocess import preprocess
from components.map import render_map
from components.analytics import global_stats
from components.compare import compare_ui

st.set_page_config(layout="wide")

data = preprocess(fetch_data())
name_map = {c["name"]: c for c in data}
names = sorted(name_map.keys())

if "country" not in st.session_state:
    st.session_state.country = None

selected = st.selectbox("Davlat", ["—"] + names)

if selected != "—":
    st.session_state.country = selected

active = name_map.get(st.session_state.country)

map_data = render_map(data, active)

clicked = map_data.get("last_object_clicked_tooltip")
if clicked:
    st.session_state.country = clicked
    st.rerun()

# analytics
max_pop, max_area = global_stats(data)
st.write("Max population:", max_pop["name"])

# compare
compare_ui(name_map, names)
