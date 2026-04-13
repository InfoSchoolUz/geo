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

/* ── Success / Warning ── */
[data-testid="stAlert"] {
    border-radius: 12px;
    border: none;
}

/* ── Divider ── */
hr { border-color: rgba(56, 189, 248, 0.12) !important; }

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
# 2. MA'LUMOTLAR
# ─────────────────────────────────────────────
PRESIDENTS_DB = {
    # O'rta Osiyo
    "Uzbekistan": ("Shavkat Mirziyoyev", "2016 – hozir"),
    "Kazakhstan": ("Qasım-Jomart Toqayev", "2019 – hozir"),
    "Kyrgyzstan": ("Sadır Japarov", "2021 – hozir"),
    "Tajikistan": ("Imomali Rahmon", "1994 – hozir"),
    "Turkmenistan": ("Serdar Berdimuhamedov", "2022 – hozir"),
    "Azerbaijan": ("İlham Aliyev", "2003 – hozir"),
    "Armenia": ("Vahagn Xachaturyan", "2022 – hozir"),
    "Georgia": ("Salome Zurabişvili", "2018 – hozir"),

    # Yevroosiyо
    "Russia": ("Vladimir Putin", "2000 – hozir"),
    "Belarus": ("Aleksandr Lukashenko", "1994 – hozir"),
    "Ukraine": ("Volodimir Zelenskiy", "2019 – hozir"),
    "Moldova": ("Maia Sandu", "2020 – hozir"),

    # Sharqiy Yevropa
    "Poland": ("Andrzej Duda", "2015 – hozir"),
    "Czech Republic": ("Petr Pavel", "2023 – hozir"),
    "Hungary": ("Tamás Sulyok", "2024 – hozir"),
    "Romania": ("Klaus Iohannis", "2014 – hozir"),
    "Slovakia": ("Peter Pellegrini", "2024 – hozir"),
    "Bulgaria": ("Rumen Radev", "2017 – hozir"),
    "Serbia": ("Aleksandar Vucic", "2017 – hozir"),
    "Croatia": ("Zoran Milanović", "2020 – hozir"),

    # G'arbiy Yevropa
    "Germany": ("Frank-Walter Steinmeier", "2017 – hozir"),
    "France": ("Emmanuel Macron", "2017 – hozir"),
    "Italy": ("Sergio Mattarella", "2022 – hozir"),
    "Spain": ("Pedro Sánchez (Bosh vazir)", "2018 – hozir"),
    "Portugal": ("Marcelo Rebelo de Sousa", "2016 – hozir"),
    "Switzerland": ("Karin Keller-Sutter", "2025 – hozir"),
    "Austria": ("Alexander Van der Bellen", "2017 – hozir"),
    "Netherlands": ("Mark Rutte (Bosh vazir)", "2010 – 2024"),
    "Belgium": ("Alexandre De Croo (Bosh vazir)", "2020 – hozir"),
    "Greece": ("Katerina Sakellaropoulou", "2020 – hozir"),
    "Finland": ("Alexander Stubb", "2024 – hozir"),
    "Sweden": ("Ulf Kristersson (Bosh vazir)", "2022 – hozir"),
    "Norway": ("Jonas Gahr Støre (Bosh vazir)", "2021 – hozir"),
    "Denmark": ("Mette Frederiksen (Bosh vazir)", "2019 – hozir"),

    # Amerika
    "United States": ("Donald Trump", "2025 – hozir"),
    "Canada": ("Mark Carney (Bosh vazir)", "2025 – hozir"),
    "Mexico": ("Claudia Sheinbaum", "2024 – hozir"),
    "Brazil": ("Luiz Inácio Lula da Silva", "2023 – hozir"),
    "Argentina": ("Javier Milei", "2023 – hozir"),
    "Colombia": ("Gustavo Petro", "2022 – hozir"),
    "Chile": ("Gabriel Boric", "2022 – hozir"),
    "Peru": ("Dina Boluarte", "2022 – hozir"),
    "Venezuela": ("Nicolás Maduro", "2013 – hozir"),
    "Bolivia": ("Luis Arce", "2020 – hozir"),
    "Cuba": ("Miguel Díaz-Canel", "2018 – hozir"),

    # Osiyo
    "China": ("Xi Jinping", "2013 – hozir"),
    "Japan": ("Shigeru Ishiba (Bosh vazir)", "2024 – hozir"),
    "South Korea": ("Yoon Suk-yeol", "2022 – hozir"),
    "North Korea": ("Kim Jong-un", "2011 – hozir"),
    "India": ("Droupadi Murmu", "2022 – hozir"),
    "Pakistan": ("Asif Ali Zardari", "2024 – hozir"),
    "Bangladesh": ("Muhammad Yunus (Bosh vazir)", "2024 – hozir"),
    "Afghanistan": ("Hibatullah Axundzada", "2021 – hozir"),
    "Iran": ("Masoud Pezeshkian", "2024 – hozir"),
    "Iraq": ("Abdul Latif Rashid", "2022 – hozir"),
    "Turkey": ("Recep Tayyip Erdoğan", "2014 – hozir"),
    "Syria": ("Ahmad al-Sharaa", "2024 – hozir"),
    "Saudi Arabia": ("Muhammad bin Salman (Valiahd shahzoda)", "2022 – hozir"),
    "United Arab Emirates": ("Muhammad bin Zayed Al Nahyan", "2022 – hozir"),
    "Israel": ("Yitzhak Herzog", "2021 – hozir"),
    "Jordan": ("Abdullah II (Qirol)", "1999 – hozir"),
    "Lebanon": ("Joseph Aoun", "2025 – hozir"),
    "Qatar": ("Tamim bin Hamad Al Thani (Amir)", "2013 – hozir"),
    "Kuwait": ("Mishal Al-Ahmad Al-Jaber Al-Sabah (Amir)", "2023 – hozir"),
    "Oman": ("Haitham bin Tariq (Sultan)", "2020 – hozir"),
    "Bahrain": ("Hamad bin Isa Al Khalifa (Qirol)", "2002 – hozir"),
    "Yemen": ("Rashad al-Alimi", "2022 – hozir"),
    "Indonesia": ("Prabowo Subianto", "2024 – hozir"),
    "Philippines": ("Ferdinand Marcos Jr.", "2022 – hozir"),
    "Vietnam": ("Luong Cuong", "2024 – hozir"),
    "Thailand": ("Paetongtarn Shinawatra (Bosh vazir)", "2024 – hozir"),
    "Malaysia": ("Anwar Ibrahim (Bosh vazir)", "2022 – hozir"),
    "Singapore": ("Tharman Shanmugaratnam", "2023 – hozir"),
    "Myanmar": ("Min Aung Hlaing", "2021 – hozir"),
    "Cambodia": ("Hun Manet (Bosh vazir)", "2023 – hozir"),
    "Mongolia": ("Ukhnaagiin Khürelsükh", "2021 – hozir"),
    "Nepal": ("Ram Chandra Paudel", "2023 – hozir"),
    "Sri Lanka": ("Anura Kumara Dissanayake", "2024 – hozir"),

    # Afrika
    "South Africa": ("Cyril Ramaphosa", "2018 – hozir"),
    "Nigeria": ("Bola Tinubu", "2023 – hozir"),
    "Egypt": ("Abdel Fattah el-Sisi", "2014 – hozir"),
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

    # Okeaniya
    "Australia": ("Anthony Albanese (Bosh vazir)", "2022 – hozir"),
    "New Zealand": ("Christopher Luxon (Bosh vazir)", "2023 – hozir"),
    "Fiji": ("Wiliame Katonivere", "2021 – hozir"),

    # Boshqalar
    "United Kingdom": ("Keir Starmer (Bosh vazir)", "2024 – hozir"),
    "Ireland": ("Micheál Martin (Bosh vazir)", "2025 – hozir"),
}

GDP_DATA = {
    "United States": 27360, "China": 17794, "Germany": 4456, "Japan": 4213,
    "India": 3737, "United Kingdom": 3079, "France": 2924, "Italy": 2255,
    "Brazil": 2174, "Canada": 2140, "Russia": 1862, "South Korea": 1709,
    "Australia": 1693, "Mexico": 1323, "Spain": 1581, "Indonesia": 1319,
    "Netherlands": 1118, "Turkey": 1108, "Saudi Arabia": 1069,
    "Switzerland": 905, "Poland": 811, "Argentina": 640, "Sweden": 597,
    "Norway": 547, "Belgium": 630, "Israel": 521, "United Arab Emirates": 499,
    "Singapore": 501, "Austria": 536, "Thailand": 512, "Nigeria": 477,
    "South Africa": 380, "Philippines": 404, "Malaysia": 399, "Denmark": 406,
    "Iran": 367, "Colombia": 363, "Chile": 317, "Finland": 301,
    "Romania": 301, "Czech Republic": 330, "Vietnam": 409, "Pakistan": 342,
    "Uzbekistan": 90, "Kazakhstan": 261, "Ukraine": 149, "Greece": 242,
    "Egypt": 395, "Bangladesh": 421, "Ethiopia": 155, "Kenya": 114,
    "Morocco": 141, "Hungary": 212, "Qatar": 219, "Kuwait": 162,
    "Ghana": 72, "Tanzania": 79,
}

@st.cache_data(ttl=3600)
def get_all_data():
    try:
        resp = requests.get("https://restcountries.com/v3.1/all", timeout=15)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
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

# Tanlangan davlat
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
phone_code = ""
if phone_root.get('root'):
    suffixes = phone_root.get('suffixes', [''])
    phone_code = phone_root['root'] + (suffixes[0] if suffixes else '')
timezones = c.get('timezones', ["Noma'lum"])
tld = ", ".join(c.get('tld', ["Noma'lum"]))
car_side = c.get('car', {}).get('side', "Noma'lum")
car_signs = ", ".join(c.get('car', {}).get('signs', ["Noma'lum"]))
lat, lon = c.get('latlng', [0, 0])

# Prezident
prez_info = PRESIDENTS_DB.get(selected_country, ("Ma'lumotlar bazada mavjud emas", "—"))
prezident, prez_muddat = prez_info if isinstance(prez_info, tuple) else (prez_info, "")

# ── Yuqori blok ──────────────────────────────
col_flag, col_arms, col_info = st.columns([1, 1, 2.8])

with col_flag:
    if c.get('flags', {}).get('png'):
        st.image(c['flags']['png'], use_container_width=True, caption="🏳️ Davlat Bayrog'i")

with col_arms:
    if c.get('coatOfArms', {}).get('png'):
        st.image(c['coatOfArms']['png'], use_container_width=True, caption="🛡️ Davlat Gerbi")
    else:
        st.markdown("""
        <div style="height:180px; display:flex; align-items:center; justify-content:center;
                    border:1px dashed rgba(255,255,255,0.1); border-radius:12px; color:#475569; font-size:0.8rem;">
        Gerb mavjud emas
        </div>""", unsafe_allow_html=True)

with col_info:
    # Valyuta
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
        <div class="info-row"><span class="info-label">👤 Prezident</span>
            <span class="info-value">{prezident}
                {"<br><small style='color:#64748b;font-size:0.75rem;'>"+prez_muddat+"</small>" if prez_muddat and prez_muddat != "—" else ""}
            </span>
        </div>
        <div class="info-row"><span class="info-label">🏛️ Poytaxt</span>
            <span class="info-value">{poytaxt}</span>
        </div>
        <div class="info-row"><span class="info-label">🌐 Mintaqa</span>
            <span class="info-value">{mintaqa} <span class="badge">{sub_mintaqa}</span></span>
        </div>
        <div class="info-row"><span class="info-label">📞 Telefon kodi</span>
            <span class="info-value">{phone_code if phone_code else "Noma'lum"}</span>
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
    """, unsafe_allow_html=True)

st.markdown("---")

# ── Asosiy ko'rsatkichlar ────────────────────
m1, m2, m3, m4 = st.columns(4)
m1.metric("👥 Aholi", f"{aholi:,}")
m2.metric("📐 Maydon", f"{maydon:,.0f} km²")
m3.metric("🏘️ Zichlik", f"{aholi/maydon:.1f} /km²" if maydon else "—")
m4.metric("⏰ Vaqt zonalari", f"{len(timezones)} ta")

st.markdown("---")

# ── Tablar ──────────────────────────────────
t1, t2, t3, t4, t5 = st.tabs([
    "🗺️ Xarita",
    "🎓 Ta'lim",
    "🚜 Qishloq xo'jaligi",
    "💰 Moliya",
    "📊 Demografiya"
])

# ── TAB 1: Xarita ──
with t1:
    try:
        m_map = folium.Map(
            location=[lat, lon],
            zoom_start=5,
            tiles="CartoDB dark_matter"
        )
        folium.Marker(
            [lat, lon],
            popup=folium.Popup(
                f"<b>{selected_country}</b><br>Poytaxt: {poytaxt}<br>Aholi: {aholi:,}",
                max_width=200
            ),
            tooltip=selected_country,
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m_map)
        folium.Circle(
            [lat, lon],
            radius=min(max(aholi / 100, 50000), 500000),
            color="#38bdf8",
            fill=True,
            fill_opacity=0.15,
            weight=2
        ).add_to(m_map)
        st_folium(m_map, width="100%", height=450)
    except Exception as e:
        st.error(f"Xarita yuklanmadi: {e}")

# ── TAB 2: Ta'lim ──
with t2:
    st.subheader("🎓 Ta'lim tizimi taxminiy ko'rsatkichlari")
    unis = max(1, int(aholi / 400_000))
    colleges = int(unis * 3)
    schools = max(1, int(aholi / 3_000))
    teachers = max(1, int(aholi / 50))
    students = max(1, int(aholi * 0.22))

    e1, e2, e3 = st.columns(3)
    e1.metric("🏛️ Universitetlar", f"~{unis:,}")
    e2.metric("🏫 Kollej / Litsey", f"~{colleges:,}")
    e3.metric("📚 Maktablar", f"~{schools:,}")

    e4, e5 = st.columns(2)
    e4.metric("👨‍🏫 O'qituvchilar", f"~{teachers:,}")
    e5.metric("🎒 O'quvchilar", f"~{students:,}")

    st.info("ℹ️ Bu ko'rsatkichlar aholi soniga ko'ra hisoblangan taxminiy raqamlar.", icon="📌")

# ── TAB 3: Qishloq xo'jaligi ──
with t3:
    st.subheader("🚜 Qishloq xo'jaligi salohiyati")
    ekin_yer = int(maydon * 0.35)
    o_rmon = int(maydon * 0.28)
    yaylov = int(maydon * 0.2)

    q1, q2, q3 = st.columns(3)
    q1.metric("🌾 Taxminiy ekin maydon", f"~{ekin_yer:,} km²")
    q2.metric("🌳 O'rmon hududi", f"~{o_rmon:,} km²")
    q3.metric("🐄 Yaylov maydoni", f"~{yaylov:,} km²")

    PRODUCTS_BY_REGION = {
        "Asia": "🌾 Bug'doy · 🌿 Paxta · 🍚 Guruch · 🍑 Mevalar · 🫖 Choy",
        "Europe": "🌽 Don mahsulotlari · 🥛 Sut · 🍇 Uzum · 🫒 Zaytun",
        "Africa": "☕ Kofe · 🍫 Kakao · 🍌 Banan · 🎋 Shakarqamish",
        "Americas": "🌽 Makkajo'xori · 🫘 Soya · 🥩 Go'sht mahsulotlari",
        "Oceania": "🐑 Jun · 🐄 Mol go'shti · 🍇 Uzum · 🐟 Baliq",
    }
    st.success(f"**Asosiy mahsulotlar:** {PRODUCTS_BY_REGION.get(mintaqa, '🌾 Don va poliz mahsulotlari')}")

# ── TAB 4: Moliya ──
with t4:
    st.subheader("💰 Moliya va Iqtisodiyot")

    if c.get('currencies'):
        cur_code = list(c['currencies'].keys())[0]
        cur_name = c['currencies'][cur_code].get('name', "Noma'lum")
        cur_sym = c['currencies'][cur_code].get('symbol', "")
        f1, f2 = st.columns(2)
        f1.metric("💱 Milliy valyuta", cur_name)
        f2.metric("🔤 Valyuta belgisi", f"{cur_code}  {cur_sym}")

    if gdp_val:
        g1, g2 = st.columns(2)
        g1.metric("📊 YaIM (GDP)", f"${gdp_val:,} mlrd")
        gdp_per_capita = int(gdp_val * 1_000_000_000 / aholi) if aholi else 0
        g2.metric("💵 Aholi boshiga", f"${gdp_per_capita:,}")
    else:
        st.info("GDP ma'lumoti bazada mavjud emas.")

    bmt_status = "✅ To'liq a'zo" if c.get('unMember') else "⚪ A'zo emas"
    st.markdown(f"**🇺🇳 BMT holati:** {bmt_status}")

# ── TAB 5: Demografiya ──
with t5:
    st.subheader("📊 Demografik tahlil")
    d1, d2, d3, d4 = st.columns(4)
    d1.metric("👥 Jami aholi", f"{aholi:,}")
    d2.metric("📐 Umumiy maydon", f"{maydon:,.0f} km²")
    zichlik = aholi / maydon if maydon else 0
    d3.metric("🏘️ Aholi zichligi", f"{zichlik:.1f} /km²")
    d4.metric("🌆 Shaharlar soni", f"~{max(1, int(aholi/250_000)):,}")

    border_countries = c.get('borders', [])
    if border_countries:
        st.markdown(f"**🗺️ Qo'shni davlatlar ({len(border_countries)} ta):** `{'` · `'.join(border_countries)}`")
    else:
        st.markdown("**🗺️ Qo'shni davlatlar:** yo'q (orol davlati yoki izolyatsiya)")

    alt_spellings = c.get('altSpellings', [])
    if alt_spellings:
        st.markdown(f"**🔤 Boshqa nomlar:** {' · '.join(alt_spellings[:5])}")

# ── Footer ──────────────────────────────────
st.markdown("---")
st.markdown("""
<div style="text-align:center; color:#334155; font-size:0.78rem; font-family:'JetBrains Mono',monospace; padding:10px 0 20px;">
    Global Country Data Pro &nbsp;·&nbsp; restcountries.com API &nbsp;·&nbsp; 
    <span style="color:#38bdf8;">InfoSchoolUz</span>
</div>
""", unsafe_allow_html=True)
