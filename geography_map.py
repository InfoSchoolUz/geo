import streamlit as st
import folium
from streamlit_folium import st_folium
import requests

st.set_page_config(page_title="Geografiya Xarita", layout="wide", page_icon="🌍")

# ─────────────────────────────────────────────
# STYLE
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Exo+2:wght@300;400;600&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: #060d1a !important;
    color: #e2e8f0;
    font-family: 'Exo 2', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 20% 10%, #0d2040 0%, #060d1a 60%) !important;
}

h1 { font-family: 'Orbitron', monospace !important; }

.card {
    background: linear-gradient(135deg, #0d1f35 0%, #0a1628 100%);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 0 30px rgba(56,189,248,0.08), inset 0 1px 0 rgba(255,255,255,0.05);
}

.section-title {
    color: #38bdf8;
    font-family: 'Orbitron', monospace;
    font-size: 0.75rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    border-bottom: 1px solid #1e3a5f;
    padding-bottom: 8px;
    margin: 20px 0 12px 0;
}

.info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 6px 0;
    border-bottom: 1px solid rgba(30,58,95,0.4);
    font-size: 0.92rem;
}

.info-label { color: #94a3b8; font-weight: 300; }
.info-value { color: #e2e8f0; font-weight: 600; }

.badge {
    display: inline-block;
    background: rgba(56,189,248,0.12);
    border: 1px solid rgba(56,189,248,0.3);
    color: #38bdf8;
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.8rem;
    margin: 2px;
}

.flag-container {
    text-align: center;
    margin: 12px 0;
}

.country-name {
    font-family: 'Orbitron', monospace;
    font-size: 1.4rem;
    color: #38bdf8;
    text-align: center;
    margin: 8px 0;
    text-shadow: 0 0 20px rgba(56,189,248,0.4);
}

.stat-box {
    background: rgba(56,189,248,0.06);
    border: 1px solid rgba(56,189,248,0.15);
    border-radius: 10px;
    padding: 12px;
    text-align: center;
    margin: 4px;
}

.stat-num {
    font-family: 'Orbitron', monospace;
    font-size: 1.2rem;
    color: #38bdf8;
    display: block;
}

.stat-label {
    font-size: 0.72rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.1em;
}

.hint-box {
    text-align: center;
    padding: 40px;
    color: #334155;
    font-size: 1.1rem;
    border: 1px dashed #1e3a5f;
    border-radius: 16px;
    margin-top: 16px;
}

.stCaption { color: #334155 !important; }

div[data-testid="stHorizontalBlock"] { gap: 8px; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA FETCH
# ─────────────────────────────────────────────
@st.cache_data(ttl=3600)
def fetch_data():
    try:
        url = "https://www.apicountries.com/countries"
        res = requests.get(url, timeout=15)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"API xato: {e}")
        return None

data = fetch_data()

if not data:
    st.stop()

# tooltip → country lookup dict
name_map = {c.get("name"): c for c in data if c.get("name")}

# ─────────────────────────────────────────────
# TITLE
# ─────────────────────────────────────────────
st.markdown("""
<h1 style='text-align:center; color:#38bdf8; font-size:1.8rem; letter-spacing:0.08em; margin-bottom:4px;'>
🌍 GEOGRAFIYA XARITA
</h1>
<p style='text-align:center; color:#475569; font-size:0.9rem; margin-bottom:20px;'>
Davlat markerini bosing → to'liq ma'lumot ko'rining
</p>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAP
# ─────────────────────────────────────────────
m = folium.Map(
    location=[20, 0],
    zoom_start=2,
    tiles="CartoDB dark_matter"
)

for c in data:
    lat = c.get("latitude")
    lon = c.get("longitude")
    if lat is None or lon is None:
        continue

    # Tashqi halqa (glow effect)
    folium.CircleMarker(
        location=[lat, lon],
        radius=10,
        color="#facc15",
        fill=True,
        fill_color="#facc15",
        fill_opacity=0.2,
        weight=0,
    ).add_to(m)

    # Asosiy marker
    folium.CircleMarker(
        location=[lat, lon],
        radius=6,
        color="#ffffff",
        fill=True,
        fill_color="#facc15",
        fill_opacity=1.0,
        weight=1.5,
        tooltip=folium.Tooltip(c.get("name"), sticky=True),
        popup=folium.Popup(c.get("name"), max_width=200),
    ).add_to(m)

map_data = st_folium(
    m,
    height=480,
    use_container_width=True,
    returned_objects=["last_object_clicked_tooltip"],
)

# ─────────────────────────────────────────────
# RESULT
# ─────────────────────────────────────────────
clicked_name = map_data.get("last_object_clicked_tooltip")

if not clicked_name:
    st.markdown("""
    <div class='hint-box'>
        ☝️ Xaritadagi <b style='color:#38bdf8;'>ko'k doirachalardan</b> biriga bosing
    </div>
    """, unsafe_allow_html=True)
else:
    c = name_map.get(clicked_name)

    if c:
        population = c.get("population", 0)
        area = c.get("area", 0)
        density = population / area if area else 0
        capital = c.get("capital", "—")
        region = c.get("region", "—")
        subregion = c.get("subregion", "—")
        borders = c.get("borders", [])
        languages = ", ".join(c.get("languages", [])) if c.get("languages") else "—"
        currencies = c.get("currencies", [])
        currency_text = ", ".join([x.get("name", "") for x in currencies]) if currencies else "—"
        tld = ", ".join(c.get("topLevelDomain", [])) or "—"
        phone = ", ".join(c.get("callingCodes", [])) or "—"
        timezones = c.get("timezones", [])
        car_side = c.get("carSide", "—")
        car_signs = ", ".join(c.get("carSigns", [])) if c.get("carSigns") else "—"
        independent = c.get("independent", None)
        un_member = c.get("unMember", None)
        gini = c.get("gini", "—")
        alpha3 = c.get("alpha3Code", "—")
        flag = c.get("flag", "")

        ind_text = "✅ Ha" if independent else "❌ Yo'q"
        un_text = "✅ Ha" if un_member else "❌ Yo'q"

        st.markdown("---")

        col_left, col_right = st.columns([1, 1], gap="medium")

        with col_left:
            # Header card
            flag_html = f'<img src="{flag}" style="height:60px; border-radius:4px; box-shadow:0 0 12px rgba(0,0,0,0.5);">' if flag else ""
            st.markdown(f"""
            <div class='card' style='text-align:center;'>
                <div class='flag-container'>{flag_html}</div>
                <div class='country-name'>{clicked_name}</div>
                <div style='color:#475569; font-size:0.8rem;'>{region} · {subregion}</div>
            </div>
            """, unsafe_allow_html=True)

            # Stats row
            st.markdown(f"""
            <div style='display:grid; grid-template-columns:1fr 1fr 1fr; gap:8px; margin-top:12px;'>
                <div class='stat-box'>
                    <span class='stat-num'>{population:,.0f}</span>
                    <span class='stat-label'>Aholi</span>
                </div>
                <div class='stat-box'>
                    <span class='stat-num'>{area:,.0f}</span>
                    <span class='stat-label'>km²</span>
                </div>
                <div class='stat-box'>
                    <span class='stat-num'>{density:.1f}</span>
                    <span class='stat-label'>Zichlik</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Geography
            st.markdown(f"""
            <div class='card' style='margin-top:12px;'>
                <div class='section-title'>📌 Asosiy</div>
                <div class='info-row'><span class='info-label'>Poytaxt</span><span class='info-value'>{capital}</span></div>
                <div class='info-row'><span class='info-label'>ISO kodi</span><span class='info-value'>{alpha3}</span></div>
                <div class='info-row'><span class='info-label'>Mustaqil</span><span class='info-value'>{ind_text}</span></div>
                <div class='info-row'><span class='info-label'>BMT a'zosi</span><span class='info-value'>{un_text}</span></div>
                <div class='info-row'><span class='info-label'>GINI</span><span class='info-value'>{gini}</span></div>
            </div>
            """, unsafe_allow_html=True)

        with col_right:
            # Culture
            borders_html = "".join([f"<span class='badge'>{b}</span>" for b in borders]) if borders else "<span style='color:#475569;'>Yo'q</span>"
            st.markdown(f"""
            <div class='card'>
                <div class='section-title'>🗣️ Madaniyat</div>
                <div class='info-row'><span class='info-label'>Tillar</span><span class='info-value'>{languages}</span></div>
                <div class='info-row'><span class='info-label'>Valyuta</span><span class='info-value'>{currency_text}</span></div>

                <div class='section-title'>📡 Texnologiya</div>
                <div class='info-row'><span class='info-label'>Domen</span><span class='info-value'>{tld}</span></div>
                <div class='info-row'><span class='info-label'>Tel. kod</span><span class='info-value'>+{phone}</span></div>
                <div class='info-row'><span class='info-label'>Timezone</span><span class='info-value'>{len(timezones)} ta</span></div>

                <div class='section-title'>🚗 Transport</div>
                <div class='info-row'><span class='info-label'>Yo'l tomoni</span><span class='info-value'>{car_side}</span></div>
                <div class='info-row'><span class='info-label'>Belgilar</span><span class='info-value'>{car_signs}</span></div>

                <div class='section-title'>🌐 Qo'shni davlatlar</div>
                <div style='padding:8px 0;'>{borders_html}</div>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("---")
st.caption("🌍 Geografiya Platformasi · APICountries · InfoSchoolUz")
