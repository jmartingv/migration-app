import streamlit as st
import pandas as pd
import geopandas as gpd
import plotly.express as px

st.set_page_config(page_title="Choropleth Map")

st.sidebar.header("Visualizing net migration rate")
st.sidebar.caption("In this section, you can visualize the net migration rate on each state, per 100,000 inhabitants.")
st.sidebar.caption("This map was done using plotly, geopandas and pandas, with data taken from Mexico's National Institute of Statistics and Geography (INEGI).")

## LOADING DATA:

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    return df

def load_geo_data(path):
    geodf = gpd.read_file(path)
    return geodf

## PROCESSING THE DATA

geo_df = load_geo_data("./data/00ent.shp")
df_migracion = load_data("./data/migration.csv")

# Transforming CVE_ENT to int
geo_df["CVE_ENT"] = geo_df["CVE_ENT"].astype(int)
geo_df.rename(columns={'CVE_ENT':"State Code"},inplace=True)

# Merging geospatial data with the numerical data
geo_df = geo_df.merge(df_migracion, left_on="NOMGEO", right_on="Entidad federativa").drop(columns="Entidad federativa").set_index("State Code")

# Obtaining the net rate per 100,000 inhabitants
geo_df = geo_df[["NOMGEO","inmigrante","emigrante","neto","pob_total","geometry"]]
geo_df["Net Rate"] = (geo_df["neto"] / geo_df["pob_total"]) * 100000
geo_df["Net Rate"] = geo_df["Net Rate"].round(2)
geo_df = geo_df.to_crs("EPSG:4326")

## Adding title

st.markdown('# Net migration rate map')
st.markdown("Try hovering over each state for more details!")


## Generating map

with st.spinner("Loading map..."):
    fig = px.choropleth(
        geo_df,
        geojson=geo_df.geometry,
        locations=geo_df.index,
        color='Net Rate',
        hover_name='NOMGEO',
        #title='Saldo neto migratorio por Estado, por cada 100 mil habitantes',
        color_continuous_scale='Reds', # You can choose other color scales
        projection = "conic conformal"  
    )

    # Customize the map layout if needed
    fig.update_geos(fitbounds="locations", visible=False)

    fig.update_layout(width=800,
                    height=600)

    fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)'))

    fig.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0},
                    coloraxis_colorbar=dict(title="Net Change"))

    st.plotly_chart(fig)

st.success("Map loaded successfully!")