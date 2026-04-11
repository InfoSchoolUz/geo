import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

st.set_page_config(layout="wide", page_title="🌍 Global Map", page_icon="🌍")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Share+Tech+Mono&display=swap');
html,body,[class*="css"]{background:#050a0e!important;color:#00f5ff!important;font-family:'Share Tech Mono',monospace!important}
.stApp{background:#050a0e}
h1,h2,h3{font-family:'Orbitron',monospace!important;color:#00f5ff!important;text-shadow:0 0 20px #00f5ff88}
.mb{background:linear-gradient(135deg,#0a1628,#0d2137);border:1px solid #00f5ff33;border-left:3px solid #00f5ff;border-radius:4px;padding:10px 14px;margin:5px 0}
.ml{font-size:10px;color:#00f5ff88;text-transform:uppercase;letter-spacing:2px}
.mv{font-size:15px;color:#00f5ff;font-weight:bold}
.win{background:#00f5ff22;border:1px solid #00f5ff;color:#00f5ff;padding:2px 8px;border-radius:2px;font-size:11px}
.lose{background:#ff006622;border:1px solid #ff0066;color:#ff0066;padding:2px 8px;border-radius:2px;font-size:11px}
.tie{background:#ffaa0022;border:1px solid #ffaa00;color:#ffaa00;padding:2px 8px;border-radius:2px;font-size:11px}
section[data-testid="stSidebar"]{background:#030709!important;border-right:1px solid #00f5ff22!important}
div[data-testid="stInfo"]{background:#0a1628!important;border:1px solid #00f5ff33!important;border-radius:4px!important}
</style>
""", unsafe_allow_html=True)

COUNTRIES = [
    {"name":"Afghanistan","code":"af","capital":"Kabul","region":"Asia","subregion":"Southern Asia","lat":33,"lon":65,"pop":40218234,"area":652230,"lang":"Dari, Pashto","currency":"Afghan afghani (؋)","tld":".af","tz":"UTC+04:30","borders":6,"calling":"+93","landlocked":True,"un":True,"drive":"right","gini":None},
    {"name":"Albania","code":"al","capital":"Tirana","region":"Europe","subregion":"Southern Europe","lat":41,"lon":20,"pop":2837743,"area":28748,"lang":"Albanian","currency":"Albanian lek (L)","tld":".al","tz":"UTC+01:00","borders":5,"calling":"+355","landlocked":False,"un":True,"drive":"right","gini":33.2},
    {"name":"Algeria","code":"dz","capital":"Algiers","region":"Africa","subregion":"Northern Africa","lat":28,"lon":3,"pop":44700000,"area":2381741,"lang":"Arabic, Tamazight","currency":"Algerian dinar (د.ج)","tld":".dz","tz":"UTC+01:00","borders":6,"calling":"+213","landlocked":False,"un":True,"drive":"right","gini":27.6},
    {"name":"Argentina","code":"ar","capital":"Buenos Aires","region":"Americas","subregion":"South America","lat":-34,"lon":-64,"pop":45376763,"area":2780400,"lang":"Spanish","currency":"Argentine peso ($)","tld":".ar","tz":"UTC-03:00","borders":5,"calling":"+54","landlocked":False,"un":True,"drive":"right","gini":42.9},
    {"name":"Australia","code":"au","capital":"Canberra","region":"Oceania","subregion":"Australia and New Zealand","lat":-27,"lon":133,"pop":25687041,"area":7692024,"lang":"English","currency":"Australian dollar ($)","tld":".au","tz":"UTC+10:00","borders":0,"calling":"+61","landlocked":False,"un":True,"drive":"left","gini":34.3},
    {"name":"Austria","code":"at","capital":"Vienna","region":"Europe","subregion":"Central Europe","lat":47.33,"lon":13.33,"pop":9006398,"area":83871,"lang":"German","currency":"Euro (€)","tld":".at","tz":"UTC+01:00","borders":8,"calling":"+43","landlocked":True,"un":True,"drive":"right","gini":30.5},
    {"name":"Bangladesh","code":"bd","capital":"Dhaka","region":"Asia","subregion":"Southern Asia","lat":24,"lon":90,"pop":166303498,"area":147570,"lang":"Bengali","currency":"Bangladeshi taka (৳)","tld":".bd","tz":"UTC+06:00","borders":2,"calling":"+880","landlocked":False,"un":True,"drive":"left","gini":32.4},
    {"name":"Belgium","code":"be","capital":"Brussels","region":"Europe","subregion":"Western Europe","lat":50.83,"lon":4,"pop":11555997,"area":30528,"lang":"Dutch, French, German","currency":"Euro (€)","tld":".be","tz":"UTC+01:00","borders":4,"calling":"+32","landlocked":False,"un":True,"drive":"right","gini":27.2},
    {"name":"Brazil","code":"br","capital":"Brasília","region":"Americas","subregion":"South America","lat":-10,"lon":-55,"pop":214326223,"area":8515767,"lang":"Portuguese","currency":"Brazilian real (R$)","tld":".br","tz":"UTC-03:00","borders":10,"calling":"+55","landlocked":False,"un":True,"drive":"right","gini":53.4},
    {"name":"Canada","code":"ca","capital":"Ottawa","region":"Americas","subregion":"North America","lat":60,"lon":-95,"pop":38005238,"area":9984670,"lang":"English, French","currency":"Canadian dollar ($)","tld":".ca","tz":"UTC-05:00","borders":1,"calling":"+1","landlocked":False,"un":True,"drive":"right","gini":33.3},
    {"name":"Chile","code":"cl","capital":"Santiago","region":"Americas","subregion":"South America","lat":-30,"lon":-71,"pop":19116201,"area":756102,"lang":"Spanish","currency":"Chilean peso ($)","tld":".cl","tz":"UTC-04:00","borders":3,"calling":"+56","landlocked":False,"un":True,"drive":"right","gini":44.4},
    {"name":"China","code":"cn","capital":"Beijing","region":"Asia","subregion":"Eastern Asia","lat":35,"lon":105,"pop":1402112000,"area":9706961,"lang":"Chinese","currency":"Chinese yuan (¥)","tld":".cn","tz":"UTC+08:00","borders":14,"calling":"+86","landlocked":False,"un":True,"drive":"right","gini":38.5},
    {"name":"Colombia","code":"co","capital":"Bogotá","region":"Americas","subregion":"South America","lat":4,"lon":-72,"pop":51874024,"area":1141748,"lang":"Spanish","currency":"Colombian peso ($)","tld":".co","tz":"UTC-05:00","borders":5,"calling":"+57","landlocked":False,"un":True,"drive":"right","gini":51.3},
    {"name":"Czech Republic","code":"cz","capital":"Prague","region":"Europe","subregion":"Central Europe","lat":49.75,"lon":15.5,"pop":10701777,"area":78865,"lang":"Czech","currency":"Czech koruna (Kč)","tld":".cz","tz":"UTC+01:00","borders":4,"calling":"+420","landlocked":True,"un":True,"drive":"right","gini":25.3},
    {"name":"Denmark","code":"dk","capital":"Copenhagen","region":"Europe","subregion":"Northern Europe","lat":56,"lon":10,"pop":5831404,"area":42924,"lang":"Danish","currency":"Danish krone (kr)","tld":".dk","tz":"UTC+01:00","borders":1,"calling":"+45","landlocked":False,"un":True,"drive":"right","gini":29.0},
    {"name":"Egypt","code":"eg","capital":"Cairo","region":"Africa","subregion":"Northern Africa","lat":27,"lon":30,"pop":102334404,"area":1002450,"lang":"Arabic","currency":"Egyptian pound (£)","tld":".eg","tz":"UTC+02:00","borders":4,"calling":"+20","landlocked":False,"un":True,"drive":"right","gini":31.5},
    {"name":"Ethiopia","code":"et","capital":"Addis Ababa","region":"Africa","subregion":"Eastern Africa","lat":8,"lon":38,"pop":117876227,"area":1104300,"lang":"Oromo, Amharic","currency":"Ethiopian birr (Br)","tld":".et","tz":"UTC+03:00","borders":6,"calling":"+251","landlocked":True,"un":True,"drive":"right","gini":35.0},
    {"name":"Finland","code":"fi","capital":"Helsinki","region":"Europe","subregion":"Northern Europe","lat":64,"lon":26,"pop":5530719,"area":338424,"lang":"Finnish, Swedish","currency":"Euro (€)","tld":".fi","tz":"UTC+02:00","borders":3,"calling":"+358","landlocked":False,"un":True,"drive":"right","gini":27.7},
    {"name":"France","code":"fr","capital":"Paris","region":"Europe","subregion":"Western Europe","lat":46,"lon":2,"pop":67391582,"area":551695,"lang":"French","currency":"Euro (€)","tld":".fr","tz":"UTC+01:00","borders":8,"calling":"+33","landlocked":False,"un":True,"drive":"right","gini":32.4},
    {"name":"Germany","code":"de","capital":"Berlin","region":"Europe","subregion":"Western Europe","lat":51,"lon":9,"pop":83240525,"area":357114,"lang":"German","currency":"Euro (€)","tld":".de","tz":"UTC+01:00","borders":9,"calling":"+49","landlocked":False,"un":True,"drive":"right","gini":31.9},
    {"name":"Ghana","code":"gh","capital":"Accra","region":"Africa","subregion":"Western Africa","lat":8,"lon":-2,"pop":31072940,"area":238533,"lang":"English","currency":"Ghanaian cedi (₵)","tld":".gh","tz":"UTC","borders":3,"calling":"+233","landlocked":False,"un":True,"drive":"right","gini":43.5},
    {"name":"Greece","code":"gr","capital":"Athens","region":"Europe","subregion":"Southern Europe","lat":39,"lon":22,"pop":10715549,"area":131990,"lang":"Greek","currency":"Euro (€)","tld":".gr","tz":"UTC+02:00","borders":4,"calling":"+30","landlocked":False,"un":True,"drive":"right","gini":32.9},
    {"name":"Hungary","code":"hu","capital":"Budapest","region":"Europe","subregion":"Central Europe","lat":47,"lon":20,"pop":9749763,"area":93028,"lang":"Hungarian","currency":"Hungarian forint (Ft)","tld":".hu","tz":"UTC+01:00","borders":7,"calling":"+36","landlocked":True,"un":True,"drive":"right","gini":30.4},
    {"name":"India","code":"in","capital":"New Delhi","region":"Asia","subregion":"Southern Asia","lat":20,"lon":77,"pop":1380004385,"area":3287590,"lang":"Hindi, English","currency":"Indian rupee (₹)","tld":".in","tz":"UTC+05:30","borders":6,"calling":"+91","landlocked":False,"un":True,"drive":"left","gini":35.7},
    {"name":"Indonesia","code":"id","capital":"Jakarta","region":"Asia","subregion":"South-Eastern Asia","lat":-5,"lon":120,"pop":273523621,"area":1904569,"lang":"Indonesian","currency":"Indonesian rupiah (Rp)","tld":".id","tz":"UTC+07:00","borders":3,"calling":"+62","landlocked":False,"un":True,"drive":"left","gini":38.2},
    {"name":"Iran","code":"ir","capital":"Tehran","region":"Asia","subregion":"Southern Asia","lat":32,"lon":53,"pop":83992953,"area":1648195,"lang":"Persian","currency":"Iranian rial (﷼)","tld":".ir","tz":"UTC+03:30","borders":7,"calling":"+98","landlocked":False,"un":True,"drive":"right","gini":42.0},
    {"name":"Iraq","code":"iq","capital":"Baghdad","region":"Asia","subregion":"Western Asia","lat":33,"lon":44,"pop":40222493,"area":438317,"lang":"Arabic, Kurdish","currency":"Iraqi dinar (ع.د)","tld":".iq","tz":"UTC+03:00","borders":6,"calling":"+964","landlocked":False,"un":True,"drive":"right","gini":29.5},
    {"name":"Ireland","code":"ie","capital":"Dublin","region":"Europe","subregion":"Northern Europe","lat":53,"lon":-8,"pop":4994724,"area":70273,"lang":"Irish, English","currency":"Euro (€)","tld":".ie","tz":"UTC","borders":1,"calling":"+353","landlocked":False,"un":True,"drive":"left","gini":31.4},
    {"name":"Israel","code":"il","capital":"Jerusalem","region":"Asia","subregion":"Western Asia","lat":31.5,"lon":34.75,"pop":9216900,"area":20770,"lang":"Hebrew, Arabic","currency":"Israeli new shekel (₪)","tld":".il","tz":"UTC+02:00","borders":4,"calling":"+972","landlocked":False,"un":True,"drive":"right","gini":39.0},
    {"name":"Italy","code":"it","capital":"Rome","region":"Europe","subregion":"Southern Europe","lat":42.83,"lon":12.83,"pop":59554023,"area":301336,"lang":"Italian","currency":"Euro (€)","tld":".it","tz":"UTC+01:00","borders":6,"calling":"+39","landlocked":False,"un":True,"drive":"right","gini":35.9},
    {"name":"Japan","code":"jp","capital":"Tokyo","region":"Asia","subregion":"Eastern Asia","lat":36,"lon":138,"pop":125836021,"area":377930,"lang":"Japanese","currency":"Japanese yen (¥)","tld":".jp","tz":"UTC+09:00","borders":0,"calling":"+81","landlocked":False,"un":True,"drive":"left","gini":32.9},
    {"name":"Kazakhstan","code":"kz","capital":"Astana","region":"Asia","subregion":"Central Asia","lat":48,"lon":68,"pop":18754440,"area":2724900,"lang":"Kazakh, Russian","currency":"Kazakhstani tenge (₸)","tld":".kz","tz":"UTC+06:00","borders":5,"calling":"+7","landlocked":True,"un":True,"drive":"right","gini":27.8},
    {"name":"Kenya","code":"ke","capital":"Nairobi","region":"Africa","subregion":"Eastern Africa","lat":1,"lon":38,"pop":53771296,"area":580367,"lang":"Swahili, English","currency":"Kenyan shilling (Ksh)","tld":".ke","tz":"UTC+03:00","borders":5,"calling":"+254","landlocked":False,"un":True,"drive":"left","gini":40.8},
    {"name":"Malaysia","code":"my","capital":"Kuala Lumpur","region":"Asia","subregion":"South-Eastern Asia","lat":2.5,"lon":112.5,"pop":32365999,"area":329613,"lang":"Malay","currency":"Malaysian ringgit (RM)","tld":".my","tz":"UTC+08:00","borders":3,"calling":"+60","landlocked":False,"un":True,"drive":"left","gini":41.1},
    {"name":"Mexico","code":"mx","capital":"Mexico City","region":"Americas","subregion":"North America","lat":23,"lon":-102,"pop":128932753,"area":1964375,"lang":"Spanish","currency":"Mexican peso ($)","tld":".mx","tz":"UTC-06:00","borders":3,"calling":"+52","landlocked":False,"un":True,"drive":"right","gini":45.4},
    {"name":"Morocco","code":"ma","capital":"Rabat","region":"Africa","subregion":"Northern Africa","lat":32,"lon":-5,"pop":36910560,"area":446550,"lang":"Arabic, Berber","currency":"Moroccan dirham (د.م.)","tld":".ma","tz":"UTC+01:00","borders":2,"calling":"+212","landlocked":False,"un":True,"drive":"right","gini":39.5},
    {"name":"Netherlands","code":"nl","capital":"Amsterdam","region":"Europe","subregion":"Western Europe","lat":52.5,"lon":5.75,"pop":17441139,"area":41543,"lang":"Dutch","currency":"Euro (€)","tld":".nl","tz":"UTC+01:00","borders":3,"calling":"+31","landlocked":False,"un":True,"drive":"right","gini":28.2},
    {"name":"New Zealand","code":"nz","capital":"Wellington","region":"Oceania","subregion":"Australia and New Zealand","lat":-41,"lon":174,"pop":5084300,"area":270467,"lang":"English, Māori","currency":"New Zealand dollar ($)","tld":".nz","tz":"UTC+12:00","borders":0,"calling":"+64","landlocked":False,"un":True,"drive":"left","gini":36.2},
    {"name":"Nigeria","code":"ng","capital":"Abuja","region":"Africa","subregion":"Western Africa","lat":10,"lon":8,"pop":206139589,"area":923768,"lang":"English","currency":"Nigerian naira (₦)","tld":".ng","tz":"UTC+01:00","borders":4,"calling":"+234","landlocked":False,"un":True,"drive":"right","gini":35.1},
    {"name":"Norway","code":"no","capital":"Oslo","region":"Europe","subregion":"Northern Europe","lat":62,"lon":10,"pop":5379475,"area":323802,"lang":"Norwegian","currency":"Norwegian krone (kr)","tld":".no","tz":"UTC+01:00","borders":3,"calling":"+47","landlocked":False,"un":True,"drive":"right","gini":26.1},
    {"name":"Pakistan","code":"pk","capital":"Islamabad","region":"Asia","subregion":"Southern Asia","lat":30,"lon":70,"pop":220892340,"area":881912,"lang":"Urdu, English","currency":"Pakistani rupee (₨)","tld":".pk","tz":"UTC+05:00","borders":6,"calling":"+92","landlocked":False,"un":True,"drive":"left","gini":31.6},
    {"name":"Peru","code":"pe","capital":"Lima","region":"Americas","subregion":"South America","lat":-10,"lon":-76,"pop":32971854,"area":1285216,"lang":"Spanish, Quechua","currency":"Peruvian sol (S/.)","tld":".pe","tz":"UTC-05:00","borders":5,"calling":"+51","landlocked":False,"un":True,"drive":"right","gini":43.8},
    {"name":"Philippines","code":"ph","capital":"Manila","region":"Asia","subregion":"South-Eastern Asia","lat":13,"lon":122,"pop":109581078,"area":342353,"lang":"Filipino, English","currency":"Philippine peso (₱)","tld":".ph","tz":"UTC+08:00","borders":0,"calling":"+63","landlocked":False,"un":True,"drive":"right","gini":42.3},
    {"name":"Poland","code":"pl","capital":"Warsaw","region":"Europe","subregion":"Central Europe","lat":52,"lon":20,"pop":37950802,"area":312679,"lang":"Polish","currency":"Polish złoty (zł)","tld":".pl","tz":"UTC+01:00","borders":7,"calling":"+48","landlocked":False,"un":True,"drive":"right","gini":30.2},
    {"name":"Portugal","code":"pt","capital":"Lisbon","region":"Europe","subregion":"Southern Europe","lat":39.5,"lon":-8,"pop":10305564,"area":92212,"lang":"Portuguese","currency":"Euro (€)","tld":".pt","tz":"UTC","borders":1,"calling":"+351","landlocked":False,"un":True,"drive":"right","gini":33.5},
    {"name":"Romania","code":"ro","capital":"Bucharest","region":"Europe","subregion":"Eastern Europe","lat":46,"lon":25,"pop":19237691,"area":238397,"lang":"Romanian","currency":"Romanian leu (lei)","tld":".ro","tz":"UTC+02:00","borders":5,"calling":"+40","landlocked":False,"un":True,"drive":"right","gini":34.8},
    {"name":"Russia","code":"ru","capital":"Moscow","region":"Europe","subregion":"Eastern Europe","lat":60,"lon":100,"pop":144104080,"area":17098242,"lang":"Russian","currency":"Russian ruble (₽)","tld":".ru","tz":"UTC+03:00","borders":14,"calling":"+7","landlocked":False,"un":True,"drive":"right","gini":37.5},
    {"name":"Saudi Arabia","code":"sa","capital":"Riyadh","region":"Asia","subregion":"Western Asia","lat":25,"lon":45,"pop":34813871,"area":2149690,"lang":"Arabic","currency":"Saudi riyal (ر.س)","tld":".sa","tz":"UTC+03:00","borders":4,"calling":"+966","landlocked":False,"un":True,"drive":"right","gini":45.9},
    {"name":"South Africa","code":"za","capital":"Pretoria","region":"Africa","subregion":"Southern Africa","lat":-29,"lon":25,"pop":59308690,"area":1221037,"lang":"Zulu, Xhosa, Afrikaans","currency":"South African rand (R)","tld":".za","tz":"UTC+02:00","borders":6,"calling":"+27","landlocked":False,"un":True,"drive":"left","gini":63.0},
    {"name":"South Korea","code":"kr","capital":"Seoul","region":"Asia","subregion":"Eastern Asia","lat":37,"lon":127.5,"pop":51780579,"area":100210,"lang":"Korean","currency":"South Korean won (₩)","tld":".kr","tz":"UTC+09:00","borders":1,"calling":"+82","landlocked":False,"un":True,"drive":"right","gini":31.4},
    {"name":"Spain","code":"es","capital":"Madrid","region":"Europe","subregion":"Southern Europe","lat":40,"lon":-4,"pop":47351567,"area":505990,"lang":"Spanish","currency":"Euro (€)","tld":".es","tz":"UTC+01:00","borders":5,"calling":"+34","landlocked":False,"un":True,"drive":"right","gini":34.7},
    {"name":"Sweden","code":"se","capital":"Stockholm","region":"Europe","subregion":"Northern Europe","lat":62,"lon":15,"pop":10353442,"area":450295,"lang":"Swedish","currency":"Swedish krona (kr)","tld":".se","tz":"UTC+01:00","borders":2,"calling":"+46","landlocked":False,"un":True,"drive":"right","gini":29.3},
    {"name":"Switzerland","code":"ch","capital":"Bern","region":"Europe","subregion":"Western Europe","lat":47,"lon":8,"pop":8654622,"area":41285,"lang":"German, French, Italian","currency":"Swiss franc (Fr)","tld":".ch","tz":"UTC+01:00","borders":5,"calling":"+41","landlocked":True,"un":True,"drive":"right","gini":33.1},
    {"name":"Thailand","code":"th","capital":"Bangkok","region":"Asia","subregion":"South-Eastern Asia","lat":15,"lon":100,"pop":69799978,"area":513120,"lang":"Thai","currency":"Thai baht (฿)","tld":".th","tz":"UTC+07:00","borders":4,"calling":"+66","landlocked":False,"un":True,"drive":"left","gini":36.4},
    {"name":"Turkey","code":"tr","capital":"Ankara","region":"Asia","subregion":"Western Asia","lat":39,"lon":35,"pop":84339067,"area":783562,"lang":"Turkish","currency":"Turkish lira (₺)","tld":".tr","tz":"UTC+03:00","borders":8,"calling":"+90","landlocked":False,"un":True,"drive":"right","gini":41.9},
    {"name":"Ukraine","code":"ua","capital":"Kyiv","region":"Europe","subregion":"Eastern Europe","lat":49,"lon":32,"pop":43733762,"area":603550,"lang":"Ukrainian","currency":"Ukrainian hryvnia (₴)","tld":".ua","tz":"UTC+02:00","borders":7,"calling":"+380","landlocked":False,"un":True,"drive":"right","gini":26.6},
    {"name":"United Arab Emirates","code":"ae","capital":"Abu Dhabi","region":"Asia","subregion":"Western Asia","lat":24,"lon":54,"pop":9890402,"area":83600,"lang":"Arabic","currency":"UAE dirham (د.إ)","tld":".ae","tz":"UTC+04:00","borders":2,"calling":"+971","landlocked":False,"un":True,"drive":"right","gini":None},
    {"name":"United Kingdom","code":"gb","capital":"London","region":"Europe","subregion":"Northern Europe","lat":54,"lon":-2,"pop":67215293,"area":242900,"lang":"English","currency":"Pound sterling (£)","tld":".uk","tz":"UTC","borders":1,"calling":"+44","landlocked":False,"un":True,"drive":"left","gini":35.1},
    {"name":"United States","code":"us","capital":"Washington D.C.","region":"Americas","subregion":"North America","lat":38,"lon":-97,"pop":329484123,"area":9372610,"lang":"English","currency":"United States dollar ($)","tld":".us","tz":"UTC-05:00","borders":2,"calling":"+1","landlocked":False,"un":True,"drive":"right","gini":41.4},
    {"name":"Uzbekistan","code":"uz","capital":"Tashkent","region":"Asia","subregion":"Central Asia","lat":41,"lon":64,"pop":35300000,"area":447400,"lang":"Uzbek","currency":"Uzbekistani soʻm (so'm)","tld":".uz","tz":"UTC+05:00","borders":5,"calling":"+998","landlocked":True,"un":True,"drive":"right","gini":35.3},
    {"name":"Venezuela","code":"ve","capital":"Caracas","region":"Americas","subregion":"South America","lat":8,"lon":-66,"pop":28435943,"area":916445,"lang":"Spanish","currency":"Venezuelan bolívar (Bs.F)","tld":".ve","tz":"UTC-04:00","borders":3,"calling":"+58","landlocked":False,"un":True,"drive":"right","gini":44.8},
    {"name":"Vietnam","code":"vn","capital":"Hanoi","region":"Asia","subregion":"South-Eastern Asia","lat":16,"lon":106,"pop":97338579,"area":331212,"lang":"Vietnamese","currency":"Vietnamese đồng (₫)","tld":".vn","tz":"UTC+07:00","borders":3,"calling":"+84","landlocked":False,"un":True,"drive":"right","gini":35.7},
]

for c in COUNTRIES:
    c["density"] = round(c["pop"]/c["area"],1) if c["area"] else 0
    c["pop_fmt"] = f"{round(c['pop']/1e6,2)} mln" if c["pop"]>=1e6 else f"{c['pop']:,}"
    c["area_fmt"] = f"{c['area']:,.0f} km²"

REGION_COLORS = {"Asia":"#ff6b35","Europe":"#00f5ff","Africa":"#ffd700","Americas":"#00ff88","Oceania":"#ff006e"}

with st.sidebar:
    st.markdown("### ⚡ FILTER")
    regions = sorted(set(c["region"] for c in COUNTRIES))
    sel_region = st.selectbox("🌐 Region", ["All"]+regions)
    st.divider()
    compare_mode = st.checkbox("⚖️ Compare Mode")
    if compare_mode:
        names = [c["name"] for c in COUNTRIES]
        c1n = st.selectbox("🔵 Country 1", names, index=names.index("Uzbekistan"))
        c2n = st.selectbox("🔴 Country 2", names, index=names.index("Kazakhstan"))
    st.divider()
    map_style = st.selectbox("🗺️ Map", ["Dark Matter","Positron","OpenStreetMap"])

st.markdown('<h1 style="font-size:26px;letter-spacing:3px;">🌍 GLOBAL INTELLIGENCE MAP</h1>', unsafe_allow_html=True)
st.markdown(f'<p style="color:#00f5ff66;font-size:11px;letter-spacing:2px;">{len(COUNTRIES)} COUNTRIES — OFFLINE — NO API KEY</p>', unsafe_allow_html=True)

filtered = [c for c in COUNTRIES if sel_region=="All" or c["region"]==sel_region]

def mbox(col, label, val):
    col.markdown(f'<div class="mb"><div class="ml">{label}</div><div class="mv">{val}</div></div>', unsafe_allow_html=True)

c1s,c2s,c3s,c4s = st.columns(4)
mbox(c1s,"Countries",len(filtered))
mbox(c2s,"Population",f"{round(sum(c['pop'] for c in filtered)/1e9,2)} B")
mbox(c3s,"Total Area",f"{round(sum(c['area'] for c in filtered)/1e6,1)} M km²")
mbox(c4s,"Landlocked",sum(1 for c in filtered if c["landlocked"]))

st.markdown("<br>",unsafe_allow_html=True)

tiles={"Dark Matter":"CartoDB dark_matter","Positron":"CartoDB positron","OpenStreetMap":"OpenStreetMap"}
m=folium.Map(location=[20,10],zoom_start=2,tiles=tiles[map_style])
for c in filtered:
    folium.CircleMarker([c["lat"],c["lon"]],radius=5,
        color=REGION_COLORS.get(c["region"],"#00f5ff"),fill=True,fill_opacity=0.8,weight=1.5,
        tooltip=folium.Tooltip(f"<b>{c['name']}</b><br>🏛 {c['capital']}<br>👥 {c['pop_fmt']}<br>🌐 {c['region']}",
            style="background:#0a1628;color:#00f5ff;border:1px solid #00f5ff44;font-family:monospace;font-size:12px;")
    ).add_to(m)
map_data=st_folium(m,width="100%",height=460,returned_objects=["last_object_clicked"])

if compare_mode:
    st.markdown("---")
    st.markdown('<h2 style="font-size:16px;letter-spacing:3px;">⚖️ COMPARISON</h2>',unsafe_allow_html=True)
    ca=next((c for c in COUNTRIES if c["name"]==c1n),None)
    cb=next((c for c in COUNTRIES if c["name"]==c2n),None)
    if ca and cb:
        col1,colm,col2=st.columns([5,1,5])
        def render(col,c,color):
            with col:
                st.image(f"https://flagcdn.com/w160/{c['code']}.png",width=160)
                st.markdown(f'<h3 style="color:{color};font-size:15px;">{c["name"].upper()}</h3>',unsafe_allow_html=True)
                for lbl,val in [("🏛 Capital",c["capital"]),("🌐 Region",c["region"]),("👥 Population",c["pop_fmt"]),
                    ("📐 Area",c["area_fmt"]),("👨 Density",f"{c['density']} /km²"),("💬 Language",c["lang"]),
                    ("💰 Currency",c["currency"]),("📞 Calling",c["calling"]),("🌐 TLD",c["tld"]),
                    ("⏰ Timezone",c["tz"]),("🚗 Drive",c["drive"]),("🏳️ Landlocked","Yes" if c["landlocked"] else "No"),
                    ("🇺🇳 UN","Yes" if c["un"] else "No"),("🤝 Borders",f'{c["borders"]} countries'),
                    ("📊 Gini",str(c["gini"]) if c["gini"] else "N/A")]:
                    st.markdown(f'<div class="mb"><div class="ml">{lbl}</div><div class="mv" style="font-size:13px;">{val}</div></div>',unsafe_allow_html=True)
        render(col1,ca,"#00f5ff")
        with colm:
            st.markdown('<div style="text-align:center;padding-top:100px;font-size:24px;color:#ffffff33;">VS</div>',unsafe_allow_html=True)
        render(col2,cb,"#ff006e")
        st.markdown("---")
        st.markdown('<h3 style="font-size:14px;letter-spacing:2px;">📊 HEAD TO HEAD</h3>',unsafe_allow_html=True)
        def h2h(label,va,vb,unit="",hib=True):
            if va==vb: w1=w2="tie"
            elif va>vb: w1,w2=("win","lose") if hib else ("lose","win")
            else: w1,w2=("lose","win") if hib else ("win","lose")
            lm={"win":"▲ WINNER","lose":"▼ LOWER","tie":"= EQUAL"}
            a,b,c_=st.columns([4,3,4])
            a.markdown(f'<div style="text-align:right"><span class="{w1}">{lm[w1]}</span><br><b style="color:#00f5ff;font-size:16px">{va:,.1f}{unit}</b></div>',unsafe_allow_html=True)
            b.markdown(f'<div style="text-align:center;font-size:10px;color:#ffffff66;padding-top:10px;letter-spacing:1px">{label}</div>',unsafe_allow_html=True)
            c_.markdown(f'<div style="text-align:left"><span class="{w2}">{lm[w2]}</span><br><b style="color:#ff006e;font-size:16px">{vb:,.1f}{unit}</b></div>',unsafe_allow_html=True)
        h2h("POPULATION (M)",ca["pop"]/1e6,cb["pop"]/1e6," M")
        h2h("AREA (km²)",ca["area"],cb["area"]," km²")
        h2h("DENSITY",ca["density"],cb["density"]," /km²")
        h2h("BORDERS",float(ca["borders"]),float(cb["borders"]))
        if ca["gini"] and cb["gini"]: h2h("GINI (lower=equal)",ca["gini"],cb["gini"],"",hib=False)
        df=pd.DataFrame({ca["name"]:[ca["pop"]/1e6,ca["area"]/1000,ca["density"],float(ca["borders"])],
            cb["name"]:[cb["pop"]/1e6,cb["area"]/1000,cb["density"],float(cb["borders"])]},
            index=["Population(M)","Area(k km²)","Density","Borders"])
        st.bar_chart(df,height=260)
    st.stop()

if map_data and map_data.get("last_object_clicked"):
    lat=map_data["last_object_clicked"]["lat"]
    lon=map_data["last_object_clicked"]["lng"]
    c=min(filtered,key=lambda x:(x["lat"]-lat)**2+(x["lon"]-lon)**2)
    st.markdown("---")
    cf,ci=st.columns([2,5])
    with cf:
        st.image(f"https://flagcdn.com/w320/{c['code']}.png",use_container_width=True)
        if c["un"]: st.markdown('<div style="text-align:center;color:#00f5ff88;font-size:11px;">🇺🇳 UN MEMBER</div>',unsafe_allow_html=True)
        if c["landlocked"]: st.markdown('<div style="text-align:center;color:#ffaa0088;font-size:11px;">🔒 LANDLOCKED</div>',unsafe_allow_html=True)
    with ci:
        st.markdown(f'<h2 style="font-size:20px;letter-spacing:2px;">{c["name"].upper()}</h2>',unsafe_allow_html=True)
        ca_,cb_,cc_=st.columns(3)
        for col,fields in [
            (ca_,[("🏛 Capital",c["capital"]),("🌐 Region",c["region"]),("🗺️ Subregion",c["subregion"]),("📞 Calling",c["calling"]),("🌐 TLD",c["tld"])]),
            (cb_,[("👥 Population",c["pop_fmt"]),("📐 Area",c["area_fmt"]),("👨 Density",f"{c['density']} /km²"),("🤝 Borders",str(c["borders"])),("📊 Gini",str(c["gini"]) if c["gini"] else "N/A")]),
            (cc_,[("💬 Language",c["lang"]),("💰 Currency",c["currency"]),("⏰ Timezone",c["tz"]),("🚗 Drive",c["drive"]),("🇺🇳 UN","Yes" if c["un"] else "No")]),
        ]:
            with col:
                for lbl,val in fields:
                    st.markdown(f'<div class="mb"><div class="ml">{lbl}</div><div class="mv" style="font-size:12px;">{val}</div></div>',unsafe_allow_html=True)
    world_pop=sum(x["pop"] for x in COUNTRIES)
    pct=round(c["pop"]/world_pop*100,3)
    st.markdown(f'<div style="font-size:11px;color:#00f5ff88;margin-top:10px;">WORLD POP SHARE: <b style="color:#00f5ff">{pct}%</b></div>',unsafe_allow_html=True)
    st.progress(min(pct/20,1.0))
else:
    st.info("🖱️ Xaritada davlatni bosing")
    st.markdown("---")
    region_data={}
    for c in filtered:
        r=c["region"]
        if r not in region_data: region_data[r]={"count":0,"pop":0}
        region_data[r]["count"]+=1; region_data[r]["pop"]+=c["pop"]
    cc1,cc2=st.columns(2)
    with cc1:
        st.markdown('<div style="font-size:11px;color:#00f5ff88;margin-bottom:6px;letter-spacing:2px">COUNTRIES PER REGION</div>',unsafe_allow_html=True)
        st.bar_chart(pd.DataFrame({"n":{r:v["count"] for r,v in region_data.items()}}),height=220)
    with cc2:
        st.markdown('<div style="font-size:11px;color:#00f5ff88;margin-bottom:6px;letter-spacing:2px">POPULATION SHARE</div>',unsafe_allow_html=True)
        total_p=sum(v["pop"] for v in region_data.values())
        for r,v in sorted(region_data.items(),key=lambda x:-x[1]["pop"]):
            pct=round(v["pop"]/total_p*100,1) if total_p else 0
            col=REGION_COLORS.get(r,"#00f5ff")
            st.markdown(f'<div style="margin:4px 0"><div style="display:flex;justify-content:space-between;font-size:10px;color:#ffffff88"><span>{r}</span><span style="color:{col}">{pct}%</span></div><div style="background:#0a1628;height:7px;border-radius:2px"><div style="width:{pct}%;background:{col};height:7px;border-radius:2px"></div></div></div>',unsafe_allow_html=True)
    st.markdown('<div style="font-size:11px;color:#00f5ff88;margin:12px 0 6px;letter-spacing:2px">🏆 TOP 10 POPULOUS</div>',unsafe_allow_html=True)
    top10=sorted(filtered,key=lambda x:-x["pop"])[:10]
    mx=top10[0]["pop"]
    for i,c in enumerate(top10):
        col=REGION_COLORS.get(c["region"],"#00f5ff"); pct=c["pop"]/mx*100
        st.markdown(f'<div style="margin:4px 0"><div style="display:flex;justify-content:space-between;font-size:10px;color:#ffffff88"><span style="color:{col}">#{i+1} {c["name"]}</span><span>{c["pop_fmt"]}</span></div><div style="background:#0a1628;height:9px;border-radius:2px"><div style="width:{pct:.1f}%;background:{col};height:9px;border-radius:2px;box-shadow:0 0 6px {col}66"></div></div></div>',unsafe_allow_html=True)
