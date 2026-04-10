import streamlit as st

st.set_page_config(layout="centered")
st.title("🌍 Jahon davlatlari (to‘liq)")

countries = [
("uz","O‘zbekiston","Toshkent","Osiyo"),
("us","AQSh","Vashington","Amerika"),
("cn","Xitoy","Pekin","Osiyo"),
("ru","Rossiya","Moskva","Yevropa/Osiyo"),
("de","Germaniya","Berlin","Yevropa"),
("fr","Fransiya","Parij","Yevropa"),
("gb","Buyuk Britaniya","London","Yevropa"),
("jp","Yaponiya","Tokio","Osiyo"),
("in","Hindiston","Dehli","Osiyo"),
("br","Braziliya","Brasiliya","Amerika"),
("ca","Kanada","Ottava","Amerika"),
("au","Avstraliya","Kanberra","Okeaniya"),
("tr","Turkiya","Anqara","Yevropa/Osiyo"),
("kz","Qozog‘iston","Astana","Osiyo"),
("kg","Qirg‘iziston","Bishkek","Osiyo"),
("tj","Tojikiston","Dushanbe","Osiyo"),
("af","Afg‘oniston","Kobul","Osiyo"),
("ir","Eron","Tehron","Osiyo"),
("iq","Iroq","Bag‘dod","Osiyo"),
("sa","Saudiya Arabistoni","Riyod","Osiyo"),
("ae","BAA","Abu-Dabi","Osiyo"),
("qa","Qatar","Doha","Osiyo"),
("pk","Pokiston","Islomobod","Osiyo"),
("bd","Bangladesh","Dakka","Osiyo"),
("id","Indoneziya","Jakarta","Osiyo"),
("my","Malayziya","Kuala-Lumpur","Osiyo"),
("sg","Singapur","Singapur","Osiyo"),
("th","Tailand","Bangkok","Osiyo"),
("vn","Vetnam","Xanoy","Osiyo"),
("kr","Janubiy Koreya","Seul","Osiyo"),
("kp","Shimoliy Koreya","Pxenyan","Osiyo"),
("it","Italiya","Rim","Yevropa"),
("es","Ispaniya","Madrid","Yevropa"),
("pt","Portugaliya","Lissabon","Yevropa"),
("nl","Niderlandiya","Amsterdam","Yevropa"),
("be","Belgiya","Bryussel","Yevropa"),
("ch","Shveytsariya","Bern","Yevropa"),
("at","Avstriya","Vena","Yevropa"),
("se","Shvetsiya","Stokgolm","Yevropa"),
("no","Norvegiya","Oslo","Yevropa"),
("fi","Finlyandiya","Xelsinki","Yevropa"),
("dk","Daniya","Kopengagen","Yevropa"),
("pl","Polsha","Varshava","Yevropa"),
("cz","Chexiya","Praga","Yevropa"),
("hu","Vengriya","Budapesht","Yevropa"),
("ro","Ruminiya","Buxarest","Yevropa"),
("gr","Gretsiya","Afina","Yevropa"),
("ua","Ukraina","Kiyev","Yevropa"),
("by","Belarus","Minsk","Yevropa"),
("eg","Misr","Qohira","Afrika"),
("za","Janubiy Afrika","Pretoriya","Afrika"),
("ng","Nigeriya","Abuja","Afrika"),
("ke","Keniya","Nayrobi","Afrika"),
("et","Efiopiya","Addis-Abeba","Afrika"),
("dz","Jazoir","Jazoir","Afrika"),
("ma","Marokash","Rabot","Afrika"),
("tn","Tunis","Tunis","Afrika"),
("ly","Liviya","Tripoli","Afrika"),
("sd","Sudan","Xartum","Afrika"),
("mx","Meksika","Meksiko","Amerika"),
("ar","Argentina","Buenos-Ayres","Amerika"),
("cl","Chili","Santyago","Amerika"),
("co","Kolumbiya","Bogota","Amerika"),
("pe","Peru","Lima","Amerika"),
("ve","Venesuela","Karakas","Amerika"),
("uy","Urugvay","Montevideo","Amerika"),
("py","Paragvay","Asunsion","Amerika")
]

def flag(code):
    return ''.join(chr(127397 + ord(c)) for c in code.upper())

names = [c[1] for c in countries]

selected = st.selectbox(
    "🌍 Davlatni tanlang:",
    names,
    format_func=lambda x: f"{flag(next(c[0] for c in countries if c[1]==x))} {x}"
)

code, name, capital, region = next(c for c in countries if c[1] == selected)

st.markdown("## Tanlangan davlat")

st.image(f"https://flagcdn.com/w320/{code}.png", width=150)
st.write("📍 Davlat:", name)
st.write("🏙 Poytaxt:", capital)
st.write("🌍 Mintaqa:", region)

st.caption("ℹ️ Ma'lumotlar statik dataset asosida")
