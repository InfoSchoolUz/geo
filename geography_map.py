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
[data-testid="stSidebar"] {
    background: #0a1628 !important;
    border-right: 1px solid #1e3a5f;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }

h1 { font-family: 'Orbitron', monospace !important; }

.card {
    background: linear-gradient(135deg, #0d1f35 0%, #0a1628 100%);
    border: 1px solid #1e3a5f;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 0 30px rgba(56,189,248,0.08), inset 0 1px 0 rgba(255,255,255,0.05);
    margin-bottom: 12px;
}
.section-title {
    color: #facc15;
    font-family: 'Orbitron', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    border-bottom: 1px solid #1e3a5f;
    padding-bottom: 6px;
    margin: 16px 0 10px 0;
}
.info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 5px 0;
    border-bottom: 1px solid rgba(30,58,95,0.4);
    font-size: 0.88rem;
}
.info-label { color: #94a3b8; font-weight: 300; }
.info-value { color: #e2e8f0; font-weight: 600; text-align: right; max-width: 60%; }
.badge {
    display: inline-block;
    background: rgba(250,204,21,0.1);
    border: 1px solid rgba(250,204,21,0.3);
    color: #facc15;
    border-radius: 20px;
    padding: 2px 10px;
    font-size: 0.78rem;
    margin: 2px;
}
.country-name {
    font-family: 'Orbitron', monospace;
    font-size: 1.2rem;
    color: #facc15;
    text-align: center;
    margin: 8px 0 4px 0;
    text-shadow: 0 0 20px rgba(250,204,21,0.4);
}
.stat-box {
    background: rgba(250,204,21,0.06);
    border: 1px solid rgba(250,204,21,0.15);
    border-radius: 10px;
    padding: 10px 6px;
    text-align: center;
}
.stat-num {
    font-family: 'Orbitron', monospace;
    font-size: 1rem;
    color: #facc15;
    display: block;
}
.stat-label {
    font-size: 0.68rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}
.hint-box {
    text-align: center;
    padding: 60px 20px;
    color: #334155;
    font-size: 1rem;
    border: 1px dashed #1e3a5f;
    border-radius: 16px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DATA FETCH
# ─────────────────────────────────────────────
@st.cache_data(ttl=3600)
def fetch_data():
    try:
        res = requests.get("https://www.apicountries.com/countries", timeout=15)
        res.raise_for_status()
        return res.json()
    except Exception as e:
        st.error(f"API xato: {e}")
        return None

data = fetch_data()
if not data:
    st.stop()

name_map     = {c.get("name"): c for c in data if c.get("name")}
sorted_names = sorted(name_map.keys())

# ─────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────
if "active_country" not in st.session_state:
    st.session_state.active_country = None

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <h2 style='font-family:Orbitron,monospace;color:#facc15;
               font-size:1rem;letter-spacing:0.1em;margin-bottom:4px;'>
    🌍 GEOGRAFIYA
    </h2>
    <p style='color:#475569;font-size:0.8rem;margin-bottom:20px;'>
    Davlatni tanlang yoki xaritadan bosing
    </p>
    """, unsafe_allow_html=True)

    options = ["— Tanlang —"] + sorted_names

    # Sidebar selectbox — session state bilan sinxron
    current_idx = 0
    if st.session_state.active_country in sorted_names:
        current_idx = sorted_names.index(st.session_state.active_country) + 1

    selected = st.selectbox(
        "🔍 Davlat tanlang",
        options=options,
        index=current_idx,
        key="sidebar_select"
    )

    if selected != "— Tanlang —" and selected != st.session_state.active_country:
        st.session_state.active_country = selected
        st.rerun()

    st.markdown("---")
    st.markdown("""
    <p style='color:#334155;font-size:0.75rem;text-align:center;'>
    APICountries · InfoSchoolUz
    </p>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TITLE
# ─────────────────────────────────────────────
st.markdown("""
<h1 style='text-align:center;color:#facc15;font-size:1.6rem;
           letter-spacing:0.08em;margin-bottom:2px;'>
🌍 GEOGRAFIYA XARITA
</h1>
<p style='text-align:center;color:#475569;font-size:0.85rem;margin-bottom:16px;'>
Chap paneldan tanlang yoki xaritadagi markerga bosing
</p>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# MAP
# ─────────────────────────────────────────────
active   = st.session_state.active_country
active_c = name_map.get(active) if active else None

# Xarita markazi: tanlangan davlatga fly-to
if active_c and active_c.get("latitude") and active_c.get("longitude"):
    map_center = [active_c["latitude"], active_c["longitude"]]
    map_zoom   = 5
else:
    map_center = [20, 0]
    map_zoom   = 2

m = folium.Map(location=map_center, zoom_start=map_zoom, tiles="CartoDB dark_matter")

for c in data:
    lat = c.get("latitude")
    lon = c.get("longitude")
    if lat is None or lon is None:
        continue

    is_active = (c.get("name") == active)

    if is_active:
        # Tanlangan — yashil, katta
        folium.CircleMarker(
            location=[lat, lon], radius=18,
            color="#4ade80", fill=True, fill_color="#4ade80",
            fill_opacity=0.2, weight=0,
        ).add_to(m)
        folium.CircleMarker(
            location=[lat, lon], radius=9,
            color="#ffffff", fill=True, fill_color="#4ade80",
            fill_opacity=1.0, weight=2,
            tooltip=folium.Tooltip(c.get("name"), sticky=True),
            popup=folium.Popup(c.get("name"), max_width=200),
        ).add_to(m)
    else:
        # Oddiy — sariq
        folium.CircleMarker(
            location=[lat, lon], radius=10,
            color="#facc15", fill=True, fill_color="#facc15",
            fill_opacity=0.15, weight=0,
        ).add_to(m)
        folium.CircleMarker(
            location=[lat, lon], radius=5,
            color="#ffffff", fill=True, fill_color="#facc15",
            fill_opacity=1.0, weight=1,
            tooltip=folium.Tooltip(c.get("name"), sticky=True),
            popup=folium.Popup(c.get("name"), max_width=200),
        ).add_to(m)

map_data = st_folium(
    m,
    height=460,
    use_container_width=True,
    returned_objects=["last_object_clicked_tooltip"],
)

# Xaritadan bosildi → session state yangilanadi
clicked_name = map_data.get("last_object_clicked_tooltip")
if clicked_name and clicked_name != active:
    st.session_state.active_country = clicked_name
    st.rerun()

# ─────────────────────────────────────────────
# DATA PANEL
# ─────────────────────────────────────────────
active = st.session_state.active_country
c = name_map.get(active) if active else None

if not c:
    st.markdown("""
    <div class='hint-box'>
        🌍 Chap paneldan davlat tanlang<br>yoki
        xaritadagi <b style='color:#facc15;'>sariq markerga</b> bosing
    </div>
    """, unsafe_allow_html=True)
else:
    population    = c.get("population", 0)
    area          = c.get("area", 0)
    density       = population / area if area else 0
    capital       = c.get("capital", "—")
    region        = c.get("region", "—")
    subregion     = c.get("subregion", "—")
    borders       = c.get("borders", [])
    def safe_list(val):
        if isinstance(val, list): return val
        if isinstance(val, dict): return list(val.values())
        return []

    def parse_languages(val):
        items = safe_list(val)
        result = []
        for l in items:
            if isinstance(l, dict): result.append(l.get("name") or l.get("nativeName") or str(l))
            else: result.append(str(l))
        return ", ".join(result) if result else "—"

    def parse_currencies(val):
        items = safe_list(val)
        result = []
        for x in items:
            if isinstance(x, dict): result.append(x.get("name") or x.get("code") or str(x))
            else: result.append(str(x))
        return ", ".join(result) if result else "—"

    languages     = parse_languages(c.get("languages"))
    currency_text = parse_currencies(c.get("currencies"))
    tld           = ", ".join(safe_list(c.get("topLevelDomain"))) or "—"
    phone         = ", ".join(safe_list(c.get("callingCodes"))) or "—"
    timezones     = c.get("timezones", [])
    car_side      = c.get("carSide", "—")
    car_signs     = ", ".join(c.get("carSigns", [])) if c.get("carSigns") else "—"
    independent   = c.get("independent", None)
    un_member     = c.get("unMember", None)
    gini          = c.get("gini", "—")
    alpha3        = c.get("alpha3Code", "—")
    flag          = c.get("flag", "")

    ind_text = "✅ Ha" if independent else "❌ Yo'q"
    un_text  = "✅ Ha" if un_member  else "❌ Yo'q"

    st.markdown("---")
    col1, col2, col3 = st.columns([1.2, 1.2, 1], gap="medium")

    with col1:
        flag_html = f'<img src="{flag}" style="height:55px;border-radius:4px;box-shadow:0 0 16px rgba(0,0,0,0.6);">' if flag else ""
        st.markdown(f"""
        <div class='card' style='text-align:center;'>
            <div style='margin-bottom:8px;'>{flag_html}</div>
            <div class='country-name'>{active}</div>
            <div style='color:#475569;font-size:0.78rem;'>{region} · {subregion}</div>
        </div>
        <div style='display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:12px;'>
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
        <div class='card'>
            <div class='section-title'>📌 Asosiy</div>
            <div class='info-row'><span class='info-label'>Poytaxt</span><span class='info-value'>{capital}</span></div>
            <div class='info-row'><span class='info-label'>ISO kodi</span><span class='info-value'>{alpha3}</span></div>
            <div class='info-row'><span class='info-label'>Mustaqil</span><span class='info-value'>{ind_text}</span></div>
            <div class='info-row'><span class='info-label'>BMT a'zosi</span><span class='info-value'>{un_text}</span></div>
            <div class='info-row'><span class='info-label'>GINI</span><span class='info-value'>{gini}</span></div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
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
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class='card'>
            <div class='section-title'>🌐 Qo'shni davlatlar</div>
            <div style='padding:8px 0;'>{borders_html}</div>
        </div>
        """, unsafe_allow_html=True)
