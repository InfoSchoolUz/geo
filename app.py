import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="🌍 World Data Explorer", layout="wide")

# ====== TITLE ======
st.markdown("""
# 🌍 World Data Explorer
### Interaktiv xarita + davlat statistikasi
""")

# ====== LOAD DATA ======
@st.cache_data
def load_data():
    df = px.data.gapminder()
    df = df[df["year"] == 2007]  # Oxirgi to‘liq dataset
    return df

df = load_data()

# ====== MAP ======
st.subheader("🌎 Xarita ustida davlat tanlang")

fig = px.choropleth(
    df,
    locations="iso_alpha",
    color="gdpPercap",
    hover_name="country",
    color_continuous_scale="viridis",
    title="GDP per Capita (2007)",
)

fig.update_layout(
    height=600,
    margin=dict(l=0, r=0, t=50, b=0)
)

selected_country = st.plotly_chart(
    fig,
    use_container_width=True,
    on_select="rerun"
)

# ====== HANDLE CLICK ======
country_name = None

if "selection" in selected_country and selected_country["selection"]:
    try:
        point = selected_country["selection"]["points"][0]
        iso = point["location"]
        country_row = df[df["iso_alpha"] == iso]

        if not country_row.empty:
            country_name = country_row.iloc[0]["country"]
    except:
        pass

# ====== DEFAULT STATE ======
if not country_name:
    st.info("👆 Xarita ustidan davlat ustiga bosing")
    st.stop()

# ====== COUNTRY DATA ======
country_data = df[df["country"] == country_name].iloc[0]

# ====== DISPLAY ======
st.markdown(f"# 📊 {country_name} statistikasi")

col1, col2, col3, col4 = st.columns(4)

col1.metric("👥 Aholi", f"{int(country_data['pop']):,}")
col2.metric("💰 GDP per capita", f"${country_data['gdpPercap']:.2f}")
col3.metric("❤️ Life expectancy", f"{country_data['lifeExp']:.1f} yil")
col4.metric("🌍 Qit'a", country_data['continent'])

# ====== CHARTS ======
st.subheader("📈 Trendlar (1952–2007)")

history = px.data.gapminder()
history = history[history["country"] == country_name]

colA, colB = st.columns(2)

with colA:
    fig_pop = px.line(
        history,
        x="year",
        y="pop",
        title="Aholi o‘sishi"
    )
    st.plotly_chart(fig_pop, use_container_width=True)

with colB:
    fig_life = px.line(
        history,
        x="year",
        y="lifeExp",
        title="Hayot davomiyligi"
    )
    st.plotly_chart(fig_life, use_container_width=True)

# ====== EXTRA ======
st.subheader("🌐 Qo‘shimcha ma'lumotlar")

st.dataframe(history[["year", "pop", "lifeExp", "gdpPercap"]])

# ====== FOOTER ======
st.markdown("---")
st.markdown("Developed by Azamat Madrimov 🚀")
