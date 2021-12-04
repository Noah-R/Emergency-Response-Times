import folium
import pandas as pd

map = folium.Map(location=[40.7128, -74.0060], zoom_start=12)
data = pd.read_csv("responsetimes.csv")

folium.Choropleth(
    geo_data="zipcodes.json",
    data=data,
    columns=["ZIPCODE", "INCIDENT_TRAVEL_TM_SECONDS_QY"],
    key_on="feature.properties.postalCode",
    fill_color="YlGn",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="EMS Average Response Time(Seconds)",
).add_to(map)

folium.LayerControl().add_to(map)

map.save("map.html")