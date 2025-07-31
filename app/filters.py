import streamlit as st
from datetime import datetime, timedelta
from app.streamlit_queries import (retrieve_historical_data,
                                   retrieve_live_data,
                                   retrieve_latest_data)
from utils.db_utils import create_connection, create_db_engine
from config.db_config import load_db_config


@st.cache_data
def fetch_data(start=None, end=None):

    db_details = load_db_config()['target_database']

    engine = create_db_engine(db_details)
    conn = create_connection(engine)
    if start or end:
        return retrieve_historical_data(conn, start, end)

    livedata = retrieve_live_data(conn)

    if livedata.empty is False:
        return livedata
    return retrieve_latest_data(conn)


def display_live_data():
    if st.sidebar.button(label='Show Live Data'):
        st.session_state['data'] = fetch_data().copy()
        st.session_state['filtered_data'] = st.session_state['data'].copy()


def toggle_heatmap():
    heatmap = st.sidebar.toggle("heatmap")
    if heatmap:
        st.session_state['heatmap'] = True
    else:
        st.session_state['heatmap'] = False


def filter_magnitude():
    st.sidebar.slider(
        label='filter minimum magnitude',
        min_value=0.0,
        max_value=max(st.session_state['data']['magnitude']),
        key='mag_filter'
        )


def filter_type(options):
    st.sidebar.pills(
        'Type',
        options,
        selection_mode='single',
        default=options[0],
        key='type_filter'
        )


def call_select_filters():
    options = st.session_state['data']['type'].unique()
    filter_type(options)
    filter_magnitude()

    check_if_empty = st.session_state['data'][
        (st.session_state['data']['magnitude'] >= st.session_state.mag_filter)
        & (st.session_state['data']['type'] ==
           str(st.session_state.type_filter))
    ]
    if check_if_empty.empty:
        st.badge(
            'No data available for the selected filters, '
            'default data will be displayed instead!',
            icon='❌',
            color='red'
            )
    else:
        st.session_state['filtered_data'] = check_if_empty.copy()


def filter_date():
    data_filter = st.sidebar.container()
    with data_filter:
        st.write('Filter By Date')
        start, end = st.columns(2)
        with start:
            start_date = st.date_input(
                'start date',
                value=datetime.now() - timedelta(hours=6),

            )

            start_time = st.time_input(
                'start time',
                value=datetime.now() - timedelta(hours=6)
            )
        with end:
            end_date = st.date_input('end date')
            end_time = st.time_input('end time')

        start_dt = datetime.combine(start_date, start_time)
        end_dt = datetime.combine(end_date, end_time)

        if st.button(label='filter date'):
            if start_dt >= end_dt:
                st.warning("Start date/time must be before end date/time.")
            else:
                start_datetime = f'{start_date} {start_time}'
                end_datetime = f'{end_date} {end_time}'
                st.session_state['data'] = fetch_data(
                    start_datetime,
                    end_datetime
                    ).copy()
                st.session_state[
                    'filtered_data'
                    ] = st.session_state['data'].copy()


def apply_filters():
    st.sidebar.header('Filter Data')
    display_live_data()
    # toggle_heatmap()
    # call_select_filters()
    filter_date()
