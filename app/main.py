import streamlit as st
from utils.db_utils import create_connection, create_db_engine
from config.db_config import load_db_config
from retrieve_data import retrieve_live_data, retrieve_historical_data
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime


@st.cache_data
def load_data(start = None, end = None):
    db_details = load_db_config()['target_database']
    engine = create_db_engine(db_details)
    conn = create_connection(engine)
    if start or end:
        return retrieve_historical_data(conn,start,end)
    return retrieve_live_data(conn)


def main():
    st.set_page_config(
        page_title="Earthquake Dashboard",
        page_icon="🚢",
        layout="wide",
        initial_sidebar_state="auto",
    )

    data = load_data()
    
    if 'display_name' not in st.session_state:
        st.session_state.display_name = None

    map = folium.Map(zoom_start=30)
    for i,row in data.iterrows():
        folium.CircleMarker([row.latitude,row.longitude],radius=5).add_to(map)

    print(data[['longitude','latitude']].dtypes)


    st.title('Earthquake visualiser')

    st.sidebar.header("Filter Data")
    select_live_data = st.sidebar.button(
        label='Show live data',
        
    )
    if select_live_data:
        data = load_data()
    date_filter = st.sidebar.slider(
            label='Select time range',
            min_value=datetime.strptime('2025-03-05 00:00:46', '%Y-%m-%d %H:%M:%S'),
            max_value=datetime.strptime('2025-05-05 17:05:58', '%Y-%m-%d %H:%M:%S')
        )

    tab1, tab2 = st.tabs(["View Map", "Data Analyser"])
    location = 'None'
    #st.map(data=df,longitude='longitude',latitude='latitude')
    #st.map(data=data,size='magnitude'*50)
    col1, col2 = st.columns([3,1])
    with col1.container():
        map_data = st_folium(map,use_container_width=True)
        st.session_state.display_name = map_data['last_object_clicked']
        print(map_data)
        print(map_data['last_object_clicked'])
        print(st.session_state.display_name)
        if st.session_state.display_name is not None:
            location = st.session_state.display_name

    with col2.container():
        st.write(f'latitude: {location['lat']}')
        st.write(f'longitude: {location['lng']}')


if __name__ == "__main__":
    main()
