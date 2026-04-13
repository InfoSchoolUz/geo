import streamlit as st
import folium
from streamlit_folium import st_folium
import requests

# 1. SAHIFA SOZLAMALARI
st.set_page_config(
    page_title="Global Country Data Pro",
    layout="wide",
    page_icon="🌍"
)

# Custom CSS dizayn
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');
html, body, [class*="css"] { font-family: 'Sora', sans-serif; }
.stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%); color: #e2e8f0; }
.hero-title { text-align: center; font-size: 2.6rem; font-weight: 700; background: linear-gradient(90deg, #38bdf8, #818cf8, #f472b6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.2rem; }
.hero-sub { text-align: center; color: #64748b; font-size: 0.95rem; margin-bottom: 2rem; font-family: 'JetBrains Mono', monospace; }
[data-testid="stMetric"] { background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 14px; padding: 18px 22px; backdrop-filter: blur(8px); }
.info-card { background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(129, 140, 248, 0.25); border-radius: 16px; padding: 24px; backdrop-filter: blur(10px); }
.info-row { display: flex; align-items: center; gap: 10px; padding: 9px 0; border-bottom: 1px solid rgba(255,255,255,0.05); font-size: 0.92rem; }
.info-label { color: #64748b; min-width: 160px; font-size: 0.78rem; text-transform: uppercase; }
.badge { background: rgba(56, 189, 248, 0.15); color: #38bdf8; font-size: 0.72rem; padding: 2px 10px; border-radius: 999px; }
</style>
""", unsafe_allow_html=True)

# 2. MA'LUMOTLAR BAZASI (Lug'atlar birlashtirildi)
PRESIDENTS_DB = {
    "Uzbekistan": ("Shavkat Mirziyoyev", "2016 – hozir"),
    "Kazakhstan": ("Qasım-Jomart Toqayev", "2019 – hozir"),
    "USA": ("Donald Trump", "2025 – hozir"),
    "Russia": ("Vladimir Putin", "2000 – hozir"),
    "Turkey": ("Recep Tayyip Erdoğan", "2014 – hozir"),
    "Ethiopia": ("Sahle-Work Zewde", "2018 – hozir"),
    "Kenya": ("William Ruto", "2022 – hozir"),
    "Ghana": ("John Mahama", "2025 – hozir"),
    "Tanzania": ("Samia Suluhu Hassan", "2021 – hozir"),
    "Uganda": ("Yoweri Museveni", "1986 – hozir"),
    "Zimbabwe": ("Emmerson Mnangagwa", "2017 – hozir"),
    "Morocco": ("Muhammad VI (Qirol)", "1999 – hozir"),
    "Algeria": ("Abdelmadjid Tebboune", "2019 – hozir"),
    "Tunisia": ("Kais Saied", "2019 – hozir"),
    "Libya": ("Muhammad al-Menfi", "2021 – hozir"),
    "Sudan": ("Abdel Fattah al-Burhan", "2021 – hozir"),
    "Somalia": ("Hassan Sheikh Mohamud", "2022 – hozir"),
    "Senegal": ("Bassirou Diomaye Faye", "2024 – hozir"),
    "Cameroon": ("Paul Biya", "1982 – hozir"),
    "Ivory Coast": ("Alassane Ouattara", "2011 – hozir"),
    "Rwanda": ("Paul Kagame", "2000 – hozir"),
    "Democratic Republic of the Congo": ("Félix Tshisekedi", "2019 – hozir"),
    "Mozambique": ("Daniel Chapo", "2025 – hozir"),
    "Angola": ("João Lourenço", "2017 – hozir"),
    "Australia": ("Anthony Albanese (Bosh vazir)", "2022 – hozir"),
    "New Zealand": ("Christopher Luxon (Bosh vazir)", "2023 – hozir"),
    "United Kingdom": ("Keir Starmer (Bosh vazir)", "2024 – hozir"),
}

GDP_DATA = {
    "United States": 27360, "China": 17794, "Germany": 4456, "Japan": 4213,
    "India": 3737, "United Kingdom": 3079, "France": 2924, "Italy": 2255,
    "Brazil": 2174, "Canada": 2140, "Russia": 1862, "South Korea": 1709,
    "Uzbekistan": 90, "Kazakhstan": 261, "Ethiopia": 155, "Kenya": 114,
    "Morocco": 141, "Ghana": 72, "Tanzania": 79,
}

# 3. API BILAN BOG'LANISH (Filtr qo'shildi - 400 xatosini oldini olish uchun)
@st.cache_data(ttl=3600)
def get_all_data():
    # Faqat kerakli maydonlarni so'raymiz (max 10-12 ta)
    f = "name,capital,population,area,region,subregion,flags,coatOfArms,currencies,languages,latlng,unMember"
    url = f"https://restcountries.com/v3.1/all?fields={f}"
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        resp = requests.get(url, headers=headers, timeout=15)
        if resp.status_code == 200:
            return resp.json()
    except:
        return None
    return None

data = get_all_data()

# 4. SIDEBAR
with st.sidebar:
    st.markdown('<div style="font-size:3rem; text-align:center;">🌍</div>', unsafe_allow_html=True)
    if data:
        countries_list = sorted([c['name']['common'] for c in data])
        selected_country = st.selectbox("🔍 Davlatni tanlang", countries_list, index=countries_list.index("Uzbekistan") if "Uzbekistan" in countries_list else 0)
    else:
        st.error("API ulanmadi")
        st.stop()

# 5. ASOSIY KONTENT
st.markdown('<h1 class="hero-title">🌍 Dunyo Davlatlari Explorer</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-sub">real-time · 250+ davlat · to\'liq statistika</p>', unsafe_allow_html=True)

c = next((item for item in data if item["name"]["common"] == selected_country), None)

if c:
    # Ma'lumotlarni ajratish
    poytaxt = c.get('capital', ["Noma'lum"])[0] if c.get('capital') else "Noma'lum"
    aholi = c.get('population', 0)
    maydon = c.get('area', 0)
    lat, lon = c.get('latlng', [0, 0])
    
    col1, col2, col3 = st.columns([1, 1, 2.8])
    with col1:
        st.image(c.get('flags', {}).get('png', ""), use_container_width=True, caption="Bayroq")
    with col2:
        gerb = c.get('coatOfArms', {}).get('png')
        if gerb: st.image(gerb, use_container_width=True, caption="Gerb")
    
    with col3:
        prez, muddat = PRESIDENTS_DB.get(selected_country, ("Ma'lumot yo'q", "—"))
        gdp_val = GDP_DATA.get(selected_country)
        gdp_text = f"${gdp_val:,} mlrd" if gdp_val else "Ma'lumot yo'q"

        st.markdown(f"""
        <div class="info-card">
            <h2>📍 {selected_country}</h2>
            <div class="info-row"><span class="info-label">👤 Prezident</span><span class="info-value">{prez}</span></div>
            <div class="info-row"><span class="info-label">🏛️ Poytaxt</span><span class="info-value">{poytaxt}</span></div>
            <div class="info-row"><span class="info-label">🌐 Mintaqa</span><span class="info-value">{c.get('region')} <span class="badge">{c.get('subregion', '')}</span></span></div>
            <div class="info-row"><span class="info-label">💰 YaIM (GDP)</span><span class="info-value">{gdp_text}</span></div>
            <div class="info-row"><span class="info-label">🇺🇳 BMT a'zosi</span><span class="info-value">{'✅ Ha' if c.get('unMember') else '❌ Yo\'q'}</span></div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    # Metrikalar
    m1, m2, m3 = st.columns(3)
    m1.metric("👥 Aholi", f"{aholi:,}")
    m2.metric("📐 Maydon", f"{maydon:,.0f} km²")
    m3.metric("🏘️ Zichlik", f"{aholi/maydon:.1f} /km²" if maydon else "0")

    # Tablar
    t1, t2, t3 = st.tabs(["🗺️ Xarita", "🎓 Ta'lim", "🚜 Agro"])
    with t1:
        m = folium.Map(location=[lat, lon], zoom_start=5, tiles="CartoDB dark_matter")
        folium.Marker([lat, lon], popup=selected_country).add_to(m)
        st_folium(m, width="100%", height=400)
    
    with t2:
        st.subheader("🎓 Ta'lim statistikasi (Taxminiy)")
        st.metric("🏛️ Universitetlar", f"~{max(1, int(aholi/400000)):,}")
        st.metric("🏫 Maktablar", f"~{max(1, int(aholi/3000)):,}")

    with t3:
        st.subheader("🚜 Qishloq xo'jaligi salohiyati")
        st.metric("🌾 Ekin maydoni", f"~{int(maydon*0.35):,} km²")
        st.info(f"Mintaqa: {c.get('region')}")

st.markdown("---")
st.markdown('<p style="text-align:center; color:#475569; font-size:0.8rem;">Global Country Data Pro · InfoSchoolUz</p>', unsafe_allow_html=True)
