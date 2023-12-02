import pandas as pd
import streamlit as st
import altair as alt

st.set_page_config(page_title="Data comparison")

## LOADING DATA
@st.cache_data
def get_data():
    df = pd.read_csv("./data/migration.csv")
    df["net_100k"] = (df["neto"] / df["pob_total"]) * 100000
    df["net_100k"] = df["net_100k"].round(2)
    df.columns=["State","Immigrants","Emigrants","Net Change","Total Population","Net Rate per 100k"]
    return df.set_index("State")


def data_plot():
    df = get_data()

    ## MULTI SELECT WIDGET
    states = st.multiselect(
        "Choose states", list(df.index), ["Sonora","Sinaloa"]
    )
    # IF there are no states selected
    if not states:
        st.error("Please select at least one state.")

    else:
        #Filter dataframe by states selected
        data = df.loc[states]
        st.write("### Migration data per state", data.sort_index())

        # Select the column we want to plot
        column = st.selectbox(
        "Choose a variable to plot", list(df.columns)
        )

        data = data[column].T.reset_index()
        #data = pd.melt(data, id_vars=["index"]).rename(
        #    columns={"index": "Variable", "value": "Value"}
        #)

        chart = (
            alt.Chart(data)
            .mark_bar(opacity=0.6)
            .encode(
                x=alt.X("State", sort="y"),
                y=f"{column}",
                #color=alt.Color("State",legend=None)
            )
            .properties(height=500)
        )
        st.altair_chart(chart, use_container_width=True)

st.markdown("# State-level migration data")
st.markdown("Choose as many states as you'd like.")

st.sidebar.header("Comparing state-level data")
st.sidebar.caption("In this section, you can compare migration and population data for different states!")
st.sidebar.caption("You can select as many states as you want to add to the dataframe, and you can select which variable to compare in the bar chart below.")

data_plot()