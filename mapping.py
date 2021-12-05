import folium
import pandas as pd

def processdata(filename):
    rawdata = pd.read_csv(filename, dtype={'ZIPCODE': str}).dropna()
    rawdata["ZIPCODE"] = rawdata["ZIPCODE"].apply(lambda x: x.replace(",",""))
    rawdata = rawdata.astype({'ZIPCODE': 'int32'})

    zipcodes = list(rawdata["ZIPCODE"].unique())
    averages = []

    for code in zipcodes:
        col = rawdata[rawdata["ZIPCODE"] == code]["INCIDENT_TRAVEL_TM_SECONDS_QY"]
        averages.append(col.mean())

    for i in range(len(zipcodes)):
        if(zipcodes[i]==83):
            zipcodes[i]="00083"
        else:
            zipcodes[i]=str(zipcodes[i])

    processeddata = pd.DataFrame()
    processeddata["zipcode"] = zipcodes
    processeddata["average_response_time"] = averages

    processeddata.to_csv("processeddata.csv", index=False)

#processdata("responsetimes.csv")
processeddata = pd.read_csv("processeddata.csv", dtype={'zipcode': str})

map = folium.Map(location=[40.7128, -74.0060], zoom_start=12)

folium.Choropleth(
    geo_data="zipcodes.json",
    data=processeddata,
    columns=["zipcode", "average_response_time"],
    key_on="feature.properties.postalCode",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="EMS Average Response Time(Seconds)",
).add_to(map)

folium.LayerControl().add_to(map)

map.save("map.html")