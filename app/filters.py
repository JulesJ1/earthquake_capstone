import streamlit as st
from datetime import datetime
from retrieve_data import retrieve_historical_data, retrieve_live_data


def display_live_data():
    return st.sidebar.button(
    label='Show live data',
        
    )
    #if select_live_data:
    #    data = load_data()

def filter_date():
    return st.sidebar.slider(
        label='Select time range',
        min_value=datetime.strptime('2025-03-05 00:00:46', '%Y-%m-%d %H:%M:%S'),
        max_value=datetime.strptime('2025-05-05 17:05:58', '%Y-%m-%d %H:%M:%S')
    )


def apply_filters():
    st.sidebar.header('Filter data')
    live_data = display_live_data()
    filtered_date = filter_date()