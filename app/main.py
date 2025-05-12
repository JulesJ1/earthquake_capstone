import streamlit as st
from utils.db_utils import create_connection, create_db_engine
from config.db_config import load_db_config
from retrieve_data import retrieve_live_data, retrieve_historical_data
import pandas as pd
import folium
from streamlit_folium import st_folium
from datetime import datetime
from filters import apply_filters, load_data,display_live_data, filter_date
from visualisations import display_visualisations


def pick_colour(magnitude):
    if magnitude < 2.5:
        return '#fae22b'
    elif magnitude < 6:
        return 'orange'
    return 'red'


def main():
    st.set_page_config(
        page_title="Earthquake Dashboard",
        page_icon="🚢",
        layout="wide",
        initial_sidebar_state="auto",
    )

    #data = load_data()
   
    if 'display_name' not in st.session_state:
        st.session_state.display_name = None

    if 'data' not in st.session_state:
        print('not is session')
        st.session_state['data'] = load_data()
        #load_data()
    

        
    #print(f'here{st.session_state['d']}')


    #print(data[['longitude','latitude']].dtypes)


    st.title('Earthquake visualiser')


    #st.sidebar.header("Filter Data")
    #display_live_data()
    #filter_date()

    apply_filters()

    st.session_state['data']['normalised_mag'] = (st.session_state['data']['magnitude'] - st.session_state['data']['magnitude'].min()) / (st.session_state['data']['magnitude'].max() - st.session_state['data']['magnitude'].min())
    st.session_state['data']['colour'] = st.session_state['data']['magnitude'].transform(pick_colour)
    print('data:')
    print(st.session_state['data'])

    #filter_date(data)
    
    #data = apply_filters(data)

   
    display_visualisations()


if __name__ == "__main__":
    main()
