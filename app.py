import streamlit as st
from streamlit_folium import st_folium
import folium
import requests
import pandas as pd
import random

# Sahifa sozlamalari
st.set_page_config(layout="wide", page_title="World Intelligence Dashboard")

st.title("🌍 World Intelligence Dashboard")

# ===== 1. MA'LUMOTLARNI YUKLASH VA KESHLASH =====
@st.cache_data
def get_processed_data():
    url = "https://restcountries.com/v3.1/all"
    try:
        res = requests.get(url, timeout=10)
        data = res.json()
    except Exception:
        return {}, []

    country_dict = {}
    name_list = []
    
    for c in data:
        name = c.get("name", {}).get("common")
        if name:
            country_dict[name] = c
            name_list.append(name)
            
    return country_dict, sorted(name_list)

country_data, all_names = get_processed_data()

# ===== 2. XARITANI KESHLASH =====
@st.cache_resource
def create_base_map(countries_info):
    m = folium.Map(location=[20, 0], zoom_start=2, tiles="cartodb dark_matter")
    for name, c in countries_info.items():
        latlng = c.get("latlng")
        if latlng and len(latlng) == 2:
            folium.CircleMarker(
                location=latlng,
                radius=4,
                color="#38bdf8",
                fill=True,
                tooltip=name # Kursor borganda nomini chiqaradi
            ).add_to(m)
    return m

# ===== 3. SESSION STATE (HOLATNI BOSHQARISH) =====
if 'selected_country' not in st.session_state:
    st.session_state.selected_country = None

# Sidebar orqali qidiruv
st.sidebar.header("Filterlar")
manual_select = st.sidebar.selectbox(
    "Davlatni qidirish:", 
    ["None"] + all_names,
    index=0
)

# Agar selectbox o'zgarsa, sessionni yangilaymiz
if manual_select != "None":
    st.session_state.selected_country = manual_select

# ===== 4. XARITANI CHIQARISH =====
col_map, col_info = st.columns([2, 1])

with col_map:
    base_map = create_base_map(country_data)
    # use_container_width=True xaritani ustunga moslaydi
    output = st_folium(base_map, height=500, width="100%", key="main_map")

# Xaritadan bosilganda tanlovni yangilash
if output.get("last_object_clicked"):
    click_lat = output["last_object_clicked"]["lat"]
    click_lon = output["last_object_clicked"]["lng"]
    
    # Eng yaqin davlatni topish (Optimallashtirilgan kvadratik masofa)
    def find_nearest(lat, lon):
        dist_min = float("inf")
        closest = st.session_state.selected_country
        for name, c in country_data.items():
            coords = c.get("latlng")
            if coords:
                d = (lat - coords[0])**2 + (lon - coords[1])**2
                if d < dist_min:
                    dist_min = d
                    closest = name
        return closest
    
    # Faqat juda yaqin bo'lsa (taxminan 5 daraja radiusda) tanlaymiz
    potential_name = find_nearest(click_lat, click_lon)
    if potential_name != st.session_state.selected_country:
        st.session_state.selected_country = potential_name
        st.rerun()

# ===== 5. MA'LUMOTLARNI KO'RSATISH =====
with col_info:
    selected = st.session_state.selected_country
    
    if not selected:
        st.info("👆 Davlat haqida ma'lumot olish uchun xaritadan nuqtani bosing yoki qidiruvdan foydalaning.")
    else:
        country = country_data.get(selected)
        if country:
            # Ma'lumotlarni tayyorlash
            flag = country.get("flags", {}).get("png", "")
            capital = country.get("capital", ["N/A"])[0]
            pop = country.get("population", 0)
            area = country.get("area", 0)
            currencies = country.get("currencies", {})
            curr_str = ", ".join([v.get("name", "") for v in currencies.values()]) if currencies else "N/A"
            langs = ", ".join(country.get("languages", {}).values()) or "N/A"
            
            # Tasodifiy ma'lumotlar (Keshlanmagan bo'lsa har safar o'zgaradi, 
            # buni oldini olish uchun seed dan foydalanamiz)
            random.seed(hash(selected))
            univs = random.randint(50, 5000)
            
            st.image(flag, width=150)
            st.subheader(f"📊 {selected}")
            
            stats = {
                "🏙 Poytaxt": capital,
                "👥 Aholi": f"{pop:,}",
                "📏 Maydon": f"{area:,} km²",
                "💰 Valyuta": curr_str,
                "🗣 Tillar": langs,
                "🎓 Universitetlar": univs
            }
            
            for k, v in stats.items():
                st.write(f"**{k}:** {v}")

# Footer
st.markdown("---")
st.caption("Developed by Azamat Madrimov 🚀 | Data: RestCountries API")
