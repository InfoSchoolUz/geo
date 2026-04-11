import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import pandas as pd

st.set_page_config(
    layout="wide",
    page_title="🌍 Global Intelligence Map",
    page_icon="🌍",
    initial_sidebar_state="expanded"
)

# ===== DARK CYBER THEME =====
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Share+Tech+Mono&display=swap');

html, body, [class*="css"] {
    background-color: #050a0e !important;
    color: #00f5ff !important;
    font-family: 'Share Tech Mono', monospace !important;
}

.stApp { background: #050a0e; }

h1, h2, h3 {
    font-family: 'Orbitron', monospace !important;
    color: #00f5ff !important;
    text-shadow: 0 0 20px #00f5ff88;
}

.metric-box {
    background: linear-gradient(135deg, #0a1628 0%, #0d2137 100%);
    border: 1px solid #00f5ff33;
    border-left: 3px solid #00f5ff;
    border-radius: 4px;
    padding: 12px 16px;
    margin: 6px 0;
    box-shadow: 0 0 15px #00f5ff11;
}
.metric-label {
    font-size: 10px;
    color: #00f5ff88;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 4px;
}
.metric-value {
    font-size: 18px;
    color: #00f5ff;
    font-weight: bold;
    text-shadow: 0 0 10px #00f5ff66;
}

.compare-header {
    background: linear-gradient(90deg, #0a1628, #0d2137);
    border: 1px solid #00f5ff22;
    border-top: 2px solid #00f5ff;
    padding: 16px;
    border-radius: 4px;
    text-align: center;
    margin-bottom: 12px;
}

.flag-container {
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 10px;
    border: 1px solid #00f5ff22;
    border-radius: 4px;
    background: #0a1628;
    margin-bottom: 10px;
}

.stSelectbox > div > div {
    background: #0a1628 !important;
    border: 1px solid #00f5ff44 !important;
    color: #00f5ff !important;
}

.stCheckbox label { color: #00f5ff !important; }

section[data-testid="stSidebar"] {
    background: #030709 !important;
    border-right: 1px solid #00f5ff22 !important;
}

.stButton button {
    background: transparent !important;
    border: 1px solid #00f5ff !important;
    color: #00f5ff !important;
    font-family: 'Share Tech Mono', monospace !important;
    letter-spacing: 1px;
    transition: all 0.3s;
}
.stButton button:hover {
    background: #00f5ff22 !important;
    box-shadow: 0 0 20px #00f5ff44 !important;
}

.win-badge {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 2px;
    font-size: 11px;
    font-weight: bold;
    letter-spacing: 1px;
}
.win { background: #00f5ff22; border: 1px solid #00f5ff; color: #00f5ff; }
.lose { background: #ff006622; border: 1px solid #ff0066; color: #ff0066; }
.tie { background: #ffaa0022; border: 1px solid #ffaa00; color: #ffaa00; }

div[data-testid="stInfo"] {
    background: #0a1628 !important;
    border: 1px solid #00f5ff33 !important;
    color: #00f5ff88 !important;
    border-radius: 4px !important;
}
</style>
""", unsafe_allow_html=True)

# ===== REGION COLORS =====
REGION_COLORS = {
    "Asia": "#ff6b35",
    "Europe": "#00f5ff",
    "Africa": "#ffd700",
    "Americas": "#00ff88",
    "Oceania": "#ff006e",
    "Antarctic": "#aaaaaa",
    "Polar": "#aaaaaa",
}

# ===== LOAD DATA =====
@st.cache_data(ttl=3600)
def load_countries():
    try:
        res = requests.get("https://restcountries.com/v3.1/all", timeout=15)
        res.raise_for_status()
        data = res.json()
        countries = []
        for c in data:
            try:
                latlng = c.get("latlng", [0, 0])
                if len(latlng) < 2:
                    continue
                region = c.get("region", "Other")
                pop = c.get("population", 0)
                area = c.get("area", 0)

                # population density
                density = round(pop / area, 1) if area and area > 0 else 0

                # gini
                gini_dict = c.get("gini", {})
                gini_val = list(gini_dict.values())[-1] if gini_dict else None

                # timezones
                timezones = c.get("timezones", [])

                # borders
                borders = c.get("borders", [])

                # calling codes
                idd = c.get("idd", {})
                root = idd.get("root", "")
                suffixes = idd.get("suffixes", [""])
                calling_code = root + (suffixes[0] if suffixes else "")

                countries.append({
                    "name": c["name"]["common"],
                    "official": c["name"].get("official", c["name"]["common"]),
                    "code": c["cca2"].lower(),
                    "cca3": c.get("cca3", ""),
                    "capital": c.get("capital", ["N/A"])[0],
                    "region": region,
                    "subregion": c.get("subregion", "N/A"),
                    "lat": latlng[0],
                    "lon": latlng[1],
                    "color": REGION_COLORS.get(region, "#00f5ff"),
                    "population": pop,
                    "population_fmt": f"{round(pop/1e6, 2)} mln" if pop >= 1e6 else f"{pop:,}",
                    "area": area,
                    "area_fmt": f"{area:,.0f} km²" if area else "N/A",
                    "density": density,
                    "density_fmt": f"{density} /km²" if density else "N/A",
                    "language": ", ".join(c.get("languages", {}).values()) if c.get("languages") else "N/A",
                    "currency": ", ".join([f"{v['name']} ({v.get('symbol','?')})" for v in c.get("currencies", {}).values()]) if c.get("currencies") else "N/A",
                    "tld": ", ".join(c.get("tld", [])) if c.get("tld") else "N/A",
                    "timezones": ", ".join(timezones[:3]) + ("..." if len(timezones) > 3 else ""),
                    "borders_count": len(borders),
                    "borders": ", ".join(borders[:10]),
                    "calling_code": calling_code or "N/A",
                    "independent": c.get("independent", False),
                    "un_member": c.get("unMember", False),
                    "landlocked": c.get("landlocked", False),
                    "gini": gini_val,
                    "driving_side": c.get("car", {}).get("side", "N/A"),
                    "start_of_week": c.get("startOfWeek", "N/A"),
                    "continent": ", ".join(c.get("continents", [])),
                })
            except Exception as e:
                continue
        return sorted(countries, key=lambda x: x["name"])
    except Exception as e:
        st.error(f"API xatosi: {e}")
        return []

countries = load_countries()

# ===== SIDEBAR =====
with st.sidebar:
    st.markdown('<h3 style="font-family:Orbitron;color:#00f5ff;font-size:14px;letter-spacing:3px;">⚡ CONTROL PANEL</h3>', unsafe_allow_html=True)
    st.divider()

    regions = sorted(set(c["region"] for c in countries if c["region"]))
    selected_region = st.selectbox("🌐 Region filter", ["All"] + regions)

    st.divider()
    compare_mode = st.checkbox("⚖️ Compare Mode")

    if compare_mode:
        country_names = [c["name"] for c in countries]
        c1_name = st.selectbox("🔵 Country 1", country_names, index=0)
        c2_name = st.selectbox("🔴 Country 2", country_names, index=1)

    st.divider()
    map_style = st.selectbox("🗺️ Map Style", ["Dark Matter", "Positron", "OpenStreetMap"])

    st.divider()
    st.markdown(f'<div style="font-size:11px;color:#00f5ff44;letter-spacing:1px;">LOADED: {len(countries)} COUNTRIES</div>', unsafe_allow_html=True)

# ===== TITLE =====
st.markdown('<h1 style="font-size:28px;letter-spacing:4px;margin-bottom:4px;">🌍 GLOBAL INTELLIGENCE MAP</h1>', unsafe_allow_html=True)
st.markdown('<p style="color:#00f5ff66;font-size:12px;letter-spacing:2px;margin-top:0;">REAL-TIME COUNTRY DATA PLATFORM — NO API KEY REQUIRED</p>', unsafe_allow_html=True)

# ===== TOP STATS =====
col_s1, col_s2, col_s3, col_s4 = st.columns(4)
filtered = [c for c in countries if selected_region == "All" or c["region"] == selected_region]
total_pop = sum(c["population"] for c in filtered)
total_area = sum(c["area"] for c in filtered if c["area"])

with col_s1:
    st.markdown(f'<div class="metric-box"><div class="metric-label">Countries</div><div class="metric-value">{len(filtered)}</div></div>', unsafe_allow_html=True)
with col_s2:
    st.markdown(f'<div class="metric-box"><div class="metric-label">Total Population</div><div class="metric-value">{round(total_pop/1e9,2)} B</div></div>', unsafe_allow_html=True)
with col_s3:
    st.markdown(f'<div class="metric-box"><div class="metric-label">Total Area</div><div class="metric-value">{round(total_area/1e6,1)} M km²</div></div>', unsafe_allow_html=True)
with col_s4:
    landlocked = sum(1 for c in filtered if c["landlocked"])
    st.markdown(f'<div class="metric-box"><div class="metric-label">Landlocked</div><div class="metric-value">{landlocked}</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ===== MAP =====
tile_map = {
    "Dark Matter": "CartoDB dark_matter",
    "Positron": "CartoDB positron",
    "OpenStreetMap": "OpenStreetMap"
}

m = folium.Map(
    location=[20, 10],
    zoom_start=2,
    tiles=tile_map[map_style]
)

for c in filtered:
    folium.CircleMarker(
        [c["lat"], c["lon"]],
        radius=5,
        color=c["color"],
        fill=True,
        fill_color=c["color"],
        fill_opacity=0.8,
        weight=1.5,
        tooltip=folium.Tooltip(
            f"<b>{c['name']}</b><br>🏛 {c['capital']}<br>👥 {c['population_fmt']}<br>🌐 {c['region']}",
            style="background:#0a1628;color:#00f5ff;border:1px solid #00f5ff44;font-family:monospace;font-size:12px;"
        )
    ).add_to(m)

map_data = st_folium(m, width="100%", height=480, returned_objects=["last_object_clicked"])

# ===== COMPARE MODE =====
if compare_mode:
    st.markdown("---")
    st.markdown('<h2 style="font-size:18px;letter-spacing:3px;">⚖️ COUNTRY COMPARISON</h2>', unsafe_allow_html=True)

    ca = next((c for c in countries if c["name"] == c1_name), None)
    cb = next((c for c in countries if c["name"] == c2_name), None)

    if ca and cb:
        col1, col_mid, col2 = st.columns([5, 1, 5])

        def render_country(col, c, color):
            with col:
                # Flag
                st.image(f"https://flagcdn.com/w160/{c['code']}.png", use_container_width=False, width=160)
                st.markdown(f'<h3 style="color:{color};font-size:16px;letter-spacing:2px;">{c["name"].upper()}</h3>', unsafe_allow_html=True)
                st.markdown(f'<div style="color:#ffffff66;font-size:11px;margin-bottom:12px;">{c["official"]}</div>', unsafe_allow_html=True)

                fields = [
                    ("🏛 Capital", c["capital"]),
                    ("🌐 Region", f'{c["region"]} / {c["subregion"]}'),
                    ("👥 Population", c["population_fmt"]),
                    ("📐 Area", c["area_fmt"]),
                    ("👨‍👩‍👧 Density", c["density_fmt"]),
                    ("💬 Language", c["language"][:40] + "..." if len(c["language"]) > 40 else c["language"]),
                    ("💰 Currency", c["currency"][:40] + "..." if len(c["currency"]) > 40 else c["currency"]),
                    ("📞 Calling", c["calling_code"]),
                    ("🌐 TLD", c["tld"]),
                    ("⏰ Timezone", c["timezones"]),
                    ("🚗 Drive side", c["driving_side"]),
                    ("🏳️ Landlocked", "Yes" if c["landlocked"] else "No"),
                    ("🇺🇳 UN Member", "Yes" if c["un_member"] else "No"),
                    ("🤝 Borders", f'{c["borders_count"]} countries'),
                    ("📊 Gini Index", str(c["gini"]) if c["gini"] else "N/A"),
                ]
                for label, value in fields:
                    st.markdown(f'<div class="metric-box"><div class="metric-label">{label}</div><div class="metric-value" style="font-size:14px;">{value}</div></div>', unsafe_allow_html=True)

        render_country(col1, ca, "#00f5ff")
        with col_mid:
            st.markdown('<div style="text-align:center;padding-top:120px;font-size:28px;color:#ffffff33;">VS</div>', unsafe_allow_html=True)
        render_country(col2, cb, "#ff006e")

        # ===== COMPARISON CHART =====
        st.markdown("---")
        st.markdown('<h3 style="font-size:15px;letter-spacing:2px;">📊 STATISTICAL COMPARISON</h3>', unsafe_allow_html=True)

        # Winner badges
        def compare_metric(label, val_a, val_b, unit="", higher_is_better=True):
            if val_a == 0 and val_b == 0:
                return
            if val_a > val_b:
                w1, w2 = ("win", "lose") if higher_is_better else ("lose", "win")
            elif val_b > val_a:
                w1, w2 = ("lose", "win") if higher_is_better else ("win", "lose")
            else:
                w1 = w2 = "tie"
            label_map = {"win": "▲ WINNER", "lose": "▼ LOWER", "tie": "= EQUAL"}
            col_a, col_c, col_b = st.columns([4, 3, 4])
            with col_a:
                st.markdown(f'<div style="text-align:right;"><span class="win-badge {w1}">{label_map[w1]}</span><br><span style="font-size:18px;color:#00f5ff;">{val_a:,.1f}{unit}</span></div>', unsafe_allow_html=True)
            with col_c:
                st.markdown(f'<div style="text-align:center;font-size:11px;color:#ffffff66;padding-top:12px;letter-spacing:1px;">{label}</div>', unsafe_allow_html=True)
            with col_b:
                st.markdown(f'<div style="text-align:left;"><span class="win-badge {w2}">{label_map[w2]}</span><br><span style="font-size:18px;color:#ff006e;">{val_b:,.1f}{unit}</span></div>', unsafe_allow_html=True)

        compare_metric("POPULATION", ca["population"]/1e6, cb["population"]/1e6, " M")
        compare_metric("AREA", ca["area"], cb["area"], " km²")
        compare_metric("DENSITY", ca["density"], cb["density"], " /km²")
        compare_metric("BORDER COUNTRIES", ca["borders_count"], cb["borders_count"])
        if ca["gini"] and cb["gini"]:
            compare_metric("GINI INDEX (equality)", ca["gini"], cb["gini"], "", higher_is_better=False)

        # Bar chart — native st.bar_chart
        import pandas as pd
        chart_df = pd.DataFrame({
            ca["name"]: [ca["population"]/1e6, ca["area"]/1000, ca["density"], float(ca["borders_count"])],
            cb["name"]: [cb["population"]/1e6, cb["area"]/1000, cb["density"], float(cb["borders_count"])],
        }, index=["Population (M)", "Area (k km²)", "Density (/km²)", "Borders"])
        st.bar_chart(chart_df, height=300)

    st.stop()

# ===== DETAIL VIEW =====
if map_data and map_data.get("last_object_clicked"):
    lat = map_data["last_object_clicked"]["lat"]
    lon = map_data["last_object_clicked"]["lng"]
    c = min(filtered, key=lambda x: (x["lat"]-lat)**2 + (x["lon"]-lon)**2)

    st.markdown("---")
    col_flag, col_info = st.columns([2, 5])

    with col_flag:
        st.image(f"https://flagcdn.com/w320/{c['code']}.png", use_container_width=True)
        if c["un_member"]:
            st.markdown('<div style="text-align:center;color:#00f5ff88;font-size:11px;letter-spacing:1px;margin-top:8px;">🇺🇳 UN MEMBER</div>', unsafe_allow_html=True)
        if c["independent"]:
            st.markdown('<div style="text-align:center;color:#00ff8888;font-size:11px;letter-spacing:1px;">✅ INDEPENDENT</div>', unsafe_allow_html=True)
        if c["landlocked"]:
            st.markdown('<div style="text-align:center;color:#ffaa0088;font-size:11px;letter-spacing:1px;">🔒 LANDLOCKED</div>', unsafe_allow_html=True)

    with col_info:
        st.markdown(f'<h2 style="font-size:22px;letter-spacing:3px;margin-bottom:2px;">{c["name"].upper()}</h2>', unsafe_allow_html=True)
        st.markdown(f'<div style="color:#ffffff44;font-size:12px;margin-bottom:16px;">{c["official"]}</div>', unsafe_allow_html=True)

        col_a, col_b, col_c = st.columns(3)
        fields_left = [
            ("🏛 Capital", c["capital"]),
            ("🌐 Region", c["region"]),
            ("🗺️ Subregion", c["subregion"]),
            ("🌍 Continent", c["continent"]),
            ("📞 Calling Code", c["calling_code"]),
            ("🌐 TLD", c["tld"]),
        ]
        fields_mid = [
            ("👥 Population", c["population_fmt"]),
            ("📐 Area", c["area_fmt"]),
            ("👨‍👩‍👧 Density", c["density_fmt"]),
            ("🤝 Border Countries", str(c["borders_count"])),
            ("📊 Gini Index", str(c["gini"]) if c["gini"] else "N/A"),
            ("🚗 Driving Side", c["driving_side"]),
        ]
        fields_right = [
            ("💬 Language(s)", c["language"]),
            ("💰 Currency", c["currency"]),
            ("⏰ Timezone(s)", c["timezones"]),
            ("📅 Week starts", c["start_of_week"]),
            ("🌍 Borders", c["borders"] if c["borders"] else "None"),
        ]

        with col_a:
            for label, value in fields_left:
                st.markdown(f'<div class="metric-box"><div class="metric-label">{label}</div><div class="metric-value" style="font-size:13px;">{value}</div></div>', unsafe_allow_html=True)
        with col_b:
            for label, value in fields_mid:
                st.markdown(f'<div class="metric-box"><div class="metric-label">{label}</div><div class="metric-value" style="font-size:13px;">{value}</div></div>', unsafe_allow_html=True)
        with col_c:
            for label, value in fields_right:
                st.markdown(f'<div class="metric-box"><div class="metric-label">{label}</div><div class="metric-value" style="font-size:13px;">{value}</div></div>', unsafe_allow_html=True)

    # Population bar vs world
    st.markdown("---")
    world_pop = sum(x["population"] for x in countries)
    pct = round(c["population"] / world_pop * 100, 3)
    st.markdown(f'<div style="font-size:12px;letter-spacing:2px;color:#00f5ff88;margin-bottom:8px;">WORLD POPULATION SHARE: <span style="color:#00f5ff;">{pct}%</span></div>', unsafe_allow_html=True)
    st.progress(min(pct / 20, 1.0))

else:
    st.info("🖱️ Xaritada davlatni bosing — to'liq ma'lumot ko'rsatiladi")

    # ===== REGION CHART =====
    st.markdown("---")
    st.markdown('<h3 style="font-size:15px;letter-spacing:2px;">📊 REGIONAL OVERVIEW</h3>', unsafe_allow_html=True)
    region_data = {}
    for c in filtered:
        r = c["region"] or "Other"
        if r not in region_data:
            region_data[r] = {"count": 0, "population": 0}
        region_data[r]["count"] += 1
        region_data[r]["population"] += c["population"]

    col_c1, col_c2 = st.columns(2)
    import pandas as pd
    with col_c1:
        st.markdown('<div style="font-size:12px;letter-spacing:2px;color:#00f5ff88;margin-bottom:8px;">COUNTRIES PER REGION</div>', unsafe_allow_html=True)
        df_count = pd.DataFrame({"Countries": {r: v["count"] for r, v in region_data.items()}})
        st.bar_chart(df_count, height=250)

    with col_c2:
        st.markdown('<div style="font-size:12px;letter-spacing:2px;color:#00f5ff88;margin-bottom:8px;">POPULATION SHARE (%)</div>', unsafe_allow_html=True)
        total_p = sum(v["population"] for v in region_data.values())
        for r, v in sorted(region_data.items(), key=lambda x: -x[1]["population"]):
            pct = round(v["population"] / total_p * 100, 1) if total_p else 0
            color = REGION_COLORS.get(r, "#00f5ff")
            st.markdown(f"""
            <div style="margin:4px 0;">
              <div style="display:flex;justify-content:space-between;font-size:11px;color:#ffffff88;margin-bottom:2px;">
                <span>{r}</span><span style="color:{color};">{pct}%</span>
              </div>
              <div style="background:#0a1628;border-radius:2px;height:8px;">
                <div style="width:{pct}%;background:{color};height:8px;border-radius:2px;box-shadow:0 0 6px {color}88;"></div>
              </div>
            </div>""", unsafe_allow_html=True)

    # TOP 10 populous
    st.markdown('<h3 style="font-size:15px;letter-spacing:2px;margin-top:16px;">🏆 TOP 10 MOST POPULOUS</h3>', unsafe_allow_html=True)
    top10 = sorted(filtered, key=lambda x: x["population"], reverse=True)[:10]
    max_pop = top10[0]["population"] if top10 else 1
    for i, c in enumerate(top10):
        pct = c["population"] / max_pop * 100
        color = c["color"]
        st.markdown(f"""
        <div style="margin:5px 0;">
          <div style="display:flex;justify-content:space-between;font-size:11px;color:#ffffff88;margin-bottom:2px;">
            <span style="color:{color};">#{i+1} {c["name"]}</span>
            <span style="color:#00f5ff88;">{c["population_fmt"]}</span>
          </div>
          <div style="background:#0a1628;border-radius:2px;height:10px;">
            <div style="width:{pct:.1f}%;background:{color};height:10px;border-radius:2px;box-shadow:0 0 8px {color}66;"></div>
          </div>
        </div>""", unsafe_allow_html=True)
