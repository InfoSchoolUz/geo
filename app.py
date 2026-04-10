import streamlit as st

st.set_page_config(layout="centered")
st.title("🌍 Jahon davlatlari (o‘zbekcha, bayroqli)")

# ===== FULL DATA (ISO + UZ) =====
countries = [
("af","Afg‘oniston"),("al","Albaniya"),("dz","Jazoir"),("ad","Andorra"),
("ao","Angola"),("ag","Antigua va Barbuda"),("ar","Argentina"),
("am","Armaniston"),("au","Avstraliya"),("at","Avstriya"),
("az","Ozarbayjon"),("bs","Bagama orollari"),("bh","Bahrayn"),
("bd","Bangladesh"),("bb","Barbados"),("by","Belarus"),
("be","Belgiya"),("bz","Beliz"),("bj","Benin"),
("bt","Butan"),("bo","Boliviya"),("ba","Bosniya va Gersegovina"),
("bw","Botsvana"),("br","Braziliya"),("bn","Bruney"),
("bg","Bolgariya"),("bf","Burkina-Faso"),("bi","Burundi"),
("kh","Kambodja"),("cm","Kamerun"),("ca","Kanada"),
("cv","Kabo-Verde"),("cf","Markaziy Afrika Respublikasi"),
("td","Chad"),("cl","Chili"),("cn","Xitoy"),
("co","Kolumbiya"),("km","Komor orollari"),("cg","Kongo"),
("cd","Kongo DR"),("cr","Kosta-Rika"),("ci","Kot-d’Ivuar"),
("hr","Xorvatiya"),("cu","Kuba"),("cy","Kipr"),
("cz","Chexiya"),("dk","Daniya"),("dj","Jibuti"),
("dm","Dominika"),("do","Dominikan Respublikasi"),
("ec","Ekvador"),("eg","Misr"),("sv","Salvador"),
("gq","Ekvatorial Gvineya"),("er","Eritreya"),
("ee","Estoniya"),("sz","Eswatini"),("et","Efiopiya"),
("fj","Fiji"),("fi","Finlyandiya"),("fr","Fransiya"),
("ga","Gabon"),("gm","Gambiya"),("ge","Gruziya"),
("de","Germaniya"),("gh","Gana"),("gr","Gretsiya"),
("gd","Grenada"),("gt","Gvatemala"),("gn","Gvineya"),
("gw","Gvineya-Bisau"),("gy","Gayana"),("ht","Gaiti"),
("hn","Gonduras"),("hu","Vengriya"),("is","Islandiya"),
("in","Hindiston"),("id","Indoneziya"),("ir","Eron"),
("iq","Iroq"),("ie","Irlandiya"),("il","Isroil"),
("it","Italiya"),("jm","Yamayka"),("jp","Yaponiya"),
("jo","Iordaniya"),("kz","Qozog‘iston"),("ke","Keniya"),
("ki","Kiribati"),("kp","Shimoliy Koreya"),("kr","Janubiy Koreya"),
("kw","Kuvayt"),("kg","Qirg‘iziston"),("la","Laos"),
("lv","Latviya"),("lb","Livan"),("ls","Lesoto"),
("lr","Liberiya"),("ly","Liviya"),("li","Lixtenshteyn"),
("lt","Litva"),("lu","Lyuksemburg"),("mg","Madagaskar"),
("mw","Malavi"),("my","Malayziya"),("mv","Maldiv orollari"),
("ml","Mali"),("mt","Malta"),("mh","Marshall orollari"),
("mr","Mavritaniya"),("mu","Mavrikiy"),("mx","Meksika"),
("fm","Mikroneziya"),("md","Moldova"),("mc","Monako"),
("mn","Mongoliya"),("me","Chernogoriya"),("ma","Marokash"),
("mz","Mozambik"),("mm","Myanma"),("na","Namibiya"),
("nr","Nauru"),("np","Nepal"),("nl","Niderlandiya"),
("nz","Yangi Zelandiya"),("ni","Nikaragua"),
("ne","Niger"),("ng","Nigeriya"),("no","Norvegiya"),
("om","Ummon"),("pk","Pokiston"),("pw","Palau"),
("ps","Falastin"),("pa","Panama"),("pg","Papua-Yangi Gvineya"),
("py","Paragvay"),("pe","Peru"),("ph","Filippin"),
("pl","Polsha"),("pt","Portugaliya"),("qa","Qatar"),
("ro","Ruminiya"),("ru","Rossiya"),("rw","Ruanda"),
("kn","Sent-Kits va Nevis"),("lc","Sent-Lyusiya"),
("vc","Sent-Vinsent"),("ws","Samoa"),("sm","San-Marino"),
("st","San-Tome va Prinsipi"),("sa","Saudiya Arabistoni"),
("sn","Senegal"),("rs","Serbiya"),("sc","Seyshel"),
("sl","Syerra-Leone"),("sg","Singapur"),
("sk","Slovakiya"),("si","Sloveniya"),
("sb","Solomon orollari"),("so","Somali"),
("za","Janubiy Afrika"),("es","Ispaniya"),
("lk","Shri-Lanka"),("sd","Sudan"),("ss","Janubiy Sudan"),
("sr","Surinam"),("se","Shvetsiya"),("ch","Shveytsariya"),
("sy","Suriya"),("tw","Tayvan"),("tj","Tojikiston"),
("tz","Tanzaniya"),("th","Tailand"),("tl","Timor-Leste"),
("tg","Togo"),("to","Tonga"),("tt","Trinidad va Tobago"),
("tn","Tunis"),("tr","Turkiya"),("tm","Turkmaniston"),
("tv","Tuvalu"),("ug","Uganda"),("ua","Ukraina"),
("ae","BAA"),("gb","Buyuk Britaniya"),("us","AQSh"),
("uy","Urugvay"),("uz","O‘zbekiston"),("vu","Vanuatu"),
("va","Vatikan"),("ve","Venesuela"),("vn","Vetnam"),
("ye","Yaman"),("zm","Zambiya"),("zw","Zimbabve")
]

# ===== FLAG =====
def flag(code):
    return ''.join(chr(127397 + ord(c)) for c in code.upper())

# ===== DROPDOWN =====
names = [name for code, name in countries]

selected = st.selectbox(
    "🌍 Davlatni tanlang:",
    names,
    format_func=lambda x: f"{flag(next(c for c,n in countries if n==x))} {x}"
)

# ===== FIND =====
code = next(c for c,n in countries if n == selected)

# ===== SHOW =====
st.markdown("## Tanlangan davlat")

st.image(f"https://flagcdn.com/w320/{code}.png", width=150)
st.write("📍", selected)
