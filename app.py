import streamlit as st
from streamlit_folium import st_folium
import folium
import requests
import pandas as pd
import random
import wikipedia

# --- SAHIFA SOZLAMALARI ---
st.set_page_config(
    page_title="Dunyo Ma'lumotlari Paneli",
    page_icon="🌍",
    layout="wide"
)

# Wikipedia tilini o'zbekchaga sozlash
wikipedia.set_lang("uz")

# --- MA'LUMOTLARNI YUKLASH (O'ZBEKCHA TRANSLATSIYA BILAN) ---
@st.cache_data(ttl=86400)
def fetch_global_data():
    url = "https://restcountries.com/v3.1/all"
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()
        
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
        st.error(f"Ma'lumotlarni yuklashda xatolik: {e}")
        return {}, []

COUNTRIES_DB, COUNTRY_NAMES = fetch_global_data()

@st.cache_data(ttl=86400)
def get_wiki_summary(uz_name, en_name):
    """Wikipedia'dan qisqacha ma'lumot olish"""
    try:
        wikipedia.set_lang("uz")
        return wikipedia.summary(uz_name, sentences=3)
    except:
        try:
            wikipedia.set_lang("en")
            return wikipedia.summary(en_name, sentences=3)
        except:
            return "Ushbu davlat haqida o'zbekcha Wikipedia ma'lumoti topilmadi."

# --- SESSION STATE (HOLATNI SAQLASH) ---
if 'selected_country' not in st.session_state:
    st.session_state.selected_country = "Oʻzbekiston" if "Oʻzbekiston" in COUNTRY_NAMES else COUNTRY_NAMES[0]

# --- SIDEBAR (YON PANEL) ---
with st.sidebar:
    st.title("🗺 Dunyo Intelligence")
    st.markdown("---")
    
    choice = st.selectbox(
        "Davlatni tanlang:",
        COUNTRY_NAMES,
        index=COUNTRY_NAMES.index(st.session_state.selected_country) if st.session_state.selected_country in COUNTRY_NAMES else 0
    )
    
    if choice != st.session_state.selected_country:
        st.session_state.selected_country = choice
        st.rerun()
    
    st.info("💡 Maslahat: Xaritadagi nuqtalarni bosib ham davlatni o'zgartirishingiz mumkin.")

# --- ASOSIY INTERFEYS ---
st.title(f"🌍 {st.session_state.selected_country} bo'yicha tahliliy ma'lumotlar")

col_left, col_right = st.columns([1.8, 1.2], gap="large")

with col_left:
    # Xarita qismi
    current_data = COUNTRIES_DB.get(st.session_state.selected_country)
    m = folium.Map(
        location=current_data["latlng"], 
        zoom_start=4, 
        tiles="cartodb dark_matter"
    )
    
    # Nuqtalarni xaritaga qo'shish
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

    map_data = st_folium(m, height=500, width="100%", key="main_map")

    # Xaritadan bosilganda tanlovni o'zgartirish
    if map_data.get("last_object_clicked"):
        lat = map_data["last_object_clicked"]["lat"]
        lon = map_data["last_object_clicked"]["lng"]
        
        closest = min(COUNTRIES_DB.keys(), 
                      key=lambda n: (COUNTRIES_DB[n]["latlng"][0]-lat)**2 + (COUNTRIES_DB[n]["latlng"][1]-lon)**2)
        
        if closest != st.session_state.selected_country:
            st.session_state.selected_country = closest
            st.rerun()

with col_right:
    if current_data:
        # Bayroq va Asosiy ma'lumotlar
        st.image(current_data.get("flags", {}).get("png"), width=180)
        
        # JADVAL KO'RINISHIDA MA'LUMOTLAR
        st.subheader("📊 Asosiy ko'rsatkichlar")
        
        # API ma'lumotlarini o'zbekchalashtirish
        curr_info = current_data.get("currencies", {})
        valyuta = ", ".join([f"{v.get('name')} ({v.get('symbol')})" for v in curr_info.values()]) if curr_info else "Noma'lum"
        tillar = ", ".join(current_data.get("languages", {}).values()) if current_data.get("languages") else "Noma'lum"
        
        # Tasodifiy demo ma'lumotlar (o'zgarmas seed bilan)
        random.seed(hash(st.session_state.selected_country))
        savodxonlik = random.randint(70, 99)
        internet_speed = random.randint(15, 200)

        df_data = {
            "Ko'rsatkich": [
                "🏙 Poytaxt", 
                "👥 Aholi soni", 
                "📏 Maydon", 
                "💰 Milliy valyuta", 
                "🗣 Rasmiy tillar",
                "🌍 Mintaqa",
                "📶 Internet tezligi",
                "🎓 Savodxonlik"
            ],
            "Qiymat": [
                current_data.get("capital", ["Noma'lum"])[0],
                f"{current_data.get('population', 0):,}",
                f"{current_data.get('area', 0):,} km²",
                valyuta,
                tillar,
                current_data.get("region", "Noma'lum"),
                f"{internet_speed} Mb/s (Demo)",
                f"{savodxonlik}% (Demo)"
            ]
        }
        
        st.table(pd.DataFrame(df_data))

# --- WIKIPEDIA VA FOOTER ---
st.markdown("---")
st.subheader("📖 Ensiklopedik ma'lumot (Wikipedia)")

with st.spinner("Wikipedia'dan o'zbekcha ma'lumotlar qidirilmoqda..."):
    wiki_text = get_wiki_summary(st.session_state.selected_country, current_data['en_name_ref'])
    st.write(wiki_text)

st.markdown("---")
st.caption(f"Ma'lumotlar manbasi: RestCountries API & Wikipedia. Ishlab chiquvchi: Azamat Madrimov 🚀")
