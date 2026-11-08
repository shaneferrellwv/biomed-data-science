import streamlit as st
import folium
from streamlit_folium import st_folium

st.title("Map")

latitude = st.number_input("Latitude", value=40.0000, step=0.0001, format="%.4f")
longitude = st.number_input("Longitude", value=-75.0000, step=0.0001, format="%.4f")
map = folium.Map(location=[latitude, longitude], zoom_start=12)

folium.CircleMarker(
    location=[latitude, longitude],
    radius=8,
    color="red",
    fill=True,
    fill_color="red",
    fill_opacity=1,
    popup="Selected Location"
).add_to(map)

st_folium(map, width=700, height=450, key="map")