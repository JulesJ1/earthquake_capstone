import streamlit as st
from datetime import datetime, timedelta
from retrieve_data import retrieve_historical_data, retrieve_live_data
from utils.db_utils import create_connection, create_db_engine
from config.db_config import load_db_config

@st.cache_data
def fetch_data(start=None, end=None):
    db_details = load_db_config()['target_database']

    engine = create_db_engine(db_details)
    conn = create_connection(engine)
    if start or end:
        return retrieve_historical_data(conn, start, end)
    return retrieve_live_data(conn)


def display_live_data():
    if st.sidebar.button(label='Show live data'):
        st.session_state['data'] = fetch_data()


def filter_magnitude():
    magnitude = st.sidebar.slider(
        label='filter minimum magnitude',
        min_value=0.0,
        max_value=9.5
        )
    st.session_state['data'] = st.session_state['data'][
            st.session_state['data']['magnitude'] > magnitude
        ]


def filter_type():
    options = ['earthquake', 'ice quake', 'quarry blast', 'explosion']
    type = st.sidebar.pills('Type', options, selection_mode='multi')
    #st.session_state['data'] = st.session_state['data'][st.session_state['data']['type'].isin(type)]


def filter_date():
    data_filter = st.sidebar.container()
    with data_filter:
        st.write('Filter By Date')
        start, end = st.columns(2)
        with start:
            start_date = st.date_input(
                'start date',
                value=datetime.now() - timedelta(hours=6)
            )

            start_time = st.time_input(
                'start time',
                value=datetime.now() - timedelta(hours=6)
            )
        with end:
            end_date = st.date_input('end date')
            end_time = st.time_input('end time')

        if st.button(label='filter date'):
            start_datetime = f'{start_date} {start_time}'
            end_datetime = f'{end_date} {end_time}'
            st.session_state['data'] = fetch_data(start_datetime, end_datetime)


def apply_filters():
    st.sidebar.header('Filter data')
    display_live_data()
    filter_magnitude()
    filter_type()
    filter_date()
