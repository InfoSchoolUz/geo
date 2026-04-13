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

# CSS styling (unchanged)
st.markdown("""<style> ... </style>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# 2. MA'LUMOTLAR
# ─────────────────────────────────────────────
PRESIDENTS_DB = {
    "Uzbekistan": ("Shavkat Mirziyoyev", "2016 – hozir"),
    # ... boshqa davlatlar ...
}

GDP_DATA = {
    "United States": 27360, "China": 17794, "Germany": 4456,
    # ... boshqa davlatlar ...
}

@st.cache_data(ttl=3600)
def get_all_data():
    try:
        resp = requests.get("https://restcountries.com/v3.1/all", timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None

# ─────────────────────────────────────────────
# 3. SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-logo">🌍</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-tagline">Global Country Intelligence</div>', unsafe_allow_html=True)
    st.markdown("---")

    data = get_all_data()

    if data:
        countries_list = sorted([c['name']['common'] for c in data])
        default_idx = countries_list.index("Uzbekistan") if "Uzbekistan" in countries_list else 0
        selected_country = st.selectbox("🔍 Davlatni tanlang", countries_list, index=default_idx)

        st.markdown("---")
        total = len(countries_list)
        st.markdown(f"""
        <div style="text-align:center; color:#475569; font-size:0.75rem; font-family:'JetBrains Mono',monospace;">
        {total} ta davlat • restcountries.com<br>
        <span style="color:#38bdf8;">● Ma'lumotlar yangilangan</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("API ulanmadi")
        selected_country = None

# ─────────────────────────────────────────────
# 4. ASOSIY KONTENT
# ─────────────────────────────────────────────
st.markdown('<h1 class="hero-title">🌍 Dunyo Davlatlari Explorer</h1>', unsafe_allow_html=True)
st.markdown('<p class="hero-sub">real-time · 250+ davlat · to\'liq statistika</p>', unsafe_allow_html=True)

if not data:
    st.error("❌ API'dan ma'lumot yuklab bo'lmadi. Internetni tekshiring.")
    st.stop()

c = next((item for item in data if item["name"]["common"] == selected_country), None)
if not c:
    st.warning("Davlat topilmadi.")
    st.stop()

# O'zgaruvchilar
poytaxt = c.get('capital', ["Noma'lum"])[0] if c.get('capital') else "Noma'lum"
aholi = c.get('population', 0)
maydon = c.get('area', 0)
mintaqa = c.get('region', "Noma'lum")
sub_mintaqa = c.get('subregion', "Noma'lum")

phone_root = c.get('idd', {})
phone_code = "Noma'lum"
if phone_root.get('root'):
    suffixes = phone_root.get('suffixes', [])
    phone_code = phone_root['root'] + ", ".join(suffixes) if suffixes else phone_root['root']

timezones = c.get('timezones', ["Noma'lum"])
tld = ", ".join(c.get('tld', ["Noma'lum"]))
car_side = c.get('car', {}).get('side', "Noma'lum")
car_signs = ", ".join(c.get('car', {}).get('signs', ["Noma'lum"]))
lat, lon = c.get('latlng', [0, 0])

# Davlat rahbari
prez_info = PRESIDENTS_DB.get(selected_country, ("Ma'lumotlar bazada mavjud emas", "—"))
rahbar, muddat = prez_info if isinstance(prez_info, tuple) else (prez_info, "")

# ── Yuqori blok ──────────────────────────────
col_flag, col_arms, col_info = st.columns([1, 1, 2.8])

with col_flag:
    if c.get('flags', {}).get('png'):
        st.image(c['flags']['png'], use_container_width=True, caption="🏳️ Davlat Bayrog'i")

with col_arms:
    if c.get('coatOfArms', {}).get('png'):
        st.image(c['coatOfArms']['png'], use_container_width=True, caption="🛡️ Davlat Gerbi")
    else:
        st.markdown("<div style='height:180px;display:flex;align-items:center;justify-content:center;border:1px dashed rgba(255,255,255,0.1);border-radius:12px;color:#475569;font-size:0.8rem;'>Gerb mavjud emas</div>", unsafe_allow_html=True)

with col_info:
    cur_text = "Noma'lum"
    if c.get('currencies'):
        cur_code = list(c['currencies'].keys())[0]
        cur_name = c['currencies'][cur_code].get('name', "Noma'lum")
        cur_sym = c['currencies'][cur_code].get('symbol', "")
        cur_text = f"{cur_name} ({cur_code}) {cur_sym}"

    tillar = ", ".join(c.get('languages', {}).values()) if c.get('languages') else "Noma'lum"
    bmt = "✅ Ha" if c.get('unMember') else "❌ Yo'q"
    gdp_val = GDP_DATA.get(selected_country)
    gdp_text = f"~${gdp_val:,} mlrd" if gdp_val else "Ma'lumot yo'q"

    st.markdown(f"""
    <div class="info-card">
        <h2>📍 {selected_country}</h2>
        <div class="info-row"><span class="info-label">👤 Davlat rahbari</span>
            <span class="info-value">{rahbar}
                {"<br><small style='color:#64748b;font-size:0.75rem;'>"+muddat+"</small>" if muddat and muddat != "—" else ""}
            </span>
        </div>
        <div class="info-row"><span class="info-label">🏛️ Poytaxt</span>
            <span class="info-value">{poytaxt}</span>
        </div>
        <div class="info-row"><span class="info-label">🌐 Mintaqa</span>
            <span class="info-value">{mintaqa} <span class="badge">{sub_mintaqa}</span></span>
        </div>
        <div class="info-row"><span class="info-label">📞 Telefon kodi</span>
            <span class="info-value">{phone_code}</span>
        </div>
        <div class="info-row"><span class="info-label">🌐 Domen (.tld)</span>
            <span class="info-value">{tld}</span>
        </div>
        <div class="info-row"><span class="info-label">🚗 Yo'l tomoni</span>
            <span class="info-value">{car_side.capitalize()} &nbsp;|&nbsp; <span class="badge">{car_signs}</span></span>
        </div>
        <div class="info-row"><span class="info-label">💱 Valyuta</span>
            <span class="info-value">{cur_text}</span>
        </div>
        <div class="info-row"><span class="info-label">🗣️ Rasmiy tillar</span>
            <span class="info-value">{tillar}</span>
        </div>
        <div class="info-row"><span class="info-label">💰 YaIM (GDP)</span>
            <span class="info-value">{gdp_text}</span>
        </div>
        <div class="info-row"><span class="info-label">🇺🇳 BMT a'zosi</span>
            <span class="info-value">{bmt}</span>
        </div>
        <div class="info-row"><span class="info-label">⏰ Vaqt zonalari</span>
            <span class="info-value">{" · ".join(timezones[:3])}{"..." if len(timezones) > 3 else ""}</span>
        </div>
    </div>
