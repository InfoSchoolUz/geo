import streamlit as st

def compare_ui(name_map, names):
    st.markdown("## ⚔️ Compare")

    c1 = st.selectbox("1-davlat", names, key="c1")
    c2 = st.selectbox("2-davlat", names, key="c2")

    if c1 and c2:
        d1 = name_map[c1]
        d2 = name_map[c2]

        st.write(d1["population"], d2["population"])
