
import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from bs4 import BeautifulSoup
from io import StringIO

st.title("Interactive GDP Stacked Bar Chart")

# fetch GDP data
headers = {"User-Agent": "Mozilla/5.0 (compatible; GDPStreamlitDemo/1.0)"}
url = "https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)"
response = requests.get(url, headers=headers, timeout=30)
response.raise_for_status()
soup = BeautifulSoup(response.text, "html.parser")
table = soup.find("table", class_="wikitable")

gdp = pd.read_html(StringIO(str(table)))[0]
gdp.columns = [" ".join(str(p) for p in col) if isinstance(col, tuple) else str(col) for col in gdp.columns]
country_col = [c for c in gdp.columns if "Country/Territory".lower() in c.lower()][0]
source_cols = {name: [c for c in gdp.columns if name.lower() in c.lower()][0] for name in ("IMF", "World Bank", "United Nations")}

# clean the data
clean = pd.DataFrame()
clean["Country"] = (gdp[country_col].astype(str).str.replace(r"\[.*?\]", "", regex=True).str.strip())
for source, col in source_cols.items():
    clean[source] = pd.to_numeric(gdp[col].astype(str).str.replace(",", "", regex=False).str.extract(r"(\d+(?:\.\d+)?)", expand=False), errors="coerce")
clean.drop(clean.index[0], inplace=True)

# fetch region data
region_url = ("https://en.wikipedia.org/w/index.php?title=List_of_countries_by_GDP_(nominal)&oldid=1187446467")
response = requests.get(region_url, headers=headers, timeout=30)
response.raise_for_status()
region_soup = BeautifulSoup(response.text, "html.parser")
caption = region_soup.find("caption", string=lambda s: s and "GDP (USD million) by country" in s)

# match countries to their region
rows = []
for tr in caption.find_parent("table").find_all("tr"):
    cells = tr.find_all("td")
    if len(cells) == 8:
        rows.append({"Country": cells[0].get_text(" ", strip=True), "Region": cells[1].get_text(" ", strip=True)})
regions = pd.DataFrame(rows)
regions["Country"] = (regions["Country"].str.replace(r"\[.*?\]", "", regex=True).str.strip())

df = clean.merge(regions.drop_duplicates("Country"), on="Country", how="inner")

# create dropdown on app
source = st.selectbox("GDP source", ["IMF", "United Nations", "World Bank"])

# create plot on app
plot_df = df.dropna(subset=[source, "Region"])
fig = px.bar(
    plot_df,
    x="Region",
    y=source,
    color="Country",
    labels={source: "GDP (USD millions)", "Region": "Region"},
    hover_data={"Country": True, source: ":,.0f"},
    title="GDP by Region",
)
fig.update_layout(
    barmode="stack",
    xaxis={"categoryorder": "total descending"},
    showlegend=False,
    height=650,
)
st.plotly_chart(fig, use_container_width=True)
