import streamlit as st
import folium
from streamlit_folium import st_folium
import requests

# 1. Sahifa sozlamalari
st.set_page_config(page_title="Global Country Data Pro", layout="wide", page_icon="🌍")

# CSS dizayn - Vizual joziba uchun
st.markdown("""
    <style>
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
    h1 { color: #1e3a8a; text-align: center; }
    .stTabs [data-baseweb="tab"] { font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌍 Dunyo Davlatlari: To'liq Statistik Ma'lumotlar")

# 2. Ma'lumotlarni API orqali yuklash
@st.cache_data
def get_all_data():
    try:
        url = "https://restcountries.com/v3.1/all"
        response = requests.get(url)
        return response.json()
    except:
        return None

data = get_all_data()

if data:
    # Davlatlar ro'yxati
    countries_list = sorted([c['name']['common'] for c in data])
    st.sidebar.header("Qidiruv va Tanlov")
    selected_country = st.sidebar.selectbox("Davlatni tanlang:", countries_list, index=countries_list.index("Uzbekistan") if "Uzbekistan" in countries_list else 0)
    
    # Tanlangan davlat ma'lumotlari
    c = next(item for item in data if item["name"]["common"] == selected_country)
    
    # Xavfsiz o'zgaruvchilar (Xatolik chiqmasligi uchun)
    poytaxt_list = c.get('capital', ["Noma'lum"])
    poytaxt = poytaxt_list[0]
    aholi = c.get('population', 0)
    maydon = c.get('area', 0)
    mintaqa = c.get('region', "Noma'lum")
    sub_mintaqa = c.get('subregion', "Noma'lum")
    
    # 3. Yuqori qism: Ramzlar va Prezident
    col1, col2, col3 = st.columns([1, 1, 2])
    
    with col1:
        st.image(c['flags']['png'], use_container_width=True, caption="Davlat Bayrog'i")
    
    with col2:
        if 'coatOfArms' in c and 'png' in c['coatOfArms']:
            st.image(c['coatOfArms']['png'], use_container_width=True, caption="Davlat Gerbi")
        else:
            st.warning("Gerb topilmadi")
            
    with col3:
        # Prezidentlar bazasi
        presidents_db = {
            "Uzbekistan": "Shavkat Mirziyoyev",
            "USA": "Joe Biden",
            "Russia": "Vladimir Putin",
            "Turkey": "Recep Tayyip Erdoğan",
            "Kazakhstan": "Kassym-Jomart Tokayev",
            "Kyrgyzstan": "Sadyr Japarov",
            "Tajikistan": "Emomali Rahmon",
            "Turkmenistan": "Serdar Berdimuhamedov",
            "China": "Xi Jinping",
            "Germany": "Frank-Walter Steinmeier",
            "France": "Emmanuel Macron"
        }
        prezident = presidents_db.get(selected_country, "Ma'lumotlar bazada mavjud emas")
        
        st.subheader(f"📍 {selected_country}")
        st.write(f"👤 **Prezident:** {prezident}")
        st.write(f"🏛️ **Poytaxt:** {poytaxt}")
        st.write(f"🌐 **Mintaqa:** {mintaqa} ({sub_mintaqa})")

    st.markdown("---")

    # 4. Tablar orqali batafsil statistika
    t1, t2, t3, t4 = st.tabs(["🗺️ Xarita", "🎓 Ta'lim", "🚜 Qishloq Xo'jaligi", "💰 Moliya va Til"])

    with t1:
        lat, lon = c['latlng']
        m = folium.Map(location=[lat, lon], zoom_start=5)
        folium.Marker([lat, lon], popup=selected_country).add_to(m)
        st_folium(m, width=800, height=400)
        
        c_m1, c_m2 = st.columns(2)
        c_m1.metric("Aholi soni", f"{aholi:,} kishi")
        c_m2.metric("Yer maydoni", f"{maydon:,} km²")

    with t2:
        st.subheader("🎓 Ta'lim statistikasi (Aholi soniga ko'ra)")
        # Statistik hisob-kitoblar
        unis = max(1, int(aholi / 400000))
        schools = max(1, int(aholi / 3000))
        colleges = int(unis * 3)
        
        st.write(f"Ushbu davlatda taxminan quyidagicha ta'lim muassasalari mavjud:")
        st.metric("Universitetlar", f"~{unis:,}")
        st.metric("Kollej va Litseylar", f"~{colleges:,}")
        st.metric("Maktablar", f"~{schools:,}")

    with t3:
        st.subheader("🚜 Qishloq xo'jaligi salohiyati")
        unumi_yer = int(maydon * 0.35) # Taxminan 35% ekin maydoni
        st.write(f"**Taxminiy ekin maydonlari:** ~{unumi_yer:,} km²")
        
        m_products = {
            "Asia": "Paxta, Bug'doy, Guruch, Mevalar",
            "Europe": "Don mahsulotlari, Sut va Go'sht, Uzum",
            "Africa": "Kofe, Kakao, Banan, Shakarqamish",
            "Americas": "Makkajo'xori, Soya, Go'sht mahsulotlari"
        }
        st.success(f"**Asosiy yetishtiriladigan mahsulotlar:** {m_products.get(mintaqa, 'Don va poliz mahsulotlari')}")

    with t4:
        st.subheader("💰 Moliya va Muloqot")
        # Pul birligi
        if c.get('currencies'):
            cur_code = list(c.get('currencies').keys())[0]
            cur_name = c['currencies'][cur_code].get('name', "Noma'lum")
            cur_symbol = c['currencies'][cur_code].get('symbol', "")
            st.metric("Milliy valyuta", f"{cur_name} ({cur_code})", cur_symbol)
        else:
            st.write("Valyuta ma'lumoti topilmadi")
            
        # Tillar
        tillar = ", ".join(c.get('languages', {}).values()) if c.get('languages') else "Noma'lum"
        st.write(f"🗣️ **Rasmiy tillar:** {tillar}")
        
        # BMT
        bmt = "Ha" if c.get('unMember') else "Yo'q"
        st.write(f"🇺🇳 **BMT a'zosi:** {bmt}")

else:
    st.error("Xatolik: API'dan ma'lumot yuklab bo'lmadi. Internetni tekshiring.")
    
