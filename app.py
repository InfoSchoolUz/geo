import streamlit as st
import folium
from streamlit_folium import st_folium

st.set_page_config(
    layout="wide",
    page_title="🌍 Global Davlatlar Platformasi",
    page_icon="🌍"
)

# ===== CUSTOM CSS =====
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
}

.stApp {
    background: #0a0e1a;
    color: #e8eaf6;
}

.main-title {
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(135deg, #64b5f6, #e040fb, #00e5ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 0.2rem;
    letter-spacing: -1px;
}

.subtitle {
    text-align: center;
    color: #546e7a;
    font-size: 0.9rem;
    font-family: 'Space Mono', monospace;
    margin-bottom: 1.5rem;
    letter-spacing: 2px;
}

.country-hero {
    background: linear-gradient(135deg, #0d1b2a 0%, #1a1a2e 50%, #16213e 100%);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    position: relative;
    overflow: hidden;
}

.country-hero::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #64b5f6, #e040fb, #00e5ff);
}

.hero-name {
    font-size: 2.2rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0;
}

.hero-capital {
    font-family: 'Space Mono', monospace;
    color: #64b5f6;
    font-size: 0.85rem;
    margin-top: 0.3rem;
    letter-spacing: 1px;
}

.section-card {
    background: #0d1b2a;
    border: 1px solid #1e3a5f;
    border-radius: 12px;
    padding: 1.2rem;
    margin-bottom: 0.8rem;
    transition: border-color 0.3s;
}

.section-card:hover {
    border-color: #64b5f6;
}

.section-title {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 3px;
    color: #64b5f6;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.4rem 0;
    border-bottom: 1px solid #1a2744;
    font-size: 0.88rem;
}

.info-row:last-child { border-bottom: none; }

.info-label {
    color: #546e7a;
    font-family: 'Space Mono', monospace;
    font-size: 0.78rem;
}

.info-value {
    color: #e8eaf6;
    font-weight: 600;
    text-align: right;
    max-width: 60%;
}

.metric-box {
    background: #0d1b2a;
    border: 1px solid #1e3a5f;
    border-radius: 10px;
    padding: 1rem;
    text-align: center;
}

.metric-num {
    font-size: 1.5rem;
    font-weight: 800;
    color: #64b5f6;
}

.metric-label {
    font-family: 'Space Mono', monospace;
    font-size: 0.68rem;
    color: #546e7a;
    letter-spacing: 1px;
    margin-top: 0.2rem;
}

.tag {
    display: inline-block;
    background: #1e3a5f;
    color: #64b5f6;
    border-radius: 20px;
    padding: 0.2rem 0.7rem;
    font-size: 0.75rem;
    font-family: 'Space Mono', monospace;
    margin: 0.15rem;
}

.conflict-badge {
    background: #2d1b1b;
    color: #ef5350;
    border: 1px solid #ef5350;
    border-radius: 6px;
    padding: 0.3rem 0.8rem;
    font-size: 0.8rem;
    font-family: 'Space Mono', monospace;
}

.peace-badge {
    background: #1b2d1b;
    color: #66bb6a;
    border: 1px solid #66bb6a;
    border-radius: 6px;
    padding: 0.3rem 0.8rem;
    font-size: 0.8rem;
    font-family: 'Space Mono', monospace;
}

.placeholder-box {
    background: #0d1b2a;
    border: 2px dashed #1e3a5f;
    border-radius: 16px;
    padding: 3rem;
    text-align: center;
    color: #37474f;
}

.placeholder-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
}

.placeholder-text {
    font-family: 'Space Mono', monospace;
    font-size: 0.85rem;
    letter-spacing: 2px;
}

.compare-header {
    background: linear-gradient(135deg, #1a1a2e, #0d1b2a);
    border: 1px solid #e040fb44;
    border-radius: 12px;
    padding: 0.8rem 1.2rem;
    text-align: center;
    margin-bottom: 1rem;
}

.sidebar-filter {
    background: #0d1b2a;
    border-radius: 8px;
    padding: 0.5rem;
}

[data-testid="stSidebar"] {
    background: #070d1a !important;
    border-right: 1px solid #1e3a5f;
}

div[data-testid="metric-container"] {
    background: #0d1b2a;
    border: 1px solid #1e3a5f;
    border-radius: 10px;
    padding: 0.8rem;
}

.stSelectbox > div > div {
    background: #0d1b2a;
    border-color: #1e3a5f;
    color: #e8eaf6;
}
</style>
""", unsafe_allow_html=True)


# ===== FULL DATASET =====
countries = [
    {
        "name": "O'zbekiston", "code": "uz", "capital": "Toshkent", "region": "Osiyo",
        "lat": 41.3, "lon": 69.2, "color": "#4caf50",
        "president": "Shavkat Mirziyoyev", "language": "O'zbek tili",
        "currency": "So'm (UZS)", "usd_rate": "~12,800",
        "population": "36 mln", "area": "448,978 km²",
        "gdp": "$90 mlrd", "gdp_pc": "$2,600",
        "education": {"schools": "10,000+", "colleges": "1,200+", "universities": "150+", "academies": "30+"},
        "specialization": "Qishloq xo'jaligi, sanoat",
        "wealth": "Paxta, oltin, gaz, uran", "specialists": "Muhandis, o'qituvchi",
        "rockets": "Yo'q", "conflict": "Yo'q", "peace": True,
        "weather": "Kontinental, quruq", "farming": "Paxta, g'alla, meva",
        "allies": "MDH, SCO, CSTO (kuzatuvchi)", "army": "50,000+",
        "internet": "~80%", "religion": "Islom"
    },
    {
        "name": "AQSh", "code": "us", "capital": "Vashington D.C.", "region": "Amerika",
        "lat": 38.9, "lon": -77.0, "color": "#2196f3",
        "president": "Joe Biden", "language": "Ingliz tili",
        "currency": "Dollar (USD)", "usd_rate": "1 USD",
        "population": "331 mln", "area": "9.83 mln km²",
        "gdp": "$25.5 trln", "gdp_pc": "$76,000",
        "education": {"schools": "130,000+", "colleges": "4,000+", "universities": "5,000+", "academies": "Ko'p"},
        "specialization": "Texnologiya, harbiy, moliya",
        "wealth": "Neft, texnologiya, Dollar", "specialists": "IT, tibbiyot, harbiy",
        "rockets": "Apollo, Falcon 9, SLS", "conflict": "Global siyosiy ziddiyatlar",
        "peace": False, "weather": "Turli iqlim", "farming": "Makkajo'xori, bug'doy, soya",
        "allies": "NATO, G7, AUKUS", "army": "1.4 mln",
        "internet": "~92%", "religion": "Xristianlik"
    },
    {
        "name": "Xitoy", "code": "cn", "capital": "Pekin", "region": "Osiyo",
        "lat": 39.9, "lon": 116.4, "color": "#f44336",
        "president": "Xi Jinping", "language": "Mandarin xitoy tili",
        "currency": "Yuan (CNY)", "usd_rate": "~1 USD = 7.2 CNY",
        "population": "1.4 mlrd", "area": "9.6 mln km²",
        "gdp": "$18 trln", "gdp_pc": "$12,800",
        "education": {"schools": "500,000+", "colleges": "3,000+", "universities": "3,000+", "academies": "Ko'p"},
        "specialization": "Ishlab chiqarish, texnologiya",
        "wealth": "Sanoat, eksport, noyob metallar", "specialists": "Muhandis, IT",
        "rockets": "Long March, Shenzhou", "conflict": "Tayvan, Janubiy Xitoy dengizi",
        "peace": False, "weather": "Mo'tadil, subtropik", "farming": "Guruch, choy, bug'doy",
        "allies": "SCO, BRICS, Rossiya", "army": "2 mln",
        "internet": "~73%", "religion": "Buddizm, ateizm"
    },
    {
        "name": "Rossiya", "code": "ru", "capital": "Moskva", "region": "Yevropa/Osiyo",
        "lat": 55.7, "lon": 37.6, "color": "#ff9800",
        "president": "Vladimir Putin", "language": "Rus tili",
        "currency": "Rubl (RUB)", "usd_rate": "~1 USD = 90 RUB",
        "population": "144 mln", "area": "17.1 mln km²",
        "gdp": "$2.2 trln", "gdp_pc": "$15,000",
        "education": {"schools": "42,000+", "colleges": "2,700+", "universities": "750+", "academies": "Ko'p"},
        "specialization": "Energetika, harbiy, kosmik",
        "wealth": "Gaz, neft, qo'rg'oshin", "specialists": "Muhandis, harbiy",
        "rockets": "Soyuz, Proton, Angara", "conflict": "Ukraina urushi",
        "peace": False, "weather": "Kontinental, arktik", "farming": "Bug'doy, kartoshka",
        "allies": "MDH, SCO, CSTO", "army": "1 mln+",
        "internet": "~85%", "religion": "Pravoslav xristianlik"
    },
    {
        "name": "Germaniya", "code": "de", "capital": "Berlin", "region": "Yevropa",
        "lat": 52.5, "lon": 13.4, "color": "#9c27b0",
        "president": "Frank-Walter Steinmeier", "language": "Nemis tili",
        "currency": "Yevro (EUR)", "usd_rate": "~1 EUR = 1.08 USD",
        "population": "84 mln", "area": "357,114 km²",
        "gdp": "$4.5 trln", "gdp_pc": "$52,000",
        "education": {"schools": "34,000+", "colleges": "1,000+", "universities": "400+", "academies": "Ko'p"},
        "specialization": "Mashinasozlik, kimyo, avtomobil",
        "wealth": "Sanoat, eksport", "specialists": "Muhandis, tibbiyot",
        "rockets": "ESA orqali", "conflict": "Ukraina urushiga yordamchi",
        "peace": True, "weather": "Mo'tadil, okean", "farming": "Bug'doy, kartoshka, shakar lavlagi",
        "allies": "NATO, EU, G7", "army": "183,000",
        "internet": "~92%", "religion": "Xristianlik"
    },
    {
        "name": "Yaponiya", "code": "jp", "capital": "Tokio", "region": "Osiyo",
        "lat": 35.7, "lon": 139.7, "color": "#e91e63",
        "president": "Fumio Kishida (Bosh vazir)", "language": "Yapon tili",
        "currency": "Iyena (JPY)", "usd_rate": "~1 USD = 150 JPY",
        "population": "125 mln", "area": "377,975 km²",
        "gdp": "$4.9 trln", "gdp_pc": "$39,000",
        "education": {"schools": "35,000+", "colleges": "780+", "universities": "800+", "academies": "Ko'p"},
        "specialization": "Elektronika, avtomobil, robotika",
        "wealth": "Texnologiya, eksport", "specialists": "Muhandis, IT, tibbiyot",
        "rockets": "H-IIA, H3", "conflict": "Minimal (Kurilly orollari)",
        "peace": True, "weather": "Mo'tadil, musson", "farming": "Guruch, choy",
        "allies": "AQSh, NATO (hamkor)", "army": "250,000 (himoya)",
        "internet": "~93%", "religion": "Sintoizm, Buddizm"
    },
    {
        "name": "Braziliya", "code": "br", "capital": "Braziliya", "region": "Amerika",
        "lat": -15.8, "lon": -47.9, "color": "#00bcd4",
        "president": "Luiz Inácio Lula da Silva", "language": "Portugalcha",
        "currency": "Real (BRL)", "usd_rate": "~1 USD = 5 BRL",
        "population": "215 mln", "area": "8.5 mln km²",
        "gdp": "$2.1 trln", "gdp_pc": "$9,000",
        "education": {"schools": "180,000+", "colleges": "2,400+", "universities": "300+", "academies": "Ko'p"},
        "specialization": "Qishloq xo'jaligi, sanoat",
        "wealth": "Soya, qand, temir", "specialists": "Qishloq xo'jaligi, muhandis",
        "rockets": "VLS (loyiha)", "conflict": "Ichki ijtimoiy keskinlik",
        "peace": True, "weather": "Tropik, subtropik", "farming": "Soya, qand, kofe, apelsin",
        "allies": "BRICS, Mercosur", "army": "334,000",
        "internet": "~81%", "religion": "Xristianlik"
    },
    {
        "name": "Hindiston", "code": "in", "capital": "Yangi Delhi", "region": "Osiyo",
        "lat": 28.6, "lon": 77.2, "color": "#ff5722",
        "president": "Narendra Modi (Bosh vazir)", "language": "Hind, Ingliz",
        "currency": "Rupiya (INR)", "usd_rate": "~1 USD = 83 INR",
        "population": "1.43 mlrd", "area": "3.29 mln km²",
        "gdp": "$3.7 trln", "gdp_pc": "$2,600",
        "education": {"schools": "1.5 mln+", "colleges": "45,000+", "universities": "900+", "academies": "Ko'p"},
        "specialization": "IT, farmatsevtika, kosmik",
        "wealth": "IT xizmatlari, ziravorlar", "specialists": "IT, muhandis, tibbiyot",
        "rockets": "PSLV, GSLV, Chandrayaan", "conflict": "Pokiston chegara, Xitoy chegara",
        "peace": False, "weather": "Tropik, musson", "farming": "Guruch, bug'doy, paxta",
        "allies": "BRICS, Quad, SCO", "army": "1.45 mln",
        "internet": "~52%", "religion": "Hinduizm, Islom"
    },
    {
        "name": "Fransiya", "code": "fr", "capital": "Parij", "region": "Yevropa",
        "lat": 48.8, "lon": 2.3, "color": "#3f51b5",
        "president": "Emmanuel Macron", "language": "Frantsuz tili",
        "currency": "Yevro (EUR)", "usd_rate": "~1 EUR = 1.08 USD",
        "population": "68 mln", "area": "551,695 km²",
        "gdp": "$3.1 trln", "gdp_pc": "$45,000",
        "education": {"schools": "68,000+", "colleges": "2,500+", "universities": "70+", "academies": "Ko'p"},
        "specialization": "Aviatsiya, turizm, mode",
        "wealth": "Turizm, Airbus, vino", "specialists": "Muhandis, san'at, tibbiyot",
        "rockets": "Ariane 5/6", "conflict": "Mali, Sahel",
        "peace": False, "weather": "Mo'tadil, O'rta er", "farming": "Bug'doy, uzum, qand lavlagi",
        "allies": "NATO, EU, G7", "army": "270,000",
        "internet": "~92%", "religion": "Xristianlik (laik davlat)"
    },
    {
        "name": "Saudiya Arabistoni", "code": "sa", "capital": "Ar-Riyod", "region": "Yaqin Sharq",
        "lat": 24.7, "lon": 46.7, "color": "#8bc34a",
        "president": "Muhammad ibn Salmon (Valiahd shahzoda)", "language": "Arab tili",
        "currency": "Riyal (SAR)", "usd_rate": "~1 USD = 3.75 SAR",
        "population": "35 mln", "area": "2.15 mln km²",
        "gdp": "$1.1 trln", "gdp_pc": "$30,000",
        "education": {"schools": "28,000+", "colleges": "2,400+", "universities": "30+", "academies": "Ko'p"},
        "specialization": "Neft, turizm (Vision 2030)",
        "wealth": "Neft (Aramco), gaz", "specialists": "Neft muhandislari",
        "rockets": "Yo'q (loyiha)", "conflict": "Yaman urushi",
        "peace": False, "weather": "Issiq cho'l", "farming": "Xurmo, bug'doy (irrigatsiya)",
        "allies": "G20, Arab Ligasi, AQSh", "army": "230,000",
        "internet": "~97%", "religion": "Islom (sunna)"
    },
    {
        "name": "Turkiya", "code": "tr", "capital": "Anqara", "region": "Yaqin Sharq/Yevropa",
        "lat": 39.9, "lon": 32.9, "color": "#ff6f00",
        "president": "Recep Tayyip Erdoğan", "language": "Turk tili",
        "currency": "Lira (TRY)", "usd_rate": "~1 USD = 32 TRY",
        "population": "85 mln", "area": "783,562 km²",
        "gdp": "$1.0 trln", "gdp_pc": "$12,000",
        "education": {"schools": "60,000+", "colleges": "1,600+", "universities": "210+", "academies": "Ko'p"},
        "specialization": "Qurilish, tekstil, mudofaa",
        "wealth": "Turistik, qurol eksporti (Bayraktar)", "specialists": "Muhandis, turizm",
        "rockets": "Roketsan, Bayraktar TB2", "conflict": "Suriya, Iroq, Kurdlar",
        "peace": False, "weather": "Mo'tadil, O'rta er", "farming": "Bug'doy, paxta, oliva",
        "allies": "NATO, G20", "army": "355,000",
        "internet": "~83%", "religion": "Islom"
    },
    {
        "name": "Avstraliya", "code": "au", "capital": "Kanberra", "region": "Okeaniya",
        "lat": -35.3, "lon": 149.1, "color": "#00acc1",
        "president": "Anthony Albanese (Bosh vazir)", "language": "Ingliz tili",
        "currency": "Avstraliya dollari (AUD)", "usd_rate": "~1 AUD = 0.65 USD",
        "population": "26 mln", "area": "7.69 mln km²",
        "gdp": "$1.7 trln", "gdp_pc": "$65,000",
        "education": {"schools": "9,500+", "colleges": "1,100+", "universities": "40+", "academies": "Ko'p"},
        "specialization": "Kon sanoati, qishloq xo'jaligi",
        "wealth": "Temir, ko'mir, oltin", "specialists": "Muhandis, tibbiyot, IT",
        "rockets": "Yo'q (AUKUS orqali)", "conflict": "Minimal",
        "peace": True, "weather": "Quruq, subtropik", "farming": "Bug'doy, qo'y, sigir",
        "allies": "AUKUS, Five Eyes, NATO (hamkor)", "army": "85,000",
        "internet": "~90%", "religion": "Xristianlik"
    },
    {
        "name": "Kanada", "code": "ca", "capital": "Ottava", "region": "Amerika",
        "lat": 45.4, "lon": -75.7, "color": "#ef5350",
        "president": "Justin Trudeau (Bosh vazir)", "language": "Ingliz, Frantsuz",
        "currency": "Kanada dollari (CAD)", "usd_rate": "~1 CAD = 0.74 USD",
        "population": "38 mln", "area": "9.98 mln km²",
        "gdp": "$2.1 trln", "gdp_pc": "$55,000",
        "education": {"schools": "15,000+", "colleges": "200+", "universities": "100+", "academies": "Ko'p"},
        "specialization": "Resurslar, texnologiya, moliya",
        "wealth": "Neft, yog'och, oltin", "specialists": "IT, tibbiyot, muhandis",
        "rockets": "CSA orqali", "conflict": "Minimal",
        "peace": True, "weather": "Kontinental, arktik", "farming": "Bug'doy, Kanola, arpa",
        "allies": "NATO, G7, NORAD", "army": "68,000",
        "internet": "~93%", "religion": "Xristianlik"
    },
    {
        "name": "Janubiy Koreya", "code": "kr", "capital": "Seul", "region": "Osiyo",
        "lat": 37.6, "lon": 127.0, "color": "#ab47bc",
        "president": "Yoon Suk-yeol", "language": "Koreys tili",
        "currency": "Won (KRW)", "usd_rate": "~1 USD = 1330 KRW",
        "population": "52 mln", "area": "100,339 km²",
        "gdp": "$1.7 trln", "gdp_pc": "$33,000",
        "education": {"schools": "20,000+", "colleges": "1,000+", "universities": "400+", "academies": "Ko'p"},
        "specialization": "Elektronika, avtomobil, kemasozlik",
        "wealth": "Samsung, Hyundai, LG", "specialists": "Muhandis, IT",
        "rockets": "Nuri (KSLV-2)", "conflict": "Shimoliy Koreya tahdidi",
        "peace": False, "weather": "Mo'tadil, musson", "farming": "Guruch, kimchi sabzavotlari",
        "allies": "AQSh, NATO (hamkor)", "army": "600,000",
        "internet": "~98%", "religion": "Xristianlik, Buddizm"
    },
    {
        "name": "Misr", "code": "eg", "capital": "Qohira", "region": "Afrika/Yaqin Sharq",
        "lat": 30.1, "lon": 31.2, "color": "#ffa726",
        "president": "Abdel Fattah el-Sisi", "language": "Arab tili",
        "currency": "Misr funti (EGP)", "usd_rate": "~1 USD = 31 EGP",
        "population": "104 mln", "area": "1 mln km²",
        "gdp": "$480 mlrd", "gdp_pc": "$4,600",
        "education": {"schools": "60,000+", "colleges": "2,000+", "universities": "70+", "academies": "Ko'p"},
        "specialization": "Turizm, Suets kanali, gaz",
        "wealth": "Suets kanali, turizm, gaz", "specialists": "Muhandis, tibbiyot",
        "rockets": "Yo'q", "conflict": "Sinay yarim oroli, Liviya",
        "peace": False, "weather": "Issiq cho'l", "farming": "Bug'doy, guruch, xurmo",
        "allies": "Arab Ligasi, Afrika Ittifoqi", "army": "440,000",
        "internet": "~72%", "religion": "Islom, Xristianlik"
    },
    {
        "name": "Isroil", "code": "il", "capital": "Tel-Aviv / Quddus", "region": "Yaqin Sharq",
        "lat": 31.8, "lon": 35.2, "color": "#42a5f5",
        "president": "Benjamin Netanyahu", "language": "Ibroniy, Arab",
        "currency": "Shekel (ILS)", "usd_rate": "~1 USD = 3.7 ILS",
        "population": "9.7 mln", "area": "20,770 km²",
        "gdp": "$530 mlrd", "gdp_pc": "$54,000",
        "education": {"schools": "4,300+", "colleges": "60+", "universities": "40+", "academies": "Ko'p"},
        "specialization": "Texnologiya, mudofaa, qishloq xo'jaligi",
        "wealth": "Hi-Tech, Kiber, Olmos", "specialists": "IT, mudofaa, tibbiyot",
        "rockets": "Shavit, Arrow (PRO)", "conflict": "Gʻazo, Livan, Eron",
        "peace": False, "weather": "O'rta er, cho'l", "farming": "Tarvuz, apelsin, tomat",
        "allies": "AQSh, NATO (hamkor)", "army": "170,000 (+rezerv)",
        "internet": "~87%", "religion": "Yahudiylik, Islom"
    },
    {
        "name": "Argentina", "code": "ar", "capital": "Buenos Aires", "region": "Amerika",
        "lat": -34.6, "lon": -58.4, "color": "#26c6da",
        "president": "Javier Milei", "language": "Ispan tili",
        "currency": "Peso (ARS)", "usd_rate": "~1 USD = 800+ ARS",
        "population": "45 mln", "area": "2.78 mln km²",
        "gdp": "$640 mlrd", "gdp_pc": "$14,000",
        "education": {"schools": "50,000+", "colleges": "2,000+", "universities": "130+", "academies": "Ko'p"},
        "specialization": "Qishloq xo'jaligi, moliya",
        "wealth": "Soya, bug'doy, litiy", "specialists": "Qishloq xo'jaligi, tibbiyot",
        "rockets": "Tronador (loyiha)", "conflict": "Falkland/Malvinas da'vosi",
        "peace": True, "weather": "Mo'tadil, subtropik", "farming": "Soya, bug'doy, gʻo'za",
        "allies": "Mercosur, BRICS (yangi)", "army": "73,000",
        "internet": "~85%", "religion": "Xristianlik"
    },
    {
        "name": "Nigeriya", "code": "ng", "capital": "Abujo", "region": "Afrika",
        "lat": 9.1, "lon": 7.5, "color": "#66bb6a",
        "president": "Bola Tinubu", "language": "Ingliz tili, Yoruba, Hausa, Igbo",
        "currency": "Naira (NGN)", "usd_rate": "~1 USD = 1400 NGN",
        "population": "220 mln", "area": "923,768 km²",
        "gdp": "$477 mlrd", "gdp_pc": "$2,100",
        "education": {"schools": "100,000+", "colleges": "3,000+", "universities": "200+", "academies": "Ko'p"},
        "specialization": "Neft, qishloq xo'jaligi",
        "wealth": "Neft, gaz, Nollywood", "specialists": "Neft muhandislari, IT",
        "rockets": "Yo'q", "conflict": "Boko Haram, separatizm",
        "peace": False, "weather": "Tropik", "farming": "Kassava, yam, kakao",
        "allies": "Afrika Ittifoqi, ECOWAS", "army": "220,000",
        "internet": "~55%", "religion": "Islom, Xristianlik"
    },
    {
        "name": "Indoneziya", "code": "id", "capital": "Jakarta", "region": "Janubi-Sharqiy Osiyo",
        "lat": -6.2, "lon": 106.8, "color": "#ef5350",
        "president": "Joko Widodo", "language": "Indonez tili",
        "currency": "Rupiya (IDR)", "usd_rate": "~1 USD = 15,700 IDR",
        "population": "275 mln", "area": "1.9 mln km²",
        "gdp": "$1.3 trln", "gdp_pc": "$4,900",
        "education": {"schools": "400,000+", "colleges": "4,500+", "universities": "700+", "academies": "Ko'p"},
        "specialization": "Yoqilg'i, qishloq xo'jaligi, turizm",
        "wealth": "Neft, ko'mir, palma yog'i", "specialists": "Muhandis, turizm",
        "rockets": "Yo'q", "conflict": "Papua separatizm",
        "peace": True, "weather": "Tropik, ekvatorial", "farming": "Guruch, palma, kofe",
        "allies": "G20, ASEAN", "army": "395,000",
        "internet": "~77%", "religion": "Islom"
    },
    {
        "name": "Pokiston", "code": "pk", "capital": "Islomobod", "region": "Janubiy Osiyo",
        "lat": 33.7, "lon": 73.1, "color": "#26a69a",
        "president": "Shehbaz Sharif", "language": "Urdu, Ingliz",
        "currency": "Rupiya (PKR)", "usd_rate": "~1 USD = 278 PKR",
        "population": "231 mln", "area": "881,913 km²",
        "gdp": "$376 mlrd", "gdp_pc": "$1,600",
        "education": {"schools": "260,000+", "colleges": "5,000+", "universities": "200+", "academies": "Ko'p"},
        "specialization": "Tekstil, qishloq xo'jaligi",
        "wealth": "Tekstil, paxta, naryad", "specialists": "Muhandis, IT (diaspora)",
        "rockets": "Shaheen (ballistik)", "conflict": "Hindiston chegara, Afg'on chegara",
        "peace": False, "weather": "Quruq, musson", "farming": "Bug'doy, paxta, shakarqamish",
        "allies": "Xitoy, SCO", "army": "650,000",
        "internet": "~36%", "religion": "Islom"
    },
]

REGIONS = sorted(set(c["region"] for c in countries))

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0; border-bottom: 1px solid #1e3a5f; margin-bottom: 1rem;'>
        <div style='font-size:2rem'>🌍</div>
        <div style='font-family: Space Mono; font-size:0.7rem; color:#546e7a; letter-spacing:2px'>GLOBAL PLATFORM</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**🗺 Mintaqa filtri**")
    selected_region = st.selectbox(
        "Mintaqa",
        ["Barchasi"] + REGIONS,
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("**⚖️ Taqqoslash rejimi**")
    compare_mode = st.checkbox("2 davlatni taqqosla", value=False)

    if compare_mode:
        st.markdown("**Davlat 1:**")
        compare_c1 = st.selectbox("1", [c["name"] for c in countries], key="c1", label_visibility="collapsed")
        st.markdown("**Davlat 2:**")
        compare_c2 = st.selectbox("2", [c["name"] for c in countries], index=1, key="c2", label_visibility="collapsed")

    st.markdown("---")
    total = len(countries)
    peaceful = sum(1 for c in countries if c["peace"])
    st.metric("Jami davlatlar", total)
    st.metric("Tinch davlatlar", f"{peaceful}/{total}")

# ===== TITLE =====
st.markdown('<div class="main-title">🌍 Global Davlatlar Platformasi</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">INTERAKTIV DUNYO ATLASI · v2.0</div>', unsafe_allow_html=True)

# ===== COMPARE MODE =====
if compare_mode:
    c1 = next(x for x in countries if x["name"] == compare_c1)
    c2 = next(x for x in countries if x["name"] == compare_c2)

    st.markdown('<div class="compare-header"><span style="color:#e040fb; font-family: Space Mono; letter-spacing:2px; font-size:0.8rem">⚖️ TAQQOSLASH REJIMI</span></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    def render_compare(col, c):
        with col:
            st.image(f"https://flagcdn.com/w320/{c['code']}.png", width=120)
            st.markdown(f'<div class="hero-name">{c["name"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="hero-capital">🏙 {c["capital"]} · {c["region"]}</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            rows = [
                ("Prezident", c["president"]),
                ("Aholi", c["population"]),
                ("Maydon", c["area"]),
                ("YaIM", c["gdp"]),
                ("Bosh ishlash", c["gdp_pc"]),
                ("Til", c["language"]),
                ("Valyuta", c["currency"]),
                ("Internet", c["internet"]),
                ("Din", c["religion"]),
                ("Ittifoqdoshlar", c["allies"]),
                ("Armiya", c["army"]),
                ("Raketalar", c["rockets"]),
            ]

            for label, val in rows:
                st.markdown(f"""
                <div class="info-row">
                    <span class="info-label">{label}</span>
                    <span class="info-value">{val}</span>
                </div>""", unsafe_allow_html=True)

            badge_html = f'<span class="peace-badge">☮️ Tinch</span>' if c["peace"] else f'<span class="conflict-badge">⚠️ {c["conflict"][:30]}</span>'
            st.markdown(badge_html, unsafe_allow_html=True)

    render_compare(col1, c1)
    render_compare(col2, c2)
    st.stop()

# ===== MAP =====
filtered = [c for c in countries if selected_region == "Barchasi" or c["region"] == selected_region]

m = folium.Map(
    location=[20, 0],
    zoom_start=2,
    tiles="CartoDB dark_matter"
)

for c in filtered:
    popup_html = f"""
    <div style='font-family:sans-serif; min-width:120px'>
        <img src='https://flagcdn.com/w80/{c["code"]}.png' style='width:60px; margin-bottom:4px'><br>
        <b style='font-size:14px'>{c["name"]}</b><br>
        <span style='color:#888; font-size:11px'>{c["capital"]} · {c["population"]}</span>
    </div>
    """
    folium.CircleMarker(
        [c["lat"], c["lon"]],
        radius=8,
        color=c["color"],
        fill=True,
        fill_color=c["color"],
        fill_opacity=0.85,
        popup=folium.Popup(c["name"], max_width=200),
        tooltip=f"{c['name']} — {c['capital']}"
    ).add_to(m)

st.markdown("### 🗺 Xaritadan davlatni tanlang")
map_data = st_folium(m, width="100%", height=460, returned_objects=["last_object_clicked"])

# ===== DETAIL VIEW =====
st.markdown("---")

if map_data and map_data.get("last_object_clicked"):
    clicked = map_data["last_object_clicked"]
    clicked_lat = clicked.get("lat")
    clicked_lng = clicked.get("lng")

    # Find closest country
    if clicked_lat and clicked_lng:
        def dist(c):
            return (c["lat"] - clicked_lat)**2 + (c["lon"] - clicked_lng)**2
        c = min(filtered, key=dist)

        # HERO CARD
        col_flag, col_info = st.columns([1, 3])
        with col_flag:
            st.image(f"https://flagcdn.com/w320/{c['code']}.png", width=180)
        with col_info:
            st.markdown(f'<div class="hero-name">{c["name"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="hero-capital">🏙 {c["capital"]} &nbsp;·&nbsp; 🌍 {c["region"]}</div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            badge_html = f'<span class="peace-badge">☮️ Tinch holat</span>' if c["peace"] else f'<span class="conflict-badge">⚠️ Konflikt: {c["conflict"]}</span>'
            st.markdown(badge_html, unsafe_allow_html=True)

            tags = [c["specialization"], c["religion"], c["weather"]]
            tags_html = "".join(f'<span class="tag">{t}</span>' for t in tags)
            st.markdown(f'<div style="margin-top:0.8rem">{tags_html}</div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # METRICS ROW
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("👥 Aholi", c["population"])
        with m2:
            st.metric("📐 Maydon", c["area"])
        with m3:
            st.metric("💰 YaIM", c["gdp"])
        with m4:
            st.metric("💵 YaIM/kishi", c["gdp_pc"])

        st.markdown("<br>", unsafe_allow_html=True)

        # DETAIL COLUMNS
        left, right = st.columns(2)

        with left:
            # POLITICS
            st.markdown('<div class="section-card"><div class="section-title">🏛 SIYOSAT</div>', unsafe_allow_html=True)
            for label, val in [("Prezident / PM", c["president"]), ("Ittifoqdoshlar", c["allies"]), ("Armiya", c["army"]), ("Raketalar", c["rockets"])]:
                st.markdown(f'<div class="info-row"><span class="info-label">{label}</span><span class="info-value">{val}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # ECONOMY
            st.markdown('<div class="section-card"><div class="section-title">💰 IQTISOD</div>', unsafe_allow_html=True)
            for label, val in [("Valyuta", c["currency"]), ("USD kurs", c["usd_rate"]), ("Boylik manbalari", c["wealth"]), ("Ixtisoslashuv", c["specialization"]), ("Mutaxassislar", c["specialists"])]:
                st.markdown(f'<div class="info-row"><span class="info-label">{label}</span><span class="info-value">{val}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with right:
            # EDUCATION
            st.markdown('<div class="section-card"><div class="section-title">🎓 TA\'LIM</div>', unsafe_allow_html=True)
            for label, val in [("Maktablar", c["education"]["schools"]), ("Kollejlar", c["education"]["colleges"]), ("Universitetlar", c["education"]["universities"]), ("Akademiyalar", c["education"]["academies"])]:
                st.markdown(f'<div class="info-row"><span class="info-label">{label}</span><span class="info-value">{val}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # CULTURE & GEO
            st.markdown('<div class="section-card"><div class="section-title">🌐 MADANIYAT & JUG\'ROFIYA</div>', unsafe_allow_html=True)
            for label, val in [("Til", c["language"]), ("Din", c["religion"]), ("Iqlim", c["weather"]), ("Dehqonchilik", c["farming"]), ("Internet", c["internet"])]:
                st.markdown(f'<div class="info-row"><span class="info-label">{label}</span><span class="info-value">{val}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="placeholder-box">
        <div class="placeholder-icon">🌐</div>
        <div class="placeholder-text">XARITADAN DAVLATNI BOSING</div>
        <div style='color:#37474f; font-size:0.75rem; margin-top:0.5rem'>Yoki yonma-yon taqqoslash uchun sidebar-dan rejimni yoqing</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
st.caption("ℹ️ Ma'lumotlar statik dataset · 2024-yil holati · API ishlatilmagan")
