import streamlit as st
import folium
from streamlit_folium import st_folium
import requests

# ─────────────────────────────────────────────
# 1. SAHIFA SOZLAMALARI
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Global Country Data Pro",
    layout="wide",
    page_icon="🌍"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sora:wght@300;400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Sora', sans-serif;
}

/* ── Fon ── */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 50%, #0f172a 100%);
    color: #e2e8f0;
}

/* ── Sarlavha bloki ── */
.hero-title {
    text-align: center;
    font-size: 2.6rem;
    font-weight: 700;
    background: linear-gradient(90deg, #38bdf8, #818cf8, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
    letter-spacing: -0.5px;
}
.hero-sub {
    text-align: center;
    color: #64748b;
    font-size: 0.95rem;
    margin-bottom: 2rem;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Metrik kartalar ── */
[data-testid="stMetric"] {
    background: rgba(30, 41, 59, 0.8);
    border: 1px solid rgba(56, 189, 248, 0.2);
    border-radius: 14px;
    padding: 18px 22px;
    backdrop-filter: blur(8px);
    transition: transform 0.2s, border-color 0.2s;
}
[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    border-color: rgba(56, 189, 248, 0.6);
}
[data-testid="stMetricLabel"] { color: #94a3b8 !important; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 1px; }
[data-testid="stMetricValue"] { color: #38bdf8 !important; font-size: 1.55rem; font-weight: 700; font-family: 'JetBrains Mono', monospace; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0f172a 0%, #1e293b 100%);
    border-right: 1px solid rgba(56, 189, 248, 0.15);
}
[data-testid="stSidebar"] * { color: #cbd5e1 !important; }
[data-testid="stSidebar"] .stSelectbox label { color: #94a3b8 !important; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px; }

/* ── Info kartasi ── */
.info-card {
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(129, 140, 248, 0.25);
    border-radius: 16px;
    padding: 24px;
    backdrop-filter: blur(10px);
}
.info-card h2 {
    color: #f1f5f9;
    font-size: 1.6rem;
    font-weight: 700;
    margin-bottom: 16px;
}
.info-row {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 9px 0;
    border-bottom: 1px solid rgba(255,255,255,0.05);
    font-size: 0.92rem;
    color: #cbd5e1;
}
.info-row:last-child { border-bottom: none; }
.info-label { color: #64748b; min-width: 160px; font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.8px; }
.info-value { color: #e2e8f0; font-weight: 500; }
.badge {
    display: inline-block;
    background: rgba(56, 189, 248, 0.15);
    border: 1px solid rgba(56, 189, 248, 0.3);
    color: #38bdf8;
    font-size: 0.72rem;
    padding: 2px 10px;
    border-radius: 999px;
    font-family: 'JetBrains Mono', monospace;
}

/* ── Tablar ── */
[data-testid="stTabs"] button {
    color: #64748b !important;
    font-weight: 600;
    font-size: 0.85rem;
    letter-spacing: 0.5px;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #38bdf8 !important;
    border-bottom-color: #38bdf8 !important;
}

/* ── Sidebar logo ── */
.sidebar-logo {
    text-align: center;
    padding: 20px 0 10px;
    font-size: 2.5rem;
}
.sidebar-tagline {
    text-align: center;
    font-size: 0.72rem;
    color: #475569;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 20px;
    font-family: 'JetBrains Mono', monospace;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 2. MA'LUMOTLAR BAZASI (PREZIDENTLAR VA YaIM)
# ─────────────────────────────────────────────
PRESIDENTS_DB = {
    "Uzbekistan": ("Shavkat Mirziyoyev", "2016 – hozir"),
    "Kazakhstan": ("Qasım-Jomart Toqayev", "2019 – hozir"),
    "Kyrgyzstan": ("Sadır Japarov", "2021 – hozir"),
    "Tajikistan": ("Imomali Rahmon", "1994 – hozir"),
    "Turkmenistan": ("Serdar Berdimuhamedov", "2022 – hozir"),
    "Russia": ("Vladimir Putin", "2000 – hozir"),
    "Turkey": ("Recep Tayyip Erdoğan", "2014 – hozir"),
    "United States": ("Donald Trump", "2025 – hozir"),
    "China": ("Xi Jinping", "2013 – hozir"),
    "Germany": ("Frank-Walter Steinmeier", "2017 – hozir"),
    "France": ("Emmanuel Macron", "2017 – hozir"),
    "United Kingdom": ("Keir Starmer", "2024 – hozir"),
}

GDP_DATA = {
    "United States": 27360, "China": 17794, "Germany": 4456, "Japan": 4213,
    "India": 3737, "United Kingdom": 3079, "France": 2924, "Italy": 2255,
    "Russia": 1862, "Uzbekistan": 90, "Kazakhstan": 261, "Turkey": 1108
}

@st.cache_data(ttl=3600)
def get_all_data():
    # Faqat kerakli maydonlarni so'raymiz (bu yuklanishni 5x tezlashtiradi)
    fields = "name,capital,population,area,region,subregion,flags,coatOfArms,currencies,languages,unMember,latlng,idd,timezones,tld,car,borders,altSpellings"
    url = f"https://restcountries.com/v3.1/all?fields={fields}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        resp = requests.get(url, headers=headers, timeout=30)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None

# ─────────────────────────────────────────────
# 3. SIDEBAR VA TANLOV
# ─────────────────────────────────────────────
data = get_all_data()

with st.sidebar:
    st.markdown('<div class="sidebar-logo">🌍</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tagline">Global Country Intelligence</div>', unsafe_allow_html=True)
    st.markdown("---")

    if data:
        countries_list = sorted([c['name']['common'] for c in data])
        default_idx = countries_list.index("Uzbekistan") if "Uzbekistan" in countries_list else 0
        selected_country = st.selectbox("🔍 Davlatni tanlang", countries_list, index=default_idx)
        
        st.markdown("---")
        st.markdown(f"""
        <div style="text-align:center; color:#475569; font-size:0.75rem; font-family:'JetBrains Mono',monospace;">
        {len(countries_list)} ta davlat yuklandi<br>
        <span style="color:#38bdf8;">● API barqaror</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("❌ API ulanmadi")
        selected_country = None

# ─────────────────────────────────────────────
# 4. ASOSIY KONTENT
# ─────────────────────────────────────────────
st.markdown('<h1 class="hero-title">🌍 Dunyo Davlatlari Explorer</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-sub">real-time · 250+ davlat · to\'liq statistika</p>', unsafe_allow_html=True)

if not data:
    st.error("❌ Ma'lumotlarni yuklab bo'lmadi. Iltimos, internetni tekshiring va sahifani yangilang.")
    st.stop()

c = next((item for item in data if item["name"]["common"] == selected_country), None)
if not c:
    st.stop()

# O'zgaruvchilarni tayyorlash
poytaxt = c.get('capital', ["Noma'lum"])[0] if c.get('capital') else "Noma'lum"
aholi = c.get('population', 0)
maydon = c.get('area', 0)
mintaqa = c.get('region', "Noma'lum")
sub_mintaqa = c.get('subregion', "Noma'lum")
lat, lon = c.get('latlng', [0, 0])

# Prezident
prez_info = PRESIDENTS_DB.get(selected_country, ("Ma'lumot topilmadi", "—"))
prezident, prez_muddat = prez_info

# ── Yuqori blok ──
col_flag, col_arms, col_info = st.columns([1, 1, 2.8])

with col_flag:
    if c.get('flags', {}).get('png'):
        st.image(c['flags']['png'], use_container_width=True, caption="Bayroq")

with col_arms:
    if c.get('coatOfArms', {}).get('png'):
        st.image(c['coatOfArms']['png'], use_container_width=True, caption="Gerb")
    else:
        st.info("Gerb yo'q")

with col_info:
    cur_text = "Noma'lum"
    if c.get('currencies'):
        code = list(c['currencies'].keys())[0]
        cur_text = f"{c['currencies'][code].get('name')} ({code})"

    tillar = ", ".join(c.get('languages', {}).values()) if c.get('languages') else "Noma'lum"
    
    st.markdown(f"""
    <div class="info-card">
        <h2>📍 {selected_country}</h2>
        <div class="info-row"><span class="info-label">👤 Prezident</span><span class="info-value">{prezident}</span></div>
        <div class="info-row"><span class="info-label">🏛️ Poytaxt</span><span class="info-value">{poytaxt}</span></div>
        <div class="info-row"><span class="info-label">🌐 Mintaqa</span><span class="info-value">{mintaqa} <span class="badge">{sub_mintaqa}</span></span></div>
        <div class="info-row"><span class="info-label">💱 Valyuta</span><span class="info-value">{cur_text}</span></div>
        <div class="info-row"><span class="info-label">🗣️ Tillar</span><span class="info-value">{tillar}</span></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ── Metrikalar ──
m1, m2, m3, m4 = st.columns(4)
m1.metric("👥 Aholi", f"{aholi:,}")
m2.metric("📐 Maydon", f"{maydon:,} km²")
m3.metric("🏘️ Zichlik", f"{aholi/maydon:.1f}/km²" if maydon else "0")
m4.metric("🇺🇳 BMT a'zosi", "Ha" if c.get('unMember') else "Yo'q")

# ── Tablar ──
t1, t2, t3 = st.tabs(["🗺️ Xarita", "🎓 Ta'lim", "🚜 Agro"])

with t1:
    m_map = folium.Map(location=[lat, lon], zoom_start=5, tiles="CartoDB dark_matter")
    folium.Marker([lat, lon], popup=selected_country).add_to(m_map)
    st_folium(m_map, width="100%", height=400)

with t2:
    st.subheader("🎓 Taxminiy ta'lim ko'rsatkichlari")
    u, s = max(1, int(aholi/400000)), max(1, int(aholi/3000))
    st.metric("🏛️ Universitetlar", f"~{u:,}")
    st.metric("🏫 Maktablar", f"~{s:,}")

with t3:
    st.subheader("🚜 Qishloq xo'jaligi")
    st.metric("🌾 Ekin maydoni (taxmin)", f"~{int(maydon*0.35):,} km²")
    st.info(f"Asosiy mintaqa: {mintaqa}")

st.markdown("---")
st.caption("© 2026 | Global Country Data Pro | InfoSchoolUz")
