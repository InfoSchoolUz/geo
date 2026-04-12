import streamlit as st
from streamlit_folium import st_folium
import folium
import requests
import pandas as pd
import random
import wikipedia

# --- 1. SAHIFA SOZLAMALARI ---
st.set_page_config(
    page_title="Dunyo Ma'lumotlari Paneli",
    page_icon="🌍",
    layout="wide"
)

# Wikipedia tilini o'zbekchaga sozlash
wikipedia.set_lang("uz")

# --- 2. MA'LUMOTLARNI YUKLASH (XATOLIKDAN HIMOYALANGAN) ---
@st.cache_data(ttl=86400)
def fetch_global_data():
    url = "https://restcountries.com/v3.1/all"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if not isinstance(data, list):
            raise ValueError("API noto'g'ri formatda ma'lumot qaytardi")
            
        countries_map = {}
        for c in data:
            # O'zbekcha nomini olish (API'dan translations -> uzb)
            uz_name = c.get("translations", {}).get("uzb", {}).get("common")
            en_name = c.get("name", {}).get("common")
            display_name = uz_name if uz_name else en_name
            
            if display_name and "latlng" in c:
                countries_map[display_name] = c
                countries_map[display_name]['en_name_ref'] = en_name
                
        return countries_map, sorted(list(countries_map.keys()))
    
    except Exception as e:
        # API xato bersa, zaxira (fallback) ma'lumot qaytaramiz
        st.warning(f"API ma'lumotlarini yuklashda muammo: {e}. Zaxira rejimi ishga tushdi.")
        fallback = {
            "Oʻzbekiston": {
                "latlng": [41.0, 64.0],
                "en_name_ref": "Uzbekistan",
                "capital": ["Toshkent"],
                "population": 36000000,
                "area": 448978,
                "region": "Osiyo",
                "flags": {"png": "https://flagcdn.com/w320/uz.png"},
                "currencies": {"UZS": {"name": "O'zbek so'mi", "symbol": "so'm"}},
                "languages": {"uzb": "O'zbek tili"}
            }
        }
        return fallback, ["Oʻzbekiston"]

COUNTRIES_DB, COUNTRY_NAMES = fetch_global_data()

# --- 3. WIKIPEDIA FUNKSIYASI ---
@st.cache_data(ttl=86400)
def get_wiki_summary(uz_name, en_name):
    try:
        wikipedia.set_lang("uz")
        return wikipedia.summary(uz_name, sentences=3)
    except:
        try:
            wikipedia.set_lang("en")
            return wikipedia.summary(en_name, sentences=3)
        except:
            return "Ushbu davlat haqida Wikipedia ma'lumoti topilmadi."

# --- 4. SESSION STATE (HOLATNI BOSHQARISH) ---
if 'selected_country' not in st.session_state:
    if "Oʻzbekiston" in COUNTRY_NAMES:
        st.session_state.selected_country = "Oʻzbekiston"
    elif COUNTRY_NAMES:
        st.session_state.selected_country = COUNTRY_NAMES[0]
    else:
        st.session_state.selected_country = None

# --- 5. SIDEBAR (YON PANEL) ---
with st.sidebar:
    st.title("🗺 Dunyo Intelligence")
    st.markdown("---")
    
    if COUNTRY_NAMES:
        choice = st.selectbox(
            "Davlatni tanlang:",
            COUNTRY_NAMES,
            index=COUNTRY_NAMES.index(st.session_state.selected_country) if st.session_state.selected_country in COUNTRY_NAMES else 0
        )
        
        if choice != st.session_state.selected_country:
            st.session_state.selected_country = choice
            st.rerun()
    
    st.info("💡 Maslahat: Xaritadagi nuqtalarni bosib ham davlatni o'zgartirishingiz mumkin.")
    st.markdown("Developed by **Azamat Madrimov** 🚀")

# --- 6. ASOSIY INTERFEYS ---
if not st.session_state.selected_country:
    st.error("Ma'lumotlar mavjud emas.")
    st.stop()

st.title(f"🌍 {st.session_state.selected_country} bo'yicha tahlil")

col_left, col_right = st.columns([1.8, 1.2], gap="large")

with col_left:
    # Xarita
    current_data = COUNTRIES_DB.get(st.session_state.selected_country)
    m = folium.Map(
        location=current_data["latlng"], 
        zoom_start=4, 
        tiles="cartodb dark_matter"
    )
    
    # Barcha davlat nuqtalarini chizish
    for name, d in COUNTRIES_DB.items():
        is_selected = (name == st.session_state.selected_country)
        folium.CircleMarker(
            location=d["latlng"],
            radius=6 if is_selected else 3,
            color="#00f2ff" if is_selected else "#475569",
            fill=True,
            fill_opacity=0.7,
            popup=name
        ).add_to(m)

    map_res = st_folium(m, height=500, width="100%", key="main_map")

    # Xaritadan bosilganda tanlovni yangilash
    if map_res.get("last_object_clicked"):
        lat = map_res["last_object_clicked"]["lat"]
        lon = map_res["last_object_clicked"]["lng"]
        closest = min(COUNTRIES_DB.keys(), 
                      key=lambda n: (COUNTRIES_DB[n]["latlng"][0]-lat)**2 + (COUNTRIES_DB[n]["latlng"][1]-lon)**2)
        
        if closest != st.session_state.selected_country:
            st.session_state.selected_country = closest
            st.rerun()

with col_right:
    # Ma'lumotlar jadvali
    st.image(current_data.get("flags", {}).get("png"), width=150)
    st.subheader("📊 Asosiy ko'rsatkichlar")
    
    curr_info = current_data.get("currencies", {})
    valyuta = ", ".join([f"{v.get('name')} ({v.get('symbol')})" for v in curr_info.values()]) if curr_info else "Noma'lum"
    tillar = ", ".join(current_data.get("languages", {}).values()) if current_data.get("languages") else "Noma'lum"
    
    # Demo ma'lumotlar uchun seed
    random.seed(hash(st.session_state.selected_country))
    df_data = {
        "Ko'rsatkich": ["🏙 Poytaxt", "👥 Aholi", "📏 Maydon", "💰 Valyuta", "🗣 Tillar", "🌍 Mintaqa"],
        "Qiymat": [
            current_data.get("capital", ["Noma'lum"])[0],
            f"{current_data.get('population', 0):,}",
            f"{current_data.get('area', 0):,} km²",
            valyuta,
            tillar,
            current_data.get("region", "Noma'lum")
        ]
    }
    st.table(pd.DataFrame(df_data))

# --- 7. WIKIPEDIA MATNI ---
st.markdown("---")
st.subheader("📖 Vikipediya ma'lumoti")
with st.spinner("Wikipedia'dan yuklanmoqda..."):
    summary = get_wiki_summary(st.session_state.selected_country, current_data.get('en_name_ref', ''))
    st.write(summary)

st.markdown(f"*[Batafsil Wikipedia'da o'qing](https://uz.wikipedia.org/wiki/{st.session_state.selected_country.replace(' ', '_')})*")
