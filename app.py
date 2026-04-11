import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import pandas as pd
import feedparser
from bs4 import BeautifulSoup

st.set_page_config(layout="wide", page_title="🌍 Global Davlatlar Platformasi")

# ================= API =================
@st.cache_data
def load_countries():
    try:
        res = requests.get("https://restcountries.com/v3.1/all", timeout=10)
        data = res.json()

        countries = []
        for d in data:
            try:
                # 💰 VALYUTA (nom + kod + belgi)
                curr = d.get("currencies", {})
                if curr:
                    code = list(curr.keys())[0]
                    val = curr[code]
                    name = val.get("name", "")
                    symbol = val.get("symbol", "")
                    currency = f"{name} ({code}) {symbol}"
                else:
                    currency = "Noma'lum"

                countries.append({
                    "nom": d["name"]["common"],
                    "kod": d["cca2"].lower(),
                    "poytaxt": d.get("capital", ["Noma'lum"])[0],
                    "mintaqa": d.get("region", "Boshqa"),
                    "lat": d["latlng"][0],
                    "lon": d["latlng"][1],
                    "aholi": d.get("population", 0),
                    "maydon": d.get("area", 0),
                    "til": ", ".join(d.get("languages", {}).values()) if d.get("languages") else "Noma'lum",
                    "valyuta": currency,
                })
            except:
                continue

        return countries
    except:
        return []

countries = load_countries()

# ================= FORMAT =================
for c in countries:
    c["aholi_fmt"] = f"{round(c['aholi']/1e6,2)} mln"
    c["maydon_fmt"] = f"{c['maydon']:,.0f} km²"
    c["zichlik"] = round(c["aholi"]/c["maydon"],1) if c["maydon"] else 0

# ================= WIKIPEDIA =================
@st.cache_data
def get_prezident(davlat):
    try:
        url = f"https://en.wikipedia.org/wiki/{davlat.replace(' ', '_')}"
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        infobox = soup.find("table", {"class": "infobox"})
        rows = infobox.find_all("tr")

        for row in rows:
            th = row.find("th")
            if th:
                txt = th.text.lower()
                if "president" in txt or "prime minister" in txt:
                    return row.find("td").text.strip()

        return "Topilmadi"
    except:
        return "Xato"

# ================= STATIC =================
DEEP = {
    "Japan": {"zilzila":"Yuqori","nizo":"Xitoy"},
    "Turkey": {"zilzila":"Yuqori","nizo":"Suriya"},
    "Ukraine": {"zilzila":"Past","nizo":"Rossiya"},
    "Uzbekistan": {"zilzila":"O‘rta","nizo":"Yo‘q"},
}

# ================= NEWS =================
@st.cache_data(ttl=600)
def get_news(country):
    url = f"https://news.google.com/rss/search?q={country}"
    feed = feedparser.parse(url)
    return [(e.title, e.link) for e in feed.entries[:5]]

# ================= SIDEBAR =================
with st.sidebar:
    st.markdown("## 🌍 Filtr")
    regions = sorted(set(c["mintaqa"] for c in countries))
    sel = st.selectbox("Mintaqa", ["Barchasi"] + regions)

    st.markdown("---")
    comp = st.checkbox("⚖️ Taqqoslash")

    if comp:
        names = [c["nom"] for c in countries]
        c1 = st.selectbox("1-davlat", names)
        c2 = st.selectbox("2-davlat", names, index=1)

# ================= MAP =================
st.title("🌍 Global Davlatlar Platformasi")
st.caption("Davlatni xaritada bosing")

filtered = [c for c in countries if sel=="Barchasi" or c["mintaqa"]==sel]

m = folium.Map(location=[20,0], zoom_start=2, tiles="CartoDB dark_matter")

for c in filtered:
    folium.CircleMarker([c["lat"],c["lon"]], radius=5, color="#00e5ff", fill=True).add_to(m)

map_data = st_folium(m, width="100%", height=500, returned_objects=["last_object_clicked"])

# ================= COMPARE =================
if comp:
    a = next((x for x in countries if x["nom"]==c1), None)
    b = next((x for x in countries if x["nom"]==c2), None)

    col1, col2 = st.columns(2)

    def show(c, col):
        with col:
            st.image(f"https://flagcdn.com/w160/{c['kod']}.png")
            st.subheader(c["nom"])
            st.write("Poytaxt:", c["poytaxt"])
            st.write("Aholi:", c["aholi_fmt"])
            st.write("Valyuta:", c["valyuta"])

    show(a, col1)
    show(b, col2)
    st.stop()

# ================= DETAIL =================
if map_data and map_data.get("last_object_clicked"):
    lat = map_data["last_object_clicked"]["lat"]
    lon = map_data["last_object_clicked"]["lng"]

    c = min(filtered, key=lambda x:(x["lat"]-lat)**2+(x["lon"]-lon)**2)

    st.image(f"https://flagcdn.com/w320/{c['kod']}.png")
    st.header(c["nom"])

    prezident = get_prezident(c["nom"])

    extra = DEEP.get(c["nom"], {})
    zilzila = extra.get("zilzila","Noma'lum")
    nizo = extra.get("nizo","Noma'lum")

    df = pd.DataFrame({
        "Ko‘rsatkich":[
            "Poytaxt","Aholi","Maydon","Zichlik",
            "Til","Valyuta","Prezident"
        ],
        "Qiymat":[
            c["poytaxt"],c["aholi_fmt"],c["maydon_fmt"],
            f"{c['zichlik']}/km²",
            c["til"],c["valyuta"],prezident
        ]
    })

    st.table(df)

    st.markdown("### 🌋 Xavf va nizo")
    st.error(f"Zilzila: {zilzila}")
    st.warning(f"Nizo: {nizo}")

    st.markdown("### 📰 Yangiliklar")
    for t,l in get_news(c["nom"]):
        st.markdown(f"- [{t}]({l})")

else:
    st.info("👉 Xarita ustida davlatni bosing")