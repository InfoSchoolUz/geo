import streamlit as st
import folium
from streamlit_folium import st_folium
import requests

# ================= CONFIG =================
st.set_page_config(layout="wide", page_title="🌍 Global Davlatlar Platformasi")

# ================= API =================
@st.cache_data
def davlatlarni_yuklash():
    try:
        res = requests.get("https://restcountries.com/v3.1/all", timeout=10)
        data = res.json()

        davlatlar = []
        for d in data:
            try:
                davlatlar.append({
                    "nom": d["name"]["common"],
                    "kod": d["cca2"].lower(),
                    "poytaxt": d.get("capital", ["Noma'lum"])[0],
                    "mintaqa": d.get("region", "Boshqa"),
                    "lat": d["latlng"][0],
                    "lon": d["latlng"][1],
                    "aholi": f"{round(d.get('population',0)/1e6,1)} mln",
                    "maydon": f"{round(d.get('area',0),0)} km²",
                    "til": ", ".join(d.get("languages", {}).values()) if d.get("languages") else "Noma'lum",
                    "valyuta": ", ".join([v["name"] for v in d.get("currencies", {}).values()]) if d.get("currencies") else "Noma'lum",
                })
            except:
                continue

        return davlatlar
    except:
        return []

davlatlar = davlatlarni_yuklash()

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("## 🌍 Filtr")

    mintaqalar = sorted(set(d["mintaqa"] for d in davlatlar))
    tanlangan_mintaqa = st.selectbox("Mintaqa tanlang", ["Barchasi"] + mintaqalar)

    st.markdown("---")
    taqqoslash = st.checkbox("⚖️ 2 ta davlatni solishtirish")

    if taqqoslash:
        d1 = st.selectbox("1-davlat", [d["nom"] for d in davlatlar])
        d2 = st.selectbox("2-davlat", [d["nom"] for d in davlatlar], index=1)

    st.markdown("---")
    st.metric("Jami davlatlar", len(davlatlar))

# ================= TITLE =================
st.title("🌍 Global Davlatlar Platformasi")
st.caption("Interaktiv dunyo xaritasi")

# ================= MAP =================
filtrlangan = [d for d in davlatlar if tanlangan_mintaqa == "Barchasi" or d["mintaqa"] == tanlangan_mintaqa]

xarita = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB dark_matter")

for d in filtrlangan:
    folium.CircleMarker(
        [d["lat"], d["lon"]],
        radius=6,
        color="#00e5ff",
        fill=True
    ).add_to(xarita)

map_data = st_folium(xarita, width="100%", height=500, returned_objects=["last_object_clicked"])

# ================= TAQQOSLASH =================
if taqqoslash:
    col1, col2 = st.columns(2)

    def chiqar(d):
        st.image(f"https://flagcdn.com/w160/{d['kod']}.png")
        st.subheader(d["nom"])
        st.write("🏙 Poytaxt:", d["poytaxt"])
        st.write("👥 Aholi:", d["aholi"])
        st.write("📐 Maydon:", d["maydon"])
        st.write("🗣 Til:", d["til"])
        st.write("💰 Valyuta:", d["valyuta"])

    with col1:
        chiqar(next(d for d in davlatlar if d["nom"] == d1))

    with col2:
        chiqar(next(d for d in davlatlar if d["nom"] == d2))

    st.stop()

# ================= DETAIL =================
if map_data and map_data.get("last_object_clicked"):
    lat = map_data["last_object_clicked"]["lat"]
    lon = map_data["last_object_clicked"]["lng"]

    d = min(davlatlar, key=lambda x: (x["lat"]-lat)**2 + (x["lon"]-lon)**2)

    st.image(f"https://flagcdn.com/w320/{d['kod']}.png")
    st.header(d["nom"])

    st.write("🏙 Poytaxt:", d["poytaxt"])
    st.write("🌍 Mintaqa:", d["mintaqa"])
    st.write("👥 Aholi:", d["aholi"])
    st.write("📐 Maydon:", d["maydon"])
    st.write("🗣 Til:", d["til"])
    st.write("💰 Valyuta:", d["valyuta"])

else:
    st.info("👉 Xarita ustida davlatni bosing")
