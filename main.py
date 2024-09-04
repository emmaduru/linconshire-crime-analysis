import geojson
import streamlit as st
import plotly.express as px

def crime_location():
    from helpers import crime_df, crimes
    st.title("Lincolnshire Crime Analysis")
    st.text("Map representation of crime in Lincolnshire County, UK in March, 2024")
    st.subheader("Location of Crime in Lincolnshire")
    option = st.selectbox(
        "Crime type",
        crimes)

    if option != "All Crimes":
        crime_df = crime_df[crime_df['Crime type'] == option]
    fig = px.scatter_mapbox(crime_df, lat="Latitude", lon="Longitude", hover_name="Location", hover_data=["Crime type", "City"],
                            color="Crime type",
                            color_discrete_sequence=px.colors.qualitative.Vivid,
                            center  = {"lat": 53.19, "lon" : -0.53},
                            zoom=7)
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)

def crime_per_city():
    from helpers import all_crime_df, crimes
    st.title("Lincolnshire Crime Analysis")
    st.text("Map representation of crime in Lincolnshire County, UK in March, 2024")
    st.subheader("Total Crime per county")
    option = st.selectbox(
        "Crime type",
        crimes)

    f = open("LAD_Dec_2021_Great_Britain.geojson")
    data = f.read()
    counties = geojson.loads(data)

    fig = px.choropleth_mapbox(all_crime_df, geojson=counties, locations='City', color=option,featureidkey="properties.LAD21NM",
                            color_continuous_scale="Viridis", 
                            range_color=(0, 30),
                            mapbox_style="carto-positron",
                            center  = {"lat": 53.19, "lon" : -0.53},
                            zoom=7
                            )
    fig.update_geos(fitbounds=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    st.plotly_chart(fig)

page_names_to_funcs = {
    "Crime Locations": crime_location,
    "Crime Per City": crime_per_city,
}

demo_name = st.sidebar.selectbox("Choose a visualization", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()